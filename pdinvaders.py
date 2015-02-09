#-----------------------------------------------------------
#
# PD Invaders
#
#-----------------------------------------------------------

import sys, pygame
import pygame.mixer
import os

# Load an image. Returns the image and its 'rect'
def load_image(name):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        raise SystemExit('Error while loading image: ' + fullname)
    image = image.convert()
    return image, image.get_rect()

# Load a sound.
def load_sound(name):
    fullname = os.path.join('sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        raise SystemExit('Error while loading sound: ' + fullname)
    return sound

# Build a sprite-group holding the monsters.
def build_monsters(rows, columns, allsprites):
    monsters = pygame.sprite.Group()
    horizontal_spacing = 50
    vertical_spacing = 50

    start_x = (screen_size[0] / 2) - 185
    start_y = 50
    monster_start = (start_x, start_y)

    for row in range(rows):
        for col in range(columns):
            monster_x = monster_start[0] + col * horizontal_spacing
            monster_y = monster_start[1] + row * vertical_spacing
    
            monster = Monster(row+1, (monster_x, monster_y), col, row)
            monsters.add(monster)
            allsprites.add(monster)
    return monsters

# Class for holding some named constants - kind of an enum.
class Movement:
    NONE = 0
    RIGHT = 1
    LEFT = 2

def get_movement(keys_pressed):
    movement = Movement.NONE

    if keys_pressed[pygame.K_LEFT]:
        movement = Movement.LEFT
    elif keys_pressed[pygame.K_RIGHT]:
        movement = Movement.RIGHT

    return movement

# Class for representing the player.
class Player(pygame.sprite.Sprite):

    # Initialize image, position and speed
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('player.png')
        self.rect = self.rect.move((screen_size[0] / 2, screen_size[1] - 50))
        self.speed = 5

    # Move player right or left
    def move(self, movement):
        if movement == Movement.RIGHT:
            self.rect = self.rect.move(self.speed, 0)
        elif movement == Movement.LEFT:
            self.rect = self.rect.move(-self.speed, 0)

        # Make sure we don't fall of the screen (to the right)
        if self.rect.right > screen_size[0]:
            self.rect.right = screen_size[0]
        # ... or to the left
        if self.rect.left < 0:
            self.rect.left = 0

# Class for representing a single monster.
class Monster(pygame.sprite.Sprite):

    # Initialize image and position.
    #   startpos: screen-coordinates for initial position of the monster
    #   x, y: logical coordinates in grid of monsters - fx (2,3)
    def __init__(self, kind, startpos, x, y):
        pygame.sprite.Sprite.__init__(self)
        filename = 'monster{0}.png'.format(kind)
        self.image, self.rect = load_image(filename)
        self.rect = self.rect.move(startpos)
        self.x = x
        self.y = y

    def update(self):
        # monster_controller calculates how we should move
        movement = monster_controller.speed
        self.rect = self.rect.move(movement)

# Class for calculating how the monsters should move.
class MonsterMovementController:
    def __init__(self, monsters):
        self.speed = (2, 0)
        self.monsters = monsters

        # We maintain a reference to the right-most and left-most
        # monster. This is used when deciding when the monsters should
        # change direction (horizontally).
        self.update()

    def calculate_movement(self):
        # If the right-most monster has crossed the right screen boundary, or
        # the left-most monster has crossed the left screen boundary, then
        # start moving in the opposite direction, and move a bit down as well.

        switch_direction = (self.rightmost_monster.rect.right > screen_size[0]
                            or self.leftmost_monster.rect.left < 0)

        if switch_direction:
            self.speed = (-self.speed[0], 2)
        else:
            self.speed = (self.speed[0], 0)

    def update(self):
        self.set_rightmost_monster()
        self.set_leftmost_monster()

    def set_rightmost_monster(self):
        self.rightmost_monster = self.get_rightmost_monster()

    def set_leftmost_monster(self):
        self.leftmost_monster = self.get_leftmost_monster()

    # Find a leftmost monster - ie. one with the lowest value of 'self.x'
    def get_leftmost_monster(self):
        if not self.monsters.sprites():
            return None

        leftmost = self.monsters.sprites()[0]

        for m in self.monsters.sprites():
            if m.x < leftmost.x:
                leftmost = m
        return leftmost

    # Find a rightmost monster.
    def get_rightmost_monster(self):
        if not self.monsters.sprites():
            return None

        rightmost = self.monsters.sprites()[0]

        for m in self.monsters.sprites():
            if m.x > rightmost.x:
                rightmost = m
        return rightmost

# Class for representing player-missile
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('missile.png')
        self.speed = 20
        # Sound played when shooting
        self.missile_sound = load_sound('15.wav')

    def fire(self, player):
        self.rect.center = player.rect.center
        self.missile_sound.play()

    # Move missile towards top of the screen.
    # If the missile leaves the screen it is 'killed' - ie.
    # it will not be part of the sprite-group 'allsprites'
    def update(self):
        self.rect = self.rect.move(0, -self.speed)
        if self.rect.bottom < 0:
            self.kill()
        
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

background = load_image('background.png')[0]
allsprites = pygame.sprite.RenderClear()
player = Player()
allsprites.add(player)
monsters = build_monsters(4, 8, allsprites)
missile = Missile() # Will be added to 'allsprites' when fired.
monster_controller = MonsterMovementController(monsters)

#--------------------------
# Paint startscreen
#--------------------------
screen.blit(background, (0, 0))

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

    # Erase all sprites from previous position
    allsprites.clear(screen, background)

    # React to player input
    keys_pressed = pygame.key.get_pressed()
    player_movement = get_movement(keys_pressed)
    player.move(player_movement)

    if keys_pressed[pygame.K_SPACE] and not missile.alive():
        allsprites.add(missile)
        missile.fire(player)

    monster_controller.calculate_movement()

    allsprites.update()
    
    # Check for collisions between player-missile and monsters
    if missile.alive():
        for monster in pygame.sprite.spritecollide(missile, monsters, 1):
            # A monster was hit - kill that and the missile (the missile can
            # only kill one monster)
            monster.kill()
            missile.kill()
            monster_controller.update()

    # Draw all sprites in new positions
    allsprites.draw(screen)
    pygame.display.update()

    clock.tick(frames_per_second)
