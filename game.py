import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football Game")

# Colors
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game objects
ball = pygame.Rect(WIDTH//2 - 10, HEIGHT//2 - 10, 20, 20)
player1 = pygame.Rect(200, HEIGHT//2 - 20, 20, 40)
player2 = pygame.Rect(800, HEIGHT//2 - 20, 20, 40)

goal1 = pygame.Rect(50, HEIGHT//2 - 50, 10, 100)
goal2 = pygame.Rect(WIDTH - 60, HEIGHT//2 - 50, 10, 100)

# Game variables
ball_speed = [random.choice([-3, 3]), random.choice([-3, 3])]
player_speed = 5
score1, score2 = 0, 0
running = True
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()  # Start timer
time_limit = 30  # Time limit in seconds

# Game loop
while running:
    screen.fill(GREEN)  # Football field background

    # Draw field lines
    pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 5)
    pygame.draw.rect(screen, WHITE, (50, 50, WIDTH-100, HEIGHT-100), 5)

    # Draw players, ball, and goalposts
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.rect(screen, BLUE, player1)
    pygame.draw.rect(screen, RED, player2)
    pygame.draw.rect(screen, BLACK, goal1)
    pygame.draw.rect(screen, BLACK, goal2)

    # Move ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with walls (excluding goal posts)
    if ball.top <= 50 or ball.bottom >= HEIGHT - 50:
        ball_speed[1] = -ball_speed[1]
    if ball.left <= 50 or ball.right >= WIDTH - 50:
        ball_speed[0] = -ball_speed[0]

    # Ball collision with players
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed[0] = -ball_speed[0]

    # Ball goal detection
    if ball.colliderect(goal1):
        score2 += 1
        ball.x, ball.y = WIDTH//2, HEIGHT//2
    elif ball.colliderect(goal2):
        score1 += 1
        ball.x, ball.y = WIDTH//2, HEIGHT//2

    # Player movement (Keyboard Control)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 50:
        player1.y -= player_speed
    if keys[pygame.K_s] and player1.bottom < HEIGHT - 50:
        player1.y += player_speed
    if keys[pygame.K_UP] and player2.top > 50:
        player2.y -= player_speed
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT - 50:
        player2.y += player_speed

    # Display score
    font = pygame.font.Font(None, 48)
    score1_text = font.render(f"Team 1: {score1}", True, WHITE)
    score2_text = font.render(f"Team 2: {score2}", True, WHITE)
    screen.blit(score1_text, (WIDTH//4 - score1_text.get_width()//2, 10))
    screen.blit(score2_text, (3*WIDTH//4 - score2_text.get_width()//2, 10))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check time limit
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    if elapsed_time >= time_limit:
        running = False

    pygame.display.flip()
    clock.tick(30)  # Limit FPS

# Announce the winner
screen.fill(GREEN)
font = pygame.font.Font(None, 72)
if score1 > score2:
    winner_text = font.render("Team 1 Wins!", True, WHITE)
elif score2 > score1:
    winner_text = font.render("Team 2 Wins!", True, WHITE)
else:
    winner_text = font.render("It's a Draw!", True, WHITE)
screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - winner_text.get_height()//2))
pygame.display.flip()
pygame.time.wait(5000)  # Display the winner for 5 seconds

pygame.quit()
