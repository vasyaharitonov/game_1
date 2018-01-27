import pygame
import sys
from objects import Player, Warhead, Backgroud, Menu, Enemy
from constants import *


pygame.init()
pygame.display.set_caption("Hello")

screen = pygame.display.set_mode(size)

warheads = pygame.sprite.Group()
background = Backgroud()
player = Player(warheads)

all_obj = pygame.sprite.Group()
all_obj.add(player)
all_obj.add(background)
enemys = pygame.sprite.Group()

#enemy = Enemy()

clock = pygame.time.Clock()

menu = Menu(clock, screen)
menu.pause()

game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        menu.pause()



    score = Enemy.generationEnemy(enemys, score)
    background.update()
    player.update()
    warheads.update()
    enemys.update(player)


    score = Player.hitting(score, enemys, warheads)
    Player.crash(player, enemys, menu)
    print(score)
    #print(list(pygame.sprite.groupcollide(enemys, warheads, True, True)))    #Удаляет объекты если они пересекаются

    screen.blit(background.image, background.rect)
    warheads.draw(screen)
    screen.blit(player.image, player.rect)
    enemys.draw(screen)

    menu.render_score(score)
    menu.info()
    player.render_timer(screen)     #показатель перезарядки

    pygame.display.flip()
    clock.tick(60)
