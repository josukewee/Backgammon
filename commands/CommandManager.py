from commands.command import Command


class CommandManager:
    def __init__(self):
        self._history: list[Command] = []
        self._undone: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        self._undone.clear()
    def undo(self) -> Command:
        if not self._history:
            raise RuntimeError("No commands to undo")

        command = self._history.pop()
        command.undo()
        self._undone.append(command)
        return command

    def redo(self) -> Command:
        if not self._undone:
            raise RuntimeError("No commands to redo")

        command = self._undone.pop()
        command.execute()
        self._history.append(command)
        return command

    def clear(self) -> None:
        self._history.clear()
        self._undone.clear()

    def get_history(self):
        return list(self._history)

    def get_redo_stack(self):
        return list(self._undone)