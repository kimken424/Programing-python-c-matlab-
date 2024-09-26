import pygame
import time
import random

# 게임 기본 설정
pygame.init()

# 색상 설정
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# 화면 크기 설정
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# 게임 화면 생성
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# 스네이크 속도와 크기 설정
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# 폰트 설정
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# 점수 표시 함수
def display_score(score):
    value = score_font.render(f"Score: {score}", True, YELLOW)
    screen.blit(value, [0, 0])

# 뱀 그리기 함수
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

# 메시지 표시 함수
def display_message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])

# 게임 메인 루프
def gameLoop():
    game_over = False
    game_close = False

    # 스네이크 시작 위치
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    # 스네이크 이동 방향
    x_change = 0
    y_change = 0

    # 스네이크 몸통을 리스트로 관리
    snake_list = []
    length_of_snake = 1

    # 음식 위치 설정
    food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    clock = pygame.time.Clock()

    while not game_over:

        # 게임 오버 시 다시 시작 또는 종료 옵션
        while game_close:
            screen.fill(BLUE)
            display_message("You Lost! Press Q-Quit or C-Play Again", RED)
            display_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # 키보드 입력 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -SNAKE_BLOCK
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = SNAKE_BLOCK
                    x_change = 0

        # 화면 경계에 닿으면 게임 종료
        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            game_close = True
        x += x_change
        y += y_change
        screen.fill(BLACK)

        # 음식 그리기
        pygame.draw.rect(screen, BLUE, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        # 스네이크 위치 업데이트
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # 스네이크가 자기 몸에 닿으면 게임 종료
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(SNAKE_BLOCK, snake_list)
        display_score(length_of_snake - 1)

        pygame.display.update()

        # 스네이크가 음식을 먹으면 길이 증가
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()

gameLoop()
