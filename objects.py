import pygame, sys
from constants import *
import random


class Menu(object):
    def __init__(self, clock, screen):
        super().__init__()
        self.screen = screen
        self.clock = clock

    def render(self):
        fontObj1 = pygame.font.Font('freesansbold.ttf', 50)
        fontObj2 = pygame.font.Font('freesansbold.ttf', 30)
        textSurfaceObj1 = fontObj1.render('Добро пожаловать в игру!',True,  yellow)
        textSurfaceObj2 = fontObj2.render('Чтобы начать/продолжить игру нажмите "S"',True,  yellow)
        textSurfaceObj3 = fontObj2.render('Чтобы закрыть игру нажмите "Q"',True,  yellow)
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (500, 100)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj3 = textSurfaceObj3.get_rect()
        textRectObj2.center = (395, 300)
        textRectObj3.center = (314, 400)
        self.screen.fill(lightGrey)
        self.screen.blit(textSurfaceObj1, textRectObj1)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        self.screen.blit(textSurfaceObj3, textRectObj3)
        pygame.display.flip()
        self.clock.tick(30)


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

    def info(self):
        fontObj2 = pygame.font.Font('freesansbold.ttf', 30)
        textSurfaceObj2 = fontObj2.render('Чтобы поставить на паузу нажмите "Esc"',True,  black, grey)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (width-320, height-10)
        self.screen.blit(textSurfaceObj2, textRectObj2)

    def render_score(self, score):
        fontObj2 = pygame.font.Font('freesansbold.ttf', 30)
        textSurfaceObj2 = fontObj2.render('Счёт: {}'.format(score), True,  black, grey)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (width-200, height-35)
        self.screen.blit(textSurfaceObj2, textRectObj2)

    def gameOver(self):
        pass



class Enemy(pygame.sprite.Sprite):
    delay = 90
    generation_delay = 0
    def __init__(self):
        super().__init__()
        img_name = 'img/enemy_{}.png'.format(random.randint(1, 4))
        self.image = pygame.image.load(img_name)
        self.rect = self.image.get_rect()
        self.rect.midleft = (width, random.randint(0, height))

    def update(self, player):
        if player.rect.centery > self.rect.centery:
            self.rect.move_ip((-3, 2))
        elif player.rect.centery < self.rect.centery:
            self.rect.move_ip((-3, -2))
        elif player.rect.centery == self.rect.centery:
            self.rect.move_ip((-3, 0))

    @staticmethod
    def generationEnemy(enemys, score):
        if Enemy.generation_delay <= 0:
            enemys.add(Enemy())
            Enemy.generation_delay = Enemy.delay
        else:
            Enemy.generation_delay -= 1

        for enemy in list(enemys):
            if enemy.rect.right <= 0:
                enemys.remove(enemy)
                score += 1
        return score





class Backgroud(pygame.sprite.Sprite):
    speed = 100
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/carp.jpg')
        self.rect = self.image.get_rect()
        self.rect.bottom = height
        self.rect.right = width

    def update(self):
        self.rect.right += 1

        if self.rect.right >= self.rect.width:
            self.rect.right = width


class Warhead(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('img/warhead.png')
        self.rect = self.image.get_rect()
        self.speed = 20
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

        self.rect.bottom = height - 10
        self.speed = 0
        self.shoot_delay = 0
        self.timer = 100

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.speed = 10
            if self.rect.bottom >= height:
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
        for shoot in list(self.warheads):
            if shoot.rect.left >= width:
                self.warheads.remove(shoot)

    def render_timer(self, screen):
        fontObj1 = pygame.font.Font('freesansbold.ttf', 30)
        textSurfaceObj1 = fontObj1.render('К выстрелу готов на {}%'.format(self.timer),True,  (0, 0, 0), (100, 100, 100))
        textRectObj1 = textSurfaceObj1.get_rect()
        screen.blit(textSurfaceObj1, textRectObj1)

    @staticmethod
    def hitting(score, enemys, warheads):
        if len(pygame.sprite.groupcollide(enemys, warheads, True, True)) != 0:
            score += 1
        return score

    @staticmethod
    def crash(player, enemys, menu):
        player_enemy = pygame.sprite.spritecollide(player, enemys, False)
        if player_enemy:
            menu.pause()
