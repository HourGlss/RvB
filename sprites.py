import pygame as pg
from random import uniform
from settings import *
from tilemap import collide_hit_rect

vec = pg.math.Vector2
import math
import random


class Mellee(pg.sprite.Sprite):
    def __init__(self, game, x, y, easy_dir, owner):
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = (x, y)
        self.owner = owner
        self.groups = game.all_sprites, game.mellees
        self.game = game
        if easy_dir == 1 or easy_dir == 3:
            self.image = pg.Surface((2, 48))
        else:
            self.image = pg.Surface((48, 2))
        self.rect = self.image.get_rect()
        self.image = pg.transform.rotate(self.image,45)

        self.image.fill(pg.Color("RED"))
        self.vel = 3
        self.dir = easy_dir
        # print(f"pos:{self.pos}")
        # print(f"vec:{self.vel}")
        # print(f"dir:{dir}")
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos = self.owner.rect.centerx,self.owner.rect.centery
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > MELLEE_LIFETIME:
            self.kill()


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.pos = vec(x, y) * TILESIZE
        self.groups = game.all_sprites

        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.id = random.randint(1000000, 9999999)
        self.image = pg.Surface((TILESIZE, TILESIZE), PLAYERCOLOR)
        self.rect = self.image.get_rect()

        # print("colorkey")
        # print(self.image.get_colorkey())
        # self.rect = pg.draw.circle(self.image, pg.Color("YELLOW"), (int(TILESIZE / 2), int(TILESIZE / 2)), PLAYER_RADIUS)

        # pg.gfxdraw.aacircle(self.image, int(TILESIZE / 2), int(TILESIZE / 2), PLAYER_RADIUS, pg.Color("CYAN"))
        # pygame.gfxdraw.filled_circle(self.image, int(TILESIZE / 2), int(TILESIZE / 2), PLAYER_RADIUS,
        #                              pg.Color("YELLOW"))

        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.in_water = False
        self.rect.x = self.x
        self.rect.y = self.y
        self.vel = vec(0, 0)

        self.last_shot = 0
        self.last_movement = 0
        self.last_stabbed = 0
    def shoot(self,now):
        mouse_x, mouse_y = pg.mouse.get_pos()
        shift_x, shift_y = self.game.camera.camera.topleft
        mouse_x = mouse_x - shift_x
        mouse_y = mouse_y - shift_y
        self.last_shot = now
        x_to_use = self.rect.centerx
        y_to_use = self.rect.centery
        rel_x, rel_y = mouse_x - x_to_use, mouse_y - y_to_use
        # print(f"player's position: ({x_to_use},{y_to_use})")
        distance = math.sqrt(((mouse_x - x_to_use) ** 2) + ((mouse_y - y_to_use) ** 2))
        dir = vec(rel_x / distance, rel_y / distance)
        # print(f"bullet's direction: {dir})")
        Bullet(self.game, self.rect.centerx, self.rect.centery, dir, self.id)

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        now = pg.time.get_ticks()
        if self.in_water:
            PLAYER_SPEED = ORIGINAL_PLAYER_SPEED * .6
        else:
            PLAYER_SPEED = ORIGINAL_PLAYER_SPEED
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
            self.last_movement = 2
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.last_movement = 0
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.last_movement = 3
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.last_movement = 1
            self.vy = PLAYER_SPEED
        if keys[pg.K_1]: # MELLEE
            if now - self.last_stabbed > MELLEE_RATE:
                self.last_stabbed = now
                dir = self.last_movement
                Mellee(self.game, self.rect.centerx, self.rect.centery, dir, self)
        if keys[pg.K_2]: # ORDINARY SHOOTING
            if now - self.last_shot > BULLET_RATE:
                self.shoot(now)



        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def print_status(self):
        print(f"x:{int(self.x)},y:{int(self.y)}")
        # print(f"recx:{self.x},recy:{self.y}")

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def circle_collide_with_walls(self,
                                  rleft, rtop, width, height,  # rectangle definition
                                  center_x, center_y, radius):  # circle definition
        """ Detect collision between a rectangle and circle. """

        # complete boundbox of the rectangle
        rright, rbottom = rleft + width / 2, rtop + height / 2

        # bounding box of the circle
        cleft, ctop = center_x - radius, center_y - radius
        cright, cbottom = center_x + radius, center_y + radius

        # trivial reject if bounding boxes do not intersect
        if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
            return False  # no collision possible

        # check whether any point of rectangle is inside circle's radius
        for x in (rleft, rleft + width):
            for y in (rtop, rtop + height):
                # compare distance between circle's center point and each point of
                # the rectangle with the circle's radius
                if math.hypot(x - center_x, y - center_y) <= radius:
                    return True  # collision detected

        # check if center of circle is inside rectangle
        if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
            return True  # overlaid

        return False  # no collision detected

    def update(self):

        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.pos += self.vel * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        # self.print_status()
        self.collide_with_liquid()

    def collide_with_liquid(self):
        hits = pg.sprite.spritecollide(self, self.game.liquids, False)
        if hits:
            self.in_water = True
        else:
            self.in_water = False


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # print("bullet made")
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WALLCOLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Liquid(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.liquids
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIQUIDCOLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Brush(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.brushes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BRUSHCOLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Goal(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.goals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GOALCOLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Test(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.tests
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((10, 10))
        self.image.fill(pg.Color("RED"))
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.rect.center = self.pos


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y, dir, owner):
        self.owner = owner
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((5, 5))
        self.image.fill(PLAYERCOLOR)
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.vel = dir * BULLET_SPEED
        # print(f"pos:{self.pos}")
        # print(f"vec:{self.vel}")
        # print(f"dir:{dir}")
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
