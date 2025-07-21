

class Stone:
    def __init__(self, uid: int, color: str):
        self._uid = uid
        self._color = color
        self.is_on_bar = False

    @property
    def get_color(self) -> str:
        return self._color
    
    @property
    def get_stone_by_uid(self, uid: int):
        return self._uid

    def __repr__(self):
        return f"Stone {self._uid}"