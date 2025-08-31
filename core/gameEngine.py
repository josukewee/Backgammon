import pygame as pg
from typing import List, Optional

from datastructures.Board import Board
from core.gameState import GameState
from core.moveMediator import MoveMediator
from core.eventHandler import eventHandler
from presentation.Renderer import Renderer
from core.InputHandler import InputHandler


class GameEngine:
    """
    Orchestrates the game:
      - rolls dice and manages turn flow
      - pulls events from the queue and applies game logic via MoveMediator
      - updates the Renderer

    Key invariants:
      - Only the engine mutates turn/dice flow.
      - MoveMediator validates and performs moves.
      - Renderer only draws based on the current board state + UI hints.
    """

    def __init__(self) -> None:
        pg.init()
        self.clock = pg.time.Clock()

        # Core domain state
        self.board = Board()
        self.game_state = GameState()
        self.mediator = MoveMediator(self.board, self.game_state)

        # Events & presentation
        self.events = eventHandler()
        self.renderer = Renderer(self.board)
        self.input_handler = InputHandler(self.renderer, self.events)

        # Turn state
        self.turn_active: bool = False
        self.moves_remaining: List[int] = []  # pip values left to spend this turn

        self.running = True

    # -----------------------
    # Main loop
    # -----------------------
    def run(self):
        self.renderer.init()

        while self.running and not self.game_state.check_winner(self.board):
            # Start the turn properly
            self._start_turn()

            # Main turn loop
            while self.turn_active:
                # try:
                    # Handle input (mouse, keyboard)
                    self.input_handler.process_events()

                    # Process queued game events (includes StackSelected + MoveEvent)
                    self.process_game_events()
                    self.renderer.draw_frame()

                    # End turn if no moves left or no legal moves
                    if not self.moves_remaining or not self._any_legal_moves():
                        self._end_turn()

                    # Render the board
                    self.clock.tick(60)

                # except Exception as e:
                #     print(f"[ERROR] {e}") 
                    

        # Game finished
        winner = self.game_state.check_winner(self.board)
        print(f"Winner: {winner}")
        pg.quit()


    # -----------------------
    # Turn management
    # -----------------------
    def _start_turn(self) -> None:
        current = self.game_state.get_current_player
        dice = self.game_state.roll_dice()  # tuple from GameState
        self.moves_remaining = self._explode_dice(dice)
        # Keep GameState._dice in sync (so MoveMediator.validate_move can read it)
        self._set_game_dice(tuple(self.moves_remaining))
        self.turn_active = True
        print(f"\n--- {current}'s turn --- rolled {dice} → moves {self.moves_remaining}")

        # Optional: immediate pass if literally nothing legal
        if not self._any_legal_moves():
            print(f"{current} has no legal moves. Passing turn.")
            self._end_turn()

    def _end_turn(self) -> None:
        """Finish current turn and pass to the next player."""
        if not self.turn_active:
            return
        self.turn_active = False
        self.moves_remaining = []
        self._set_game_dice(tuple())  # no pips available between turns
        self.game_state.next_turn()

    @staticmethod
    def _explode_dice(dice: tuple[int, int]) -> List[int]:
        """Turn (a, b) into [a, b] or [a, a, a, a] for doubles."""
        a, b = dice
        # in case i want the doubles to be doubled
        # return [a, a, a, a] if a == b els e [a, b]

        return [a, b]

    def _set_game_dice(self, dice_tuple: tuple[int, ...]) -> None:
        """
        Keep mediator-visible dice in sync. (Ideally expose a setter in GameState;
        for now we assign the private field.)
        """
        self.game_state._dice = dice_tuple  # type: ignore[attr-defined]

    # -----------------------
    # Event processing
    # -----------------------
    def process_game_events(self) -> None:
        """Process all queued events and apply game logic."""
        while not self.events.empty_events():
            event = self.events.pop_event()
            print("DEBUG popped event:", event)

            if event["type"] == "StackSelected":
                # Highlight possible destinations
                stack_id = event["stack_id"]
                possible_moves = self._get_valid_destinations(stack_id)
                print(f"DEBUG Highlight stacks: {possible_moves}")
                self.renderer.highlight_stacks(possible_moves)

            elif event["type"] == "MoveEvent":
                # Handle full move (from_stack → to_stack)
                self._handle_move_event(event)
                self.renderer.clear_highlights()
            
            elif event["type"] == "QuitEvent":
                ...

                



    def _handle_move_event(self, ev: dict) -> None:
        print(f"DEBUG: Handling MoveEvent {ev}")
        if not self.turn_active or not self.moves_remaining:
            print("DEBUG: No active turn or no moves remaining")
            return

        from_stack = ev.get("from_stack")
        to_stack = ev.get("to_stack")
        if not isinstance(from_stack, int) or not isinstance(to_stack, int):
            print("DEBUG: Invalid from/to stack")
            return

        current = self.game_state.get_current_player  # FIXED HERE
        print(f"DEBUG: Checking move for player {current}")

        allowed = self.mediator.validate_move(from_stack, to_stack)
        print(f"DEBUG validate_move returned: {allowed}")

        if not allowed:
            print(f"Rejected move {from_stack} → {to_stack}")
            return

        print("DEBUG: move is allowed")
        moved_stone, _ = self.mediator.execute_move(from_stack, to_stack)

        used = self._distance_for_player(from_stack, to_stack, current)
        print(f"DEBUG: Consuming pip {used}")
        self._consume_pip(used)


    # -----------------------
    # Dice consumption
    # -----------------------
    def _consume_pip(self, distance: int) -> None:
        """
        Remove the used pip from moves_remaining.
        If 'distance' doesn't match a remaining die (overshoot during bear-off),
        remove the max remaining die.
        """
        if distance in self.moves_remaining:
            self.moves_remaining.remove(distance)
        elif self.moves_remaining:
            self.moves_remaining.remove(max(self.moves_remaining))
        self._set_game_dice(tuple(self.moves_remaining))

    @staticmethod
    def _distance_for_player(from_stack: int, to_stack: int, player: str) -> int:
        """
        Mirror MoveMediator._calculate_distance (for int→int case):
        white moves down (to smaller numbers): distance = from - to
        black moves up (to larger numbers):  distance = to - from
        """
        if player == "white":
            return from_stack - to_stack
        return to_stack - from_stack

    # -----------------------
    # Legal-move probing (simple, fast)
    # -----------------------
    def _any_legal_moves(self) -> bool:
        """
        Quick probe: for each die pip left and each top stone of current player,
        see if at least one valid destination exists (including simple bear-off target).
        This avoids turns getting stuck when no moves are possible.
        """
        p = self.game_state.get_current_player
        pips = sorted(set(self.moves_remaining), reverse=True)  # try larger first

        # If player has stones on the bar, only bar entries are legal sources
        if self.board.get_bar.must_reenter(p):
            return self._any_bar_entry_legal(p, pips)

        # Scan all stacks with a top stone of the current color
        for s in range(1, 25):
            stack = self.board.get_stack(s)
            if stack.is_empty():
                continue
            if stack.peek_stone().get_color != p:
                continue

            for pip in pips:
                # Try board destination
                to = s - pip if p == "white" else s + pip

                # Board square
                if 1 <= to <= 24 and self.mediator.validate_move(s, to):
                    return True

                # Off-board “virtual” target for bear-off (25 for white, 0 for black)
                if not (1 <= to <= 24):
                    target_off = 25 if p == "white" else 0
                    if self.mediator.validate_move(s, target_off):
                        return True

        return False

    def _any_bar_entry_legal(self, player: str, pips: list[int]) -> bool:
        """When on bar, can we enter with any die?"""
        # White enters on 24→19 (top-right quadrant), black on 1→6 (bottom-left)
        for pip in pips:
            to = (25 - pip) if player == "white" else pip
            if 1 <= to <= 24 and self.mediator.validate_move(self.board.get_bar, to):
                return True
        return False
    
    def _handle_stack_selected(self, stack_id: int):
        current_player = self._game_state.get_current_player

        # Step 1: Check if stack has stones for current player
        stack = self.board.get_stack(stack_id)
        stones = stack.get_stones
        if not stones or stones[0].get_color != current_player:
            print("Invalid selection: Not your stack.")
            return

        # Step 2: Find possible destinations
        moves = self.game_state.get_current_dice
        possible_destinations = []

        for move in moves:
            direction = 1 if current_player == "white" else -1
            target = stack_id + (move * direction)
            
            # Bearing off special case
            if target < 1 or target > 24:
                target = 0 if current_player == "black" else 25
            
            # Validate with mediator
            if self.mediator.validate_move(stack_id, target):
                possible_destinations.append(target)

        # Step 3: Send to renderer
        self.renderer.highlight_stacks(possible_destinations)
        print(f"Possible destinations for stack {stack_id}: {possible_destinations}")

    def _get_valid_destinations(self, from_stack: int) -> list[int]:
        valid_destinations = []
        current_player = self.game_state.get_current_player
        direction = -1 if current_player == "white" else 1  # White moves down (24→1), Black moves up (1→24)

        for pip in self.moves_remaining:
            candidate = from_stack + (direction * pip)

            # Bear-off logic can be added later; skip out-of-range for now
            if candidate < 1 or candidate > 24:
                continue

            if self.mediator.validate_move(from_stack, candidate):
                valid_destinations.append(candidate)

        print(f"DEBUG: from_stack {from_stack}, pips {self.moves_remaining}, candidates {valid_destinations}")


        return valid_destinations

ge = GameEngine()

ge.run()