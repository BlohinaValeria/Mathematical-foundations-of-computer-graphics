class Settings:
    """Настройки игры"""
    def __init__(self):
        # Экран
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 0)

        # Корабль
        self.ship_speed = 3   # скорость корабля
        self.ship_limit = 3   # количество жизней

        # Пули
        self.bullet_speed = 4
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 0)
        self.bullets_allowed = 5

        # Инопланетяне
        self.alien_speed = 0.3
        self.fleet_drop_speed = 5
        self.fleet_direction = 1  # 1 — вправо, -1 — влево

        # Ускорение игры
        self.speedup_scale = 1.05
