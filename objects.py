import pygame, sys
from constants import heigth, width

class Menu(object):
    def __init__(self, screen):
        self.screen = screen

    def render(self):
        fontObj1 = pygame.font.Font('freesansbold.ttf', 50)
        fontObj2 = pygame.font.Font('freesansbold.ttf', 30)
        textSurfaceObj1 = fontObj1.render('Добро пожаловать в игру!',True,  (255, 255,   0))
        textSurfaceObj2 = fontObj2.render('Чтобы начать/продолжить игру нажмите "S"',True,  (255, 255,   0))
        textSurfaceObj3 = fontObj2.render('Чтобы закрыть игру нажмите "Q"',True,  (255, 255,   0))
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (500, 100)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj3 = textSurfaceObj3.get_rect()
        textRectObj2.center = (395, 300)
        textRectObj3.center = (314, 400)
        self.screen.fill((162, 164, 189))
        self.screen.blit(textSurfaceObj1, textRectObj1)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        self.screen.blit(textSurfaceObj3, textRectObj3)
        pygame.display.flip()

    def pause(self):
        pause = True

        while pause:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if keys[pygame.K_s]:
                pause = False
            elif keys[pygame.K_q]:
                sys.exit()
            self.render()


class Knight(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('img/knight.png')
        self.rect = self.image.get_rect()


class Backgroud(pygame.sprite.Sprite):
    speed = 100
    def __init__(self):
        self.image = pygame.image.load('img/carp.jpg')
        self.rect = self.image.get_rect()
        self.rect.bottom = heigth
        self.rect.right = width

    def update(self):
        pass
        self.rect.right += 1

        if self.rect.right >= self.rect.width:
            self.rect.right = width


class Warhead(pygame.sprite.Sprite):
    speed = 20

    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('img/warhead.png')
        self.rect = self.image.get_rect()

        self.rect.midbottom = (position[0], position[1] + 40)

    def update(self):
        self.rect.move_ip((self.speed, 0))


class Player(pygame.sprite.Sprite):
    delay = 100  #задержка между выстрелами
    def __init__(self, warheads):
        super().__init__()
        self.warheads = warheads
        self.image = pygame.image.load('img/player_min.png')
        self.rect = self.image.get_rect()

        self.rect.bottom = heigth - 10
        self.speed = 0
        self.shoot_delay = 0
        self.timer = 100

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.speed = 10
            if self.rect.bottom >= heigth:
                self.speed = 0
        elif keys[pygame.K_UP]:
            self.speed = -10
            if self.rect.top <= 0:
                self.speed = 0
        else:
            self.speed = 0
        self.rect.move_ip((0, self.speed))   #смещаемся на вектор
        self.shooting()

    def shooting(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.shoot_delay <= 0:
            self.warheads.add(Warhead(self.rect.midtop))
            self.shoot_delay = self.delay
            self.timer = 0
        else:
            self.shoot_delay -= 1
            if self.timer < 100:
                self.timer += 1

    def render_timer(self, screen):
        fontObj1 = pygame.font.Font('freesansbold.ttf', 30)
        textSurfaceObj1 = fontObj1.render('{}%'.format(self.timer),True,  (0, 0, 0), (100, 100, 100))
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (900, 40)
        screen.blit(textSurfaceObj1, textRectObj1)
