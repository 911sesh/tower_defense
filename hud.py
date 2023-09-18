import pygame as pg

pg.init()
#для клавиш 1-9 выбирается ячейка в хотбаре
class HUDBar(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 600))
        self.rect = self.image.get_rect(centery=900//2)
        self.image.fill('grey')
        self.cells = self.__get_cells()
        self.chosen_cell = self.cells.sprites()[0]

    def __get_cells(self):
        group = pg.sprite.Group()
        for y in range(10, self.image.get_size()[1] - 65, 65):
            HUDBarCell(self.rect.x + 5, self.rect.y + y, group)
        return group

    def fill_chosen_cell(self):
            self.chosen_cell.image.fill('red')

    def choose_cell(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            self.chosen_cell = self.cells.sprites()[0]
        elif keys[pg.K_2]:
            self.chosen_cell = self.cells.sprites()[1]
        elif keys[pg.K_3]:
            self.chosen_cell = self.cells.sprites()[2]
        elif keys[pg.K_4]:
            self.chosen_cell = self.cells.sprites()[3]
        elif keys[pg.K_5]:
            self.chosen_cell = self.cells.sprites()[4]
        elif keys[pg.K_6]:
            self.chosen_cell = self.cells.sprites()[5]
        elif keys[pg.K_7]:
            self.chosen_cell = self.cells.sprites()[6]
        elif keys[pg.K_8]:
            self.chosen_cell = self.cells.sprites()[7]
        elif keys[pg.K_9]:
            self.chosen_cell = self.cells.sprites()[8]

    def update(self, screen):
        screen.blit(self.image, self.rect)
        self.choose_cell()
        self.fill_chosen_cell()
        self.cells.update(screen)


class HUDBarCell(pg.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((40, 60))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image.fill('white')
        self.item = None

    def update(self, screen):
        screen.blit(self.image, self.rect)
