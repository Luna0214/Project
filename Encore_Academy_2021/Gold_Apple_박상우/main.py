import random
import pygame
from pygame import mixer
import time

pygame.mixer.pre_init(44100, -16, 2, 2048) #효과음 초기화
##############################################################
pygame.init() #초기화
screen_size = [600, 800] #가로, 세로 크기
screen = pygame.display.set_mode(screen_size) #스크린 사이즈 설정
pygame.display.set_caption("GOLD Apple Farm") #캡션:게임이름
game_title = pygame.image.load('gametitle.png') #타이틀 화면
in_game_bg = pygame.image.load('ingame_bg.png') #인게임 화면
game_over_bg = pygame.image.load('gameover.png') #종료 화면
font = pygame.font.SysFont(None, 75) #글자입력
clock = pygame.time.Clock() #시간
apples = []

#BGM
mixer.music.load("bgm_likesun.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

#색깔
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Start_button
start_button = pygame.Rect(100, 600, 400, 125)
start_button.center = (300, 650)

#게임이 시작 되었는가?
start = False
#게임 메인 루프
running = True  #프로그램이 실행중인가?

#Score
score_value = 0
font_score = pygame.font.Font(None, 40) #score 폰트, 폰트사이즈

#스테이지
lvl = 1

##############################################################

def check_buttons(pos):
    if start_button.collidepoint(pos):
        global start
        start = True

def game_start_message(msg, color):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, [135, 640])

def show_score(x, y):
    score = font_score.render("SCORE: " + str(score_value).zfill(4), True, WHITE)
    screen.blit(score, [x, y])

def show_clock(x, y):
    time = font_score.render("TIME: " + str(int(show_time)), True, WHITE)
    screen.blit(time, [x, y])

def show_level(x, y):
    stage = font_score.render("STAGE: " + str(int(level)), True, WHITE)
    screen.blit(stage, [x, y])

def game_end_message(msg, color):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, [55, 640])

def high_score_message(msg, color):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, [50, 540])

def high_score_value():
    with open('highest_score.txt', "r") as f:
        return f.read()

def game_over_screen():
    screen.blit(game_over_bg, (0, 0))
    high_score_message('Highest Score: {}'.format(high_score_value()), WHITE)
    game_end_message('Your Score is: {}'.format(score_value), WHITE)
    if int(high_score_value()) < score_value:
        with open('highest_score.txt', "w") as f:
            f.write(str(score_value))

##############################################################

#배경
background1 = pygame.image.load("gametitle.png")
background2 = pygame.image.load("ingame_bg.png")

#지렁이
w_img = pygame.image.load("w_R.png")
w_img = pygame.transform.scale(w_img, (90, 90))
character_size = w_img.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_size[0] / 2) - (character_width / 2)
character_y_pos = screen_size[1] - character_height

# 이동 위치
to_x = 0
character_speed = 10

#사과
a_img = pygame.image.load("Rapple.png")
a_img = pygame.transform.scale(a_img, (70, 70))
bomb_size = a_img.get_rect().size
bomb_width = bomb_size[0]
bomb_height = bomb_size[1]
bomb_x_pos = random.randint(0, screen_size[0] - bomb_width)
bomb_y_pos = 0
bomb_speed = 5

#청사과
g_img = pygame.image.load("Gapple.png")
g_img = pygame.transform.scale(g_img, (100, 100))
bomb2_size = g_img.get_rect().size
bomb2_width = bomb2_size[0]
bomb2_height = bomb2_size[1]
bomb2_x_pos = random.randint(0, screen_size[0] - bomb2_width)
bomb2_y_pos = 0
bomb2_speed = 10

#########################################################################################

while running:
        dt = clock.tick(30)
        screen.blit(game_title, (0, 0))
        pygame.draw.rect(screen, WHITE, [100, 600, 400, 125], 5)
        game_start_message('START GAME', WHITE)
        pygame.display.update()

        # 2. 이벤트 처리 (키보드, 마우스 등)
        for event in pygame.event.get():
            click_pos = None
            if event.type == pygame.QUIT:
                running = False
            # 클릭 입력
            if event.type == pygame.MOUSEBUTTONUP:
                click_pos = pygame.mouse.get_pos()  # 클릭 좌표

            if click_pos:
                check_buttons(click_pos)  # return start = True
                start_time = time.time()
 #################################################################################
                while start:
                    dt = clock.tick(30)
                    show_time = time.time() - start_time
                    background2.blit(in_game_bg, (0, 0))
                    level = lvl + int(show_time)/10
                    bomb_speed += level /100
                    character_speed += level/100
                    score_value += int(show_time)

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                to_x -= character_speed
                                w_img = pygame.image.load('w_L.png')
                                w_img = pygame.transform.scale(w_img, (90, 90))
                            elif event.key == pygame.K_RIGHT:
                                to_x += character_speed
                                w_img = pygame.image.load('w_R.png')
                                w_img = pygame.transform.scale(w_img, (90, 90))

                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                                to_x = 0
                    # 게임 캐릭터 위치 정의
                    character_x_pos += to_x

                    if character_x_pos < 0:
                        character_x_pos = 0
                    elif character_x_pos > screen_size[0] - character_width:
                        character_x_pos = screen_size[0] - character_width

                    #사과 Drop
                    bomb_y_pos += bomb_speed

                    if bomb_y_pos > screen_size[1]:
                        score_value += 100
                        bomb_y_pos = 0
                        bomb_x_pos = random.randint(0, screen_size[0] - bomb_width)

                    #청사과 Drop
                    bomb2_y_pos += bomb2_speed

                    if bomb2_y_pos > screen_size[1]:
                        score_value += 500
                        bomb2_y_pos = 0
                        bomb2_x_pos = random.randint(0, screen_size[0] - bomb2_width)




                    # 충돌 처리
                    character_rect = w_img.get_rect()
                    character_rect.left = character_x_pos
                    character_rect.top = character_y_pos

                    bomb_rect = a_img.get_rect()
                    bomb_rect.left = bomb_x_pos
                    bomb_rect.top = bomb_y_pos

                    bomb2_rect = g_img.get_rect()
                    bomb2_rect.left = bomb2_x_pos
                    bomb2_rect.top = bomb2_y_pos

                    #사과 충돌 결과
                    if character_rect.colliderect(bomb_rect):
                        print("GameOver")
                        game_over_screen()
                        high_score_value()
                        gameover_sound = mixer.Sound('gameover.wav')
                        gameover_sound.set_volume(0.7)
                        gameover_sound.play()
                        pygame.display.update()
                        time.sleep(5)
                        running = False
                        break

                    #청사과 충돌 결과
                    if character_rect.colliderect(bomb2_rect):
                        print("GameOver")
                        game_over_screen()
                        high_score_value()
                        gameover_sound = mixer.Sound('gameover.wav')
                        gameover_sound.set_volume(0.7)
                        gameover_sound.play()
                        pygame.display.update()
                        time.sleep(5)
                        running = False
                        break


                    # 화면에 그리기
                    screen.blit(background2, (0, 0))
                    screen.blit(w_img, (character_x_pos, character_y_pos))
                    screen.blit(a_img, (bomb_x_pos, bomb_y_pos))
                    screen.blit(g_img, (bomb2_x_pos, bomb2_y_pos))
                    show_score(400, 10)
                    show_clock(10, 10)
                    show_level(230, 10)
                    pygame.display.update()


pygame.quit()