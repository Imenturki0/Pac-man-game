import math
import random

import pygame
from board import boards1


class Ghost:
    def __init__(self, position_x, position_y, num_width, num_height, direction, speed, img, target, dead, id, mode):
        self.id = id
        self.x_pos = position_x
        self.y_pos = position_y
        self.center_x = self.x_pos + 17
        self.center_y = self.y_pos + 17
        self.num_width = num_width
        self.num_height = num_height
        self.direction = direction
        self.speed = speed
        self.img = img
        self.target = target
        self.direction = direction  # right, left, up, down
        self.dead = dead
        self.turns, self.in_box = self.check_positions()
        self.mode = mode
        self.rect = pygame.rect.Rect((self.x_pos, self.y_pos), (36, 36))

    def draw(self, screen, powerup, eaten_ghost):
        # screen.blit(self.img, (self.x_pos, self.y_pos))

        spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (35, 35))
        dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (35, 35))
        if not eaten_ghost[self.id] and not self.dead:
            if not powerup or self.in_box:
                screen.blit(self.img, (self.x_pos, self.y_pos))
            else:
                screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        # pygame.draw.rect(screen, (255, 0, 0),
        #                  pygame.Rect(self.num_width * 9, self.num_height * 8, self.num_width, self.num_height * 3), 2)
        #
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, width=1)

    def check_positions(self):

        self.turns = [False] * 4
        self.in_box = False

        if self.center_y // 30 < 29:
            if self.direction == 0:
                if boards1[self.center_y // self.num_height][
                    (self.center_x - (self.num_width // 2)) // self.num_width] != 4:
                    self.turns[1] = True
            if self.direction == 1:
                if boards1[self.center_y // self.num_height][
                    (self.center_x + (self.num_width // 2)) // self.num_width] != 4:
                    self.turns[0] = True
            if self.direction == 2:
                if boards1[(self.center_y + (self.num_height // 2)) // self.num_height][
                    (self.center_x) // self.num_width] != 4:
                    self.turns[3] = True
            if self.direction == 3:
                if boards1[(self.center_y - (self.num_height // 2)) // self.num_height][
                    (self.center_x) // self.num_width] != 4:
                    self.turns[2] = True

            if self.direction == 2 or self.direction == 3:

                if 16 <= self.center_x % self.num_width <= 22:
                    if boards1[(self.center_y + (self.num_height // 2)) // self.num_height][
                        self.center_x // self.num_width] != 4:
                        self.turns[3] = True
                    if boards1[(self.center_y - (self.num_height // 2)) // self.num_height][
                        self.center_x // self.num_width] != 4:
                        self.turns[2] = True
                if 16 <= self.center_y % self.num_height <= 22:
                    if boards1[self.center_y // self.num_height][
                        (self.center_x - self.num_width) // self.num_width] != 4:
                        self.turns[1] = True
                    if boards1[self.center_y // self.num_height][
                        (self.center_x + self.num_width) // self.num_width] != 4:
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 16 <= self.center_x % self.num_width <= 22:
                    if boards1[(self.center_y + self.num_height) // self.num_height][
                        self.center_x // self.num_width] != 4:
                        self.turns[3] = True
                    if boards1[(self.center_y - self.num_height) // self.num_height][
                        self.center_x // self.num_width] != 4:
                        self.turns[2] = True
                if 16 <= self.center_y % self.num_height <= 22:
                    if boards1[self.center_y // self.num_height][
                        (self.center_x - (self.num_width // 2)) // self.num_width] != 4:
                        self.turns[1] = True
                    if boards1[self.center_y // self.num_height][
                        (self.center_x + (self.num_width // 2)) // self.num_width] != 4:
                        self.turns[0] = True
            # else:
            #     turns[2] = True
            #     turns[3] = True
            if self.num_width * 9 < self.center_x < self.num_width * 10 and self.num_height * 8 < self.center_y < self.num_height * 11:
                self.in_box = True
            else:
                self.in_box = False

        return self.turns, self.in_box

    def calculate_distance(self, x, y):
        # Euclidean distance to the target
        return math.sqrt((x - self.target[0]) ** 2 + (y - self.target[1]) ** 2)

    def opposite_direction(self, direction):
        if direction == 0:
            return 1  # Opposite of right is left
        elif direction == 1:
            return 0  # Opposite of left is right
        elif direction == 2:
            return 3  # Opposite of up is down
        else:  # direction == 3
            return 2  # Opposite of down is up

    def move_blinky(self):
        # Calculate distances for each possible direction

        directions = [(0, self.x_pos + self.speed, self.y_pos),  # Right
                      (1, self.x_pos - self.speed, self.y_pos),  # Left
                      (2, self.x_pos, self.y_pos - self.speed),  # Up
                      (3, self.x_pos, self.y_pos + self.speed)]  # Down

        distances = [(d, self.calculate_distance(x, y)) for d, x, y in directions if self.turns[d]]

        # Exclude the opposite direction unless it's the only option
        opposite_direction = self.opposite_direction(self.direction)
        if len(distances) > 1:
            distances = [dist for dist in distances if dist[0] != opposite_direction]

        # Choose the direction with the shortest distance
        if distances:
            # If multiple directions have the same shortest distance, choose based on preference order
            best_direction = min(distances, key=lambda x: (x[1], x[0]))[0]

            self.direction = best_direction

        # Move based on the chosen direction
        if self.direction == 0:  # right
            self.x_pos += self.speed
        elif self.direction == 1:  # left
            self.x_pos -= self.speed
        elif self.direction == 2:  # up
            self.y_pos -= self.speed
        elif self.direction == 3:  # down
            self.y_pos += self.speed

        # Handle screen wrap-around

        if self.x_pos < -50:
            self.x_pos = 700
        elif self.x_pos > 700:
            self.x_pos = -47

        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self, pac_man_pos, pac_man_direction, scatter_target):
        # print("mode",self.mode)
        # Aim for a few tiles ahead of Pac-Man's current direction
        offset = 4  # Number of tiles ahead of Pac-Man
        if not self.dead and self.mode == "Chase":
            if pac_man_direction == 2:
                # Note: Adjust as per your coordinate system. Sometimes, 'up' means decreasing y.
                self.target = [self.target[0], self.target[1] - offset * self.num_height]
            elif pac_man_direction == 3:
                self.target = [self.target[0], self.target[1] + offset * self.num_height]
            elif pac_man_direction == 1:
                self.target = [self.target[0] - offset * self.num_width, self.target[1]]
            elif pac_man_direction == 0:
                self.target = [self.target[0] + offset * self.num_width, self.target[1]]

        # Calculate distances for each possible direction
        directions = [
            (0, self.x_pos + self.speed, self.y_pos),  # Right
            (1, self.x_pos - self.speed, self.y_pos),  # Left
            (2, self.x_pos, self.y_pos - self.speed),  # Up
            (3, self.x_pos, self.y_pos + self.speed)  # Down
        ]

        # Filter out opposite direction and calculate distances
        opposite_direction = self.opposite_direction(self.direction)
        distances = [
            (d, self.calculate_distance(x, y))
            for d, x, y in directions
            if self.turns[d] and d != opposite_direction
        ]
        if not distances:
            self.direction = opposite_direction
        # if self.in_box and self.turns[1]:

        # Choose the direction with the shortest distance
        if distances:
            best_direction = min(distances, key=lambda x: x[1])[0]
            self.direction = best_direction

        if self.direction == 0 and self.turns[0]:  # right
            self.x_pos += self.speed
        elif self.direction == 1 and self.turns[1]:  # left
            self.x_pos -= self.speed
        elif self.direction == 2 and self.turns[2]:  # up
            self.y_pos -= self.speed
        elif self.direction == 3 and self.turns[3]:  # down
            self.y_pos += self.speed

        if self.y_pos < -50:
            self.y_pos = 700
        elif self.y_pos > 700:
            self.y_pos = -47

        return self.x_pos, self.y_pos, self.direction

    def move_inky(self, pac_man_pos, pac_man_direction, scatter_target, blinky_pos):
        # Set target based on mode
        if not self.dead and self.mode == "Chase":
            self.target = [2 * self.target[0] - blinky_pos[0], 2 * self.target[1] - blinky_pos[1]]

        directions = [
            (0, self.x_pos + self.speed, self.y_pos),  # Right
            (1, self.x_pos - self.speed, self.y_pos),  # Left
            (2, self.x_pos, self.y_pos - self.speed),  # Up
            (3, self.x_pos, self.y_pos + self.speed)  # Down
        ]

        # Filter out opposite direction and calculate distances
        opposite_direction = self.opposite_direction(self.direction)
        distances = [
            (d, self.calculate_distance(x, y))
            for d, x, y in directions
            if self.turns[d] and d != opposite_direction
        ]
        if not distances:
            self.direction = opposite_direction

        # Choose the direction with the shortest distance
        if distances:
            best_direction = min(distances, key=lambda x: x[1])[0]
            self.direction = best_direction

        # Move based on the chosen direction
        if self.direction == 0 and self.turns[0]:  # right
            self.x_pos += self.speed
        elif self.direction == 1 and self.turns[1]:  # left
            self.x_pos -= self.speed
        elif self.direction == 2 and self.turns[2]:  # up
            self.y_pos -= self.speed
        elif self.direction == 3 and self.turns[3]:  # down
            self.y_pos += self.speed

        # Handle screen wrap-around
        if self.y_pos < -50:
            self.y_pos = 700
        elif self.y_pos > 700:
            self.y_pos = -47

        return self.x_pos, self.y_pos, self.direction

    def move_clyde(self, pac_man_pos, pac_man_direction, scatter_target, scatter_time):
        # Check if the ghost is close to the player
        # self.target=pac_man_pos
        scatter_time += 1
        distance_to_player = self.calculate_distance(self.x_pos, self.y_pos)
        if not self.dead:
            if distance_to_player < 100:  # Adjust the distance threshold as needed
                self.mode = "Scatter"
                scatter_time = 0  # Reset scatter_mode_timer when switching to Scatter mode
                self.target = scatter_target
            elif distance_to_player > 100 and scatter_time > 600:  # Adjust the scatter duration as needed
                self.mode = "Chase"
                self.target = pac_man_pos

        # Calculate distances for each possible direction
        directions = [
            (0, self.x_pos + self.speed, self.y_pos),  # Right
            (1, self.x_pos - self.speed, self.y_pos),  # Left
            (2, self.x_pos, self.y_pos - self.speed),  # Up
            (3, self.x_pos, self.y_pos + self.speed)  # Down
        ]

        distances = [(d, self.calculate_distance(x, y)) for d, x, y in directions if self.turns[d]]

        # Exclude the opposite direction unless it's the only option
        opposite_direction = self.opposite_direction(self.direction)
        if len(distances) > 1:
            distances = [dist for dist in distances if dist[0] != opposite_direction]

        # Choose the direction with the shortest distance
        if distances:
            # If multiple directions have the same shortest distance, choose based on preference order
            best_direction = min(distances, key=lambda x: (x[1], x[0]))[0]
            self.direction = best_direction

        # Move based on the chosen direction
        if self.direction == 0:  # right
            self.x_pos += self.speed
        elif self.direction == 1:  # left
            self.x_pos -= self.speed
        elif self.direction == 2:  # up
            self.y_pos -= self.speed
        elif self.direction == 3:  # down
            self.y_pos += self.speed

        if self.y_pos < -50:
            self.y_pos = 700
        elif self.y_pos > 700:
            self.y_pos = -47

        return self.x_pos, self.y_pos, self.direction, scatter_time, self.mode
