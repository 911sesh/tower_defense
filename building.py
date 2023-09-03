import pygame as pg


class Cell(pg.sprite.Sprite):
    def __init__(self, size: int, x: int, y: int, *groups):
        super().__init__(*groups)
        self.rect = pg.Rect(x, y, size, size)
        self.filler = 1
        self.color = (20, 20, 20)
        self.available = False

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect, self.filler)

    def click(self, player):
        m_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        if not keys[pg.K_TAB]:
            if pg.mouse.get_pressed()[0] and self.rect.collidepoint(m_pos) and self.available:
                self.filler = 0
                self.color = 'green'

    def update(self, screen, player):
        self.draw(screen)
        self.click(player)

class MapWeb:
    def __init__(self, cell_size):
        self.cells = self.create_group(cell_size)

    def create_group(self, cell_size):
        group = pg.sprite.Group()
        display_size = pg.display.get_desktop_sizes()[0]
        for x in range(0, display_size[0], cell_size):
            for y in range(0, display_size[1], cell_size):
                Cell(cell_size, x, y, group)
        return group

    def is_building_available(self, player):
        for cell in self.cells:
            if cell.rect.colliderect(player.building_zone) and not cell.rect.colliderect(player.rect):
                cell.color = (0, 100, 0)
                cell.available = True
            else:
                cell.color = (20, 20, 20)
                cell.available = False


    def update(self, screen, player):
        self.cells.update(screen, player)
        self.is_building_available(player)
