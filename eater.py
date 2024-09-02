"""
Eater
Made with PyGame
"""

import pygame, sys, time, random

WIDTH = 900
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

SPEED = 10

pygame.init()
game_window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('EATER')

fps_controller = pygame.time.Clock()

# Game variables
EATER_pos = [100, 50]
EATER_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

# Game Over
def game_over():
    gameOver_font = pygame.font.SysFont('arial', 18)
    gameOver_surface = gameOver_font.render('YOU DIED.', True, WHITE)
    game_window.blit(gameOver_surface, [100,0])
    show_score()
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Score
def show_score():
    score_font = pygame.font.SysFont('arial', 18)
    score_surface = score_font.render('Score : ' + str(score), True, WHITE)
    game_window.blit(score_surface, [0,0])
    # pygame.display.flip()


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # EATER cannot move in the opposite direction instantaneously.
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # EATER moves.
    if direction == 'UP':
        EATER_pos[1] -= 10
    if direction == 'DOWN':
        EATER_pos[1] += 10
    if direction == 'LEFT':
        EATER_pos[0] -= 10
    if direction == 'RIGHT':
        EATER_pos[0] += 10

    # EATER body grows.
    EATER_body.insert(0, list(EATER_pos))
    if EATER_pos[0] == food_pos[0] and EATER_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        EATER_body.pop()

    # food
    if not food_spawn:
        food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
    food_spawn = True

    # graphics
    game_window.fill(BLACK)
    for pos in EATER_body:
        pygame.draw.rect(game_window, BLUE, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, WHITE, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Game Over conditions
    # hitting boundaries
    if EATER_pos[0] < 0 or EATER_pos[0] > WIDTH-10:
        game_over()
    if EATER_pos[1] < 0 or EATER_pos[1] > HEIGHT-10:
        game_over()
    # hitting itself
    for block in EATER_body[1:]:
        if EATER_pos[0] == block[0] and EATER_pos[1] == block[1]:
            game_over()

    show_score()
   
    pygame.display.update()
    fps_controller.tick(SPEED)