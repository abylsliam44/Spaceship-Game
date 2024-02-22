import pygame
import random

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship")


enemy_bullet_img = pygame.image.load('C:\\Users\\Huaweu\\Downloads\\pngegg (8).png').convert_alpha()
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (64, 64))


# Загрузка музыки и звуковых эффектов
pygame.mixer.music.load('C:\\Users\\Huaweu\\Downloads\\InSaid - ALAs_mals.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

collect_star_sound = pygame.mixer.Sound('C:\\Users\\Huaweu\\Downloads\\stopka-monet-30616.wav')
collect_star_sound.set_volume(1.0)

collect_shoot_bonus_sound = pygame.mixer.Sound('C:\\Users\\Huaweu\\Downloads\\super-sovremennoe-lazernoe-orujie.wav')
collect_shoot_bonus_sound.set_volume(1.5)

collect_bonus_sound = pygame.mixer.Sound('C:\\Users\\Huaweu\\Downloads\\game-bonus-french_zkfnabeu.wav')
collect_bonus_sound.set_volume(1.0)

shoot_sound = pygame.mixer.Sound('C:\\Users\\Huaweu\\Downloads\\29daebb84e02fe2.wav')
shoot_sound.set_volume(1.0)

enemy_shoot_sound = pygame.mixer.Sound('C:\\Users\\Huaweu\\Downloads\\orujie-lazer.wav')
enemy_shoot_sound.set_volume(1.2)

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Загрузка шрифтов
menu_font = pygame.font.Font(None, 36)  # Для меню используем шрифт по умолчанию
counter_font = pygame.font.Font('C:\\Users\\Huaweu\\Downloads\\rubbed-normal2.ttf', 36)  # Для счетчиков используем новый шрифт

# Определение изображений и начальных позиций
player_img = pygame.image.load('C:\\Users\\Huaweu\\Downloads\\pngwing.com (1).png')
player_img = pygame.transform.scale(player_img, (64, 64))
player_x = 370
player_y = 480
player_x_change = 0
player_speed = 5

star_img = pygame.image.load('C:\\Users\\Huaweu\\Downloads\\pngegg (1).png')
star_img = pygame.transform.scale(star_img, (64, 64))
star_x = random.randint(0, 735)
star_y = random.randint(50, 150)
star_y_change = 2

obstacle_img = pygame.image.load('C:\\Users\\Huaweu\\Downloads\\pngegg.png')
obstacle_img = pygame.transform.scale(obstacle_img, (64, 64))

enemy_img = pygame.image.load('C:\\Users\\Huaweu\\Downloads\\pngegg (5).png')
enemy_img = pygame.transform.scale(enemy_img, (64, 64))

background_image = pygame.image.load('C:\\Users\\Huaweu\\Downloads\\120684685_auto_600_jpg_5_100.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Параметры препятствий
num_obstacles = 5
obstacle_speed_increase = 4
obstacles = [{
    'x': random.randint(0, SCREEN_WIDTH - 64),
    'y': random.randint(-150, -50),
    'y_change': 0.5 + random.random() * obstacle_speed_increase
} for _ in range(num_obstacles)]

# Параметры вражеских кораблей
num_enemies = 3
enemy_speed = 1.3
enemies = [{
    'x': random.randint(0, SCREEN_WIDTH - 64),
    'y': random.randint(-300, -50),
    'y_change': enemy_speed,
    'cooldown': random.randint(50, 200)
} for _ in range(num_enemies)]

enemy_bullets = []

# Параметры игры
score = 0
health = 3
game_over = False
end_time = pygame.time.get_ticks() + 120000

immortality_timer = 0
bonus_active = False
bonus_img = pygame.image.load('C:\\Users\\Huaweu\\Downloads\\pngegg (2).png').convert_alpha()
bonus_img = pygame.transform.scale(bonus_img, (64, 64))
bonus_x = random.randint(0, SCREEN_WIDTH - 64)
bonus_y = random.randint(-150, -50)
bonus_y_change = 2

shoot_bonus_active = False
shoot_bonus_img = pygame.image.load('C:\\Users\\Huaweu\\Downloads\\pngegg (4).png').convert_alpha()
shoot_bonus_img = pygame.transform.scale(shoot_bonus_img, (64, 64))
shoot_bonus_x = random.randint(0, SCREEN_WIDTH - 64)
shoot_bonus_y = random.randint(-150, -50)
shoot_bonus_y_change = 2
shoot_bonus_timer = 0

bullets = []
obstacles_destroyed = 0

# Функция отрисовки игрока
def draw_player(x, y):
    screen.blit(player_img, (x, y))

# Функция отрисовки бонуса
def draw_bonus(x, y):
    screen.blit(bonus_img, (x, y))

# Функция отрисовки бонуса стрельбы
def draw_shoot_bonus(x, y):
    screen.blit(shoot_bonus_img, (x, y))

# Функция отрисовки вражеского корабля
def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))


