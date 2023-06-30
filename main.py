import pygame as pg
from pygame.locals import *
from random import randint as r
from sys import exit

pg.init()
v = pg.Vector2


class Display:
    def __init__(self):
        self.dimension = v(400, 450)
        self.display = pg.display.set_mode((self.dimension))
        self.title = pg.display.set_caption("Flappy Bird")


class Bird:
    def __init__(self):
        self.dimension = v(30, 30)
        self.position = v(50, 50)
        self.velocity = v(0, 0)
        self.acceleration = v(0, 0)

        self.color = (255, 255, 0)
        self.score = 0
        self.lockMoves = False

    def move(self):
        self.acceleration = v(0, 0.5)
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        if self.position.x > DISPLAY.dimension.x:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = DISPLAY.dimension.x

    def jump(self):
        if self.position.y > 55:
            self.velocity.y = -8.5

    def reset(self):
        self.dimension = v(30, 30)
        self.position = v(50, 50)
        self.velocity = v(0, 0)
        self.acceleration = v(0, 0)

        self.color = (255, 255, 0)
        self.score = 0
        self.lockMoves = False


class Floor:
    def __init__(self):
        self.dimension = v(DISPLAY.dimension.x, 20)
        self.position = v(0, DISPLAY.dimension.y - self.dimension.y)
        self.color = (255, 0, 0)


class Pipe:
    def __init__(self):
        self.dimension = v(50, DISPLAY.dimension.y)
        self.color = (30, 230, 30)
        self.pipe_gap = 120
        self.down_pos = v(DISPLAY.dimension.x, r(
            self.pipe_gap + floor.dimension.y, DISPLAY.dimension.y))
        self.top_pos = v(DISPLAY.dimension.x,
                         self.down_pos.y - DISPLAY.dimension.y - self.pipe_gap)
        self.velocity = v(5, 0)
        self.not_reset = False

    def move(self):
        self.top_pos = self.top_pos - self.velocity
        self.down_pos = self.down_pos - self.velocity
        if self.top_pos.x < bird.position.x and not self.not_reset:
            bird.score += 1
            self.not_reset = True
        if self.top_pos.x < -50:
            self.reset()

    def reset(self):
        self.down_pos = v(DISPLAY.dimension.x, r(
            self.pipe_gap + floor.dimension.y, DISPLAY.dimension.y))
        self.top_pos = v(DISPLAY.dimension.x,
                         self.down_pos.y - DISPLAY.dimension.y - self.pipe_gap)
        self.velocity = v(5, 0)
        self.not_reset = False


def draw():
    re = pg.draw.rect
    pt = re(DISPLAY.display, pipe.color, (pipe.top_pos, pipe.dimension))
    pd = re(DISPLAY.display, pipe.color, (pipe.down_pos, pipe.dimension))
    f = re(DISPLAY.display, floor.color, (floor.position, floor.dimension))
    p = re(DISPLAY.display, bird.color, (bird.position, bird.dimension))

    if p.colliderect(f) or p.colliderect(pt) or p.colliderect(pd):
        bird.lockMoves = True
        pipe.velocity = v(0, 0)


def showScore():
    FONT = pg.font.get_default_font()
    SIZE = 110
    SysFont = pg.font.SysFont(FONT, SIZE).render
    blit = DISPLAY.display.blit
    WHITE = (255, 255, 255)

    Text_Player_Points = SysFont(str(bird.score), True, WHITE)

    if bird.score < 10:
        blit(Text_Player_Points,
             ((DISPLAY.dimension.x/2) - SIZE/5, 30))

    elif bird.score > 9:
        blit(Text_Player_Points,
             ((DISPLAY.dimension.x/2) - SIZE/2.5, 30))

    else:
        blit(Text_Player_Points,
             ((DISPLAY.dimension.x/2) - SIZE, 30))

    if bird.lockMoves == True:
        Text_Game_Over = pg.font.SysFont(FONT, 100).render(
            "Game Over", True, WHITE)
        Text_Restart = pg.font.SysFont(FONT, 20).render(
            "Press 'Space' to restart", True, WHITE)

        blit(Text_Game_Over, (10, 140))
        blit(Text_Restart, (120, 210))


if __name__ == "__main__":
    FPS = 60
    DISPLAY = Display()
    bird = Bird()
    floor = Floor()
    pipe = Pipe()
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                key = pg.key.get_pressed()
                if key[K_SPACE] and bird.lockMoves == False:
                    bird.jump()

                if bird.lockMoves == True:
                    if key[K_SPACE]:
                        for entity in [bird, pipe]:
                            entity.reset()

        for entity in [bird, pipe]:
            entity.move()

        DISPLAY.display.fill((0, 0, 0))
        draw()
        showScore()
        clock.tick(FPS)
        pg.display.update()
