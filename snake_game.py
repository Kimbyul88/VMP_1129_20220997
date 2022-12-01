import pygame
import os
import sys
import random
import time
# from time import sleeppyto
# 게임 스크린 전역변수
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700

# 게임 화면 전역변수
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

# 방향 전역변수
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 색상 전역변수
# WHITE = (255, 255, 255)
WHITE = (255, 0, 80) # 색깔 바꾸기
ORANGE = (250, 150, 0) # 먹이 색깔
YELLOW = (0, 255, 255) # 먹이2
GRAY = (0, 100, 0)

# assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')


# 키보드 이미지 초기 설정
keyboard_image = pygame.image.load(os.path.join(assets_path, 'keyboard.png'))
keyboard_x = int(SCREEN_WIDTH / 2)
keyboard_y = int(SCREEN_HEIGHT / 2)
keyboard_dx = 0
keyboard_dy = 0

# 뱀 객체
class Snake(object):
    def __init__(self):
        self.create()

    # 뱀 생성
    def create(self):
        self.length = 2
        self.positions = [(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    # 뱀 방향 조정
    def control(self, xy):
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        else:
            self.direction = xy

    # 뱀 이동
    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (cur[0] + (x * GRID_SIZE)), (cur[1] + (y * GRID_SIZE))

        # 뱀이 자기 몸통에 닿았을 경우 뱀 처음부터 다시 생성
        if new in self.positions[2:]:
            time.sleep(1)
            self.create()
        # 뱀이 게임화면을 넘어갈 경우 뱀 처음부터 다시 생성
        elif new[0] < 0 or new[0] >= SCREEN_WIDTH or \
                new[1] < 0 or new[1] >= SCREEN_HEIGHT:
            time.sleep(1)
            self.create()
        # 뱀이 정상적으로 이동하는 경우
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    # 뱀이 먹이를 먹을 때 호출
    def eat(self):
        self.length += 1

    # 뱀 그리기
    def draw(self, screen):
        red, green, blue = 50 / (self.length - 1), 150, 150 / (self.length - 1)
        for i, p in enumerate(self.positions):
            color = (100 + red * i, green, blue * i)
            rect = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, color, rect)


# 먹이 객체
class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = ORANGE
        self.color2 = YELLOW
        self.create()

    # 먹이 생성
    def create(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        self.position = x * GRID_SIZE, y * GRID_SIZE

    # 먹이 그리기
    def draw(self, screen):
        rect = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, self.color2, rect)     

class Obstacle(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (0, 0, 0)
        self.create()

    # 장애물 생성
    def create(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        self.position = x * GRID_SIZE, y * GRID_SIZE

    # 장애물 그리기
    def draw(self, screen):
        rect = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)       


# 게임 객체
class Game(object):
    def __init__(self):
        self.snake = Snake()
        self.feed = Feed()
        self.speed = 20

    # 게임 이벤트 처리 및 조작
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.control(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.control(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.control(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.control(RIGHT)
        return False

    # 게임 로직 수행
    def run_logic(self):
        self.snake.move()
        self.check_eat(self.snake, self.feed)
        self.speed = (20 + self.snake.length) / 4

    # 뱀이 먹이를 먹었는지 체크
    def check_eat(self, snake, feed):
        if snake.positions[0] == feed.position:
            snake.eat()
            feed.create()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(assets_path, relative_path)

    # 게임 정보 출력
    def draw_info(self, length, speed, screen):
        info = "Length: " + str(length) + "    " + "Speed: " + str(round(speed, 2))
        font_path = resource_path("NanumGothicCoding-Bold.ttf")
        font = pygame.font.Font(font_path, 26)
        text_obj = font.render(info, 1, GRAY)
        text_rect = text_obj.get_rect()
        text_rect.x, text_rect.y = 10, 10
        screen.blit(text_obj, text_rect)

    # 게임 프레임 처리
    def display_frame(self, screen):
        # screen.fill(WHITE)
        self.draw_info(self.snake.length, self.speed, screen)
        self.snake.draw(screen)
        self.feed.draw(screen)
        self.feed.draw(screen)# 먹이2 그리기
        screen.blit(screen, (0, 0))

# 리소스 경로 설정
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(assets_path, relative_path)


def main():
    # 게임 초기화 및 환경 설정
    pygame.init()
    pygame.display.set_caption('Snake Game')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    # 배경 음악 로드
    pygame.mixer.music.load(os.path.join(assets_path, 'bgm.wav'))
    pygame.mixer.music.play(-1) # 무한 반복 재생
    # 효과음 로드
    sound = pygame.mixer.Sound(os.path.join(assets_path, 'sound.wav'))
    #
    # 배경 이미지 로드
    background_image = pygame.image.load(os.path.join(assets_path, 'dungeon.jpg'))
    #
    # 이미지 로드
    mushroom_image_1 = pygame.image.load(os.path.join(assets_path, 'mushroom1.png'))
    mushroom_image_2 = pygame.image.load(os.path.join(assets_path, 'mushroom2.png'))
    mushroom_image_3 = pygame.image.load(os.path.join(assets_path, 'mushroom3.png'))
    done = False

    while not done: #True
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        pygame.display.flip()
        
        # 이벤트 반복 구간
        for event in pygame.event.get():
            global keyboard_dx
            global keyboard_dy

            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                sound.play()    # 효과음 재생
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    keyboard_dx = -3
                elif event.key == pygame.K_RIGHT:
                    keyboard_dx = 3
                elif event.key == pygame.K_UP:
                    keyboard_dy = -3
                elif event.key == pygame.K_DOWN:
                    keyboard_dy = 3
                # 키가 놓일 경우
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    keyboard_dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    keyboard_dy = 0
        # 게임 로직 구간
        # 키보드 이미지의 위치 변경
        global keyboard_x
        global keyboard_y

        keyboard_x += keyboard_dx
        keyboard_y += keyboard_dy

        screen.fill((160, 120, 40))

        # 화면 그리기 구간
        # 베경 이미지 그리기
        screen.blit(background_image, background_image.get_rect())
        # 버섯 이미지 그리기
        # screen.blit(mushroom_image_1, [100, 80])
        screen.blit(mushroom_image_2, [300, 100])
        screen.blit(mushroom_image_3, [500, 500])
        # 화면 그리기 구간
        # 키보드 이미지 그리기
        screen.blit(keyboard_image, [keyboard_x, keyboard_y])

        # 화면 업데이트
        # pygame.display.flip()
        #초당 60 프레임으로 업데이트
        clock.tick(5)

    pygame.quit()


if __name__ == '__main__':
    main()
