import pygame
import sys
from objects import Player, Warhead, Backgroud, Menu
from constants import size

pygame.init()
pygame.display.set_caption("Hello")

screen = pygame.display.set_mode(size)


def info():
    fontObj2 = pygame.font.Font('freesansbold.ttf', 30)
    textSurfaceObj2 = fontObj2.render('Чтобы поставить на паузу нажмите "Esc"',True,  (0, 0, 0), (100, 100, 100))
    textRectObj2 = textSurfaceObj2.get_rect()
    textRectObj2.center = (500, 20)
    screen.blit(textSurfaceObj2, textRectObj2)

warheads = pygame.sprite.Group()

background = Backgroud()
player = Player(warheads)
#warhead = Warhead(player.rect.midtop)
clock = pygame.time.Clock()

menu = Menu(screen)
menu.pause()

game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        menu.pause()

    background.update()
    player.update()
    warheads.update()

    screen.blit(background.image, background.rect)
    warheads.draw(screen)
    screen.blit(player.image, player.rect)
    #screen.blit(warhead.image, warhead.rect)
    info()
    player.render_timer(screen)     #показатель перезарядки

    pygame.display.flip()
    clock.tick(60)
