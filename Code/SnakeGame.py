import pygame, sys, random, os, json
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# High score ------------------------------------------------------------- #
path = 'data/highscore.txt'
if os.path.exists(path):
    with open(path, 'r+') as rf:
        try:
            data = json.load(rf)
            high_score = data['high_score']
        except json.JSONDecodeError:
            pass
else:
    high_score = 0

def update_highscore(score):
    new_data = {'high_score': score}
    with open(path, 'w+') as wf:
        json.dump(new_data, wf, indent=2)

# Window ----------------------------------------------------------------- #
window_size = (600, 650)
pygame.display.set_caption("Snake")
screen = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_icon(pygame.image.load('data/Images/Snake_end.png'))

# Color ------------------------------------------------------------------ #
white = (255,255,255)
light_grey = (200, 200, 200)
medium_grey = (100, 100, 100)
dark_grey = pygame.Color('grey12')
gold = (255, 219, 77)
red = (255, 128, 128)

# Public SFX ------------------------------------------------------------- #
selection_sfx = pygame.mixer.Sound('data/SFX/selection.wav')
hover_sfx = pygame.mixer.Sound('data/SFX/hover.wav')
hover_sfx.set_volume(0.5)

# Music ------------------------------------------------------------------ #
pygame.mixer.music.load('data/SneakySnake.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.8)
music_state = True

# Functions -------------------------------------------------------------- #
def draw_text(text, font, colour, surface, x, y):
    text_obj = font.render(text, 1, colour)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def hover_animation(list_, rect, speed, speed_limit, width, padding=20):
    if not list_:
        list_.append([pygame.Rect(0, 0, rect.width + padding, rect.height + padding), 0])
        hover_sfx.play()
    else:
        for border in list_:
            border[1] += speed
            if border[1] >= speed_limit:
                border[1] = -speed_limit

            border[0].width += int(border[1])
            border[0].height += int(border[1])
            if border[0].width <= rect.width + padding:
                border[0].width = rect.width + padding
            if border[0].height <= rect.height + padding:
                border[0].height = rect.height + padding

            border[0].center = rect.center

            pygame.draw.rect(screen, white, border[0], width)

def animation_id_generate(list_, path):
    frame_id_list = []
    counter = 1
    for frames in list_:
        for frame in range(frames):
            name = f'{path}{counter}.png'
            frame_id_list.append(name)
        counter += 1
    return frame_id_list

def animation_display(rect, id, scale=None):
    image = pygame.image.load(id)
    if scale:
        width, height = image.get_width(), image.get_height()
        image = pygame.transform.scale(image, (width * scale, height * scale))
        screen.blit(image, rect.topleft)
    else:
        screen.blit(image, rect.topleft)

def diagonal_line(start_pos, end_pos, color, screen, width=1):
    if width // 2:
        for i in range(1, width // 2 + 1):
            pygame.draw.aaline(screen, color, (start_pos[0] - i, start_pos[1]), (end_pos[0], end_pos[1] - i))
            pygame.draw.aaline(screen, color, (start_pos[0], start_pos[1] + i), (end_pos[0] + i, end_pos[1]))

    pygame.draw.aaline(screen, color, start_pos, end_pos)

def music_config(mouse_x, mouse_y, click):
    global music_state
    button = pygame.Rect(550, 600, 40, 40)
    if music_state:
        if button.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, medium_grey, button)
            draw_text('M', pygame.font.Font('data/FFFFORWA.ttf', 20), light_grey, screen, button.centerx, button.centery)
            if click:
                selection_sfx.play()
                pygame.mixer.music.stop()
                music_state = False
        else:
            pygame.draw.rect(screen, white, button)
            draw_text('M', pygame.font.Font('data/FFFFORWA.ttf', 20), medium_grey, screen, button.centerx, button.centery)
    else:
        if button.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, medium_grey, button)
            draw_text('M', pygame.font.Font('data/FFFFORWA.ttf', 20), light_grey, screen, button.centerx, button.centery)
            diagonal_line(button.topright, button.bottomleft, red, screen, 10)
            if click:
                selection_sfx.play()
                pygame.mixer.music.play(-1)
                music_state = True
        else:
            pygame.draw.rect(screen, white, button)
            draw_text('M', pygame.font.Font('data/FFFFORWA.ttf', 20), medium_grey, screen, button.centerx, button.centery)
            diagonal_line(button.topright, button.bottomleft, pygame.Color('red'), screen, 10)

