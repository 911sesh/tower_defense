import pygame as pg
from item_block_classes import Sand, Stone

pg.init()


class HUDBar(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 600))
        self.rect = self.image.get_rect(centery=900 // 2)
        self.image.fill('grey')
        self.cells = self.__get_cells()
        self.chosen_cell = self.cells.sprites()[0]

    def __get_cells(self):
        group = pg.sprite.Group()
        for y in range(10, self.image.get_size()[1] - 65, 65):
            HUDBarCell(self.rect.x + 5, self.rect.y + y, group)
        return group

    def fill_chosen_cell(self):
        self.chosen_cell.image.fill('grey82')

    def choose_cell(self):
        keys = pg.key.get_pressed()
        for i in range(pg.K_1, pg.K_9 + 1):
            if keys[i]:
                self.chosen_cell.image.fill('white')
                self.chosen_cell = self.cells.sprites()[i - 49]

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

        self.stack = pg.sprite.Group()
        self.stack.add(Sand(self.rect.topleft), Sand(self.rect.topleft), Sand(self.rect.topleft),
                       Sand(self.rect.topleft), Sand(self.rect.topleft), Sand(self.rect.topleft),
                       Stone(self.rect.topleft))
        self.item_counter = len(self.stack)

    def show_item_picture(self, screen):
        for item in self.stack:
            screen.blit(item.image, item.rect)

    def update(self, screen):
        screen.blit(self.image, self.rect)
        self.show_item_picture(screen)
