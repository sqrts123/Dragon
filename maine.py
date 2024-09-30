import pygame, random

# Set display surface
pygame.init()

# Set display surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed The Dragon")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game value:  CONSTANT_NAME, value
''' 5 CONSTANTS
PLAYER_STARTING_LIVES, 5
PLAYER_VELOCITY, 10
COIN_STARTING_VELOCITY, 10
COIN_ACCELERATION, 0.5
BUFFER_DISTANCE, 100
'''
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 10
COIN_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

# Set Game Variables:  variable_name
''' 3 variables
score, 0
player_lives, PLAYER_STARTING_LIVES
coin_velocity, COIN_STARTING_VELOCITY
'''
score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY
# YOU do the remaining 2 variables

# Set colors
red = (255, 0, 0)
orange = (255, 100, 0)
yellow = (255, 200, 0)
bright_green = (50, 255, 0)
green = (25, 100, 0)
bright_blue = (0, 255, 255)
blue = (0, 100, 255)
solid_blue = (0, 0, 255)
purple = (120, 0, 255)
pink = (255, 0, 240)
black = (0, 0, 0)
white = (255, 255, 255)
gray = (99, 99, 99)
darkgray = (45, 45, 45)
brown = (115, 45, 15)

# Set fonts
font = pygame.font.Font('AttackGraffiti.ttf', 32)

# Set Text for Score
'''
variable names:  score_text, score_rect
render text: "Score: " + str(score)
antialias: True
color: GREEN
background: DARKGREEN
rect location: topleft = (10, 10)  
'''
score_text = font.render("Score: " + str(score), True, green, bright_green)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

# Set Text for Title (Similar to Score)
'''
variable names:  title_text , title_rect 
render text: "Feed the Dragon"
antialias: True
color: GREEN
background: WHITE
rect location: centerx = WINDOW_WIDTH//2
rect location: y = 10 
'''

# Set Text for Lives (Similar to Score)
'''
variable names:  lives_text, lives_rect
render text: "Lives: " + str(player_lives)
antialias: True
color: GREEN
background: DARKGREEN
rect location: topright = (WINDOW_WIDTH - 10, 10) 
'''

# Set Text for Game Over (Similar to Score)
'''
variable names:  game_over_text , game_over_rect 
render text: "GAMEOVER"
antialias: True
color: GREEN
background: DARKGREEN
rect location: center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2) 
'''

# Set Text for Continue (Similar to Score)
'''
variable names:  continue_text, continue_rect  
render text: "Press any key to play again"
antialias: True
color: GREEN
background: DARKGREEN
rect location: center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)
'''

# Set sounds and music
coin_sound = pygame.mixer.Sound("coin_sound.wav")
miss_sound = pygame.mixer.Sound("miss_sound.wav")
miss_sound.set_volume(0.1)
pygame.mixer.music.load("ftd_background_music.wav")

# Set images
'''
variable names:  player_image, player_rect  
image source: "dragon_right.png"
rect location: left = 32
rect location: centery = WINDOW_HEIGHT // 2
'''
player_image = pygame.image.load("dragon_right.png")
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT // 2

'''
variable names:  coin_image, coin_rect  
image source: "coin.png"
rect location: x = WINDOW_WIDTH + BUFFER_DISTANCE
rect location: y = 0.   Note this will be a rando number.  Just later.  
'''
coin_image = pygame.image.load("coin.png")
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

pygame.mixer.music.play(-1, 0.0)

# The main game loop
running = True
while running:
    # Check to see if the user wants to quit
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
          running = False

    # Check to see if the user wants to move
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
       player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
       player_rect.y += PLAYER_VELOCITY

    #Move the coin
    if coin_rect.x < 0:
       #Player missed the coin
       player_lives -= 1
       miss_sound.play()
       coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
       coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    else:
       coin_rect.x -= coin_velocity

    #Check for collision (aka dragon eats coin)
    if player_rect.colliderect(coin_rect):
       score += 1
       coin_sound.play()
       coin_velocity += COIN_ACCELERATION
       coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
       coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

    #Update the HUD
    score_text = font.render("Score: " + str(score), True, green, bright_green)
    ''' Update the player lives text much like I did for the score'''

    #Check for game over
    if player_lives == 0:
       '''display_surface.blit(game_over_text, game_over_rect'''
       ''' Display the continue text like I did for game_over_text'''
       pygame.display.update()

       #Pause the game until player presses a key, then reset the game
       is_paused = True
       while is_paused:
          for event in pygame.event.get():
             if event.type == pygame.QUIT:
                #set variables to end game
                is_paused = False
                running = False
             if event.type == pygame.KEYDOWN:
                #reset the game
                score = 0
                player_lives = PLAYER_STARTING_LIVES
                player_rect.y = WINDOW_HEIGHT // 2
                coin_velocity = COIN_STARTING_VELOCITY
                pygame.mixer.music.play(-1, 0.0)
                is_paused = False


    # Fill the display
    display_surface.fill(black)

    # Blit the HUD to the screen.
    display_surface.blit(score_text, score_rect)
    ''' YOU DO:  blit title_text and title_rect'''
    ''' YOU DO:  blit lives_text and lives_rect'''
    display_surface.blit(player_image, player_rect)
    display_surface.blit(coin_image, coin_rect)
    pygame.draw.line(display_surface, white, (0,64), (WINDOW_WIDTH, 64), 2)

    # Update display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
