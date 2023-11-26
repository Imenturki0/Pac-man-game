import pygame
from board import boards1
import math


class Player:
    def __init__(self, position_x, position_y, counter, direction, command_direction, num_width, num_height,
                 player_speed):
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

        # self.turns_allowed=[False,False,False,False]

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

    def move_player(self):

        if self.direction == 0:  # Right
            self.position_x += self.player_speed
        elif self.direction == 1:  # Left
            self.position_x -= self.player_speed
        elif self.direction == 2:  # Up
            self.position_y -= self.player_speed
        elif self.direction == 3:  # Down
            self.position_y += self.player_speed

    def check_collisions(self, score, board, grid_x, grid_y,power ,power_count ,eaten_ghosts):
        # Check if there is a circle at the current position
        if board[grid_y][grid_x] == 1:
            # Increase score
            score += 10
            # Set the board position to 0 to indicate the circle has been eaten
            board[grid_y][grid_x] = 0
        if board[grid_y][grid_x] ==2:
            score += 50
            board[grid_y][grid_x]=0
            power =True
            power_count = 0
            eaten_ghosts =[False]*4

        return score , power , power_count ,eaten_ghosts
