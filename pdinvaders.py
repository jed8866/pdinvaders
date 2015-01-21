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

    def move(self, distance):
        self.pos = self.pos.move(distance, 0)
        
        
class AllMonsters:
    def __init__(self):
        self.monsters = []
        self.build_monsters()
        
    def build_monsters(self):
        monster_start = (screen_size[0] / 2 - 185, 50)

        for col in range(1, 9):

            for row in range(1, 5):
                monster_x = monster_start[0] + (col-1) * 50
                monster_y = monster_start[1] + (row-1) * 50
    
                self.monsters.append( Monster(row, (monster_x, monster_y)) )

#--------------------------
# Various constants
#--------------------------
frames_per_second = 60
player_speed = 5
monster_speed = 10

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
all_monsters = AllMonsters()

#--------------------------
# Paint startscreen
#--------------------------
screen.blit(background, (0, 0))
screen.blit(player.image, player.pos)
for m in all_monsters.monsters:
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
                
    # Erase objects
    screen.blit(background, player.pos, player.pos)
    for m in all_monsters.monsters:
        screen.blit(background, m.pos, m.pos)

    # Move objects
    player.move_horizontal(player_movement)

    

#    for m in all_monsters.monsters:
#        m.move(monster_speed)
        



    # Paint objects in new positions
    screen.blit(player.image, player.pos)
    for m in all_monsters.monsters:
        screen.blit(m.image, m.pos)

    pygame.display.update()
    clock.tick(frames_per_second)
