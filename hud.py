import pygame as pg

pg.init()
#для клавиш 1-9 выбирается ячейка в хотбаре
class HUDBar(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 600))
        self.rect = self.image.get_rect()
        self.image.fill('grey')

    def update(self, screen):
        screen.blit(self.image, self.rect)
