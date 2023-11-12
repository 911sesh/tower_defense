import pygame as pg
from button import Button
from player import Player
from building_map import Map
from inventory import Inventory
from enemy import Enemy

pg.init()
pg.display.set_caption('TOWER DEFENSE')
pg.display.set_icon(pg.image.load('1 Woodcutter/gamepad_icon.png'))


class PauseMenu:
    def __init__(self):
        self.resume_button = Button((200, 200), 'white', 'RESUME', 60, 'grey82', (700, 450))
        self.exit_button = Button((200, 200), 'white', 'EXIT', 60, 'grey82', (350, 450))
        self.options_button = Button((200, 200), 'white', 'OPTIONS', 60, 'grey82', (1050, 450))

    def update(self, screen):
        self.resume_button.update(screen)
        self.exit_button.update(screen)
        self.options_button.update(screen)


class MainMenu:
    def __init__(self):
        self.play_button = Button((200, 200), 'white', 'PLAY', 60, 'black', (700, 450))
        self.exit_button = Button((200, 200), 'white', 'EXIT', 60, 'black', (350, 450))
        self.options_button = Button((200, 200), 'white', 'OPTIONS', 60, 'black', (1050, 450))

    def update(self, screen):
        self.play_button.update(screen)
        self.exit_button.update(screen)
        self.options_button.update(screen)


class Game:
    def __init__(self):
        self.window = pg.display.set_mode((1400, 900))
        self.fps = pg.time.Clock()
        self.menu = MainMenu()
        self.player = Player()
        self.players = pg.sprite.Group(self.player)
        self.web = Map(32)
        self.inventory = Inventory()
        self.enemy = Enemy()
        self.enemies = pg.sprite.Group(self.enemy)
        self.pause_menu = PauseMenu()

    def run_menu(self):
        while True:
            self.window.fill('black')
            for event in pg.event.get():
                if event.type == pg.QUIT or self.menu.exit_button.is_pressed():
                    exit()
                if self.menu.play_button.is_pressed():
                    self.play()
            self.menu.update(self.window)
            pg.display.update()
            self.fps.tick(60)

    def pause(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or self.pause_menu.exit_button.is_pressed():
                    exit()
            if self.pause_menu.resume_button.is_pressed():
                break
            self.pause_menu.update(self.window)
            pg.display.update()
            self.fps.tick(60)

    def play(self):
        while True:
            self.window.fill('black')
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.pause()
            self.web.update(self.window, self.player)
            self.inventory.update(self.window)
            self.players.update(self.window, self.web, self.enemy)
            self.enemies.update(self.window, self.player, self.web)
            pg.display.update()
            self.fps.tick(60)


game = Game()
game.run_menu()
