import pygame as pg
import pygame.time
import sys
from vector import Vector
from pygame.sprite import Sprite, Group
from timer import Timer
from sound import Sound
from random import randint

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (130, 130, 130)

class AlienFleet:
    alien_exploding_images = [pg.image.load(f'images/rainbow_explode{n}.png') for n in range(8)]
    # alien_images0 = [pg.transform.rotozoom(pg.image.load(f'images/alien0{n}.bmp'), 0, 1.2) for m in range(3)]
    # alien_images1 = [pg.transform.rotozoom(pg.image.load(f'images/alien1{n}.bmp'), 0, 2) for m in range(3)]
    # alien_images2 = [pg.transform.rotozoom(pg.image.load(f'images/alien2{n}.bmp'), 0, 3) for m in range(3)]

    # alien_images = [alien_images0, alien_images1, alien_images2]

    #alien_images = [[pg.transform.rotozoom(pg.image.load(f'images/alien__{m}{n}.png'), 0, 0.5) for n in range(2)] for m
                    #in range(3)]
    alien_images = [[pg.transform.rotozoom(pg.image.load(f'images/GabeAlien{m}_{n}v2.png'), 0, 0.5) for n in range(1,3)] for m
                    in range(1,4)]
    ufo_imgs = [pg.transform.rotozoom(pg.image.load(f'images/GabeAlien4_{n}v2.png'), 0, 0.5) for n in range(1,3)]
    alien_images.append(ufo_imgs)
    alien_points = [40, 20, 10, 100]

    def __init__(self, game, v=Vector(1, 0)):
        self.game = game
        self.ship = self.game.ship
        self.settings = game.settings
        self.screen = self.game.screen
        self.sound = game.sound
        self.screen_rect = self.screen.get_rect()
        self.v = v
        alien = Alien(self.game, sound=self.sound, alien_index=0, image_list=AlienFleet.alien_images)
        self.alien_h, self.alien_w = alien.rect.height, alien.rect.width
        self.fleet = Group()
        self.create_fleet()
        self.lasers = None
        self.alienPositions = []
        self.fire_timer = pygame.time.get_ticks() + randint(0, 10000)
        self.ufoCounter = pygame.time.get_ticks() + randint(0, 60000)
        self.ufoCheck = False

    def create_fleet(self):
        n_cols = self.get_number_cols(alien_width=self.alien_w)
        n_rows = self.get_number_rows(ship_height=self.ship.rect.height,
                                      alien_height=self.alien_h)
        for row in range(n_rows):
            for col in range(n_cols):
                self.create_alien(row=row, col=col)

    def set_ship(self, ship):
        self.ship = ship

    def create_alien(self, row, col):
        x = self.alien_w * (1.2 * col + 1)
        y = self.alien_h * (1.2 * row + 1)
        images = AlienFleet.alien_images
        # alien = Alien(game=self.game, ul=(x, y), v=self.v, image_list=images,
        #               start_index=randint(0, len(images) - 1))
        alien = Alien(game=self.game, sound=self.sound, alien_index=row // 2, ul=(x, y), v=self.v, image_list=images)
        self.fleet.add(alien)

    def create_UFO(self):
        x = 600
        y = 50
        print("make ufo")
        self.sound.play_ufo()
        images = AlienFleet.ufo_imgs
        alien = Alien(game=self.game, sound=self.sound, alien_index=10 // 2, ul=(x, y), v=self.v, image_list=images)
        self.fleet.add(alien)

    def empty(self):
        self.fleet.empty()

    def get_number_cols(self, alien_width):
        spacex = self.settings.screen_width - 2 * alien_width
        return int(spacex / (2 * alien_width))

    def get_number_rows(self, ship_height, alien_height):
        spacey = self.settings.screen_height - 2 * alien_height - ship_height
        return int(spacey / (1.75 * alien_height))

    def length(self):
        return len(self.fleet.sprites())

    def change_v(self, v):
        for alien in self.fleet.sprites():
            alien.change_v(v)

    def check_bottom(self):
        for alien in self.fleet.sprites():
            if alien.check_bottom():
                self.ship.hit()
                break

    def check_edges(self):
        for alien in self.fleet.sprites():
            if alien.check_edges(): return True
        return False

    def set_lasers(self, lasers):
        self.lasers = lasers

    def check_lasers(self):
        self.alienPositions = []
        for alien in self.fleet.sprites():
            self.alienPositions.append(Vector(alien.rect.centerx,alien.rect.centery))



    def update(self):
        delta_s = Vector(0, 0)  # don't change y position in general
        if self.check_edges():
            self.v.x *= -1
            self.change_v(self.v)
            delta_s = Vector(0, self.settings.fleet_drop_speed)
        if pg.sprite.spritecollideany(self.ship, self.fleet) or self.check_bottom():
            if not self.ship.is_dying(): self.ship.hit()
        for alien in self.fleet.sprites():
            alien.update(delta_s=delta_s)
        if pygame.time.get_ticks() > self.fire_timer:
            self.check_lasers()
            self.lasers.fire()
            self.fire_timer = self.fire_timer + randint(0, 5000)
        if pygame.time.get_ticks() > self.ufoCounter and self.ufoCheck == False:
            self.create_UFO()
            self.ufoCheck = True


    def draw(self):
        for alien in self.fleet.sprites():
            alien.draw()


class Alien(Sprite):
    def __init__(self, game, image_list, alien_index, sound, start_index=0, ul=(0, 100), v=Vector(1, 0),
                 points=1211):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.sound = sound

        self.stats = game.stats

        self.alien_index = alien_index

        self.image = pg.image.load('images/alien0.bmp')
        self.screen_rect = self.screen.get_rect()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = ul
        self.ul = Vector(ul[0], ul[1])  # position
        self.v = v  # velocity
        self.image_list = image_list
        self.randomNumber = randint(300, 1000)
        self.ufoExplodingImages = []
        headingFont = pg.font.SysFont(None, 192)
        #string = (str(self.randomNumber), GREEN, headingFont)
        self.ufoText = self.get_text(msg=str(self.randomNumber), color=GREEN, font=headingFont)
        print(alien_index)
        if alien_index == 5:
            self.points = self.randomNumber
            self.normal_timer = Timer(image_list=AlienFleet.ufo_imgs, delay=1000, is_loop=True)
            self.ufoExplodingImages.append(self.ufoText)
            self.ufoExplodingImages.append(pg.image.load(f'images/rainbow_explode8.png'))
            self.exploding_timer = Timer(image_list=self.ufoExplodingImages, delay=1000,start_index=start_index, is_loop=False)
        else:
            self.points = AlienFleet.alien_points[alien_index]
            self.exploding_timer = Timer(image_list=AlienFleet.alien_exploding_images, delay=200,
                                     start_index=start_index, is_loop=False)
            self.normal_timer = Timer(image_list=AlienFleet.alien_images[alien_index], delay=1000, is_loop=True)
        self.timer = self.normal_timer
        self.dying = False
        self.lasers = None
        self.fire_timer = pygame.time.get_ticks() + randint(0, 10000)

    def get_text(self, font, msg, color):
        return font.render(msg, True, color, WHITE)

    def get_text_rect(self, text, centerx, centery):
        rect = text.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect

    def draw_text(self):
        print("draw text")
        self.screen.blit(self.ufoText,self.rect)

    def change_v(self, v): self.v = v

    def check_bottom(self): return self.rect.bottom >= self.screen_rect.bottom

    def return_bottom(self): return self.rect.bottom

    def check_edges(self):
        r = self.rect
        return r.right >= self.screen_rect.right or r.left <= 0

    def hit(self):
        self.stats.alien_hit(alien=self)
        if self.alien_index == 5:
            self.rect = self.get_text_rect(text=self.ufoText, centerx=self.rect.centerx, centery=self.rect.centery)
            #self.draw_text()
            print(self.ufoExplodingImages)
            self.timer = self.exploding_timer
        else:
            self.timer = self.exploding_timer
        self.sound.play_alien_explosion()
        self.dying = True



    def update(self, delta_s=Vector(0, 0)):
        if self.dying and self.timer.is_expired():
            self.kill()
        self.ul += delta_s
        self.ul += self.v * self.settings.alien_speed_factor
        self.rect.x, self.rect.y = self.ul.x, self.ul.y


    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)