# Начать игру
def play_game():
    global game_over, score, health, obstacles, obstacles_destroyed
    game_over = False
    score = 0
    health = 3
    obstacles_destroyed = 0
    obstacles = [{
        'x': random.randint(0, SCREEN_WIDTH - 64),
        'y': random.randint(-150, -50),
        'y_change': 1 + random.random() * obstacle_speed_increase
    } for _ in range(num_obstacles)]

# Показать настройки
def show_settings():
    print("Settings selected")

# Выйти из игры
def quit_game():
    pygame.quit()
    exit()


# Отрисовка звезды
def star(x, y):
    screen.blit(star_img, (x, y))

# Отрисовка препятствия
def obstacle(x, y):
    screen.blit(obstacle_img, (x, y))

# Проверка на столкновение объектов
def is_collision(obj_x, obj_y, player_x, player_y):
    distance = ((obj_x - player_x)**2 + (obj_y - player_y)**2)**0.5
    return distance < 50

# Показ сообщения о здоровье
def show_health_message(screen, health):
    if health > 0:
        health_font = pygame.font.Font(None, 36)
        health_message = health_font.render(f"You Have {health} Lives Left", True, WHITE)
        screen.blit(health_message, (SCREEN_WIDTH // 2 - health_message.get_width() // 2, SCREEN_HEIGHT // 2 - health_message.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)

# Обновление сложности игры
def update_difficulty(score):
    global obstacle_speed_increase
    for obstacle in obstacles:
        if score < 2:
            obstacle['y_change'] = 0.1
        elif score < 4:
            obstacle['y_change'] = 0.4
        elif score < 6:
            obstacle['y_change'] = 0.6
        else:
            obstacle['y_change'] = 0.8 + random.random() * obstacle_speed_increase

# Отображение главного меню
def show_menu():
    menu_background_image = pygame.image.load('C:\\Users\\Huaweu\\Downloads\\177_2.png')
    menu_background_image = pygame.transform.scale(menu_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(menu_background_image, (0, 0))

    menu_title = menu_font.render("Spaceship vs Villains", True, WHITE)
    screen.blit(menu_title, (SCREEN_WIDTH // 2 - menu_title.get_width() // 2, 50))

    rules_text = [
        "The Rules of the GAME:",
        "1. Control the ship with the arrows",
        "2. Collect stars to score points",
        "3. Avoid collisions with obstacles",
        "4. Your health is displayed in the upper right corner",
        "5. Replenish your health by collecting bonus items",
        "6. When you score enough points, the game becomes more difficult"
    ]
    y_offset = 200
    for text in rules_text:
        rule = menu_font.render(text, True, WHITE)
        screen.blit(rule, (SCREEN_WIDTH // 2 - rule.get_width() // 2, y_offset))
        y_offset += 40

    press_any_key = menu_font.render("Press any button to start", True, WHITE)
    screen.blit(press_any_key, (SCREEN_WIDTH // 2 - press_any_key.get_width() // 2, SCREEN_HEIGHT - 100))

    pygame.display.update()
    wait_for_key()

# Ожидание нажатия клавиши
def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Показ главного меню
show_menu()

running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_SPACE and shoot_bonus_active:
                shoot_sound.play()
                bullets.append({'x': player_x + 32, 'y': player_y})

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_x_change = 0

    player_x += player_x_change
    player_x = max(0, min(player_x, SCREEN_WIDTH - 64))

    if star_y > SCREEN_HEIGHT:
        star_y = 0
        star_x = random.randint(0, 735)
    star_y += star_y_change
    if star_y > SCREEN_HEIGHT:
        game_over = True

    for obstacle in obstacles:
        obstacle['y'] += obstacle['y_change']
        if obstacle['y'] > SCREEN_HEIGHT:
            obstacle['y'] = random.randint(-150, -50)
            obstacle['x'] = random.randint(0, SCREEN_WIDTH - 64)
        screen.blit(obstacle_img, (obstacle['x'], obstacle['y']))

    if score >= 5:
        for enemy in enemies:
            enemy['y'] += enemy['y_change']
            if enemy['y'] > SCREEN_HEIGHT:
                enemy['y'] = random.randint(-300, -50)
                enemy['x'] = random.randint(0, SCREEN_WIDTH - 64)
                enemy['cooldown'] = random.randint(50, 200)
            if enemy['cooldown'] == 0:
                enemy_shoot_sound.play()
                enemy_bullets.append({'x': enemy['x'] + 32, 'y': enemy['y'] + 64})
                enemy['cooldown'] = random.randint(50, 200)
            else:
                enemy['cooldown'] -= 1
            screen.blit(enemy_img, (enemy['x'], enemy['y']))
    else:
        for enemy in enemies:
            screen.blit(enemy_img, (enemy['x'], enemy['y']))

    if is_collision(star_x, star_y, player_x, player_y):
        score += 1
        collect_star_sound.play()
        star_y = 0
        star_x = random.randint(0, 735)

    for obstacle in obstacles:
        if is_collision(obstacle['x'], obstacle['y'], player_x, player_y):
            if not bonus_active:
                health -= 1
                obstacle['y'] = random.randint(-150, -50)
                obstacle['x'] = random.randint(0, SCREEN_WIDTH - 64)
                show_health_message(screen, health)
                if health <= 0:
                    game_over = True
                    break

    for enemy in enemies:
        if is_collision(enemy['x'], enemy['y'], player_x, player_y):
            if not bonus_active:
                health -= 1
                enemy['y'] = random.randint(-300, -50)
                enemy['x'] = random.randint(0, SCREEN_WIDTH - 64)
                show_health_message(screen, health)
                if health <= 0:
                    game_over = True
                    break

    if is_collision(bonus_x, bonus_y, player_x, player_y):
        collect_bonus_sound.play()
        bonus_active = True
        immortality_timer = pygame.time.get_ticks() + 10000
        bonus_x = random.randint(0, SCREEN_WIDTH - 64)
        bonus_y = random.randint(-150, -50)

    if is_collision(shoot_bonus_x, shoot_bonus_y, player_x, player_y):
        collect_shoot_bonus_sound.play()
        shoot_bonus_active = True
        shoot_bonus_timer = pygame.time.get_ticks() + 10000
        shoot_bonus_x = random.randint(0, SCREEN_WIDTH - 64)
        shoot_bonus_y = random.randint(-150, -50)

    if not bonus_active and not shoot_bonus_active:
        draw_bonus(bonus_x, bonus_y)
        draw_shoot_bonus(shoot_bonus_x, shoot_bonus_y)
        bonus_y += bonus_y_change
        shoot_bonus_y += shoot_bonus_y_change
        if bonus_y > SCREEN_HEIGHT:
            bonus_y = random.randint(-150, -50)
            bonus_x = random.randint(0, SCREEN_WIDTH - 64)
        if shoot_bonus_y > SCREEN_HEIGHT:
            shoot_bonus_y = random.randint(-150, -50)
            shoot_bonus_x = random.randint(0, SCREEN_WIDTH - 64)

    if bonus_active and pygame.time.get_ticks() <= immortality_timer:
        draw_player(player_x, player_y)
    elif shoot_bonus_active and pygame.time.get_ticks() <= shoot_bonus_timer:
        draw_player(player_x, player_y)
    else:
        bonus_active = False
        shoot_bonus_active = False
        draw_player(player_x, player_y)

    if shoot_bonus_active:
        draw_shoot_bonus(shoot_bonus_x, shoot_bonus_y)

    bonus_y += bonus_y_change
    if bonus_y > SCREEN_HEIGHT or bonus_active:
        bonus_y = random.randint(-150, -50)
        bonus_x = random.randint(0, SCREEN_WIDTH - 64)

    star(star_x, star_y)

    for bullet in bullets:
        bullet['y'] -= 5
        pygame.draw.rect(screen, WHITE, (bullet['x'], bullet['y'], 2, 5))
        for obstacle in obstacles:
            if obstacle['y'] < bullet['y'] < obstacle['y'] + 64 and obstacle['x'] < bullet['x'] < obstacle['x'] + 64:
                bullets.remove(bullet)
                obstacle['y'] = random.randint(-150, -50)
                obstacle['x'] = random.randint(0, SCREEN_WIDTH - 64)
                obstacles_destroyed += 1
        for enemy in enemies:
            if enemy['y'] < bullet['y'] < enemy['y'] + 64 and enemy['x'] < bullet['x'] < enemy['x'] + 64:
                bullets.remove(bullet)
