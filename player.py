import pygame as pg
from item_block_classes import Stone, Sand
from hudbar import HUDBar
from health import HealthHud
from enemy import Enemy

pg.init()


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('1 Woodcutter/Woodcutter.png'), (64, 64))
        self.default_image = self.image
        self.reverse_image = pg.transform.flip(self.image, True, False)
        self.attack_images = [pg.transform.scale(pg.image.load(f'1 Woodcutter/img_{i}.png'), (64, 64)) for i in range(6)]

        self.rect = self.image.get_rect(centerx=700, bottom=900)
        self.building_zone = pg.Rect(self.rect.x - 64, self.rect.y - 64, 192, 192)
        self.hp = 100

        self.frame = 0
        self.is_animated = False

        self.jump_speed = 0
        self.boost = 9.8
        self.dir = pg.Vector2()

        self.hudbar = HUDBar()
        self.chosen_item = self.hudbar.chosen_cell.stack.sprites()[0]

        self.health_hud = HealthHud(550, 0, 300, 20, 100)

        self.enemy = Enemy()

    def refresh_item_choose(self):
        if self.hudbar.chosen_cell.stack.sprites():
            self.chosen_item = self.hudbar.chosen_cell.stack.sprites()[0]
        else:
            self.chosen_item = None

    def draw_chosen_item(self, screen):
        if self.chosen_item:
            item_image = pg.transform.scale(self.chosen_item.image, (20, 20))
            screen.blit(item_image, self.rect)

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

    def attack(self):
        if pg.mouse.get_pressed()[2] and self.frame == 0:
            self.frame = 1

    def attack_animation(self):
        if self.frame != 0:
            self.image = self.attack_images[self.frame // 10]
            self.frame += 1
            if self.frame == 60:
                self.frame = 0

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
        keys = pg.key.get_pressed()
        for block in map.blocks:
            if self.building_zone.colliderect(block.rect) and block.rect.collidepoint(m_pos) and pg.mouse.get_pressed()[1] and not keys[pg.K_TAB]:
                block.destroy()
                self.return_block(block)
            else:
                block.repair()

    def return_block(self, block):
        if block.durability == 0 or block.clarity == 0:
            block.rect.topleft = self.hudbar.cells.sprites()[0].rect.topleft
            self.hudbar.cells.sprites()[0].stack.add(block)


    @staticmethod
    def mouse_block_colliding(map):
        m_pos = pg.mouse.get_pos()
        for block in map.blocks:
            if block.rect.collidepoint(m_pos):
                return True
        return False

    def place_block(self, map, enemy):
        m_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        r_click = pg.mouse.get_pressed()[0]
        if r_click and self.chosen_item is not None and not keys[pg.K_TAB] and not self.mouse_block_colliding(map):
            for cell in map.cells:
                if self.building_zone.colliderect(cell.rect) and not self.rect.colliderect(cell.rect) and cell.rect.collidepoint(m_pos) and not enemy.rect.colliderect(cell.rect):
                    self.chosen_item.kill()
                    self.chosen_item.rect.topleft = cell.rect.topleft
                    map.blocks.add(self.chosen_item)

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

    def update(self, screen, map, enemy):
        self.change_dir()
        self.follow()
        self.flip()

        self.move()
        self.check_building_collisions_x(map)
        self.jump()
        self.check_building_collisions_y(map)

        self.break_block(map)
        self.place_block(map, enemy)

        self.hudbar.update(screen)
        self.draw_chosen_item(screen)
        self.refresh_item_choose()

        self.health_hud.update(screen, self)
        self.attack()
        self.attack_animation()

        pg.draw.rect(screen, 'green', self.rect, width=1)
        pg.draw.rect(screen, 'violet', self.building_zone, width=1)
        screen.blit(self.image, self.rect)
