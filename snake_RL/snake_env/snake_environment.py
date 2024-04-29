import gym
import numpy as np
import pygame
import sys
from gym import spaces, utils
from gym.utils import seeding

# Constants for Pygame
WIDTH, HEIGHT = 480, 480
CELL_SIZE = 20

# Define actions
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3
REPEAT = 4

class Apple:
    def __init__(self, x, y):
        self.x, self.y = x, y

class Snake:
    def __init__(self, length, head_x=2, head_y=0, initial_direction=LEFT, step_size=20):
        self._initial_length = length
        self.length = length
        self.step_size = step_size  # How many cells to move per step
        self.last_direction = self.direction(initial_direction)
        self.reset(head_x, head_y, initial_direction)

    def grow(self):
        self.length += 1
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])

    def slither(self, action):
        new_direction = self.direction(action)
        # Multiply the direction by step size to make bigger steps
        self.x = [self.x[0] + new_direction[0] * self.step_size] + self.x[:-1]
        self.y = [self.y[0] + new_direction[1] * self.step_size] + self.y[:-1]

    def reset(self, head_x, head_y, initial_direction):
        xd, yd = self.direction(initial_direction)
        self.x = [head_x - i * xd * self.step_size for i in range(self.length)]
        self.y = [head_y - i * yd * self.step_size for i in range(self.length)]

    def direction(self, action):
        if action == LEFT:
            return [-1, 0]
        elif action == RIGHT:
            return [1, 0]
        elif action == DOWN:
            return [0, 1]
        elif action == UP:
            return [0, -1]
        return self.last_direction

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(SnakeEnv, self).__init__()
        self.nrow, self.ncol = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.nrow, self.ncol, 3), dtype=np.uint8)

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # Set up game elements
        self.snake = Snake(3)
        self.apple = Apple(WIDTH // 2, HEIGHT // 2)
        self.score = 0  # Initialize score here
        self.reset()

    # def step(self, action):
    #     self.snake.slither(action)
    #     done = self.gameover()
    #     reward = 0

    #     # Check if the snake eats the apple
    #     if (self.snake.x[0], self.snake.y[0]) == (self.apple.x, self.apple.y):
    #         self.snake.grow()
    #         self.move_apple()
    #         self.score += 1  # Update score
    #         reward = 10  # Reward for eating the apple

    #     if done:
    #         reward = -10  # Penalty for losing the game

    #     return self.render(), reward, done, {}
    
    def step(self, action):
        # Execute the action and move the snake
        self.snake.slither(action)
        wall_hit = self.check_wall_hit()
        done = self.gameover()
        reward = 0

        if wall_hit:
            reward = -10  # Penalize for hitting the wall
            # Optionally, reset the snake to the center or a safe position
            self.snake.reset(WIDTH // 2, HEIGHT // 2, self.snake.last_direction)
        elif (self.snake.x[0], self.snake.y[0]) == (self.apple.x, self.apple.y):
            self.snake.grow()
            self.move_apple()
            self.score += 1
            reward = 10  # Reward for eating the apple

        if done and not wall_hit:
            reward = -10  # Penalty for losing the game in other ways (like eating itself)
            done = False  # You can decide if the game should end when hitting itself

        return self.render(), reward, done, {}

    def check_wall_hit(self):
        head_x, head_y = self.snake.x[0], self.snake.y[0]
        return head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT

    def reset(self):
        self.snake.reset(WIDTH // 2, HEIGHT // 2, RIGHT)
        self.apple = Apple(WIDTH // 4, HEIGHT // 4)
        self.score = 0  # Reset score
        return self.render(), {}  # Return observation and empty info dict

    def render(self, mode='human'):
        if mode == 'human':
            self.screen.fill((0, 0, 255))
            for x, y in zip(self.snake.x, self.snake.y):
                pygame.draw.rect(self.screen, (0, 255, 0), (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.apple.x, self.apple.y, CELL_SIZE, CELL_SIZE))
            pygame.display.flip()
            self.clock.tick(10)

    # def gameover(self):
    #     head_x, head_y = self.snake.x[0], self.snake.y[0]
    #     if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
    #         return True
    #     if (head_x, head_y) in list(zip(self.snake.x[1:], self.snake.y[1:])):
    #         return True
    #     return False
    
    def gameover(self):
        head_x, head_y = self.snake.x[0], self.snake.y[0]
        wall_hit = head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT
        self_collision = (head_x, head_y) in list(zip(self.snake.x[1:], self.snake.y[1:]))
        return wall_hit or self_collision


    def move_apple(self):
        import random
        while True:
            self.apple.x = random.randint(0, self.ncol - 1) * CELL_SIZE
            self.apple.y = random.randint(0, self.nrow - 1) * CELL_SIZE
            if (self.apple.x, self.apple.y) not in zip(self.snake.x, self.snake.y):
                break

    def close(self):
        pygame.quit()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]