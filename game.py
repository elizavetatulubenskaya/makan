print()
import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-понг с радугой и взрывами")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Настройки ракетки
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

# Настройки мяча
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Создание объектов
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Счёт
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 74)

# Класс для эффектов взрывов
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = []
        self.create_particles()
        self.lifetime = 30

    def create_particles(self):
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            color = (
                random.randint(150, 255),
                random.randint(150, 255),
                random.randint(150, 255)
            )
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'color': color,
                'size': random.uniform(2, 5)
            })

    def update(self):
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['size'] -= 0.1
        self.lifetime -= 1

    def draw(self, surface):
        for p in self.particles:
            if p['size'] > 0:
                pygame.draw.circle(surface, p['color'], (int(p['x']), int(p['y'])), p['size'])

# Список взрывов
explosions = []

# Функция для отрисовки радужного фона
def draw_rainbow_background():
    for i in range(HEIGHT):
        # Расчёт цвета радуги
        r = int(255 * (1 + math.sin(i * 0.05)) / 2)
        g = int(255 * (1 + math.sin(i * 0.05 + 2)) / 2)
        b = int(255 * (1 + math.sin(i * 0.05 + 4)) / 2)
        color = (r, g, b)
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

# Основной игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление ракетками
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED

    # Простое ИИ управление для противника
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += PADDLE_SPEED - 1
    else:
        opponent_paddle.y -= PADDLE_SPEED - 1

    # Движение мяча
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Отскок от стен
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y *= -1
        # Создаём взрыв при отскоке от стены
        explosions.append(Explosion(ball.centerx, ball.centery))

    # Отскок от ракеток
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        BALL_SPEED_X *= -1
        # Создаём взрыв при столкновении с ракеткой
        explosions.append(Explosion(ball.centerx, ball.centery))

    # Проверка счёта
    if ball.left <= 0:
        opponent_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        BALL_SPEED_X *= -1
        explosions.append(Explosion(WIDTH // 4, HEIGHT // 2))
    elif ball.right >= WIDTH:
        player_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        BALL_SPEED_X *= -1
        explosions.append(Explosion(3 * WIDTH // 4, HEIGHT // 2))

    # Обновление взрывов
    for explosion in explosions[:]:
        explosion.update()
        if explosion.lifetime <= 0:
            explosions.remove(explosion)

    # Отрисовка
    draw_rainbow_background()  # Радужный фон

    # Отрисовка объектов
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Отрисовка взрывов
    for explosion in explosions:
        explosion.draw(screen)

    # Отрисовка счёта
    player_text = font.render(str(player_score), True, WHITE)
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(player_text, (WIDTH // 4, 20))
    screen.blit(opponent_text, (3 * WIDTH // 4, 20))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()