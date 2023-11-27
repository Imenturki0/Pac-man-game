import copy

import pygame
from board import boards1
from Player import Player
from Ghost import Ghost

width = 800
height = 800
level = copy.deepcopy(boards1)
flicker = False
counter = 0
direction = 0
direction_command = 0
fps = 60
nums_height = (height - 50) // len(level)
nums_width = width // len(level[0])
exit = False
game_over = False
game_won = False

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
timer = pygame.time.Clock()
pygame.display.set_caption("My Board")

# load ghost images
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (35, 35))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (35, 35))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (35, 35))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (35, 35))

# player and game state variables
player_x = nums_width * 9
player_y = nums_height * 12
player_speed = 3
score = 0
powerup = False
power_counter = 0
eaten_ghosts = [False] * 4
moving = False
startup_counter = 0

# ghost variables
targets = [(player_x, player_y)] * 4

blinky_dead = False
blinky_direction = 0
blinky_x = 38
blinky_y = 39

pinky_dead = False
pinky_direction = 0
pinky_x = nums_width * 9
pinky_y = nums_height * 9

inky_dead = False
inky_direction = 0
inky_x = nums_width * 9
inky_y = nums_height * 10

clyde_dead = False
clyde_direction = 0
clyde_x = nums_width * 9
clyde_y = nums_height * 10

mode_timer = 0
mode = "Scatter"
clyde_mode = "Chase"
clyde_switch_time = 0
lives=3

def draw_board():
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 4:
                pygame.draw.rect(screen, 'blue', (j * nums_width, i * nums_height, nums_width, nums_height), 2)
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white',
                                   (j * nums_width + (nums_width * 0.5), i * nums_height + (nums_height * 0.5)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white',
                                   (j * nums_width + (nums_width * 0.5), i * nums_height + (nums_height * 0.5)), 10)


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if powerup:
        if not blinky_ghost.dead and not eaten_ghosts[0]:
            blink_target = (nums_width, nums_height)
        elif blinky_ghost.dead or eaten_ghosts[0] and not blinky_ghost.in_box:

            blinky_ghost.speed = 7
            blink_target = (nums_width * 9, nums_height * 9)
        if not pinky_ghost.dead and not eaten_ghosts[1]:
            pinky_target = (nums_width * 18, nums_height * 1)
        elif pinky_ghost.dead or eaten_ghosts[1]:

            pinky_ghost.speed = 7
            pinky_target = (nums_width * 9, nums_height * 9)
        if not inky_ghost.dead and not eaten_ghosts[2]:
            inky_target = (nums_width * 18, nums_height * 18)
        elif inky_ghost.dead or eaten_ghosts[2]:
            inky_target = (nums_width * 9, nums_height * 9)

            inky_ghost.speed = 7
        if not clyde_ghost.dead and not eaten_ghosts[3]:
            clyde_target = (nums_width * 1, nums_height * 18)
        elif clyde_ghost.dead or eaten_ghosts[3]:
            clyde_target = (nums_width * 9, nums_height * 9)
            clyde_ghost.speed = 7
    else:
        if blinky_ghost.dead or eaten_ghosts[0] and not blinky_ghost.in_box:
            blinky_ghost.speed = 7
            blink_target = (nums_width * 9, nums_height * 9)
        elif blinky_ghost.mode == "Scatter":
            blink_target = (nums_width, nums_height)
        else:
            blink_target = (player_x, player_y)

        if pinky_ghost.dead or eaten_ghosts[1] and not pinky_ghost.in_box:
            pinky_ghost.speed = 7
            pinky_target = (nums_width * 9, nums_height * 9)
        elif pinky_ghost.mode == "Scatter":
            pinky_target = (nums_width * 18, nums_height * 1)
        else:
            pinky_target = (player_x, player_y)

        if inky_ghost.dead or eaten_ghosts[2] and not inky_ghost.in_box:
            inky_ghost.speed = 7
            inky_target = (nums_width * 9, nums_height * 9)
        elif inky_ghost.mode == "Scatter":
            inky_target = (nums_width * 18, nums_height * 1)
        else:
            inky_target = (player_x, player_y)

        if clyde_ghost.dead or eaten_ghosts[3] and not clyde_ghost.in_box:
            clyde_target = (nums_width * 9, nums_height * 9)
            clyde_ghost.speed = 7
        elif clyde_ghost.mode == "Scatter":
            clyde_target = (nums_width * 18, nums_height * 1)
        else:
            clyde_target = (player_x, player_y)

    return [blink_target, pinky_target, inky_target, clyde_target]


