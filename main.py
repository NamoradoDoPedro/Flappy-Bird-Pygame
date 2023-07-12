import pygame as pg
from pygame import Vector2 as v
from pygame.locals import *
from random import randint as r
from sys import exit


class Display:
    dimension = v(400, 450)
    display = pg.display.set_mode((dimension))
    title = pg.display.set_caption("Flappy Bird")


class Bird:
    def __init__(self):
        self.dimension = v(30, 30)
        self.position = v(50, 50)
        self.velocity = v(0, 0)
        self.acceleration = v(0, 0)

        self.color = (255, 255, 0)
        self.score = 0
        self.lock = False
        self.died = False

    def move(self):
        if not self.lock:
            self.acceleration = v(0, 0.5)
            self.velocity += self.acceleration
            self.position += self.velocity + 0.5 * self.acceleration

            if self.position.x > Display.dimension.x:
                self.position.x = 0
            if self.position.x < 0:
                self.position.x = Display.dimension.x

    def jump(self):
        if self.position.y > 10:
            self.velocity.y = -8.5

    def reset(self):
        self.dimension = v(30, 30)
        self.position = v(50, 50)
        self.velocity = v(0, 0)
        self.acceleration = v(0, 0)

        self.color = (255, 255, 0)
        self.score = 0
        self.lock = False
        self.died = False


class Floor:
    dimension = v(Display.dimension.x, 20)
    position = v(0, Display.dimension.y - dimension.y)
    color = (255, 0, 0)


class Pipe:
    def __init__(self):
        self.dimension = v(50, Display.dimension.y)
        self.color = (30, 230, 30)
        self.pipe_gap = 120
        self.down_pos = v(Display.dimension.x,
                          r(self.pipe_gap, Display.dimension.y - self.pipe_gap + Floor.dimension.y))
        self.top_pos = v(Display.dimension.x,
                         self.down_pos.y - Display.dimension.y - self.pipe_gap)
        self.velocity = v(5, 0)
        self.not_reset = False

    def reset(self):
        self.down_pos = v(Display.dimension.x,
                          r(self.pipe_gap + Floor.dimension.y, Display.dimension.y))
        self.top_pos = v(Display.dimension.x,
                         self.down_pos.y - Display.dimension.y - self.pipe_gap)
        self.velocity = v(5, 0)
        self.not_reset = False

    def move(self):
        self.top_pos = self.top_pos - self.velocity
        self.down_pos = self.down_pos - self.velocity


class Game:
    def __init__(self):
        self._b = Bird()
        self._p = Pipe()

    def draw(self):
        ds = Display.display
        ds.fill((0, 0, 0))
        pt = pg.draw.rect(ds, self._p.color,
                          (self._p.top_pos, self._p.dimension))
        pd = pg.draw.rect(ds, self._p.color,
                          (self._p.down_pos, self._p.dimension))
        f = pg.draw.rect(ds, Floor.color,
                         (Floor.position, Floor.dimension))
        b = pg.draw.rect(ds, self._b.color,
                         (self._b.position, self._b.dimension))

        if b.colliderect(f) or b.colliderect(pt) or b.colliderect(pd):
            self._b.died = True
            self._p.velocity = v(0, 0)
            if b.colliderect(f):
                self._b.lock = True

    def show_score(self):
        FONT = pg.font.get_default_font()
        SIZE = 110
        WHITE = (255, 255, 255)
        blit = Display.display.blit

        Text_Player_Points = pg.font.SysFont(FONT, SIZE).render(
            str(self._b.score), True, WHITE)

        if self._b.score < 10:
            blit(Text_Player_Points,
                 ((Display.dimension.x/2) - SIZE/5, 30))

        elif self._b.score > 9:
            blit(Text_Player_Points,
                 ((Display.dimension.x/2) - SIZE/2.5, 30))

        else:
            blit(Text_Player_Points,
                 ((Display.dimension.x/2) - SIZE, 30))

        if self._b.died == True:
            blit(pg.font.SysFont(FONT, 100).render(
                "Game Over", True, WHITE), (10, 140))
            blit(pg.font.SysFont(FONT, 20).render(
                "Press 'Space' to restart", True, WHITE), (120, 210))

    def move(self):
        key = pg.key.get_pressed()
        if key[K_SPACE] and self._b.died == False:
            self._b.jump()

        if self._b.died == True:
            if key[K_SPACE]:
                for entity in [self._b, self._p]:
                    entity.reset()

    def update(self):
        self.draw()
        self.show_score()
        for entity in [self._b, self._p]:
            entity.move()

        if self._p.top_pos.x < self._b.position.x and not self._p.not_reset:
            self._b.score += 1
            self._p.not_reset = True

        if self._p.top_pos.x < -50:
            self._p.reset()


if __name__ == "__main__":
    pg.init()

    clock = pg.time.Clock()
    game = Game()
    FPS = 60

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                game.move()

        game.update()
        clock.tick(FPS)
        pg.display.update()
