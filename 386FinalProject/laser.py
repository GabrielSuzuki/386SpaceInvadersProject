import pygame as pg

import alien
import ship
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
from random import randint
from sound import Sound

from random import randint

# from alien import Alien
# from stats import Stats


class Lasers:
    def __init__(self, game, owner):
        self.game = game
        self.stats = game.stats
        self.sound = game.sound
        self.owner = owner
        self.alien_fleet = game.alien_fleet
        self.ship = game.ship
        #self.barrier = game.barrier
        self.lasers = Group()
        print('owner is ', self.owner, 'type is: ', type(self.owner))
        print('type is alien.AlienFleet is: ', type(owner) is alien.AlienFleet)

    def add(self, laser):
        self.lasers.add(laser)

    def empty(self):
        self.lasers.empty()

    def fire(self):
        new_laser = Laser(self.game, type(self.owner))
        self.lasers.add(new_laser)
        snd = self.sound
        snd.play_fire_phaser() if type(self.owner) is alien.AlienFleet else snd.play_fire_photon()

    def update(self):
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0: self.lasers.remove(laser)
            if laser.rect.top >= 800:
                self.lasers.remove(laser)
        if self.owner == self.alien_fleet:
            ship_collisions = pg.sprite.spritecollide(self.ship, self.lasers, True)
            if len(ship_collisions) > 0:
                if not self.ship.is_dying(): ship.Ship.hit(self.ship)
            #barrier_collisions = pg.sprite.spritecollide(self.barrier, self.lasers, True)
            #if len(barrier_collisions) > 0:
            #    barrier.barrier_elements.hit(self.barrier)
            #for ships in ship_collisions:
            #    if not ships.is_dying: ships.hit()
        else:
            alien_collisions = pg.sprite.groupcollide(self.alien_fleet.fleet, self.lasers, False, True)
            for alien in alien_collisions:
                if not alien.dying: alien.hit()
            if self.alien_fleet.length() == 0:
                self.stats.level_up()
                self.game.restart()

            #for laser in self.lasers.copy():
            #    if laser.rect.bottom >= self.settings.screen_height: self.lasers.remove(laser)
            #collosions = pg.sprite.spritecollide(self.ship,self.lasers, False, True)
            #if not ship.dying: ship.hit()

        for laser in self.lasers:
            laser.update()

    def draw(self):
        for laser in self.lasers:
            laser.draw()


class Laser(Sprite):
    def __init__(self, game, owner):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.w, self.h = self.settings.laser_width, self.settings.laser_height
        self.ship = game.ship
        self.aliens = game.alien_fleet.fleet
        self.rect = pg.Rect(0, 0, self.w, self.h)
        self.owner = owner
        self.center = Vector(0,800)

        # print(f'center is at {self.center}')
        # self.color = self.settings.laser_color
        tu = 50, 255
        self.color = randint(*tu), randint(*tu), randint(*tu)
        if owner == ship.Ship:
            self.v = Vector(0, -1) * self.settings.laser_speed_factor
            self.center = copy(self.ship.center)
        else:
            self.v = Vector(0, 1) * self.settings.laser_speed_factor
            tempRandomInt = randint(0, len(self.aliens))
            counter = 0
            for i in self.aliens:
                if counter == tempRandomInt:
                    self.center = copy(i.ul)
                counter += 1


    def update(self):
        self.center += self.v
        self.rect.x, self.rect.y = self.center.x, self.center.y

    def draw(self): pg.draw.rect(self.screen, color=self.color, rect=self.rect)