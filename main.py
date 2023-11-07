import pygame
from board import boards1
from Player import Player

pygame.init()
width = 800
height = 800
level = boards1
flicker = False
counter = 0
direction = 0
direction_command = 0
player_speed = 2
screen = pygame.display.set_mode((width, height))
timer = pygame.time.Clock()
fps = 60
# TITLE OF CANVAS
pygame.display.set_caption("My Board")
nums_height = (height - 50) // len(level)
nums_width = width // len(level[0])
exit = False


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


x = nums_width * 9
y = nums_height * 12
score = 0
while not exit:
    # screen.blit(pygame.transform.scale(image, (50,50)),(50,50))
    timer.tick(fps)
    screen.fill((0, 0, 0))
    draw_board()
    player = Player(x, y, counter, direction, direction_command, nums_width, nums_height, player_speed)  # 350,470
    turns_allowed = player.check_positions()
    #turns_allowed=player.check_positions()
    #print(x)
    if direction == 0 and turns_allowed[0]:
        x += player_speed

    elif direction == 1 and turns_allowed[1]:
        x -= player_speed
    elif direction == 2 and turns_allowed[2]:
        y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        y += player_speed

    player.draw(screen)

    #player.move_player()


    # Convert player position to grid position
    grid_x = player.position_x // nums_width
    grid_y = player.position_y // nums_height

    # Call the eat_circle method
    score=player.eat_circle(score,level, grid_x,grid_y)
    # Render the score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # Adjust the position as needed

    print(score)
    counter += 1
    if counter >= 19:
        counter = 0  # Reset counter
        flicker = not flicker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT :
                direction_command = 0
            if event.key == pygame.K_LEFT :
                direction_command = 1
            if event.key == pygame.K_UP :
                direction_command = 2
            if event.key == pygame.K_DOWN :
                direction_command = 3

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1] :
        direction = 1
    if direction_command == 2 and turns_allowed[2] :
        direction = 2
    if direction_command == 3 and turns_allowed[3] :
        direction = 3



    pygame.display.update()
    pygame.display.flip()
