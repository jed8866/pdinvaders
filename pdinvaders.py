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

class Monster:
    def __init__(self, kind, startpos):
        path = "images\\monster{0}.png".format(kind)
        self.image = pygame.image.load(path).convert()
        self.pos = self.image.get_rect().move(startpos)

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
monsters = []
monsters.append( Monster(1, (50, 50)) )
monsters.append( Monster(2, (50, 100)) )
monsters.append( Monster(3, (50, 150)) )

#--------------------------
# Various constants
#--------------------------
frames_per_second = 60
player_speed = 5

#--------------------------
# Paint startscreen
#--------------------------
screen.blit(background, (0, 0))
screen.blit(player.image, player.pos)
for m in monsters:
    screen.blit(m.image, m.pos)

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
                
    # Erase player and monsters
    screen.blit(background, player.pos, player.pos)
    for o in monsters:
        screen.blit(background, m.pos, m.pos)

    # Move player and monsters
    player.move_horizontal(player_movement)

    # Paint player and monsters in new position
    screen.blit(player.image, player.pos)
    for m in monsters:
        screen.blit(m.image, m.pos)

    pygame.display.update()
    clock.tick(frames_per_second)
