#-----------------------------------------------------------
#
# PD Invaders
#
#-----------------------------------------------------------

import sys, pygame

class Movement:
    NONE = 0
    RIGHT = 1
    LEFT = 2

class PlayerObject:
    def __init__(self, startpos):
        self.image = pygame.image.load('images\\player.png').convert()
        self.pos = self.image.get_rect().move(startpos)
        self.speed = 5

    # Move player right or left
    def move(self, movement):
        if movement == Movement.RIGHT:
            self.pos = self.pos.move(self.speed, 0)
        elif movement == Movement.LEFT:
            self.pos = self.pos.move(-self.speed, 0)

        # Make sure we don't fall of the screen (to the right)
        if self.pos.right > screen_size[0]:
            self.pos.right = screen_size[0]
        # ... or to the left
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
        self.monsters = [[None for x in range(8)] for x in range(4)]
        self.build_monsters()
        
    def paint(self, screen):
        for row in self.monsters:
            for m in row:
                screen.blit(m.image, m.pos)

    def erase(self, screen, background):
        for row in self.monsters:
            for m in row:
                screen.blit(background, m.pos, m.pos)

    def build_monsters(self):
        monster_start = (screen_size[0] / 2 - 185, 50)

        for col in range(0, 8):

            for row in range(0, 4):
                monster_x = monster_start[0] + col * 50
                monster_y = monster_start[1] + row * 50
    
                self.monsters[row][col] = Monster(row+1, (monster_x, monster_y))

#--------------------------
# Various constants
#--------------------------
frames_per_second = 60
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
all_monsters.paint(screen)

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
    player_movement = Movement.NONE

    if keys_pressed[pygame.K_LEFT]:
        player_movement = Movement.LEFT
    elif keys_pressed[pygame.K_RIGHT]:
        player_movement = Movement.RIGHT
                
    # Erase objects
    screen.blit(background, player.pos, player.pos)
    all_monsters.erase(screen, background)

    # Move objects
    player.move(player_movement)

    # Move monsters

    # Paint objects in new positions
    screen.blit(player.image, player.pos)
    all_monsters.paint(screen)

    pygame.display.update()
    clock.tick(frames_per_second)
