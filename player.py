import pygame as pg
from item_block_classes import Stone, Sand
from hudbar import HUDBar

pg.init()


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('1 Woodcutter/Woodcutter.png'), (64, 64))
        self.default_image = self.image
        self.reverse_image = pg.transform.flip(self.image, True, False)
        self.attack_images = [pg.image.load(f'1 Woodcutter/Woodcutter_attack{i}.png') for i in range(1, 4)]

        self.rect = self.image.get_rect(centerx=700, bottom=900)
        self.building_zone = pg.Rect(self.rect.x - 64, self.rect.y - 64, 192, 192)

        self.frame = 0
        self.is_animated = False

        self.jump_speed = 0
        self.boost = 9.8
        self.dir = pg.Vector2()

        self.hudbar = HUDBar()
        self.chosen_item = self.hudbar.chosen_cell.stack.sprites()[0]

    def refresh_item_choose(self):
        if self.hudbar.chosen_cell.stack.sprites():
            self.chosen_item = self.hudbar.chosen_cell.stack.sprites()[0]
        else:
            self.chosen_item = None

    def move(self):
        self.rect.x += 5 * self.dir.x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1400:
            self.rect.right = 1400

    def flip(self):
        if pg.key.get_pressed()[pg.K_a]:
            self.image = self.reverse_image
        else:
            self.image = self.default_image

    def change_dir(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.dir.x = -1
        elif keys[pg.K_d]:
            self.dir.x = 1
        else:
            self.dir.x = 0

        if self.jump_speed > 0:
            self.dir.y = 1
        elif self.jump_speed < 0:
            self.dir.y = -1

    # def attack(self):
    #     if pg.mouse.get_pressed()[2]:
    #         self.is_animated = True
    #
    # def attack_animation(self):
    #     if self.is_animated:
    #         self.frame += 1
    #         if 0 < self.frame < 61:
    #             self.image = self.attack_images[0]
    #         elif 60 < self.frame < 121:
    #             self.image = self.attack_images[1]
    #         elif 120 < self.frame < 181:
    #             self.image = self.attack_images[2]
    #         else:
    #             self.is_animated = False
    #             self.frame = 0
    #     else:
    #         self.image = self.default_image

    def jump(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.jump_speed == 0:
            self.jump_speed = -5
        if self.rect.bottom <= 900:
            self.jump_speed += self.boost / 60
            self.rect.y += self.jump_speed
        if self.rect.bottom > 900:
            self.rect.bottom = 900
            self.jump_speed = 0

    def break_block(self, map):
        m_pos = pg.mouse.get_pos()
        for block in map.blocks:
            if self.building_zone.colliderect(block.rect) and block.rect.collidepoint(m_pos) and pg.mouse.get_pressed()[1]:
                pass

    @staticmethod
    def mouse_block_colliding(map):
        m_pos = pg.mouse.get_pos()
        for block in map.blocks:
            if block.rect.collidepoint(m_pos):
                return True
        return False

    def place_block(self, map):
        m_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        r_click = pg.mouse.get_pressed()[0]
        print(self.hudbar.chosen_cell.stack.sprites())
        if r_click and self.chosen_item is not None and not keys[pg.K_TAB] and not self.mouse_block_colliding(map):
            for cell in map.cells:
                pass

    def follow(self):
        self.building_zone.center = self.rect.center

    def check_building_collisions_x(self, map):
        for cell in map.blocks:
            if self.rect.colliderect(cell.rect):
                if self.dir.x == 1:
                    self.rect.right = cell.rect.left
                elif self.dir.x == -1:
                    self.rect.left = cell.rect.right

    def check_building_collisions_y(self, map):
        for cell in map.blocks:
            if self.rect.colliderect(cell.rect):
                if self.dir.y == -1:
                    self.rect.top = cell.rect.bottom
                else:
                    self.jump_speed = 0

    def update(self, screen, map):
        self.change_dir()
        self.follow()
        self.flip()

        self.move()
        self.check_building_collisions_x(map)
        self.jump()
        self.check_building_collisions_y(map)

        self.break_block(map)
        self.place_block(map)

        self.hudbar.update(screen)
        self.refresh_item_choose()
        # self.attack()
        # self.attack_animation()

        pg.draw.rect(screen, 'green', self.rect, width=1)
        pg.draw.rect(screen, 'violet', self.building_zone, width=1)
        screen.blit(self.image, self.rect)
