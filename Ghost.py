import random

import pygame


class Ghost:
    def __init__(self, x, y, speed,img,target):
        self.x = x
        self.y = y
        self.speed = speed
        self.img=img
        self.target=target
        self.direction = random.choice([0, 1, 2, 3])  # right, left, up, down

    def draw(self, screen):

        screen.blit(self.img, (self.x, self.y))

    def chase_player(self, player_x, player_y):
        # Calculate the difference in x and y positions
        dx = player_x - self.x
        dy = player_y - self.y

        # If x difference is greater, move in the x direction; otherwise, move in the y direction
        if abs(dx) > abs(dy):
            if dx > 0:
                self.direction = 0  # right
            else:
                self.direction = 1  # left
        else:
            if dy > 0:
                self.direction = 3  # down
            else:
                self.direction = 2  # up

    def move(self, level, nums_width, nums_height,width,height):
        # Check for walls and change direction if needed
        grid_x = self.x // nums_width
        grid_y = self.y // nums_height

        directions = {
            0: (self.speed, 0),   # right
            1: (-self.speed, 0),  # left
            2: (0, -self.speed),  # up
            3: (0, self.speed)    # down
        }

        # Check if the next position is a wall (assuming 4 is a wall in the level matrix)
        next_x, next_y = directions[self.direction]
        new_grid_x = (self.x + next_x) // nums_width
        new_grid_y = (self.y + next_y) // nums_height
        if level[new_grid_y][new_grid_x] != 4:
            # Move the ghost in the chosen direction
            self.x += next_x
            self.y += next_y
        else:
            # Stop the ghost when it hits a wall
            self.direction = random.choice([0, 1, 2, 3])

        # Wrap around the screen if the ghost goes off the edge
        if self.x >= width:
            self.x = 0
        elif self.x < 0:
            self.x = width - nums_width

        if self.y >= height:
            self.y = 0
        elif self.y < 0:
            self.y = height - nums_height


