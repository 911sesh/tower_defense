import pygame as pg

class Block(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill('red')

    def update(self, screen):
        screen.blit(self.image, self.rect)

class Stone(Block):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill((180, 180, 225))
        self.durability = 6

    def update(self, screen):
        screen.blit(self.image, self.rect)

class Sand(Block):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill((255, 204, 92))
        self.durability = 3

    def update(self, screen):
        screen.blit(self.image, self.rect)




