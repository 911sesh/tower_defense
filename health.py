import pygame as pg

pg.init()


class HealthHud():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max_hp = max_hp

    def draw(self, screen, player):
        ratio = player.hp / self.max_hp
        pg.draw.rect(screen, 'red', (self.x, self.y, self.w, self.h))
        pg.draw.rect(screen, 'darkgreen', (self.x, self.y, self.w * ratio, self.h))
        my_font = pg.font.SysFont('kenvector_future.ttf', 30)
        text_surface = my_font.render('{hp}'.format(hp=player.hp), True, 'white')
        screen.blit(text_surface, (690, 0))

    def update(self, screen, player):
        self.draw(screen, player)


class Stamina():
    def __init__(self, x, y, w, h, max_stamina):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max_stamina = max_stamina

    def draw(self, screen, player):
        ratio = player.stamina / self.max_stamina
        pg.draw.rect(screen, 'red', (self.x, self.y, self.w, self.h))
        pg.draw.rect(screen, 'purple', (self.x, self.y, self.w * ratio, self.h))
        my_font = pg.font.SysFont('kenvector_future.ttf', 30)
        text_surface = my_font.render('{stamina}'.format(stamina=int(player.stamina)), True, 'white')
        screen.blit(text_surface, (690, 20))

    def update(self, screen, player):
        self.draw(screen, player)
