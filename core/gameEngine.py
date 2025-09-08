from datastructures.Bar import Bar
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
      - Renderer only draws based on the current _board state + UI hints.
    """

    def __init__(self) -> None:
        pg.init()
        self._clock = pg.time.Clock()

        # core domain state
        self._board = Board()
        self._game_state = GameState()
        self._mediator = MoveMediator(self._board, self._game_state)

        # _events & presentation
        self._events = eventHandler()
        self._renderer = Renderer(self._board)
        self._input_handler = InputHandler(self._renderer, self._events)

        # turn state
        self._turn_active: bool = False
        self._moves_remaining: List[int] = []  

        self.running = True

        self._state = "IDLE"            # IDLE | STACK_SELECTED
        self._selected_stack = None       


    # Main loop
    def run(self):
        self._renderer.init()

        while self.running and not self._game_state.check_winner(self._board):
            # Start the turn properly
            self._start_turn()

            # Main turn loop
            while self._turn_active:
                # try:
                    self._input_handler.process_events()

                    # Process queued game events (includes StackSelected + MoveEvent)
                    self.process_game_events()
                    self._renderer.draw_frame(self._game_state.get_current_player, self._game_state.get_current_dice)

                    # end turn if no moves left or no legal moves
                    if not self._moves_remaining or not self._any_legal_moves():
                        self._end_turn()

                    # Render the board
                    self._clock.tick(60)

                # except Exception as e:
                #     print(f"[ERROR] {e}") 
                    

        # Game finished
        winner = self._game_state.check_winner(self.board)
        print(f"Winner: {winner}")
        pg.quit()



    # turn management
    def _start_turn(self) -> None:
        current_player = self._game_state.get_current_player
        dice = self._game_state.roll_dice() 
        self._moves_remaining = self._explode_dice(dice)
        
        # keep GameState._dice in sync (so MoveMediator.validate_move can read it)
        self._set_game_dice(tuple(self._moves_remaining))
        self._turn_active = True
        print(f"\n--- {current_player}'s turn --- rolled {dice} → moves {self._moves_remaining}")

        bar_stones = self._board.get_bar_stones(current_player)
        if bar_stones:
            print(f"DEBUG: {current_player} has {len(bar_stones)} stone(s) on bar → forcing re-entry")

            # compute destinations as if "BarSelected"
            destinations = []
            for to_stack in range(1, 25):
                if self._mediator.validate_move(self._board.get_bar, to_stack):
                    if(to_stack in self._game_state.get_current_dice):
                        destinations.append(to_stack)

            if destinations:
                self._events.append({
                    "type": "BarSelected",
                    "stack_id": "BAR",  
                    "destinations": destinations,
                })
                self._renderer.highlight_stacks(destinations)
            else:
                # no legal moves from bar → skip turn immediately
                print(f"DEBUG: {current_player} cannot re-enter → turn skipped")
                self._end_turn()

        if not self._any_legal_moves():
            print(f"{current_player} has no legal moves. Passing turn.")
            self._end_turn()

    def _end_turn(self) -> None:
        """Finish current turn and pass to the next player."""
        if not self._turn_active:
            return
        self._turn_active = False
        self._moves_remaining = []
        self._set_game_dice(tuple()) 
        self._game_state.next_turn()




    # Event processing
    def process_game_events(self) -> None:
        """Process all queued events and apply game logic."""
        while not self._events.empty_events():
            event = self._events.pop_event()
            print("DEBUG popped event:", event)

            if event["type"] == "ClickStack":
                self._handle_click_stack(event["stack_id"])

            elif event["type"] == "QuitEvent":
                return False

            elif event["type"] == "MoveEvent":
                
                self._handle_move_event(event)
                self._renderer.clear_highlights()
            

                
    def _handle_click_stack(self, stack_id: int) -> None:
        current_player = self._game_state.get_current_player

        # Case 0: must re-enter from bar
        if self._board.get_bar.must_reenter(current_player):
            self._attempt_bar_reentry(stack_id)
            return

        if self._state == "IDLE":
            if len(self._get_valid_destinations(stack_id)) and self._board.get_stack_color(stack_id) == current_player:
                self._selected_stack = stack_id
                self._state = "STACK_SELECTED"
                destinations = self._get_valid_destinations(stack_id)
                print(f"DEBUG: stack {stack_id} selected, possible moves {destinations}")
                self._renderer.highlight_stacks(destinations)
            else:
                print(f"DEBUG: stack {stack_id} has no moves → staying IDLE")


        elif self._state == "STACK_SELECTED":
            if stack_id != self._selected_stack:
                if stack_id in self._get_valid_destinations(self._selected_stack):
                    self._handle_move_event({
                        "type": "MoveEvent",
                        "from_stack": self._selected_stack,
                        "to_stack": stack_id
                    })
                else:
                    print(f"DEBUG: invalid move {self._selected_stack} → {stack_id}")
            # Reset in both cases
            self._selected_stack = None
            self._state = "IDLE"
            self._renderer.clear_highlights()

    # Helpers
    def _attempt_bar_reentry(self, to_stack: int) -> None:
        """Handle forced re-entry from bar."""
        current_player = self._game_state.get_current_player
        bar = self._board.get_bar

        if self._mediator.validate_move(bar, to_stack):
            print(f"DEBUG: re-entering {current_player} stone to {to_stack}")
            self._handle_move_event({
                "type": "MoveEvent",
                "from_stack": bar,
                "to_stack": to_stack
            })
            self._renderer.clear_highlights()
        else:
            print(f"DEBUG: invalid bar re-entry to {to_stack}")


    def _handle_move_event(self, ev: dict) -> None:
        print(f"DEBUG: Handling MoveEvent {ev}")
        if not self._turn_active or not self._moves_remaining:
            print("DEBUG: No active turn or no moves remaining")
            return

        from_stack = ev.get("from_stack")
        to_stack = ev.get("to_stack")
        # if not isinstance(from_stack, int) or not isinstance(to_stack, int):
        #     print("DEBUG: Invalid from/to stack")
        #     return

        current = self._game_state.get_current_player  # FIXED HERE
        print(f"DEBUG: Checking move for player {current}")

        allowed = self._mediator.validate_move(from_stack, to_stack)
        print(f"DEBUG validate_move returned: {allowed}")

        if not allowed:
            print(f"Rejected move {from_stack} → {to_stack}")
            return

        print("DEBUG: move is allowed")
        moved_stone, _ = self._mediator.execute_move(from_stack, to_stack)
        if isinstance(from_stack, int):
            used = self._distance_for_player(from_stack, to_stack, current)
        elif isinstance(from_stack, Bar):
            used = self._distance_from_bar(to_stack, current)
        else:
            raise ValueError(f"Unsupported from_stack type: {type(from_stack)}")


        print(f"DEBUG: Consuming pip {used}")
        self._consume_pip(used)

    # Dice consumption
  
    def _consume_pip(self, distance: int) -> None:
        """
        Remove the used pip from moves_remaining.
        If 'distance' doesn't match a remaining die (overshoot during bear-off),
        remove the max remaining die.
        """
        if distance in self._moves_remaining:
            self._moves_remaining.remove(distance)
        elif self._moves_remaining:
            self._moves_remaining.remove(max(self._moves_remaining))
        self._set_game_dice(tuple(self._moves_remaining))

    def _set_game_dice(self, dice_tuple: tuple[int, ...]) -> None:
        """
        Keep mediator-visible dice in sync. (Ideally expose a setter in GameState;
        for now we assign the private field.)
        """
        self._game_state._dice = dice_tuple


    # Legal-move probing 
    def _any_legal_moves(self) -> bool:
        """
        Quick probe: for each die pip left and each top stone of current player,
        see if at least one valid destination exists (including bearing off).
        """

        p = self._game_state.get_current_player
        # print(self.mediator.can_bear_off(p))
        pips = sorted(set(self._moves_remaining), reverse=True)  # try larger first

        # If player has stones on the bar, only bar entries are legal sources
        if self._board.get_bar.must_reenter(p):
            return self._any_bar_entry_legal(p, pips)

        # iterate all stacks with a top stone of the current color
        for s in range(1, 25):
            stack = self._board.get_stack(s)
            if stack.is_empty():
                continue
            if stack.peek_stone().get_color != p:
                continue

            for pip in pips:
                # candidate destination
                to = s - pip if p == "white" else s + pip

                # print("it came here ")

                # 2. Bearing off
                if self._mediator.can_bear_off(p):
                    home_target = 0 if p == "white" else 25
                    # print("can bear off")
                    if self._mediator.validate_move(s, home_target):
                        # print("allowed")
                        return True

                # 1. Board move
                if 1 <= to <= 24 and self._mediator.validate_move(s, to):
                    return True


        return False


    def _any_bar_entry_legal(self, player: str, pips: list[int]) -> bool:
        """When on bar, can we enter with any die?"""
        # White enters on 24→19 (top-right quadrant), black on 1→6 (bottom-left)
        for pip in pips:
            to = (25 - pip) if player == "white" else pip
            if 1 <= to <= 24 and self._mediator.validate_move(self._board.get_bar, to):
                return True
        return False
    
    def _get_valid_destinations(self, from_stack: int) -> list[int]:
        valid_destinations = []
        current_player = self._game_state.get_current_player
        direction = -1 if current_player == "white" else 1 

        for pip in self._moves_remaining:
            candidate = from_stack + (direction * pip)

            if 1 <= candidate <= 24:
                if self._mediator.validate_move(from_stack, candidate):
                    valid_destinations.append(candidate)

            else:
                target_off = 25 if current_player == "black" else 0
                if self._mediator.validate_move(from_stack, target_off):
                    valid_destinations.append(target_off)

        print(f"DEBUG: from_stack {from_stack}, pips {self._moves_remaining}, candidates {valid_destinations}")
        return valid_destinations
    
    @staticmethod
    def _explode_dice(dice: tuple[int, int]) -> List[int]:
        """Turn (a, b) into [a, b] or [a, a, a, a] for doubles."""
        a, b = dice
        # in case i want the doubles to be doubled
        # return [a, a, a, a] if a == b els e [a, b]

        return [a, b]
    
    @staticmethod
    def _distance_for_player(from_stack: int, to_stack: int, player: str) -> int:
        """
        Mirror MoveMediator._calculate_distance (for int→int case):
        white moves down (to smaller numbers): distance = from - to
        black moves up (to larger numbers):  distance = to - from
        """
        if to_stack in (0, 25):
            if player == "white":
                return from_stack  # pip = point index
            return 25 - from_stack
        
        if player == "white":
            return from_stack - to_stack
        return to_stack - from_stack

    @staticmethod
    def _distance_from_bar(to_stack: int, player: str) -> int:
        """
        Distance when re-entering from the bar.
        - White enters on stacks 24 → 19 (dice 1 → 6).
        - Black enters on stacks 1 → 6 (dice 1 → 6).
        """
        if player == "white":
            # white enters from top into points 24..19
            return 25 - to_stack
        elif player == "black":
            # black enters from bottom into points 1..6
            return to_stack
        else:
            raise ValueError(f"Unknown player: {player}")
        
ge = GameEngine()

ge.run()