# Main Menu -------------------------------------------------------------- #
class MainMenu:

    font_80 = pygame.font.Font('data/FFFFORWA.ttf', 80)
    font_55 = pygame.font.Font('data/FFFFORWA.ttf', 55)

    # Buttons ------- #
    b_play = pygame.Rect(0, 0, 350, 100)
    b_play.center = (300, 300)

    b_quit = pygame.Rect(0, 0, 350, 100)
    b_quit.center = (300, 450)

    border_list = []

    def __init__(self):
        self.main()

    def events_(self):
        self.click = False
        self.mx, self.my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                update_highscore(high_score)
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

    def main(self):
        global program_mode
        border = []
        while True:

            # Events
            self.events_()

            # Visuals
            screen.fill(dark_grey)
            if self.b_play.collidepoint(self.mx, self.my):
                pygame.draw.rect(screen, medium_grey, self.b_play)
                draw_text("PLAY", self.font_55, gold, screen, 300, 305)
                hover_animation(self.border_list, self.b_play, 0.1, 3, 8)
                if self.click:
                    selection_sfx.play()
                    program_mode = "game"
                    break
            else:
                pygame.draw.rect(screen, white, self.b_play)
                draw_text("PLAY", self.font_55, medium_grey, screen, 300, 305)

            if self.b_quit.collidepoint(self.mx, self.my):
                pygame.draw.rect(screen, medium_grey, self.b_quit)
                draw_text("QUIT", self.font_55, red, screen, 300, 455)
                hover_animation(self.border_list, self.b_quit, 0.1, 3, 8)

                if self.click:
                    selection_sfx.play()
                    update_highscore(high_score)
                    pygame.time.delay(250)
                    pygame.quit()
                    sys.exit()
            else:
                pygame.draw.rect(screen, white, self.b_quit)
                draw_text("QUIT", self.font_55, medium_grey, screen, 300, 455)

            if self.b_play.collidepoint(self.mx, self.my) or self.b_quit.collidepoint(self.mx, self.my):
                pass
            else:
                self.border_list = []
            draw_text("SNAKE", self.font_80, gold, screen, 300, 150)
            music_config(self.mx, self.my, self.click)

            pygame.display.update()
            clock.tick(60)

# Game ------------------------------------------------------------------- #
# SFX
coin_sfx = pygame.mixer.Sound('data/SFX/coin2.wav')
death_sfx = pygame.mixer.Sound('data/SFX/death.wav')
death_sfx.set_volume(0.8)
pause_sfx = pygame.mixer.Sound('data/SFX/pause.wav')
resume_sfx = pygame.mixer.Sound('data/SFX/resume.wav')
powerup_sfx = pygame.mixer.Sound('data/SFX/powerup.wav')
powerup_sfx.set_volume(0.8)
powerup2_sfx = pygame.mixer.Sound('data/SFX/powerup2.wav')

# Grid ------------------------------------------------------------------- #
snake_grid_width = 500
snake_grid_height = snake_grid_width
rows = 20
size_between = snake_grid_width // rows
grid_pos = (50, 50)

def draw_grid(g_width, g_height, rows, color, frame=True, start_pos=(0,0)):
    global screen
    dis_between = g_width // rows
    difference_x = start_pos[0] - 0
    difference_y = start_pos[1] - 0
    g_width += difference_x
    g_height += difference_y

    if frame == True:
        pygame.draw.aaline(screen, color, (start_pos[0], start_pos[1]), (g_width, start_pos[1]))
        pygame.draw.aaline(screen, color, (start_pos[0], g_height), (g_width, g_height))
        pygame.draw.aaline(screen, color, (start_pos[0], start_pos[1]), (start_pos[0], g_height))
        pygame.draw.aaline(screen, color, (g_width, start_pos[1]), (g_width, g_height))

    for i in range(rows-1):
        i += 1
        x = (i * dis_between) + difference_x
        y = (i * dis_between) + difference_y
        pygame.draw.aaline(screen, color, (x, start_pos[1]), (x, g_height))
        pygame.draw.aaline(screen, color, (start_pos[0], y), (g_width, y))

