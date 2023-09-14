import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 910, 608
BORDER_WIDTH = 10  # Width of the white border
BALL_SPEED = 0.8
PADDLE_SPEED = 2
WHITE = (255, 225, 255)
BALL_COLOR = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ping Pong')

# Load and resize the background image
background_image = pygame.image.load(r"C:\Users\naren\Downloads\art-graffiti-wall-table-tennis.jpg")  # Replace with your background image path
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load and resize the ball image
original_ball_image = pygame.image.load(r"C:\Users\naren\Downloads\360_F_268820507_M2KbzMdUaHx1QITt6p1HKvgB1PxXxvQ9-removebg-preview.png")
ball_width, ball_height = original_ball_image.get_width() // 6, original_ball_image.get_height() // 6
ball_image = pygame.transform.scale(original_ball_image, (ball_width, ball_height))

# Load and resize the paddle image
original_paddle_image = pygame.image.load(r"C:\Users\naren\Downloads\ping-pong-paddles-sets-racket-paddle-removebg-preview.png")
paddle_width, paddle_height = original_paddle_image.get_width() // 6, original_paddle_image.get_height() // 6
paddle_image = pygame.transform.scale(original_paddle_image, (paddle_width, paddle_height))

# Ball properties
ball = pygame.Rect(WIDTH // 2 - ball_width // 2, HEIGHT // 2 - ball_height // 2, ball_width, ball_height)
ball_dx = BALL_SPEED
ball_dy = BALL_SPEED
ball_color = BALL_COLOR

# Paddle properties
left_paddle = pygame.Rect(50, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
right_paddle = pygame.Rect(WIDTH - 60, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
paddle_speed = PADDLE_SPEED

# Player scores
left_score = 0
right_score = 0

# AI difficulty (higher values make the AI more challenging)
ai_difficulty = 0.1  # Adjust as needed

# Font for displaying scores
font = pygame.font.Font(None, 36)

# Pause flag
paused = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused  # Toggle pause state when 'P' is pressed
    if not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed

        # Simple AI for the right paddle
        if random.random() < ai_difficulty:
            if ball.centery < right_paddle.centery:
                right_paddle.y -= paddle_speed
            elif ball.centery > right_paddle.centery:
                right_paddle.y += paddle_speed

        # Move the ball
        ball.x += ball_dx
        ball.y += ball_dy

        # Ball collisions
        if ball.top <= BORDER_WIDTH or ball.bottom >= HEIGHT - BORDER_WIDTH:
            ball_dy *= -1
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_dx *= -1
            ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
       # Ball out of bounds
        if ball.left <= BORDER_WIDTH:
            # Right player scores a point
            right_score += 1
            ball.x = WIDTH // 2 - ball_width // 2
            ball.y = HEIGHT // 2 - ball_height // 2
            ball_dx *= -1
            ball_color = BALL_COLOR
        elif ball.right >= WIDTH - BORDER_WIDTH:
            # Left player scores a point
            left_score += 1
            ball.x = WIDTH // 2 - ball_width // 2
            ball.y = HEIGHT // 2 - ball_height // 2
            ball_dx *= -1
            ball_color = BALL_COLOR

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw white borders around the screen
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, BORDER_WIDTH))                           # Top border
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - BORDER_WIDTH, WIDTH, BORDER_WIDTH))     # Bottom border
    pygame.draw.rect(screen, WHITE, (0, 0, BORDER_WIDTH, HEIGHT))                          # Left border
    pygame.draw.rect(screen, WHITE, (WIDTH - BORDER_WIDTH, 0, BORDER_WIDTH, HEIGHT))     # Right border
    # Draw paddles and ball
    screen.blit(paddle_image, left_paddle)
    screen.blit(paddle_image, right_paddle)
    screen.blit(ball_image, ball)

    # Draw the point table
    left_score_text = font.render(f'PLAYER 👨: {left_score}', True, WHITE)
    right_score_text = font.render(f'AI 🤖: {right_score}', True, WHITE)
    screen.blit(left_score_text, (20, 20))
    screen.blit(right_score_text, (WIDTH - right_score_text.get_width() - 20, 20))

    # Draw the pause message
    if paused:
        pause_text = font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

    # Update the display
    pygame.display.update()
