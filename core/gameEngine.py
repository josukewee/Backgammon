import pygame as pg
from commands.MoveCommand import MoveCommand
from commands.CommandManager import CommandManager
from core.eventHandler import eventHandler
from core.moveMediator import MoveMediator
from core.InputHandler import InputHandler
from presentation.Renderer import Renderer
from datastructures.Board import Board
from core.gameState import GameState
import time


class GameEngine:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()

        # Core game state
        self.board = Board()
        self.game_state = GameState()
        self.mediator = MoveMediator(self.board, self.game_state)
        self.eventHandler = eventHandler()

        # Renderer (subscribed to mediator events)
        self.renderer = Renderer()
        self.input_handler = InputHandler(self.renderer, self.eventHandler)

        # Command history
        self.command_manager = CommandManager()

        self.running = True

    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(self.renderer.FPS) / 1000.0  # seconds since last frame

            self.renderer.init()
            self.input_handler.process_events()
            # self.renderer.update(dt)

        pg.quit()

    def _handle_events(self):
        """Handle user input"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                self._handle_click(event.pos)

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_u:  # undo
                    self.command_manager.undo()

    def _handle_click(self, pos):
        """Example: map mouse click to a move"""
        stack_id = self._map_click_to_stack(pos)
        if stack_id is not None:
            # Example: try moving from clicked stack to fixed target
            move_cmd = MoveCommand(self.mediator, from_stack=stack_id, to_stack=12)
            try:
                self.command_manager.execute(move_cmd)
                self.renderer.on_board_change("move", stack_id, 12)
            except ValueError as e:
                print(f"Invalid move: {e}")

    def _map_click_to_stack(self, pos):
        """Translate a click position to a stack ID"""
        x, y = pos
        col = x // self.renderer.SQ_SIZE
        row = y // self.renderer.SQ_SIZE

        # Example: only support simple mapping for now
        if 0 <= col < 12 and row in (0, 1):
            stack_id = col if row == 0 else col + 12
            return stack_id
        return None
    
ge = GameEngine()
ge.run()