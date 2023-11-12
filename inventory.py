import pygame as pg

pg.init()


class Cell(pg.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((150, 150))
        self.color = 'green'
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, screen):
        screen.blit(self.image, self.rect)


class Inventory:
    def __init__(self):
        self.image = pg.Surface((1400 // 3, 800))
        self.rect = self.image.get_rect(centerx=1400 // 1.20, centery=900 // 2)
        self.color = 'gray'
        self.cells = self.get_cells()

    def open(self, screen):
        keys = pg.key.get_pressed()
        if keys[pg.K_TAB]:
            self.rect = pg.draw.rect(screen, self.color, self.rect)
            self.cells.update(screen)

    def get_cells(self):
        group = pg.sprite.Group()
        for x in range(5, self.image.get_size()[0], 155):
            for y in range(5, self.image.get_size()[1], 160):
                Cell(self.rect.x + x, self.rect.y + y, group)
        return group

    def update(self, screen):
        self.open(screen)
