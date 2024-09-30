import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
FONT = pygame.font.Font(None, 36)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        
    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        if keys[pygame.K_UP]:
            self.rect.bottom -= 5
        if keys[pygame.K_DOWN]:
            self.rect.bottom += 5
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 5)
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = random.randint(1000, 3000)  # Delay between enemy shots

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 5)

        # Enemy shooting
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot_bullets()

    def shoot_bullets(self):
        """Enemies shoot bullets in multiple directions."""
        num_bullets = 3  # Number of bullets per wave
        for i in range(num_bullets):
            angle = i * (360 / num_bullets)
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)

# Bullet class for the player
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Enemy bullet class (for bullet hell)
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 3
        # Convert angle to radians
        self.angle_rad = math.radians(angle)
        self.dx = math.cos(self.angle_rad) * self.speed
        self.dy = math.sin(self.angle_rad) * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.kill()

# Initialize the game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arcade Shooter with Bullet Hell")

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

def reset_game():
    """Reset the game to its initial state."""
    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    enemy_bullets.empty()
    
    # Create player
    player = Player()
    all_sprites.add(player)
    
    # Create enemies
    for i in range(3):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    return player

player = reset_game()

# Game loop
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_over = False
            player = reset_game()
    
    if not game_over:
        # Update
        player.shoot()
        all_sprites.update()

        # Check for player bullet collisions with enemies
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Check for enemy bullet collisions with the player
        if pygame.sprite.spritecollideany(player, enemy_bullets):
            game_over = True

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    if game_over:
        game_over_text = FONT.render("Game Over! Press SPACE to restart.", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

pygame.quit()