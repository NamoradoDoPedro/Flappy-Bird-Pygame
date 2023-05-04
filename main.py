import pygame
import random
from pygame.locals import *
from sys import exit

pygame.init()
vec = pygame.math.Vector2


class WindowInfo:
    def __init__(self):
        self.Dimension = vec(400, 450)


def Infos(WindowInfo):
    Window = WindowInfo()
    FPS = 60
    Height = random.randint(20, Window.Dimension.y-220)
    clock = pygame.time.Clock()
    Display = pygame.display.set_mode((Window.Dimension.x, Window.Dimension.y))
    pygame.display.set_caption("Bird Test")
    return Window, FPS, Height, clock, Display


Window, FPS, Height, clock, Display = Infos(WindowInfo)


class PlayerInfo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Dimension = pygame.Surface((30, 30))
        self.Dimension.fill((255, 255, 0))
        self.rect = self.Dimension.get_rect()

        self.Score = int(0)
        self.Position = vec((50, 50))
        self.Velocity = vec(0, 0)
        self.Acceleration = vec(0, 0)
        self.LockMoves = False
        self.LockScore = False

    def move(self):
        self.Acceleration = vec(0, 0.5)
        self.Velocity += self.Acceleration
        self.Position += self.Velocity + 0.5 * self.Acceleration

        if self.Position.x > Window.Dimension.x:
            self.Position.x = 0
        if self.Position.x < 0:
            self.Position.x = Window.Dimension.x

        self.rect.midbottom = self.Position

    def jump(self):
        if self.Position.y > 55:
            self.Velocity.y = -8.5

    def update(self):
        if Player.Position.x - 15 > PipeTop.Position.x - 25 and self.LockScore == False:
            self.Score += 1
            self.LockScore = True
        hitsFloor = pygame.sprite.spritecollide(Player, PlatformInfos, False)
        if hitsFloor:
            self.Velocity.y = 0
            self.Position.y = hitsFloor[0].rect.top + 1

    def reset(self):
        self.Dimension = pygame.Surface((30, 30))
        self.Dimension.fill((255, 255, 0))
        self.rect = self.Dimension.get_rect()

        self.Score = int(0)
        self.Position = vec((50, 50))
        self.Velocity = vec(0, 0)
        self.Acceleration = vec(0, 0)
        self.LockMoves = False
        self.LockScore = False


class PipeTopInfo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Dimension = pygame.Surface((50, Window.Dimension.y))
        self.Dimension.fill((30, 230, 30))
        self.rect = self.Dimension.get_rect()
        self.Position = vec((Window.Dimension.x, Height))
        self.Velocity = int(5)

    def update(self, Height):
        self.Height = Height
        self.rect.midbottom = self.Position
        if self.Position.x < -50:
            self.Position = vec((Window.Dimension.x, self.Height))
            Player.LockScore = False

    def move(self):
        self.Position.x = self.Position.x - self.Velocity

    def reset(self):
        self.Dimension = pygame.Surface((50, Window.Dimension.y))
        self.Dimension.fill((30, 230, 30))
        self.rect = self.Dimension.get_rect()
        self.Position = vec((Window.Dimension.x, Height))
        self.Velocity = int(5)


class PipeDownInfo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Dimension = pygame.Surface((50, Window.Dimension.y))
        self.Dimension.fill((30, 230, 30))
        self.rect = self.Dimension.get_rect()
        self.Position = vec((Window.Dimension.x, Height+580))
        self.Velocity = int(5)

    def update(self, Height):
        self.Height = Height
        self.rect.midbottom = self.Position
        if self.Position.x < -50:
            self.Position = vec((Window.Dimension.x, self.Height+580))

    def move(self):
        self.Position.x = self.Position.x - self.Velocity

    def reset(self):
        self.Dimension = pygame.Surface((50, Window.Dimension.y))
        self.Dimension.fill((30, 230, 30))
        self.rect = self.Dimension.get_rect()
        self.Position = vec((Window.Dimension.x, Height+580))
        self.Velocity = int(5)


class FloorInfo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Dimension = pygame.Surface((Window.Dimension.x, 20))
        self.Dimension.fill((255, 0, 0))
        self.rect = self.Dimension.get_rect(
            center=(Window.Dimension.x/2, Window.Dimension.y - 10))

    def move(self):
        pass


