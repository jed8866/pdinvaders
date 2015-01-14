#-----------------------------------------------------------
#
# PD Invaders
#
#-----------------------------------------------------------

import pygame
from pygame.locals import *

pygame.init()

screen_size = [400, 400]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("PD Invaders")
pygame.mouse.set_visible(0)

pygame.display.update()
pygame.time.wait(3000)
