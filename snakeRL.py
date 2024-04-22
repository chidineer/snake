import pygame
import random
import numpy as np
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 480, 480
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()


def random_food_position():
    return (random.randint(0, GRID_WIDTH - 1) * CELL_SIZE, random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE)


class SnakeGameRL:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake_pos = [(WIDTH // 2, HEIGHT // 2)]
        self.food_pos = random_food_position()
        self.direction = 'STOP'
        self.score = 0
        self.game_over = False
        return self.get_state()

    def get_state(self):
        """ Return the state of the game as needed for RL input."""
        # Create a state representation, e.g., position of snake, food, and direction
        head_x, head_y = self.snake_pos[0]
        food_x, food_y = self.food_pos
        direction_vec = np.array([head_x, head_y, food_x, food_y])
        return np.concatenate((direction_vec, np.array(self.snake_pos).flatten()))

    def step(self, action):
        # Mapping action to direction
        action_map = {
            0: 'UP',
            1: 'DOWN',
            2: 'LEFT',
            3: 'RIGHT'
        }
        self.direction = action_map[action]

        # Move snake
        if self.direction != 'STOP':
            x, y = self.snake_pos[0]
            if self.direction == 'UP':
                y -= CELL_SIZE
            elif self.direction == 'DOWN':
                y += CELL_SIZE
            elif self.direction == 'LEFT':
                x -= CELL_SIZE
            elif self.direction == 'RIGHT':
                x += CELL_SIZE
            self.snake_pos.insert(0, (x, y))

        # Check collision with food
        if self.snake_pos[0] == self.food_pos:
            self.score += 1
            self.food_pos = random_food_position()
            reward = 10
        else:
            self.snake_pos.pop()
            reward = -1

        # Check game over conditions
        if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or self.snake_pos[0] in self.snake_pos[1:]):
            self.game_over = True
            reward = -100

        return self.get_state(), reward, self.game_over, {}

    def render(self, mode='human'):
        if mode == 'human':
            screen.fill(WHITE)
            for pos in self.snake_pos:
                pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, RED, pygame.Rect(self.food_pos[0], self.food_pos[1], CELL_SIZE, CELL_SIZE))
            pygame.display.flip()
            clock.tick(5)


# Example of how to use this environment
if __name__ == "__main__":
    game = SnakeGameRL()

    while not game.game_over:
        action = np.random.choice([0, 1, 2, 3])  # Replace this with your RL model's action
        state, reward, game_over, _ = game.step(action)
        game.render()