def check_collisions( lives,eaten_ghosts, score):
    global player_x, player_y
    global blinky_direction, pinky_direction, inky_direction, clyde_direction
    global blinky_x, pinky_x, inky_x, clyde_x
    global blinky_y, pinky_y, inky_y, clyde_y
    global blinky_dead,pinky_dead,inky_dead,clyde_dead
    global game_over

    global  startup_counter, power_counter
    if powerup:
        if player.rect.colliderect(blinky_ghost.rect):
            eaten_ghosts[0] = True
            blinky_dead = True
            score += 200
        if player.rect.colliderect(pinky_ghost.rect):
            eaten_ghosts[1] = True
            pinky_dead = True
            score += 200
        if player.rect.colliderect(inky_ghost.rect):
            eaten_ghosts[2] = True
            inky_dead = True
            score += 200
        if player.rect.colliderect(clyde_ghost.rect):
            eaten_ghosts[3] = True
            clyde_dead = True
            score += 200
    else:
        if (player.rect.colliderect(blinky_ghost.rect) and not blinky_ghost.dead) or \
                (player.rect.colliderect(pinky_ghost.rect) and not pinky_ghost.dead) or \
                (player.rect.colliderect(inky_ghost.rect) and not inky_ghost.dead) or \
                (player.rect.colliderect(clyde_ghost.rect) and not clyde_ghost.dead):
            if lives > 0:
                lives -= 1
                player_x = nums_width * 9
                player_y = nums_height * 12
                startup_counter = 0
                power_counter = 0
                blinky_dead = False
                blinky_direction = 0
                blinky_x = 38
                blinky_y = 39

                pinky_dead = False
                pinky_direction = 0
                pinky_x = nums_width * 9
                pinky_y = nums_height * 9

                inky_dead = False
                inky_direction = 0
                inky_x = nums_width * 9
                inky_y = nums_height * 10

                clyde_dead = False
                clyde_direction = 0
                clyde_x = nums_width * 9
                clyde_y = nums_height * 10
            else:
                game_over = True
                #moving = False
                startup_counter = 0
    if blinky_ghost.in_box == True:
        eaten_ghosts[0] = False
        blinky_dead = False
    if pinky_ghost.in_box == True:
        eaten_ghosts[1] = False
        pinky_dead = False
    if inky_ghost.in_box == True:
        eaten_ghosts[2] = False
        inky_dead = False
    if clyde_ghost.in_box == True:
        eaten_ghosts[3] = False
        clyde_dead = False

    return {
        'player_x':player_x,
        'player_y':player_y,
        'blinky_dead': blinky_dead,
        'blinky_direction': blinky_direction,
        'blinky_x': blinky_x,
        'blinky_y': blinky_y,
        'pinky_dead': pinky_dead,
        'pinky_direction': pinky_direction,
        'pinky_x': pinky_x,
        'pinky_y': pinky_y,
        'inky_dead': inky_dead,
        'inky_direction': inky_direction,
        'inky_x': inky_x,
        'inky_y': inky_y,
        'clyde_dead': clyde_dead,
        'clyde_direction': clyde_direction,
        'clyde_x': clyde_x,
        'clyde_y': clyde_y,
        'eaten_ghosts': eaten_ghosts,
        'score': score,
        'player_lives': lives,
        'startup_counter': startup_counter,
        'power_counter': power_counter,
        'game_over':game_over

    }


def update_mode(mode_timer, mode):
    mode_timer += 1
    scatter_time, chase_time = (50, 300)
    if mode == "Scatter" and mode_timer > scatter_time:
        mode = "Chase"
        mode_timer = 0
    elif mode == "Chase" and mode_timer > chase_time:
        mode = "Scatter"
        mode_timer = 0
    return mode, mode_timer