class Cube:

    def __init__(self, size, pos, diff_grid, color):
        self.width = size
        self.height = size
        self.color = color
        self.x = pos[0] * size + diff_grid
        self.y = pos[1] * size + diff_grid
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.movement = None

    def draw_cube(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self):
        if self.movement == "LEFT":
            self.rect.x -= self.width
        if self.movement == "RIGHT":
            self.rect.x += self.width
        if self.movement == "UP":
            self.rect.y -= self.width
        if self.movement == "DOWN":
            self.rect.y += self.width

class Snake:
    body = []
    turns = {}

    snake_head_img = pygame.image.load('data/Images/Snake.png')
    snake_head_img_end = pygame.image.load('data/Images/Snake_end.png')
    snake_body_img = pygame.image.load('data/Images/Body_connect.png')
    snake_body_img_end = pygame.image.load('data/Images/Body_connect_end.png')
    snake_turn_img = pygame.image.load('data/Images/Turn.png')

    def __init__(self, size, pos, diff_grid):
        self.grid_end_pos = [snake_grid_width + diff_grid, snake_grid_height + diff_grid]
        self.size = size
        self.color = white
        self.head = Cube(size, pos, diff_grid, self.color)
        self.body.append(self.head)

    def move_snake(self):
        for number, c in enumerate(self.body):
            p = c.rect.topleft
            if p in self.turns:
                direction = self.turns[p]
                c.movement = direction
                c.move()
                if number == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move()

        for c in self.body:
            if c.rect.left < grid_pos[0]:
                c.rect.right = self.grid_end_pos[0]
            elif c.rect.right > self.grid_end_pos[0]:
                c.rect.left = grid_pos[0]
            if c.rect.top < grid_pos[1]:
                c.rect.bottom = self.grid_end_pos[1]
            elif c.rect.bottom > self.grid_end_pos[1]:
                c.rect.top = grid_pos[1]

    def draw_snake(self):
        for number, c in enumerate(self.body):
            if c == self.head:
                if len(self.body) == 1:
                    if c.movement == "LEFT":
                        screen.blit(pygame.transform.rotate(self.snake_head_img_end, 270), [c.rect.x, c.rect.y])
                    elif c.movement == "RIGHT":
                        screen.blit(pygame.transform.rotate(self.snake_head_img_end, 90), [c.rect.x, c.rect.y])
                    elif c.movement == "UP":
                        screen.blit(pygame.transform.flip(self.snake_head_img_end, False, True), [c.rect.x, c.rect.y])
                    elif c.movement == "DOWN":
                        screen.blit(self.snake_head_img_end, [c.rect.x, c.rect.y])
                    else:
                        screen.blit(self.snake_head_img_end, [c.rect.x, c.rect.y])
                else:
                    if c.movement == "LEFT":
                        screen.blit(pygame.transform.rotate(self.snake_head_img, 270), [c.rect.x, c.rect.y])
                    elif c.movement == "RIGHT":
                        screen.blit(pygame.transform.rotate(self.snake_head_img, 90), [c.rect.x, c.rect.y])
                    elif c.movement == "UP":
                        screen.blit(pygame.transform.flip(self.snake_head_img, False, True), [c.rect.x, c.rect.y])
                    elif c.movement == "DOWN":
                        screen.blit(self.snake_head_img, [c.rect.x, c.rect.y])
                    else:
                        screen.blit(self.snake_head_img, [c.rect.x, c.rect.y])
            else:
                # TURN ---------------------------- #
                snake_turn_image_rotate = None
                if c.rect.topleft in self.turns:
                    moving_dir = self.turns[c.rect.topleft]
                    if number == len(self.body) - 1:
                        if moving_dir == "LEFT":
                            screen.blit(pygame.transform.rotate(self.snake_body_img_end, 270), [c.rect.x, c.rect.y])
                        elif moving_dir == "RIGHT":
                            screen.blit(pygame.transform.rotate(self.snake_body_img_end, 90), [c.rect.x, c.rect.y])
                        elif moving_dir == "UP":
                            screen.blit(pygame.transform.flip(self.snake_body_img_end, False, True), [c.rect.x, c.rect.y])
                        else:
                            screen.blit(self.snake_body_img_end, [c.rect.x, c.rect.y])
                    else:
                        if moving_dir == "LEFT":
                                snake_turn_image_rotate = pygame.transform.rotate(self.snake_turn_img, 270)
                                if c.movement == "UP":
                                    pass
                                if c.movement == "DOWN":
                                    snake_turn_image_rotate = pygame.transform.flip(snake_turn_image_rotate, False, True)
                        elif moving_dir == "RIGHT":
                                snake_turn_image_rotate = pygame.transform.rotate(self.snake_turn_img, 90)
                                if c.movement == "UP":
                                    snake_turn_image_rotate = pygame.transform.flip(snake_turn_image_rotate, False, True)
                                if c.movement == "DOWN":
                                    pass
                        elif moving_dir == "UP":
                                snake_turn_image_rotate = pygame.transform.rotate(self.snake_turn_img, 180)
                                if c.movement == "LEFT":
                                    snake_turn_image_rotate = pygame.transform.flip(snake_turn_image_rotate, True, False)
                                if c.movement == "RIGHT":
                                    pass
                        elif moving_dir == "DOWN":
                                snake_turn_image_rotate = self.snake_turn_img
                                if c.movement == "LEFT":
                                    pass
                                if c.movement == "RIGHT":
                                    snake_turn_image_rotate = pygame.transform.flip(snake_turn_image_rotate, True, False)
                        screen.blit(snake_turn_image_rotate, [c.rect.x, c.rect.y])

                # BODY CONNECT --------------------- #
                else:
                    if number == len(self.body) - 1:
                        if c.movement == "LEFT":
                            screen.blit(pygame.transform.rotate(self.snake_body_img_end, 270), [c.rect.x, c.rect.y])
                        elif c.movement == "RIGHT":
                            screen.blit(pygame.transform.rotate(self.snake_body_img_end, 90), [c.rect.x, c.rect.y])
                        elif c.movement == "UP":
                            screen.blit(pygame.transform.flip(self.snake_body_img_end, False, True), [c.rect.x, c.rect.y])
                        else:
                            screen.blit(self.snake_body_img_end, [c.rect.x, c.rect.y])
                    else:
                        if c.movement == "LEFT":
                            screen.blit(pygame.transform.rotate(self.snake_body_img, 270), [c.rect.x, c.rect.y])
                        elif c.movement == "RIGHT":
                            screen.blit(pygame.transform.rotate(self.snake_body_img, 90), [c.rect.x, c.rect.y])
                        elif c.movement == "UP":
                            screen.blit(pygame.transform.flip(self.snake_body_img, False, True), [c.rect.x, c.rect.y])
                        else:
                            screen.blit(self.snake_body_img, [c.rect.x, c.rect.y])

    def add_cube(self):
        tail = self.body[-1]
        pos = [tail.rect.left // size_between, tail.rect.top // size_between]

        if tail.movement == "LEFT":
            pos[0] += 1
        elif tail.movement == "RIGHT":
            pos[0] -= 1
        elif tail.movement == "UP":
            pos[1] += 1
        elif tail.movement == "DOWN":
            pos[1] -= 1
        new_cube = Cube(size_between, pos, 0, self.color)
        new_cube.movement = tail.movement
        self.body.append(new_cube)

    def prevent_out(self):
        for c in self.body:
            if c.rect.left < grid_pos[0]:
                c.rect.right = self.grid_end_pos[0]
            elif c.rect.right > self.grid_end_pos[0]:
                c.rect.left = grid_pos[0]
            if c.rect.top < grid_pos[1]:
                c.rect.bottom = self.grid_end_pos[1]
            elif c.rect.bottom > self.grid_end_pos[1]:
                c.rect.top = grid_pos[1]

    def reset(self):
        self.body = []
        self.turns = {}
        self.body.append(self.head)
        self.body[0].movement = None
        self.body[0].rect.top = 10 * size_between + grid_pos[0]
        self.body[0].rect.left = 10 * size_between + grid_pos[1]

class Game:

    fps = 60
    step = 1
    speed_change_initial = 8

    # Objects
    jacob = Snake(size_between, [10, 10], grid_pos[0])

    # Images
    potion_img = pygame.image.load('data/Images/potion.png')

    def __init__(self):
        # Snack
        self.coin_pos = [random.randrange(rows), random.randrange(rows)]
        while self.coin_pos == [10, 10]:
            self.coin_pos = [random.randrange(rows), random.randrange(rows)]
        self.coin = Cube(size_between, self.coin_pos, grid_pos[0], light_grey)
        self.coin_animation_id = animation_id_generate([20, 8, 8, 8, 8], 'data/Coin/coin')
        self.coin_count = 0


        self.potion = None
        self.potion_count = 0

        # data
        self.speed_change = self.speed_change_initial
        self.score = 0
        self.scorecoin_y_velocity = 0
        self.score_coin = pygame.Rect(180, 565, 78, 78)

        # Effects
        self.border_list = []
        self.particles = []
        self.message = []

        self.running = True
        self.game()

    def events_(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause_sfx.play()
                    self.pause()

                if event.key == K_LEFT:
                    if self.jacob.body[0].movement == "RIGHT":
                        break
                    elif self.jacob.body[0].movement == "LEFT":
                        pass
                    else:
                        self.jacob.body[0].movement = "LEFT"
                        self.jacob.turns[self.jacob.body[0].rect.topleft] = "LEFT"
                        break
                if event.key == K_RIGHT:
                    if self.jacob.body[0].movement == "LEFT":
                        break
                    elif self.jacob.body[0].movement == "RIGHT":
                        pass
                    else:
                        self.jacob.body[0].movement = "RIGHT"
                        self.jacob.turns[self.jacob.body[0].rect.topleft] = "RIGHT"
                        break
                if event.key == K_UP:
                    if self.jacob.body[0].movement == "DOWN":
                        break
                    elif self.jacob.body[0].movement == "UP":
                        pass
                    else:
                        self.jacob.body[0].movement = "UP"
                        self.jacob.turns[self.jacob.body[0].rect.topleft] = "UP"
                        break
                if event.key == K_DOWN:
                    if self.jacob.body[0].movement == "UP":
                        break
                    elif self.jacob.body[0].movement == "DOWN":
                        pass
                    else:
                        self.jacob.body[0].movement = "DOWN"
                        self.jacob.turns[self.jacob.body[0].rect.topleft] = "DOWN"
                        break
            if event.type == QUIT:
                update_highscore(high_score)
                pygame.quit()
                sys.exit()

    def potion_generate(self):
        if self.score % 10 == 0 and self.score >= 10:
            if not self.potion and self.potion_count == 0:
                self.potion = Cube(size_between, [10,10], grid_pos[0], white)
                while True:
                    self.potion.rect.top = random.randrange(rows) * size_between + grid_pos[0]
                    self.potion.rect.left = random.randrange(rows) * size_between + grid_pos[1]
                    if len(list(filter(lambda z: z.rect.topleft == self.potion.rect.topleft, self.jacob.body))) > 0:
                        continue
                    elif self.potion.rect.topleft == self.coin.rect.topleft:
                        continue
                    else:
                        break
                self.potion_count = 1

    def coin_collect_effect(self):
        # [[rect, center, width_size]]
        for particle in self.particles:
            particle[0].width += 1
            particle[0].height += 1
            particle[0].center = particle[1]
            particle[2] -= 0.6
            pygame.draw.rect(screen, white, particle[0], int(particle[2]))
            if particle[2] <= 0:
                self.particles.remove(particle)

    def collision_snack(self):
        if self.jacob.body[0].rect.colliderect(self.coin.rect):
            new_rect = pygame.Rect(0, 0, self.coin.rect.width, self.coin.rect.height)
            new_rect.center = self.coin.rect.center
            self.particles.append([new_rect, self.coin.rect.center, 12])
            while True:
                self.coin.rect.top = random.randrange(rows) * size_between + grid_pos[0]
                self.coin.rect.left = random.randrange(rows) * size_between + grid_pos[1]
                if len(list(filter(lambda z: z.rect.topleft == self.coin.rect.topleft, self.jacob.body))) > 0:
                    continue
                else:
                    break
            self.jacob.add_cube()
            if self.score_coin.top >= 550:
                self.scorecoin_y_velocity -= 4
            self.score += 1
            self.speed_change -= 0.1
            self.speed_change = round(self.speed_change, 1)
            if self.speed_change == int(self.speed_change):
                if self.message:
                    self.message.append(["SPEEDING UP!!!", 20, white, 300, 300, 120])
                else:
                    self.message.append(["SPEEDING UP!!!", 20, white, 300, 250, 120])
                powerup_sfx.play()
            self.potion_count = 0
            coin_sfx.play()
        if self.potion:
            if self.jacob.body[0].rect.colliderect(self.potion):
                number = random.choice(range(0, 31))
                if number == 30:
                    random_slice = 8
                elif number <= 10:
                    random_slice = random.randint(4, 5)
                else:
                    random_slice = random.randint(1,3)
                sliced = self.jacob.body[-random_slice:]
                for c in sliced:
                    for turn in self.jacob.turns:
                        if turn == c.rect.topleft:
                            self.jacob.turns.pop(turn)
                            break

                self.jacob.body = self.jacob.body[:-random_slice]
                if random_slice == 1:
                    message = f"{random_slice} CUBE REMOVED!"
                else:
                    message = f"{random_slice} CUBES REMOVED!"
                if self.message:
                    self.message.append([message, 20, (0, 204, 122), 300, 300, 120])
                else:
                    self.message.append([message, 20, (0, 204, 122), 300, 250, 120])
                powerup2_sfx.play()
                self.potion = None

    def collision_body(self):
        for c in self.jacob.body[1:]:
            if self.jacob.body[0].rect.colliderect(c):
                self.jacob.reset()
                death_sfx.play()
                self.particles = []
                self.speed_change = self.speed_change_initial
                self.end()
                self.score_coin.bottom = 643
                self.score = 0

    def draw_snack(self):
        animation_display(self.coin.rect, self.coin_animation_id[self.coin_count])
        if self.coin_count >= len(self.coin_animation_id) - 1:
            self.coin_count = 0
        else:
            self.coin_count += 1
        if self.potion:
            screen.blit(self.potion_img, self.potion.rect.topleft)

    def display_score(self):
        self.score_coin.y += int(self.scorecoin_y_velocity)
        self.scorecoin_y_velocity += 0.2
        if self.score_coin.bottom >= 643:
            if self.scorecoin_y_velocity >= 1:
                self.scorecoin_y_velocity = -self.scorecoin_y_velocity + 0.5
            else:
                self.score_coin.bottom = 643
                self.scorecoin_y_velocity = 0
        animation_display(self.score_coin, self.coin_animation_id[0], 3)
        draw_text("x", pygame.font.Font('data/FFFFORWA.ttf', 60), gold, screen, 310, 610)
        draw_text(f"{self.score}", pygame.font.Font('data/FFFFORWA.ttf', 60), gold, screen, 390, 610)

    def display_message(self):
        # [text, size of font, color, x, y]
        for message in self.message:
            draw_text(message[0], pygame.font.Font('data/FFFFORWA.ttf', message[1]), message[2], screen, message[3],
                      message[4])
            message[-1] -= 1
            if message[-1] <= 0:
                self.message.remove(message)

    # Pages ------------------------------ #
    def game(self):
        while self.running:
            mx, my = pygame.mouse.get_pos()
            self.step += 1
            if self.step >= self.speed_change:
                # Events
                self.events_()
                self.jacob.move_snake()
                self.potion_generate()
                self.collision_snack()
                self.collision_body()
                self.jacob.prevent_out()
                self.step = 1

            if program_mode == "main_menu":
                self.jacob.reset()
                break

            # Visuals
            screen.fill(dark_grey)
            pygame.draw.rect(screen, dark_grey, pygame.Rect(0, 0, 600, 650))
            pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(50, 50, 500, 500))
            draw_grid(snake_grid_width, snake_grid_height, rows, dark_grey, start_pos=grid_pos)
            self.coin_collect_effect()
            self.draw_snack()
            self.jacob.draw_snake()
            self.display_score()
            self.display_message()
            draw_text(f"high score: {high_score}", pygame.font.Font('data/FFFFORWA.ttf', 20), gold, screen, 300, 28)

            # Update
            draw_text(f'Fps: {int(clock.get_fps())}', pygame.font.Font('data/FFFFORWA.ttf', 10), white, screen, 35, 15)
            pygame.display.update()
            clock.tick(self.fps)

    def pause(self):
        global program_mode

        # Buttons -------- #
        b_resume = pygame.Rect(0, 0, 275, 100)
        b_resume.center = (300, 260)

        b_mainmenu = pygame.Rect(0, 0, 275, 100)
        b_mainmenu.center = (300, 430)

        s = pygame.Surface((501, 501))
        s.fill(medium_grey)

        running = True
        while running:
            # Events ----- #
            mx, my = pygame.mouse.get_pos()
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    update_highscore(high_score)
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        resume_sfx.play()
                        break

            # Visuals
            screen.blit(s, (50, 50))
            pygame.draw.rect(screen, gold, pygame.Rect(60, 60, 481, 100))
            draw_text("- PAUSE -", pygame.font.Font('data/FFFFORWA.ttf', 35), dark_grey, screen, 300, 115)

            if b_resume.collidepoint(mx, my):
                pygame.draw.rect(screen, light_grey, b_resume)
                draw_text('Resume', pygame.font.Font('data/FFFFORWA.ttf', 35), dark_grey, screen, 300, 260)
                hover_animation(self.border_list, b_resume, 0.15, 3, 8)
                if click:
                    resume_sfx.play()
                    break
            else:
                pygame.draw.rect(screen, white, b_resume)
                draw_text('Resume', pygame.font.Font('data/FFFFORWA.ttf', 35), medium_grey, screen, 300, 260)
            if b_mainmenu.collidepoint(mx, my):
                pygame.draw.rect(screen, light_grey, b_mainmenu)
                draw_text('Main Menu', pygame.font.Font('data/FFFFORWA.ttf', 35), dark_grey, screen, 300, 430)
                hover_animation(self.border_list, b_mainmenu, 0.15, 3, 8)
                if click:
                    program_mode = 'main_menu'
                    self.running = False
                    self.jacob.reset()
                    self.particles = []
                    selection_sfx.play()
                    break
            else:
                pygame.draw.rect(screen, white, b_mainmenu)
                draw_text('Main Menu', pygame.font.Font('data/FFFFORWA.ttf', 35), medium_grey, screen, 300, 430)

            if b_resume.collidepoint(mx, my) or b_mainmenu.collidepoint(mx, my):
                pass
            else:
                self.border_list = []

            music_config(mx, my, click)

            # Update
            pygame.display.update()
            clock.tick(60)

    def end(self):
        global program_mode, high_score
        # Buttons ------- #
        b_playagain = pygame.Rect(0, 0, 250, 75)
        b_playagain.center = (300, 468)

        b_mainmenu = pygame.Rect(0, 0, 250, 75)
        b_mainmenu.center = (300, 580)

        if self.score > high_score:
            high_score = self.score
            h_score_color = (0, 204, 122)
        else:
            h_score_color = (255, 102, 102)
        while True:
            # Events
            mx, my = pygame.mouse.get_pos()
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    update_highscore(high_score)
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True


            # Visuals
            screen.fill(dark_grey)
            draw_text("Oops", pygame.font.Font('data/FFFFORWA.ttf', 40), white, screen, 300, 120)
            draw_text("Looks like you lost...", pygame.font.Font('data/FFFFORWA.ttf', 40), white, screen, 300, 200)

            pygame.draw.rect(screen, gold, pygame.Rect(0, 250, 600, 150))
            draw_text(f"Score: {self.score}", pygame.font.Font('data/FFFFORWA.ttf', 60), dark_grey, screen, 300, 325)
            draw_text(f"high score: {high_score}", pygame.font.Font('data/FFFFORWA.ttf', 18),
                      h_score_color, screen, 300, 380)

            if b_playagain.collidepoint(mx, my):
                pygame.draw.rect(screen, light_grey, b_playagain)
                draw_text("Again?", pygame.font.Font("data/FFFFORWA.ttf", 30), dark_grey, screen, 300, 468)
                hover_animation(self.border_list, b_playagain, 0.15, 3, 8)
                if click:
                    selection_sfx.play()
                    self.potion = None
                    break
            else:
                pygame.draw.rect(screen, white, b_playagain)
                draw_text("Again?", pygame.font.Font("data/FFFFORWA.ttf", 30), medium_grey, screen, 300, 468)
            if b_mainmenu.collidepoint(mx, my):
                pygame.draw.rect(screen, light_grey, b_mainmenu)
                draw_text("Main Menu", pygame.font.Font("data/FFFFORWA.ttf", 30), dark_grey, screen, 300, 580)
                hover_animation(self.border_list, b_mainmenu, 0.15, 3, 8)
                if click:
                    program_mode = "main_menu"
                    self.running = False
                    selection_sfx.play()
                    break
            else:
                pygame.draw.rect(screen, white, b_mainmenu)
                draw_text("Main Menu", pygame.font.Font("data/FFFFORWA.ttf", 30), medium_grey, screen, 300, 580)

            if b_playagain.collidepoint(mx, my) or b_mainmenu.collidepoint(mx, my):
                pass
            else:
                self.border_list = []

            music_config(mx, my, click)

            pygame.display.update()
            clock.tick(60)

# Start ------------------------------------------------------------------ #
program_mode = "main_menu"
while True:
    if program_mode == "main_menu":
        main_menu = MainMenu()
    elif program_mode == "game":
        game = Game()
