class StoneAnimation:
    stone: object
    start_pos: tuple[float, float]
    end_pos: tuple[float, float]
    progress: float = 0.0
    duration: float = 0.3

    def update(self, dt: float) -> bool:
        self.progress = min(self.progress + dt / self.duration, 1.0)
        return self.progress >= 1.0

    def get_current_pos(self) -> tuple[int, int]:
        t = self.progress ** 2 * (3 - 2 * self.progress)
        x = int(self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * t)
        y = int(self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * t)
        return (x, y)