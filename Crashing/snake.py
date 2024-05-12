import pygame
import random
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

# Clock
clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)
            
def random_food_position():
    return (random.randint(0, GRID_WIDTH - 1) * CELL_SIZE, random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE)

def game_loop():
    # Initial snake and food positions
    snake_pos = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2, HEIGHT // 2 + CELL_SIZE), (WIDTH // 2, HEIGHT // 2 + 2*CELL_SIZE)]
    food_pos = random_food_position()
    direction = 'STOP'
    score = 0
    font = pygame.font.Font(None, 36)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

        # Move the snake
        if direction != 'STOP':
            head_x, head_y = snake_pos[0]
            if direction == 'UP':
                head_y -= CELL_SIZE
            elif direction == 'DOWN':
                head_y += CELL_SIZE
            elif direction == 'LEFT':
                head_x -= CELL_SIZE
            elif direction == 'RIGHT':
                head_x += CELL_SIZE
            new_head_pos = (head_x, head_y)
            snake_pos.insert(0, new_head_pos)

            # Check if snake eats food
            if snake_pos[0] == food_pos:
                food_pos = random_food_position()
                score += 1  # Increase score when the snake eats food
            else:
                snake_pos.pop()

            # Check for collisions
            if (snake_pos[0] in snake_pos[1:] or
                head_x < 0 or head_x >= WIDTH or
                head_y < 0 or head_y >= HEIGHT):
                display_game_over(screen, score)
                direction = 'STOP'  # Stop movement after collision
                snake_pos = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2, HEIGHT // 2 + CELL_SIZE), (WIDTH // 2, HEIGHT // 2 + 2*CELL_SIZE)]
                food_pos = random_food_position()
                score = 0  # Reset score for the new game

        # Drawing
        screen.fill((0, 0, 0))
        # draw_grid()
        
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

        # Display score
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, [0, 0])

        pygame.display.update()
        clock.tick(10)

def display_game_over(screen, score):
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("Game Over! Score: " + str(score), True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(200)

if __name__ == "__main__":
    while True:
        game_loop()
