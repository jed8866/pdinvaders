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

# Load a bunch of images
def load_images(*files):
    images = []
    for file in files:
        images.append(load_image(file)[0])
    return images

# Load a sound.
def load_sound(name):
    fullname = os.path.join('sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        raise SystemExit('Error while loading sound: ' + fullname)
    return sound

# Build a sprite-group holding the monsters.
def build_monsters(allsprites):
    monsters = pygame.sprite.Group()
    horizontal_spacing = 50
    vertical_spacing = 50

    start_x = (screen_size[0] / 2) - 185
    start_y = 50
    monster_start = (start_x, start_y)

    build_monster_row(0, monster_start, horizontal_spacing, vertical_spacing, 1, allsprites, monsters)
    build_monster_row(1, monster_start, horizontal_spacing, vertical_spacing, 2, allsprites, monsters)
    build_monster_row(2, monster_start, horizontal_spacing, vertical_spacing, 2, allsprites, monsters)
    build_monster_row(3, monster_start, horizontal_spacing, vertical_spacing, 3, allsprites, monsters)
    build_monster_row(4, monster_start, horizontal_spacing, vertical_spacing, 3, allsprites, monsters)

    return monsters

def build_monster_row(row, monster_start, horizontal_spacing, vertical_spacing, monster_variant, allsprites, monsters):
    for col in range(8):
        monster_x = monster_start[0] + col * horizontal_spacing
        monster_y = monster_start[1] + row * vertical_spacing
    
        monster = Monster(monster_variant, (monster_x, monster_y), col, row)
        monsters.add(monster)
        allsprites.add(monster)


# Wait for user-input (close app, key-press or mouse-click)
def wait_for_input():
    while True:
        if pygame.event.wait().type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            break

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

class StaticTextSprite(pygame.sprite.Sprite):
    def __init__(self, size, color, msg, pos):
        pygame.sprite.Sprite.__init__(self)

        font = pygame.font.Font(None, size)
        color = pygame.Color(color)
        self.image = font.render(msg, 0, color)
        self.rect = self.image.get_rect().move(pos)

# Class for representing the player.
class Player(pygame.sprite.Sprite):
    images = []
    frameduration = 4 # Number of frames per 'animation-image'

    # Initialize image, position and speed
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((screen_size[0] / 2, screen_size[1] - 50))
        self.speed = 5
        self.blinks = 0
        self.image_index = 0

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

    def hit(self):
        self.blinks = 20

    def update(self):
        # When player is hit (by bomb or monster), make it blink
        # for a while.
        if self.blinks > 0:
            self.blinks -= 1
            self.image_index += 1
            self.image = self.images[self.image_index//self.frameduration % 2]
        else:
            self.image = self.images[0]

# Class for representing a single monster.
class Monster(pygame.sprite.Sprite):

    frameduration = 10 # Number of frames per 'animation-image'

    # Initialize image and position.
    #   startpos: screen-coordinates for initial position of the monster
    #   x, y: logical coordinates in grid of monsters - fx (2,3)
    def __init__(self, variant, startpos, x, y):
        pygame.sprite.Sprite.__init__(self)
        file1 = 'monster{0}_1.png'.format(variant)
        file2 = 'monster{0}_2.png'.format(variant)
        self.images = load_images(file1, file2)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(startpos)
        self.x = x
        self.y = y
        self.points = 40 - y * 10
        self.image_index = 0

    def update(self):
        # monster_controller calculates how we should move
        movement = monster_controller.speed
        self.rect = self.rect.move(movement)

        if len(bombs) < max_bombs:
            b = Bomb(self)
            bombs.add(b)
            allsprites.add(b)
            b.fire()

        self.image_index += 1
        self.image = self.images[self.image_index//self.frameduration % 2]

# Sprite for player score
class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.points = 0
        self.font = pygame.font.Font(None, 25)
        self.color = pygame.Color("red")
        self.update()
        self.rect = self.image.get_rect().move(5, 5)

    def update(self):
        msg = "Points: " + str(self.points)
        self.image = self.font.render(msg, 0, self.color)

    def addpoints(self, points):
        self.points += points

# Sprite for number of player lives
class PlayerLives(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.lives = 3
        self.font = pygame.font.Font(None, 25)
        self.color = pygame.Color("red")
        self.update()
        self.rect = self.image.get_rect().move(5, 20)

    def update(self):
        msg = "Lives: " + str(self.lives)
        self.image = self.font.render(msg, 0, self.color)

    def player_died(self):
        self.player.hit()
        self.lives -= 1
        return self.lives <= 0

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
            self.speed = (-self.speed[0], 10)
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

# Sprite for player-missile
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
        
# Sprite for a bomb (thrown by monsters)
class Bomb(pygame.sprite.Sprite):
    def __init__(self, monster):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bomb.png')
        self.speed = 5
        self.monster = monster

    def fire(self):
        self.rect.center = self.monster.rect.center

    def update(self):
        self.rect = self.rect.move(0, self.speed)
        if self.rect.top > screen_size[1]:
            self.kill()

#--------------------------
# Various constants
#--------------------------
frames_per_second = 60
max_bombs = 5
screen_size = [800, 600]

def main():
    # Initial setup
    pygame.init()
    pygame.display.set_caption("PD Invaders")
    pygame.mouse.set_visible(0)
    
    global screen, clock, background, allsprites, player, player_lives, score, monsters, missile, monster_controller, bombs

    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    Player.images = load_images('player.png', 'player_black.png')
    Monster.images = load_images('monster1_1.png', 'monster1_2.png', 'monster2_1.png', 'monster2_2.png', 'monster3_1.png', 'monster3_2.png')
    background = load_image('background.png')[0]
    allsprites = pygame.sprite.RenderClear()
    player = Player()
    player_lives = PlayerLives(player)
    score = Score()
    allsprites.add(player)
    allsprites.add(player_lives)
    allsprites.add(score)
    monsters = build_monsters(allsprites)
    missile = Missile() # Will be added to 'allsprites' when fired.
    monster_controller = MonsterMovementController(monsters)
    bombs = pygame.sprite.RenderClear()

    show_start_screen()
    run_game()
    show_game_over_screen()

def show_start_screen():

    # Print 'Press space to start game'
    # Wait for user to press space.

    start_screen_sprites = pygame.sprite.RenderClear()
    title = StaticTextSprite(100, "white", "PD invaders", (200, 200))
    start_message = StaticTextSprite(30, "red", "Press space to start", (200, 270))
    start_screen_sprites.add(title)
    start_screen_sprites.add(start_message)

    screen.blit(background, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    return

        start_screen_sprites.clear(screen, background)
        start_screen_sprites.update()
        start_screen_sprites.draw(screen)
        pygame.display.update()

        clock.tick(frames_per_second)

def show_game_over_screen():
    # Print 'Game over'
    # Wait for user to any key

    game_over_screen_sprites = pygame.sprite.RenderClear()
    text = StaticTextSprite(80, "red", "Game over", (240, 270))
    game_over_screen_sprites.add(text)

    screen.blit(background, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

        game_over_screen_sprites.clear(screen, background)
        game_over_screen_sprites.update()
        game_over_screen_sprites.draw(screen)
        pygame.display.update()

        clock.tick(frames_per_second)

def run_game():
    # Paint startscreen
    screen.blit(background, (0, 0))

    # Main loop
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
                score.addpoints(monster.points)

        # Check for collisions between player and bombs
        for bomb in pygame.sprite.spritecollide(player, bombs, 1):
            # Player was hit by a bomb
            bomb.kill()
            game_over = player_lives.player_died()
            if game_over:
                player.kill()
                return

        # Check for collisions between player and monsters
        for monster in pygame.sprite.spritecollide(player, monsters, 1):
            # Player was hit by a monster
            monster.kill()
            monster_controller.update()
            score.addpoints(monster.points)
            game_over = player_lives.player_died()
            if game_over:
                player.kill()
                return

        if len(monsters) == 0:
            return

        # Draw all sprites in new positions
        allsprites.draw(screen)
        pygame.display.update()

        clock.tick(frames_per_second)

if __name__ == '__main__':
    main()
