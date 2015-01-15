#-----------------------------------------------------------
#
# PD Invaders
#
#-----------------------------------------------------------

import sys, pygame

class PlayerObject:
    def __init__(self, startpos):
        self.image = pygame.image.load('images\\player.png').convert()
        self.pos = self.image.get_rect().move(startpos)

    def move_horizontal(self, distance):
        self.pos = self.pos.move(distance, 0)
        if self.pos.right > screen_size[0]:
            self.pos.right = screen_size[0]
        if self.pos.left < 0:
            self.pos.left = 0

#--------------------------
# Initial setup
#--------------------------
pygame.init()

pygame.display.set_caption("PD Invaders")
pygame.mouse.set_visible(0)

screen_size = [800, 600]
screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()

background = pygame.image.load('images\\background.png').convert()
player = PlayerObject((screen_size[0] / 2, screen_size[1] - 50))

#--------------------------
# Various constants
#--------------------------
player_speed = 5

#--------------------------
# Paint startscreen
#--------------------------
screen.blit(background, (0, 0))
screen.blit(player.image, player.pos)

#--------------------------
# Main loop
#--------------------------
while True:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()

    keys_pressed = pygame.key.get_pressed()
    player_movement = 0

    if keys_pressed[pygame.K_LEFT]:
        player_movement = -player_speed
    elif keys_pressed[pygame.K_RIGHT]:
        player_movement = player_speed
                
    # Erase player
    screen.blit(background, player.pos, player.pos)

    # Move player
    player.move_horizontal(player_movement)

    # Paint player in new position
    screen.blit(player.image, player.pos)

    pygame.display.update()
    clock.tick(60)
