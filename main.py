import pygame as pg
from button import Button
from player import Player
from building_map import Map
from inventory import Inventory

pg.init()


class MainMenu:
    def __init__(self):
        self.play_button = Button((200, 200), 'white', 'PLAY', 60, 'black', (700, 450))
        self.exit_button = Button((200, 200), 'white', 'EXIT', 60, 'black', (350, 450))
        self.options_button = Button((200, 200), 'white', 'OPTIONS', 60, 'black', (1050, 450))

    def update(self, surface):
        self.play_button.update(surface)
        self.exit_button.update(surface)
        self.options_button.update(surface)


class Game:
    def __init__(self):
        self.window = pg.display.set_mode((1400, 900))
        self.fps = pg.time.Clock()
        self.menu = MainMenu()
        self.player = Player()
        self.web = Map(32)
        self.inventory = Inventory()

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

    def play(self):
        while True:
            self.window.fill('black')
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
            self.web.update(self.window, self.player)
            self.inventory.update(self.window)
            self.player.update(self.window, self.web)
            pg.display.update()
            self.fps.tick(60)


game = Game()
game.run_menu()