def Sprites_Infos(PlayerInfo, FloorInfo, PipeTopInfo, PipeDownInfo):
    Floor = FloorInfo()
    Player = PlayerInfo()
    PipeTop = PipeTopInfo()
    PipeDown = PipeDownInfo()

    PlatformInfos = pygame.sprite.Group()
    PlatformInfos.add(Floor)

    PipesInfos = pygame.sprite.Group()
    PipesInfos.add(PipeTop)
    PipesInfos.add(PipeDown)

    all_sprites = All_Sprites_Infos(Floor, Player, PipeTop, PipeDown)
    return Player, PipeTop, PipeDown, PlatformInfos, PipesInfos, all_sprites


def All_Sprites_Infos(Floor, Player, PipeTop, PipeDown):
    all_sprites = pygame.sprite.Group()
    all_sprites.add(Floor)
    all_sprites.add(PipeTop)
    all_sprites.add(PipeDown)
    all_sprites.add(Player)
    return all_sprites


Player, PipeTop, PipeDown, PlatformInfos, PipesInfos, all_sprites = Sprites_Infos(
    PlayerInfo, FloorInfo, PipeTopInfo, PipeDownInfo)


def Show_Score(mid):
    Font = pygame.font.get_default_font()
    FontSize = 110
    Font_sys = pygame.font.SysFont(Font, 110)

    if Player.Score < 10:
        Text_Player_Points_Shadow = pygame.font.SysFont(
            Font, 110).render(str(int(Player.Score)), True, (0, 0, 0))
        Display.blit(Text_Player_Points_Shadow,
                     (mid - FontSize/10 - 2.5, 30 - 5))
        Text_Player_Points = Font_sys.render(
            str(int(Player.Score)), True, (255, 240, 240))
        Display.blit(Text_Player_Points, (mid - FontSize/5, 30))

    elif Player.Score > 9:
        Text_Player_Points_Shadow = pygame.font.SysFont(
            Font, 110).render(str(int(Player.Score)), True, (0, 0, 0))
        Display.blit(Text_Player_Points_Shadow,
                     (mid - FontSize/4 - 2.5, 30 - 5))
        Text_Player_Points = Font_sys.render(
            str(int(Player.Score)), True, (255, 240, 240))
        Display.blit(Text_Player_Points, (mid - FontSize/2.5, 30))

    else:
        Text_Player_Points_Shadow = pygame.font.SysFont(
            Font, 110).render(str(int(Player.Score)), True, (0, 0, 0))
        Display.blit(Text_Player_Points_Shadow,
                     (mid - FontSize/2 - 2.5, 30 - 5))
        Text_Player_Points = Font_sys.render(
            str(int(Player.Score)), True, (255, 240, 240))
        Display.blit(Text_Player_Points, (mid - FontSize, 30))

    if Player.LockMoves == True:
        Text_Game_Over = pygame.font.SysFont(Font, 100).render(
            str("Game Over"), True, (255, 240, 240))
        Text_Restart = pygame.font.SysFont(Font, 20).render(
            str("Press 'Space' to restart"), True, (255, 240, 240))
        Display.blit(Text_Game_Over, (10, 140))
        Display.blit(Text_Restart, (120, 210))


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and Player.LockMoves == False:
                    Player.jump()

                if Player.LockMoves == True:
                    if event.key == pygame.K_SPACE:
                        Player.reset()
                        PipeTop.reset()
                        PipeDown.reset()

        Height = random.randint(20, Window.Dimension.y-220)
        Display.fill((0, 0, 0))
        pygame.draw.rect(Display, (0, 0, 20), (0, 0, 5000, 5000))
        Player.update()
        PipeTop.update(Height)
        PipeDown.update(Height)

        if pygame.sprite.spritecollide(Player, PipesInfos, False) or pygame.sprite.spritecollide(Player, PlatformInfos, False):
            Player.LockMoves = True
            PipeTop.Velocity = 0
            PipeDown.Velocity = 0

        for entity in all_sprites:
            Display.blit(entity.Dimension, entity.rect)
            entity.move()

        if PipeTop.Position.x < -50:
            Height = random.randint(20, Window.Dimension.y-220)

        Show_Score(Window.Dimension.x/2)
        pygame.display.update()
        clock.tick(FPS)
