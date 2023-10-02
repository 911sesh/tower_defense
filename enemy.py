import pygame as pg
class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 50))
        self.rect = self.image.get_rect(bottom=900)
        self.color = 'red'
        self.image.fill(self.color)
        self.health = 10
        self.speed = 2
        self.is_available = False
        self.hitbox_zone = None

    def spawn(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, player):
        if not self.rect.colliderect(player.rect):
            if self.rect.x > player.rect.x:
                self.rect.x -= self.speed
            elif self.rect.x < player.rect.x:
                self.rect.x += self.speed

    def map_collisions(self, map):
        for block in map.blocks:
            if self.rect.colliderect(block.rect):
                if block.rect.left < self.rect.right < block.rect.right:
                    self.rect.right = block.rect.left
                if block.rect.right > self.rect.left > block.rect.left:
                    self.rect.left = block.rect.right
    def update(self, screen, player, map):
        self.spawn(screen)
        self.move(player)
        self.map_collisions(map)
