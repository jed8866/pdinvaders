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
    def __init__(self, kind, startpos, x, y):
        path = "images\\monster{0}.png".format(kind)
        self.image = pygame.image.load(path).convert()
        self.pos = self.image.get_rect().move(startpos)
        self.x = x
        self.y = y

    def move(self, distance):
        self.pos = self.pos.move(distance, 0)
        
class AllMonsters:
    def __init__(self):
        self.monsters = [[None for x in range(8)] for x in range(4)]
        self.build_monsters()
        self.movement = Movement.RIGHT
        self.speed = 2
        self.find_rightmost_monster()
        self.find_leftmost_monster()
        
    def paint(self, screen):
        for row in self.monsters:
            for m in row:
                screen.blit(m.image, m.pos)

    def erase(self, screen, background):
        for row in self.monsters:
            for m in row:
                screen.blit(background, m.pos, m.pos)

    def move(self):
        if self.movement == Movement.RIGHT:
            # Move all monsters to the right.
            # If the movement would cause the right-most monster to hit
            # the screen boundary, then start moving in the other direction
            # instead.

            effective_speed = self.speed

            if self.rightmost_monster.pos.right + self.speed > screen_size[0]:
                print('hitting boundary')
                effective_speed = screen_size[0] - self.rightmost_monster.pos.right
                self.movement = Movement.LEFT

            for row in self.monsters:
                for m in row:
                    m.move(effective_speed)

        elif self.movement == Movement.LEFT:
            # Move all monsters to the left.
            # If the movement would cause the left-most monster to hit
            # the screen boundary, then start moving in the other direction
            # instead.

            effective_speed = self.speed

            if self.leftmost_monster.pos.left - self.speed < 0:
                print('hitting boundary')
                effective_speed = self.leftmost_monster.pos.left
                self.movement = Movement.RIGHT

            for row in self.monsters:
                for m in row:
                    m.move(-effective_speed)

    def build_monsters(self):
        monster_start = (screen_size[0] / 2 - 185, 50)

        for col in range(0, 8):

            for row in range(0, 4):
                monster_x = monster_start[0] + col * 50
                monster_y = monster_start[1] + row * 50
    
                self.monsters[row][col] = Monster(row+1, (monster_x, monster_y), col, row)

    def find_rightmost_monster(self):
        self.rightmost_monster = self.get_rightmost_monster()
        print('rightmost')
        print(self.rightmost_monster.x)
        print(self.rightmost_monster.y)

    def find_leftmost_monster(self):
        self.leftmost_monster = self.get_leftmost_monster()
        print('leftmost')
        print(self.leftmost_monster.x)
        print(self.leftmost_monster.y)

    def get_leftmost_monster(self):
        row_with_leftmost = 0
        col_with_leftmost = 7

        for row_index, row in enumerate(self.monsters):
            for col_index, m in enumerate(row):
                if not (m is None) and col_index < col_with_leftmost:
                    row_with_leftmost = row_index
                    col_with_leftmost = col_index
        return self.monsters[row_with_leftmost][col_with_leftmost]

    def get_rightmost_monster(self):
        row_with_rightmost = 0
        col_with_rightmost = 0

        for row_index, row in enumerate(self.monsters):
            for col_index, m in enumerate(reversed(row)):
                if not (m is None) and col_index > col_with_rightmost:
                    row_with_rightmost = row_index
                    col_with_rightmost = col_index
        return self.monsters[row_with_rightmost][col_with_rightmost]

#--------------------------
# Various constants
#--------------------------
frames_per_second = 60

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
    all_monsters.move()

    # Paint objects in new positions
    screen.blit(player.image, player.pos)
    all_monsters.paint(screen)

    pygame.display.update()
    clock.tick(frames_per_second)
