class Camera:
    def __init__(self, screen_width: int, world_width: int, max_x: int):
        self.screen_width = screen_width
        self.world_width = world_width
        self.max_x = max_x
        self.x = 0
        self.follow_speed = 8

    def update(self, target):
        target_center_x = target.rect.centerx
        desired_x = target_center_x - self.screen_width // 2
        self.x = max(0, min(desired_x, self.max_x))

    def apply(self, rect):
        return rect.move(-int(self.x), 0)

    def apply_point(self, point):
        x, y = point
        return x - int(self.x), y

    def apply_points(self, points):
        return [self.apply_point(point) for point in points]

    def screen_to_world(self, point):
        x, y = point
        return x + int(self.x), y

    def world_to_screen(self, point):
        x, y = point
        return x - int(self.x), y
