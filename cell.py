import pygame as pg

class Block(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill('red')


    def update(self, screen):
        screen.blit(self.image, self.rect)
