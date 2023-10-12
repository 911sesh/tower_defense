import pygame as pg

pg.init()


class Block(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill('red')
        self.clarity = 255
        self.durability = 0
        self.start_durability = 0

    def destroy(self):
        if self.clarity != 0 and self.durability != 0:
            self.clarity -= 1
            self.durability -= 1
        else:
            self.kill()

    def repair(self):
        self.durability = self.start_durability
        self.clarity = 255


    def update(self, screen):
        self.image.set_alpha(self.clarity)
        screen.blit(self.image, self.rect)


class Stone(Block):
    def __init__(self, pos):
        super().__init__(pos)
        self.image.fill((180, 180, 225))
        self.durability = 360
        self.start_durability = 360


class Sand(Block):
    def __init__(self, pos):
        super().__init__(pos)
        self.image.fill((255, 204, 92))
        self.durability = 180
        self.start_durability = 180