while not exit:

    # screen.blit(pygame.transform.scale(image, (50,50)),(50,50))
    timer.tick(fps)
    screen.fill((0, 0, 0))
    draw_board()
    player = Player(player_x, player_y, counter, direction, direction_command,
                    nums_width, nums_height, player_speed, score, powerup,lives)  # 350,470
    turns_allowed = player.check_positions()
    mode, mode_timer = update_mode(mode_timer, mode)

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False
    # ghosts objects
    blinky_ghost = Ghost(blinky_x, blinky_y, nums_width, nums_height, blinky_direction,
                         2, blinky_img, targets[0], blinky_dead, 0, mode)
    pinky_ghost = Ghost(pinky_x, pinky_y, nums_width, nums_height, pinky_direction,
                        2, pinky_img, targets[1], pinky_dead, 1, mode)
    inky_ghost = Ghost(inky_x, inky_y, nums_width, nums_height, inky_direction,
                       2, inky_img, targets[2], inky_dead, 2, mode)
    clyde_ghost = Ghost(clyde_x, clyde_y, nums_width, nums_height, clyde_direction,
                        2, clyde_img, targets[3], clyde_dead, 3, clyde_mode)

    # ghosts draw
    blinky_ghost.draw(screen, powerup, eaten_ghosts)
    pinky_ghost.draw(screen, powerup, eaten_ghosts)
    inky_ghost.draw(screen, powerup, eaten_ghosts)
    clyde_ghost.draw(screen, powerup, eaten_ghosts)

    player.draw(screen)

    # Convert player position to grid position
    grid_x = player.center_x // nums_width
    grid_y = player.center_y // nums_height

    # Call the eat_circle method
    score, powerup, power_counter, eaten_ghosts = player.check_collisions(level, grid_x, grid_y, powerup, power_counter,
                                                                          eaten_ghosts)
    # Render the score
    player.display_onscreen(screen,game_over,game_won)

    # inky_ghost.draw(screen, powerup, eaten_ghosts)
    # pinky_ghost.draw(screen, powerup, eaten_ghosts)
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

    if moving:
        # player_x, player_y = player.move_player(player_x,player_y)
        blinky_x, blinky_y, blinky_direction = blinky_ghost.move_blinky()
        pinky_x, pinky_y, pinky_direction = pinky_ghost.move_pinky([player_x, player_y], direction, [0, 0])
        inky_x, inky_y, inky_direction = inky_ghost.move_inky([player_x, player_y], direction, [0, 0],
                                                              [blinky_x, blinky_y])
        clyde_x, clyde_y, clyde_direction, clyde_switch_time, clyde_mode = clyde_ghost.move_clyde([player_x, player_y],
                                                                                                  direction, [0, 0],
                                                                                                  clyde_switch_time)

        if direction == 0 and turns_allowed[0]:
            player_x += player_speed
        elif direction == 1 and turns_allowed[1]:
            player_x -= player_speed
        elif direction == 2 and turns_allowed[2]:
            player_y -= player_speed
        elif direction == 3 and turns_allowed[3]:
            player_y += player_speed

        data=check_collisions(lives,eaten_ghosts, score)
        print(data)
        player_x=data['player_x']
        player_y=data['player_y']
        blinky_dead=data['blinky_dead']
        blinky_direction=data['blinky_direction']
        blinky_x=data['blinky_x']
        blinky_y=data['blinky_y']
        pinky_dead=data['pinky_dead']
        pinky_direction=data['pinky_direction']
        pinky_x=data['pinky_x']
        pinky_y=data['pinky_y']
        inky_dead=data['inky_dead' ]
        inky_direction=data['inky_direction']
        inky_x=data['inky_x']
        inky_y=data['inky_y']
        clyde_dead=data['clyde_dead']
        clyde_direction=data['clyde_direction']
        clyde_x=data['clyde_x']
        clyde_y=data['clyde_y']
        eaten_ghosts=data['eaten_ghosts']
        score=data['score']
        game_over=data['game_over']

        lives=data['player_lives']
        print("player lives",player.lives)
        startup_counter=data['startup_counter']
        power_counter=data['power_counter']
    counter += 1
    if counter >= 19:
        counter = 0  # Reset counter
        flicker = not flicker
    if powerup and power_counter < 200:
        power_counter += 1
    elif powerup and power_counter >= 200:
        power_counter = 0
        powerup = False
        # eaten_ghosts = [False] * 4
    if startup_counter < 60 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):

                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = nums_width * 9
                player_y = nums_height * 12
                direction = 0
                direction_command = 0
                blinky_x = 38
                blinky_y = 39
                blinky_direction = 0
                inky_x = nums_width * 9
                inky_y = nums_height * 10
                inky_direction = 0
                pinky_x = nums_width * 9
                pinky_y = nums_height * 9
                pinky_direction = 0
                clyde_x = nums_width * 9
                clyde_y = nums_height * 10
                clyde_direction = 0
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                lives = 3
                game_over = False
                game_won = False
                level = copy.deepcopy(boards1)

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_y > 700:
        player_y = -47
    if player_y < -50:
        player_y = 700

        # Make the ghost chase the player

    pygame.display.update()
    pygame.display.flip()
pygame.quit()
