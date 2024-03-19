import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Shooter Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Define player properties
player_width, player_height = 50, 50
player_x, player_y = WIDTH // 2, HEIGHT - player_height - 10
player_speed = 5

# Define enemy properties
enemy_width, enemy_height = 50, 50
enemies = []
enemy_speed = 3
enemy_spawn_rate = 60  # Rate of spawning enemies

# Define bullet properties
bullet_width, bullet_height = 5, 20
bullet_speed = 5
bullets = []

# Define font
font = pygame.font.Font(None, 36)

# Function to draw text on screen
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to display game over screen
def show_game_over():
    screen.fill(BLACK)
    draw_text("GAME OVER", RED, WIDTH // 2 - 100, HEIGHT // 2 - 50)
    draw_text(f"Score: {score}", WHITE, WIDTH // 2 - 50, HEIGHT // 2)
    pygame.display.update()
    pygame.time.delay(2000)  # Delay for 2 seconds before quitting

# Game loop
running = True
clock = pygame.time.Clock()
score = 0
game_over = False
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullets.append(pygame.Rect(player_x + player_width // 2 - bullet_width // 2, player_y - bullet_height, bullet_width, bullet_height))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    if not game_over:
        # Enemy spawning
        if random.randint(0, enemy_spawn_rate) == 0:
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemies.append(pygame.Rect(enemy_x, -enemy_height, enemy_width, enemy_height))

        # Enemy movement and firing
        for enemy in enemies[:]:
            # Move enemy downwards
            enemy.y += enemy_speed

            # Enemy firing
            if random.randint(0, 100) == 0:  # Adjust firing rate as needed
                bullets.append(pygame.Rect(enemy.x + enemy_width // 2 - bullet_width // 2, enemy.y + enemy_height, bullet_width, bullet_height))

            # Remove enemy if it goes past the bottom of the screen
            if enemy.y > HEIGHT + enemy_height:
                enemies.remove(enemy)

        # Bullet movement and collision with enemies
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break
            if bullet.y < 0:
                bullets.remove(bullet)

        # Check for collision with player
        for enemy in enemies:
            if enemy.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                game_over = True
                break

        # Draw player
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, BLUE, bullet)

        # Draw score
        draw_text(f"Score: {score}", BLUE, 10, 10)
    else:
        show_game_over()

    pygame.display.update()
    clock.tick(60)

# Quit Pygame
pygame.quit()
