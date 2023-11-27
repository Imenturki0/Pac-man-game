import copy

import pygame
from board import boards1
import math


class Player:
    def __init__(self, position_x, position_y, counter, direction, command_direction, num_width, num_height,
                 player_speed,score,powerup,lives):
        self.position_x = position_x
        self.position_y = position_y
        self.center_x = position_x + 17
        self.center_y = position_y + 17
        # self.score=0
        self.direction = direction  # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        self.command_direction = command_direction
        self.num_width = num_width
        self.num_height = num_height
        self.counter = counter

        self.player_images = self.load_player_images()
        self.last_valid_image = self.player_images[self.counter // 5]
        self.player_speed = player_speed
        self.score=score
        self.powerup =powerup
        self.lives=lives
        self.turns_allowed=   self.check_positions()
        self.rect = pygame.rect.Rect((self.position_x, self.position_y), (36, 36))

    def load_player_images(self):
        images = []
        for i in range(1, 5):
            image_path = f'assets/player_images/{i}.png'
            image = pygame.image.load(image_path)
            scaled_image = pygame.transform.scale(image, (35, 35))
            images.append(scaled_image)
        return images

    def draw(self, surface):

        # Determine the current frame based on the counter
        current_frame = self.counter // 5
        turns_allowed = self.check_positions()
        # Draw the player based on the current direction

        if self.direction == 0:
            self.last_valid_image = self.player_images[current_frame]
            surface.blit(self.last_valid_image, (self.position_x, self.position_y))
        elif self.direction == 1:
            self.last_valid_image = pygame.transform.flip(self.player_images[current_frame], True, False)
            surface.blit(self.last_valid_image, (self.position_x, self.position_y))
        elif self.direction == 2:
            self.last_valid_image = pygame.transform.rotate(self.player_images[current_frame], 90)
            surface.blit(self.last_valid_image, (self.position_x, self.position_y))
        elif self.direction == 3:
            self.last_valid_image = pygame.transform.rotate(self.player_images[current_frame], 270)
            surface.blit(self.last_valid_image, (self.position_x, self.position_y))
        #pygame.draw.rect(surface, (255, 0, 0), self.rect, width=1)


    def check_positions(self):
        turns = [False] * 4

         #print(self.center_y // self.num_height,(self.center_x - num) // self.num_width)
        if self.center_y//30<29:
            if self.direction == 0:
                if boards1[self.center_y // self.num_height][(self.center_x - (self.num_width // 2)) // self.num_width] != 4:
                    turns[1] = True
            if self.direction == 1:
                if boards1[self.center_y // self.num_height][(self.center_x + (self.num_width // 2)) // self.num_width] != 4:
                    turns[0] = True
            if self.direction == 2:
                if boards1[(self.center_y + (self.num_height // 2)) // self.num_height][(self.center_x) // self.num_width] != 4:
                    turns[3] = True
            if self.direction == 3:
                if boards1[(self.center_y - (self.num_height // 2)) // self.num_height][(self.center_x) // self.num_width] != 4:
                    turns[2] = True

            if self.direction == 2 or self.direction == 3:

                if 16 <= self.center_x % self.num_width <= 22:
                    if boards1[(self.center_y + (self.num_height // 2)) // self.num_height][self.center_x // self.num_width] != 4:
                        turns[3] = True
                    if boards1[(self.center_y -(self.num_height // 2)) // self.num_height][self.center_x // self.num_width] != 4:
                        turns[2] = True
                if 16 <= self.center_y % self.num_height <= 22:
                    if boards1[self.center_y // self.num_height][(self.center_x - self.num_width) // self.num_width] != 4:
                        turns[1] = True
                    if boards1[self.center_y // self.num_height][(self.center_x + self.num_width) // self.num_width] != 4:
                        turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 16 <= self.center_x % self.num_width <= 22:
                    if boards1[(self.center_y + self.num_height) // self.num_height][self.center_x // self.num_width] != 4:
                        turns[3] = True
                    if boards1[(self.center_y - self.num_height) // self.num_height][self.center_x // self.num_width] != 4:
                        turns[2] = True
                if 16 <= self.center_y % self.num_height <= 22:
                    if boards1[self.center_y // self.num_height][(self.center_x - (self.num_width // 2)) // self.num_width] != 4:
                        turns[1] = True
                    if boards1[self.center_y // self.num_height][(self.center_x + (self.num_width // 2)) // self.num_width] != 4:
                        turns[0] = True
        # else:
        #     turns[2] = True
        #     turns[3] = True
        return turns

    def move_player(self,play_x,play_y):

        # r, l, u, d
        if self.direction == 0 and self.turns_allowed[0]:
            play_x += self.player_speed
        elif self.direction == 1 and self.turns_allowed[1]:
            play_x -= self.player_speed
        if self.direction == 2 and self.turns_allowed[2]:
            play_y -= self.player_speed
        elif self.direction == 3 and self.turns_allowed[3]:
            play_y += self.player_speed
        return play_x, play_y

    def check_collisions(self, board, grid_x, grid_y,power ,power_count ,eaten_ghosts):
        # Check if there is a circle at the current position

        if board[grid_y][grid_x] == 1:
            # Increase score
            self.score += 10
            # Set the board position to 0 to indicate the circle has been eaten
            board[grid_y][grid_x] = 0

        if board[grid_y][grid_x] ==2:
            self.score += 50
            board[grid_y][grid_x]=0
            power =True
            power_count = 0
            eaten_ghosts =[False]*4

        return self.score , power , power_count ,eaten_ghosts

    def display_onscreen(self,screen,game_over,game_won):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render('Score: ' + str(self.score), True, (255, 255, 255))
        screen.blit(score_text, (10, 750))
        if self.powerup:
            pygame.draw.circle(screen,'blue',(150,760),15)
        for i in range(self.lives):
            screen.blit(pygame.transform.scale(self.player_images[0],(25,25)),(650+i*35,750))
        if game_over:
            pygame.draw.rect(screen, 'white', [150, 200, 500, 300], 0, 10)
            #pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
            screen.blit(gameover_text, (200, 300))
        if game_won:
            pygame.draw.rect(screen, 'white', [150, 200, 500, 300], 0, 10)
            gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
            screen.blit(gameover_text, (200, 300))