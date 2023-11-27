import pygame
from board import boards1
from Player import Player
from Ghost import Ghost

pygame.init()
width = 800
height = 800
level = boards1
flicker = False
counter = 0
direction = 0
direction_command = 0
player_speed = 3
screen = pygame.display.set_mode((width, height))
timer = pygame.time.Clock()
fps = 60
# TITLE OF CANVAS
pygame.display.set_caption("My Board")
nums_height = (height - 50) // len(level)
nums_width = width // len(level[0])
exit = False
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (35, 35))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (35, 35))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (35, 35))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (35, 35))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (35, 35))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (35, 35))

player_x = nums_width * 9
player_y = nums_height * 12
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
score = 0
powerup = False
power_counter = 0
eaten_ghosts = [False] * 4
moving = False
startup_counter = 0


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

def get_ghost_positions():
    # Return the positions of ghosts as a list of tuples [(x1, y1), (x2, y2), ...]
    return [(blinky_ghost.x, blinky_ghost.y), (inky_ghost.x, inky_ghost.y), (pinky_ghost.x, pinky_ghost.y), (clyde_ghost.x, clyde_ghost.y)]
def get_pellet_and_powerup_locations(board):
    """
    Get the locations of pellets and power-ups on the game board.

    Returns:
    - pellet_locations (list of tuples): List of tuples representing the (x, y) positions of pellets.
    - powerup_locations (list of tuples): List of tuples representing the (x, y) positions of power-ups.
    """
    pellet_locations = []
    powerup_locations = []

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:  # Pellet
                pellet_locations.append((j, i))  # (x, y)
            elif board[i][j] == 2:  # Power-up
                powerup_locations.append((j, i))  # (x, y)

    return pellet_locations, powerup_locations

while not exit:
    # screen.blit(pygame.transform.scale(image, (50,50)),(50,50))
    timer.tick(fps)
    screen.fill((0, 0, 0))
    draw_board()
    player = Player(player_x, player_y, counter, direction, direction_command, nums_width, nums_height,
                    player_speed)  # 350,470
    turns_allowed = player.check_positions()

    blinky_ghost = Ghost(nums_width * 9, nums_height * 8, 2, blinky_img, targets[0])
    inky_ghost = Ghost(nums_width * 9, nums_height * 9, 2, inky_img, targets[1])
    pinky_ghost = Ghost(nums_width * 9, nums_height * 10, 2, pinky_img, targets[2])
    clyde_ghost = Ghost(nums_width * 9, nums_height * 11, 2, clyde_img, targets[3])
    blinky_ghost.chase_player(player.position_x, player.position_y)

    # Move and draw the ghost
    blinky_ghost.move(level, nums_width, nums_height, width, height)
    blinky_ghost.draw(screen)
    inky_ghost.draw(screen)
    pinky_ghost.draw(screen)
    blinky_ghost.draw(screen)

    # reinforcment learning part
    player_position = player.get_player_position()
    ghost_positions = get_ghost_positions()
    pellet_locations, powerup_locations = get_pellet_and_powerup_locations(level)
    positions = player.get_adjacent_positions()
    game_state = (player_position, ghost_positions, powerup, pellet_locations, powerup_locations)

    if moving:
        if direction == 0 and turns_allowed[0]:
            player_x += player_speed
        elif direction == 1 and turns_allowed[1]:
            player_x -= player_speed
        elif direction == 2 and turns_allowed[2]:
            player_y -= player_speed
        elif direction == 3 and turns_allowed[3]:
            player_y += player_speed

    player.draw(screen)

    # Convert player position to grid position
    grid_x = player.position_x // nums_width
    grid_y = player.position_y // nums_height

    # Call the eat_circle method
    score, powerup, power_counter, eaten_ghosts = player.check_collisions(score, level, grid_x, grid_y,powerup,power_counter,eaten_ghosts)
    # Render the score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # Adjust the position as needed

    print(score)
    counter += 1
    if counter >= 19:
        counter = 0  # Reset counter
        flicker = not flicker
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghosts = [False] * 4
    if startup_counter < 180:
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
