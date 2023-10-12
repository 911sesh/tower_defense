import pygame as pg

pg.init()


class Cell(pg.sprite.Sprite):
    def __init__(self, size: int, x: int, y: int, *groups):
        super().__init__(*groups)
        self.rect = pg.Rect(x, y, size, size)
        self.color = (20, 20, 20)
        self.available = False

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect, 1)

    def available_animation(self, player):
        if self.rect.colliderect(player.building_zone) and not self.rect.colliderect(player.rect):
            self.color = (0, 100, 0)
        else:
            self.color = (20, 20, 20)

    def update(self, screen, player):
        self.available_animation(player)
        self.draw(screen)


class Map:
    def __init__(self, cell_size):
        self.cells = self.__get_group(cell_size)
        self.blocks = pg.sprite.Group()

    @staticmethod
    def __get_group(cell_size):
        group = pg.sprite.Group()
        display_size = pg.display.get_desktop_sizes()[0]
        for x in range(0, display_size[0], cell_size):
            for y in range(0, display_size[1], cell_size):
                Cell(cell_size, x, y, group)
        return group

    def update(self, screen, player):
        self.cells.update(screen, player)
        self.blocks.update(screen)