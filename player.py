import pygame as pg
from item_block_classes import Stone, Sand
from hudbar import HUDBar
from health import HealthHud, Stamina
from enemy import Enemy

pg.init()


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('1 Woodcutter/Woodcutter.png'), (64, 64))
        self.default_image = self.image
        self.reverse_image = pg.transform.flip(self.image, True, False)

        self.right_attack_images = [pg.transform.scale(pg.image.load(f'1 Woodcutter/img_{i}.png'), (64, 64)) for i in
                                    range(6)]
        for i in self.right_attack_images:
            i.set_colorkey((255, 255, 255))

        self.left_attack_images = [pg.transform.flip(i, True, False) for i in self.right_attack_images]

        self.hurt_images = [pg.transform.scale(pg.image.load(f'1 Woodcutter/img_{i}.png'), (64, 64)) for i in
                            range(6, 9)]
        for i in self.hurt_images:
            i.set_colorkey((255, 255, 255))

        self.hurt_images_reverse = [pg.transform.flip(i, True, False) for i in self.hurt_images]

        self.walk_images_right = [pg.transform.scale(pg.image.load(f'1 Woodcutter/img_{i}.png'), (64, 64)) for i in
                                  range(9, 15)]
        for i in self.walk_images_right:
            i.set_colorkey((255, 255, 255))

        self.walk_images_left = [pg.transform.flip(i, True, False) for i in self.walk_images_right]

        self.run_images_right = [pg.transform.scale(pg.image.load(f'1 Woodcutter/img_{i}.png'), (64, 64)) for i in
                                 range(15, 21)]
        for i in self.run_images_right:
            i.set_colorkey((255, 255, 255))

        self.run_images_left = [pg.transform.flip(i, True, False) for i in self.run_images_right]

        self.idle_images_right = [pg.transform.scale(pg.image.load(f'1 Woodcutter/img_{i}.png'), (64, 64)) for i in
                                  range(21, 25)]
        for i in self.idle_images_right:
            i.set_colorkey((255, 255, 255))

        self.idle_images_left = [pg.transform.flip(i, True, False) for i in self.idle_images_right]

        self.jump_images_right = [pg.transform.scale(pg.image.load(f'1 Woodcutter/img_{i}.png'), (64, 64)) for i in
                                  range(25, 31)]
        for i in self.jump_images_right:
            i.set_colorkey((255, 255, 255))

        self.jump_images_left = [pg.transform.flip(i, True, False) for i in self.jump_images_right]

        self.craft_images_right = [pg.transform.scale(pg.image.load(f'1 Woodcutter/img_{i}.png'), (64, 64)) for i in
                                   range(31, 35)]
        for i in self.craft_images_right:
            i.set_colorkey((255, 255, 255))

        self.craft_images_left = [pg.transform.flip(i, True, False) for i in self.craft_images_right]

        self.die_images_right = [pg.transform.scale(pg.image.load(f'1 Woodcutter/img_{i}.png'), (64, 64)) for i in
                                 range(35, 41)]

        self.die_images_left = [pg.transform.flip(i, True, False) for i in self.die_images_right]

        self.body_rect = pg.Rect(0, 0, 30, 42)

        self.rect = self.image.get_rect(centerx=700, bottom=900)
        self.building_zone = pg.Rect(self.rect.x - 64, self.rect.y - 64, 192, 192)
        self.hp = 100
        self.stamina = 100
        self.rest = False

        self.discard_range = 0

        self.timers = {'attack': 0, 'hurt': 0, 'walk': 0, 'run': 0, 'idle': 0, 'jump': 0, 'craft': 0, 'die': 0}
        self.is_animated = False
        self.last_dir = 1

        self.jump_speed = 0
        self.speed = 3
        self.g = 9.8
        self.dir = pg.Vector2()

        self.hudbar = HUDBar()
        self.chosen_item = self.hudbar.chosen_cell.stack.sprites()[0]

        self.health_hud = HealthHud(550, 0, 300, 20, 100)
        self.stamina_hud = Stamina(550, 20, 300, 20, 100)

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
        self.rect.x += self.speed * self.dir.x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1400:
            self.rect.right = 1400

    def boost(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT] and self.dir.x != 0 and self.stamina > 0:
            self.speed = 6
            self.stamina -= 0.5
        else:
            self.speed = 3
            if self.stamina < 100:
                self.stamina += 0.2

    def flip(self):
        if self.last_dir == -1:
            self.image = self.reverse_image
        elif self.last_dir == 1:
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

    def attack(self, enemy):
        if pg.mouse.get_pressed()[2] and self.timers['attack'] == 0:
            self.timers['attack'] = 1
        if enemy.rect.colliderect(self.rect) and self.timers['attack']:
            enemy.health -= 10
            self.discard_range = 10
        if 0 < self.discard_range < 11:
            if enemy.rect.left > self.body_rect.right:
                enemy.rect.x += self.discard_range
            elif enemy.rect.right < self.body_rect.left:
                enemy.rect.x -= self.discard_range
            self.discard_range -= 0.1

    def die(self):
        if self.timers['die'] == 59:
            self.kill()
            quit()

    def die_animation(self):
        if self.timers['die'] == 0:
            self.timers['die'] = 1
        if self.timers['die'] > 0 and self.last_dir == 1 and self.hp == 0:
            self.image = self.die_images_right[self.timers['die'] // 10]
            self.timers['die'] += 1
        elif self.timers['die'] > 0 and self.last_dir == -1 and self.hp == 0:
            self.image = self.die_images_left[self.timers['die'] // 10]
            self.timers['die'] += 1
        if self.timers['die'] == 60:
            self.timers['die'] = 0

    def attack_animation(self):
        current_animation_list = None
        if self.last_dir == 1:
            current_animation_list = self.right_attack_images
        elif self.last_dir == -1:
            current_animation_list = self.left_attack_images
        if self.timers['attack'] != 0:
            self.image = current_animation_list[self.timers['attack'] // 10]
            self.timers['attack'] += 1
            if self.timers['attack'] == 60:
                self.timers['attack'] = 0
                if self.last_dir == 1:
                    self.image = self.default_image
                else:
                    self.image = self.reverse_image

    def hurt_animation(self):
        if self.timers['hurt'] == 0:
            self.timers['hurt'] = 1
        if self.timers['hurt'] > 0 and self.last_dir == 1:
            self.image = self.hurt_images[self.timers['hurt'] // 10]
            self.timers['hurt'] += 1
        elif self.timers['hurt'] > 0 and self.last_dir == -1:
            self.image = self.hurt_images_reverse[self.timers['hurt'] // 10]
            self.timers['hurt'] += 1
        if self.timers['hurt'] == 30:
            self.timers['hurt'] = 0

    def walk_animation(self):
        if self.timers['walk'] == 0:
            self.timers['walk'] = 1
        if self.timers['walk'] > 0 and self.dir.x == 1:
            self.image = self.walk_images_right[self.timers['walk'] // 10]
            self.timers['walk'] += 1
        elif self.timers['walk'] > 0 and self.dir.x == -1:
            self.image = self.walk_images_left[self.timers['walk'] // 10]
            self.timers['walk'] += 1
        if self.timers['walk'] == 60:
            self.timers['walk'] = 0

    def boost_animation(self):
        keys = pg.key.get_pressed()
        if self.stamina > 0 and not self.rest:
            if self.timers['run'] == 0:
                self.timers['run'] = 1
            if self.timers['run'] > 0 and self.dir.x == 1 and keys[pg.K_LSHIFT]:
                self.image = self.run_images_right[self.timers['run'] // 10]
                self.timers['run'] += 1
            elif self.timers['run'] > 0 and self.dir.x == -1 and keys[pg.K_LSHIFT]:
                self.image = self.run_images_left[self.timers['run'] // 10]
                self.timers['run'] += 1
            if self.timers['run'] == 60:
                self.timers['run'] = 0
        else:
            self.rest = True
        if self.stamina >= 100:
            self.rest = False

    def idle_animation(self):
        if self.timers['idle'] == 0:
            self.timers['idle'] = 1
        if self.timers['idle'] > 0 and self.last_dir == 1:
            self.image = self.idle_images_right[self.timers['idle'] // 10]
            self.timers['idle'] += 1
        elif self.timers['idle'] > 0 and self.last_dir == -1:
            self.image = self.idle_images_left[self.timers['idle'] // 10]
            self.timers['idle'] += 1
        if self.timers['idle'] == 40:
            self.timers['idle'] = 0

    def jump_animation(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            if self.timers['jump'] == 0:
                self.timers['jump'] = 1
        if self.timers['jump'] > 0 and self.last_dir == 1:
            self.image = self.jump_images_right[self.timers['jump'] // 10]
            self.timers['jump'] += 1
        elif self.timers['jump'] > 0 and self.last_dir == -1:
            self.image = self.jump_images_left[self.timers['jump'] // 10]
            self.timers['jump'] += 1
        if self.timers['jump'] == 60:
            self.timers['jump'] = 0

    def craft_animation(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_e]:
            if self.timers['craft'] == 0:
                self.timers['craft'] = 1
        if self.timers['craft'] > 0 and self.last_dir == 1:
            self.image = self.craft_images_right[self.timers['craft'] // 10]
            self.timers['craft'] += 1
        elif self.timers['craft'] > 0 and self.last_dir == -1:
            self.image = self.craft_images_left[self.timers['craft'] // 10]
            self.timers['craft'] += 1
        if self.timers['craft'] == 40:
            self.timers['craft'] = 0

    def jump(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.jump_speed == 0:
            self.jump_speed = -5
        if self.rect.bottom <= 900:
            self.jump_speed += self.g / 60
            self.rect.y += self.jump_speed
        if self.rect.bottom > 900:
            self.rect.bottom = 900
            self.jump_speed = 0

    def break_block(self, map):
        m_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        for block in map.blocks:
            if self.building_zone.colliderect(block.rect) and block.rect.collidepoint(m_pos) and pg.mouse.get_pressed()[
                1] and not keys[pg.K_TAB]:
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
                if self.building_zone.colliderect(cell.rect) and not self.rect.colliderect(
                        cell.rect) and cell.rect.collidepoint(m_pos) and not enemy.rect.colliderect(cell.rect):
                    self.chosen_item.kill()
                    self.chosen_item.rect.topleft = cell.rect.topleft
                    map.blocks.add(self.chosen_item)

    def follow(self):
        self.building_zone.center = self.rect.center
        self.body_rect.bottom = self.rect.bottom
        if self.last_dir == 1:
            self.body_rect.left = self.rect.left + 5
        else:
            self.body_rect.right = self.rect.right - 5

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
        self.boost()
        self.check_building_collisions_x(map)
        self.jump()
        self.check_building_collisions_y(map)

        self.break_block(map)
        self.place_block(map, enemy)

        self.hudbar.update(screen)
        self.draw_chosen_item(screen)
        self.refresh_item_choose()

        self.health_hud.update(screen, self)
        self.stamina_hud.update(screen, self)
        self.idle_animation()
        self.craft_animation()
        self.walk_animation()
        self.boost_animation()
        self.attack(enemy)
        self.attack_animation()
        self.jump_animation()
        self.die_animation()
        self.die()

        pg.draw.rect(screen, 'green', self.rect, width=1)
        pg.draw.rect(screen, 'red', self.body_rect, width=1)
        pg.draw.rect(screen, 'violet', self.building_zone, width=1)
        screen.blit(self.image, self.rect)
        if self.dir.x != 0:
            self.last_dir = self.dir.x
