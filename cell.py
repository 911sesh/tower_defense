import pygame as pg
pg.init()
class Block(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill('red')
        self.clarity = 255



    def update(self, screen):
        self.image.set_alpha(self.clarity)
        screen.blit(self.image, self.rect)

class Stone(Block):
    def __init__(self, pos):
        super().__init__(pos)
        self.image.fill((180, 180, 225))
        self.durability = 360

class Sand(Block):
    def __init__(self, pos):
        super().__init__(pos)
        self.image.fill((255, 204, 92))
        self.durability = 180