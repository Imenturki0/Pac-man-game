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
        turns_allowed = self.check_pos(surface)
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

    def check_pos(self, screen):

        turns = [False] * 4

        # Calculate the pixel coordinates for the edges of the object
        left_edge_x = self.position_x
        right_edge_x = self.position_x + self.num_height - 7
        top_edge_y = self.position_y + 5
        bottom_edge_y = self.position_y + self.num_width - 7
        pygame.draw.circle(screen, (255, 255, 255), (left_edge_x, top_edge_y), 2)
        pygame.draw.circle(screen, (255, 255, 255), (left_edge_x, bottom_edge_y), 2)
        pygame.draw.circle(screen, (255, 255, 255), (right_edge_x, top_edge_y), 2)
        pygame.draw.circle(screen, (255, 255, 255), (right_edge_x, bottom_edge_y), 2)
        # Calculate the grid indices from the pixel coordinates
        left_edge_index = left_edge_x // self.num_width
        right_edge_index = right_edge_x // self.num_width
        top_edge_index = top_edge_y // self.num_height
        bottom_edge_index = bottom_edge_y // self.num_height

        # Now perform the checks using indices as necessary

        # Check Right
        if boards1[self.center_y // self.num_height][((self.center_x + (self.num_width // 2)) // self.num_width)] != 4:
            if boards1[top_edge_index][right_edge_index] == 4 or boards1[bottom_edge_index][
                right_edge_index] == 4:  # Ensure within right boundary
                turns[0] = False
            else:
                turns[0] = True

        # Check Left
        if boards1[self.center_y // self.num_height][(self.center_x - (self.num_width // 2)) // self.num_width] != 4:
            if boards1[top_edge_index][left_edge_index] == 4 or boards1[bottom_edge_index][
                left_edge_index] == 4:  # Ensure within right boundary
                turns[1] = False
            else:
                turns[1] = True

        # Check Up
        if boards1[(self.center_y - (self.num_height // 2)) // self.num_height][(self.center_x // self.num_width)] != 4:

            if boards1[top_edge_index][left_edge_index] == 4 or boards1[top_edge_index][right_edge_index] == 4:
                turns[2] = False

            else:
                turns[2] = True

        # Check Down
        if boards1[(self.center_y + (self.num_height // 2)) // self.num_height][(self.center_x // self.num_width)] != 4:
            # Ensure within right boundary
            if boards1[bottom_edge_index][left_edge_index] == 4 or boards1[bottom_edge_index][right_edge_index] == 4:
                turns[3] = False

            else:
                turns[3] = True
        # print(turns)
        return turns

    def check_positions(self):
        turns = [False] * 4
        num = 16
        if self.direction == 0:
            if boards1[self.center_y // self.num_height][(self.center_x - num) // self.num_width] != 4:
                turns[1] = True
        if self.direction == 1:
            if boards1[self.center_y // self.num_height][(self.center_x + num) // self.num_width] != 4:
                turns[0] = True
        if self.direction == 2:
            if boards1[self.center_y + (self.num_height // 2) // self.num_height][(self.center_x) // self.num_width] != 4:
                turns[3] = True
        if self.direction == 3:
            if boards1[self.center_y - (self.num_height // 2) // self.num_height][(self.center_x) // self.num_width] != 4:
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
            if 12 <= self.center_y % self.num_height <= 18:
                if boards1[self.center_y // self.num_height][(self.center_x - num) // self.num_width] != 4:
                    turns[1] = True
                if boards1[self.center_y // self.num_height][(self.center_x + num) // self.num_width] != 4:
                    turns[0] = True
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

    def eat_circle(self, score, board, grid_x, grid_y):
        # Check if there is a circle at the current position
        if board[grid_y][grid_x] == 1:
            # Increase score
            score += 1
            # Set the board position to 0 to indicate the circle has been eaten
            board[grid_y][grid_x] = 0

        print(score)
        return score
