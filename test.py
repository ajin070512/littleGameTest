import pygame
import random
import sys
import os

# 初始化pygame
pygame.init()


# 游戏窗口设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("方块躲避游戏 - 按ESC退出")

# 颜色定义
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# 玩家方块
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 20
player_speed = 8

# 障碍物
obstacles = []
obstacle_speed = 5
obstacle_frequency = 30  # 控制障碍物生成频率
obstacle_timer = 0

# 分数
score = 0
font = pygame.font.SysFont(None, 36)

# 游戏状态
game_over = False

# 时钟
clock = pygame.time.Clock()
FPS = 60


def create_obstacle():
    """创建新的障碍物"""
    size = random.randint(30, 80)
    x = random.randint(0, WIDTH - size)
    y = -size
    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    return {"rect": pygame.Rect(x, y, size, size), "color": color}


def draw_player():
    """绘制玩家方块"""
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    # 添加高光效果
    pygame.draw.rect(screen, (100, 100, 255), (player_x, player_y, player_size, player_size), 2)


def draw_obstacles():
    """绘制所有障碍物"""
    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle["color"], obstacle["rect"])
        # 添加边框
        pygame.draw.rect(screen, BLACK, obstacle["rect"], 2)


def check_collision():
    """检查碰撞"""
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle["rect"]):
            return True
    return False


def draw_score():
    """绘制分数"""
    score_text = font.render(f"分数: {score}", True, YELLOW)
    screen.blit(score_text, (10, 10))

    # 绘制游戏说明
    if not game_over:
        instruction = font.render("使用 ← → 键移动方块，躲避下落的障碍物", True, GREEN)
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 40))


def draw_game_over():
    """绘制游戏结束画面"""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # 半透明黑色
    screen.blit(overlay, (0, 0))

    game_over_text = font.render("游戏结束!", True, RED)
    final_score_text = font.render(f"最终分数: {score}", True, YELLOW)
    restart_text = font.render("按R键重新开始", True, GREEN)
    quit_text = font.render("按ESC键退出", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 60))


def reset_game():
    """重置游戏"""
    global player_x, obstacles, score, game_over
    player_x = WIDTH // 2 - player_size // 2
    obstacles.clear()
    score = 0
    game_over = False


# 使项目可以加载中文字体
# 修改字体加载部分
def load_chinese_font(size=36):
    """加载中文字体"""
    # 尝试多种字体
    font_paths = [
        "fonts/simhei.ttf",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "./simhei.ttf"
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                continue

    # 如果找不到，尝试系统字体
    try:
        return pygame.font.SysFont('microsoft yahei', size)
    except:
        return pygame.font.SysFont(None, size)


# 使用中文字体
font = load_chinese_font(36)
small_font = load_chinese_font(24)


# 修改所有文本为中文
def draw_score():
    """绘制分数（中文版）"""
    score_text = font.render(f'分数: {score}', True, (255, 255, 0))
    screen.blit(score_text, (10, 10))

    if not game_over:
        instruction = small_font.render('使用 ← → 键移动方块，躲避下落的障碍物', True, (100, 255, 100))
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 40))


def draw_game_over():
    """绘制游戏结束画面（中文版）"""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    game_over_text = font.render('游戏结束!', True, (255, 100, 100))
    final_score_text = font.render(f'最终分数: {score}', True, (255, 255, 100))
    restart_text = small_font.render('按R键重新开始', True, (100, 255, 100))
    quit_text = small_font.render('按ESC键退出', True, (255, 255, 255))

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 60))
# 字体设置结束


# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and game_over:
                reset_game()

    # 游戏进行中
    if not game_over:
        # 获取按键状态
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        # 生成障碍物
        obstacle_timer += 1
        if obstacle_timer >= obstacle_frequency:
            obstacles.append(create_obstacle())
            obstacle_timer = 0
            # 随着分数增加，加快障碍物生成速度
            if obstacle_frequency > 15:
                obstacle_frequency = 30 - (score // 10)

        # 移动障碍物
        for obstacle in obstacles[:]:
            obstacle["rect"].y += obstacle_speed

            # 移除屏幕外的障碍物，增加分数
            if obstacle["rect"].y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

        # 增加障碍物速度随着分数提高
        obstacle_speed = 5 + score // 50

        # 检查碰撞
        if check_collision():
            game_over = True

    # 绘制背景
    screen.fill((20, 20, 30))  # 深蓝色背景
    # 添加星空效果
    for _ in range(5):
        pygame.draw.circle(screen, (100, 100, 150),
                           (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                           random.randint(1, 3))

    # 绘制游戏元素
    draw_player()
    draw_obstacles()
    draw_score()

    # 如果游戏结束，显示结束画面
    if game_over:
        draw_game_over()

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(FPS)

# 退出游戏
pygame.quit()
sys.exit()