import pygame as pg

pg.init()

class Button(pg.sprite.Sprite):
    def __init__(self, size: tuple[int, int], color: str, text: str, font_size: int, font_color: str,
                 pos: tuple[int, int]):
        super().__init__()
        self.font = pg.font.SysFont('kenvector_future.ttf', font_size, True)
        self.text_image = self.font.render(text, True, font_color)
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.image.blit(self.text_image, (0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.image_copy = self.image
        self.rect_copy = self.rect
        self.big_image = pg.transform.scale(self.image, (size[0] * 1.2, size[1] * 1.2))
        self.big_rect = self.big_image.get_rect(center=self.rect.center)

    def animate(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.image = self.big_image
            self.rect = self.big_rect
        else:
            self.image = self.image_copy
            self.rect = self.rect_copy

    def is_pressed(self):
        return pg.mouse.get_pressed()[0] and self.rect.collidepoint(pg.mouse.get_pos())

    def update(self, surface: pg.Surface):
        surface.blit(self.image, self.rect)
        self.animate()

