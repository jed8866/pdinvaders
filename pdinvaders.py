#-----------------------------------------------------------
#
# PD Invaders
#
#-----------------------------------------------------------

import sys, pygame

# Class for holding some named constants - kind of an enum.
class Movement:
    NONE = 0
    RIGHT = 1
    LEFT = 2

# Class for representing the player.
class PlayerObject:

    # Initialize image, position and speed
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

# Class for representing a single monster.
class Monster:

    # Initialize image and position.
    #   startpos: screen-coordinates for initial position of the monster
    #   x, y: logical coordinates in grid of monsters - fx (2,3)
    def __init__(self, kind, startpos, x, y):
        path = "images\\monster{0}.png".format(kind)
        self.image = pygame.image.load(path).convert()
        self.pos = self.image.get_rect().move(startpos)
        self.x = x
        self.y = y

    # Move the monster horizontally. Caller is responsible for checking that
    # the monster will not fall off the screen - right or left.
    def move(self, distance):
        self.pos = self.pos.move(distance, 0)

    def move_down(self, distance):
        self.pos = self.pos.move(0, distance)
        
# Class for representing the collection of monsters.
# A two-dimensional array is used to hold the monsters.
# When a monster is shot, the cell is set to 'None'.
class AllMonsters:

    # Initialize collection.
    #  rows: number of monster-rows
    #  columns: number of monster-columns
    def __init__(self, rows, columns):
        self.build_monsters(rows, columns)
        self.horizontal_direction = Movement.RIGHT
        self.speed = (2, 10)

        # We maintain a reference to the right-most and left-most
        # monster. This is used when deciding when the monsters should
        # change direction (horizontally).
        self.set_rightmost_monster()
        self.set_leftmost_monster()
        
    # Paint the monsters to the screen
    def paint(self, screen):
        for row in self.monsters:
            for m in row:
                screen.blit(m.image, m.pos)

    # Erase the monsters from the screen
    def erase(self, screen, background):
        for row in self.monsters:
            for m in row:
                screen.blit(background, m.pos, m.pos)

    # Move all monsters horizontally, and if the screen boundary is
    # hit, move them a bit down as well.
    def move(self):

        move_down = False
        effective_speed = 0

        if self.horizontal_direction == Movement.RIGHT:
            # Move all monsters to the right.
            # If the movement would cause the right-most monster to hit
            # the screen boundary, then start moving in the other direction
            # instead.

            effective_speed = self.speed[0]

            if self.rightmost_monster.pos.right + self.speed[0] > screen_size[0]:
                # Moving 'self.speed' would cause the rightmost monster to hit
                # the screen boundary. So instead move as far to the right as we can,
                # and switch direction. Also move the monsters a bit down.
                effective_speed = screen_size[0] - self.rightmost_monster.pos.right
                self.horizontal_direction = Movement.LEFT
                move_down = True

        elif self.horizontal_direction == Movement.LEFT:
            # Move all monsters to the left.
            # If the movement would cause the left-most monster to hit
            # the screen boundary, then start moving in the other direction
            # instead.

            effective_speed = -self.speed[0]

            if self.leftmost_monster.pos.left - self.speed[0] < 0:
                effective_speed = -self.leftmost_monster.pos.left
                self.horizontal_direction = Movement.RIGHT
                move_down = True

        if effective_speed != 0:
            for row in self.monsters:
                for m in row:
                    m.move(effective_speed)

        if move_down:
            for row in self.monsters:
                for m in row:
                    m.move_down(self.speed[1])

    # Helper method for building the two-dimensional array of monsters.
    # 'self.monsters' is a list of rows. Each row contains a number of monsters.
    # When indexing the grid, use self.monsters[row][column].
    def build_monsters(self, rows, columns):
        self.monsters = [[None for x in range(columns)] for x in range(rows)]

        horizontal_spacing = 50
        vertical_spacing = 50

        start_x = (screen_size[0] / 2) - 185
        start_y = 50
        monster_start = (start_x, start_y)

        for row in range(rows):

            for col in range(columns):

                monster_x = monster_start[0] + col * horizontal_spacing
                monster_y = monster_start[1] + row * vertical_spacing
    
                self.monsters[row][col] = Monster(row+1, (monster_x, monster_y), col, row)

    def set_rightmost_monster(self):
        self.rightmost_monster = self.get_rightmost_monster()

    def set_leftmost_monster(self):
        self.leftmost_monster = self.get_leftmost_monster()

    # Find leftmost monster that is not None.
    # Enumerate grid of monsters - one row at a time.
    def get_leftmost_monster(self):
        row_with_leftmost = 0
        col_with_leftmost = len(self.monsters[0])-1

        for row_index, row in enumerate(self.monsters):
            for col_index, m in enumerate(row):
                if not (m is None) and col_index < col_with_leftmost:
                    # We found one with a lower column-index. This is
                    # the left-most this far.
                    row_with_leftmost = row_index
                    col_with_leftmost = col_index
        return self.monsters[row_with_leftmost][col_with_leftmost]

    # Find rightmost monster that is not None.
    # Enumerate grid of monsters - one row at a time. Look through
    # each row from right to left - ie. reversed.
    def get_rightmost_monster(self):
        row_with_rightmost = 0
        col_with_rightmost = 0

        for row_index, row in enumerate(self.monsters):
            for col_index, m in enumerate(reversed(row)):
                if not (m is None) and col_index > col_with_rightmost:
                    # We found one with a higher column-index. This is
                    # the right-most this far.
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
all_monsters = AllMonsters(4, 8)

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
    all_monsters.move()

    # Paint objects in new positions
    screen.blit(player.image, player.pos)
    all_monsters.paint(screen)

    pygame.display.update()
    clock.tick(frames_per_second)
