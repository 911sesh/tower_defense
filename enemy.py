import pygame as pg

pg.init()
class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('xeno_grunt/img.png'), (32, 32))
        self.rect = self.image.get_rect(bottom=900)
        self.destroy_rect = pg.Rect(0, 0, 48, 48)
        self.health = 100
        self.speed = 2
        self.is_available = False
        self.discard_range = 0

    def follow(self):
        self.destroy_rect.center = self.rect.center



    def spawn(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, player):
        if not self.rect.colliderect(player.body_rect):
            if self.rect.x > player.body_rect.x:
                self.rect.x -= self.speed
            elif self.rect.x < player.body_rect.x:
                self.rect.x += self.speed

    def die(self):
        if self.health == 0:
            self.kill()

    def map_collisions(self, map):
        for block in map.blocks:
            if self.rect.colliderect(block.rect):
                if block.rect.left < self.rect.right < block.rect.right:
                    self.rect.right = block.rect.left
                if block.rect.right > self.rect.left > block.rect.left:
                    self.rect.left = block.rect.right

    def attack(self, player):
        if self.rect.colliderect(player.body_rect) and player.hp > 0:
            self.discard_range = 6
            player.hp -= 1
        if 0 < self.discard_range < 7:
            player.hurt_animation()
            if player.body_rect.bottom > self.rect.top:
                if player.body_rect.left < self.rect.right < player.body_rect.right:
                    self.rect.right = player.body_rect.left
                elif player.body_rect.right > self.rect.left > player.body_rect.left:
                    self.rect.left = player.body_rect.right
                if self.rect.right <= player.body_rect.left:
                    player.rect.x += self.discard_range
                elif self.rect.left >= player.body_rect.right:
                    player.rect.x -= self.discard_range
            else:
                player.rect.y -= self.discard_range
            self.discard_range -= 0.2

    def destroy_blocks(self, map):
        for block in map.blocks:
            if self.destroy_rect.colliderect(block.rect):
                block.destroy()

    def update(self, screen, player, map):
        self.spawn(screen)
        self.follow()
        self.move(player)
        self.map_collisions(map)
        self.attack(player)
        self.destroy_blocks(map)
        self.die()
        pg.draw.rect(screen, 'red', self.rect, 1)
        pg.draw.rect(screen, 'green', self.destroy_rect, 1)

