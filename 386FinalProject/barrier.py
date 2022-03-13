import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
from random import randint
#from timer import Timer
from laser import Lasers

# from alien import Alien
# from stats import Stats
from settings import Settings
from timer import CommandTimer

class Barriers:

    def __init__(self, game):
        self.game = game
        self.barriers = []

        barrier = Barrier(self.game,ul=(0,0),wh=(0,0))
        #self.barrier_h, self.barrier_w = barrier.rect.height, barrier.rect.width
        # self.alien_fleet = game.alien_fleet
        for n in range(5):
            self.create_barrier(col=n)

    def create_barrier(self, col):
        x = 175 * (1.2 * col + 1)
        # alien = Alien(game=self.game, ul=(x, y), v=self.v, image_list=images,
        #               start_index=randint(0, len(images) - 1))
        self.barriers.append(Barrier(game=self.game, ul=(x, 650), wh=(3,3)))
        #self.fleet.add(alien)


    def update(self):
        for barrier in self.barriers:
            barrier.update()

    def draw(self):
        for barrier in self.barriers:
            barrier.draw()


class Barrier(Sprite):
    img_list = [pg.transform.rotozoom(pg.image.load(f'images/block{n}.png'), 0, 0.5) for n in range(0, 4)]
    def __init__(self, game, ul, wh):
        self.game = game
        self.lasers = game.lasers
        self.alienLasers = game.alien_lasers
        self.barrier_elements = Group()

        self.ul = ul
        self.wh = wh
        for row in range(wh[0]):
            for col in range(wh[1]):
                be = BarrierElement(game=game, img_list=self.img_list,
                                    ul=(ul[0] + col, ul[1] + row), wh=(4, 4))
                self.barrier_elements.add(be)

    def update(self):
        collisions = pg.sprite.groupcollide(self.barrier_elements,self.lasers.lasers, True, True)
        for be in collisions:
            be.hit()
        collisions = pg.sprite.groupcollide(self.barrier_elements, self.alienLasers.lasers, True, True)
        for be in collisions:
            be.hit()

    def draw(self):
        for be in self.barrier_elements:
            be.draw()


class BarrierElement(Sprite):
    def __init__(self, game, img_list, ul, wh):
        super().__init__()
        self.ul = ul
        self.wh = wh
        self.img_list = img_list
        self.counter = 0
        self.rect = pg.Rect(ul[0], ul[1], wh[0], wh[1])
        self.timer = CommandTimer(image_list=img_list, is_loop=False)
        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))

    def update(self): pass
    def hit(self):
        #self.counter += 1
        #if self.counter > len(self.img_list) - 1:
        #    self.kill()
        #else:
        #    self.draw()
        self.timer.next_frame()
        if self.timer.is_expired():
            self.kill()
            print("kill")
        print(self.counter)


    def draw(self):
        #image = self.img_list[self.counter]
        image = self.timer.image()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
