import pygame
from pygame.locals import *
from grid import grid, dots
from blinky import Blinky
from inky import Inky
from pinky import Pinky
from clyde import Clyde
from pacman import Pacman
from level import Level

pygame.font.init()

#####Constants######
SCALE_FACTOR = 24
MAX_VELOCITY = SCALE_FACTOR // 8

SCREEN_WIDTH = 28 * SCALE_FACTOR
SCREEN_HEIGHT = 36 * SCALE_FACTOR
WIN_WIDTH = 28 * SCALE_FACTOR
WIN_HEIGHT = 31 * SCALE_FACTOR

FRAMERATE = 60

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
WIN = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('PacMan')
pygame.init()
bg = pygame.transform.scale(pygame.image.load('./assets/other/background.png'), (WIN_WIDTH, WIN_HEIGHT))
dot = pygame.transform.scale(pygame.image.load('./assets/other/pellet.png'),
                             (int(0.2 * SCALE_FACTOR), int(0.2 * SCALE_FACTOR)))
powerup = pygame.transform.scale(pygame.image.load('./assets/other/powerup.png'),
                                 (int(0.8 * SCALE_FACTOR), int(0.8 * SCALE_FACTOR)))

life = pygame.transform.scale(pygame.image.load('./assets/other/pacman_life.png'),
                              (int(1 * SCALE_FACTOR), int(1 * SCALE_FACTOR)))
font = './assets/font.ttf'

start_animation = True
start_frames = 0
start_delay = 120
death_timer = False
death_frames = 0
death_delay = 60
end_timer = False
end_frames = 0
end_delay = 120
game_over = False

level = 0
levels = [
    Level(1, 0.8, 0.9, 0.75, 0.5, 0.4, 360, 5, [420, 1200, 420, 1200, 300, 1200, 300]),
    Level(2, 0.9, 0.95, 0.85, 0.55, 0.45, 300, 5, [420, 1200, 420, 1200, 300, (1033 * 60), 1]),
    Level(3, 0.9, 0.95, 0.85, 0.55, 0.45, 240, 5, [420, 1200, 420, 1200, 300, (1033 * 60), 1]),
    Level(4, 0.9, 0.95, 0.85, 0.55, 0.45, 180, 5, [420, 1200, 420, 1200, 300, (1033 * 60), 1]),
    Level(5, 1, 1, 0.95, 0.6, 0.5, 120, 5, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(6, 1, 1, 0.95, 0.6, 0.5, 300, 5, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(7, 1, 1, 0.95, 0.6, 0.5, 120, 5, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(8, 1, 1, 0.95, 0.6, 0.5, 120, 5, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(9, 1, 1, 0.95, 0.6, 0.5, 60, 3, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(10, 1, 1, 0.95, 0.6, 0.5, 300, 5, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(11, 1, 1, 0.95, 0.6, 0.5, 120, 5, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(12, 1, 1, 0.95, 0.6, 0.5, 60, 3, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(13, 1, 1, 0.95, 0.6, 0.5, 60, 3, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(14, 1, 1, 0.95, 0.6, 0.5, 180, 5, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(15, 1, 1, 0.95, 0.6, 0.5, 60, 3, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(16, 1, 1, 0.95, 0.6, 0.5, 60, 3, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(17, 1, 1, 0.95, 0.6, 0.5, 0, 0, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(18, 1, 1, 0.95, 0.6, 0.5, 60, 3, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(19, 1, 1, 0.95, 0.6, 0.5, 0, 0, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(20, 1, 1, 0.95, 0.6, 0.5, 0, 0, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
    Level(21, 0.9, 0.9, 0.95, 0.95, 0.5, 0, 0, [300, 1200, 300, 1200, 300, (1037 * 60), 1]),
          ]

highscore_file = open("./assets/highscore.txt", "r")
highscore = highscore_file.readline()
highscore_file.close()

####Classes####
pacman = Pacman(SCALE_FACTOR, 13.5, 23, MAX_VELOCITY, grid)
blinky = Blinky(SCALE_FACTOR, 13.5, 11, MAX_VELOCITY, grid)
inky = Inky(SCALE_FACTOR, 11.5, 14, MAX_VELOCITY, grid)
pinky = Pinky(SCALE_FACTOR, 13.5, 14, MAX_VELOCITY, grid)
clyde = Clyde(SCALE_FACTOR, 15.5, 14, MAX_VELOCITY, grid)
clock = pygame.time.Clock()


####functions####

def draw_text(win, text, font, size, colour, pos):
    font = pygame.font.Font(font, size)
    textsurface = font.render(text, False, colour)
    win.blit(textsurface, pos)


def draw_highscore(win, highscore, score):
    draw_text(win, "HIGH SCORE", font, int((23 / 30) * SCALE_FACTOR), (255, 255, 255),
              (int(10.5 * SCALE_FACTOR), int((1 / 3) * SCALE_FACTOR)))
    high_score = highscore
    if score > int(highscore):
        high_score = score
    draw_text(win, str(high_score), font, int((22 / 30) * SCALE_FACTOR), (255, 255, 255),
              (int(13 * SCALE_FACTOR), int((4 / 3) * SCALE_FACTOR)))


def draw_grid(win):
    for i in range(28):
        pygame.draw.line(WIN, (200, 200, 200), (i * SCALE_FACTOR, 0), (i * SCALE_FACTOR, WIN_HEIGHT))
    for i in range(31):
        pygame.draw.line(WIN, (200, 200, 200), (0, i * SCALE_FACTOR), (WIN_WIDTH, i * SCALE_FACTOR))


def draw(win, screen, bg, sprites, dots):
    screen.fill((0, 0, 0))
    win.blit(bg, (0, 0))
    draw_dots(win, dots.positions)
    draw_lives(screen)
    if not sprites[0].dying:
        for sprite in sprites:
            sprite.draw(win)
    else:
        sprites[0].draw(win)
    # draw_grid(win)
    screen.blit(WIN, (0, 3 * SCALE_FACTOR))
    draw_text(screen, f'SCORE: {sprites[0].get_score()}', font, int((2 / 3) * SCALE_FACTOR),
              (255, 255, 255), (int((1 / 3) * SCALE_FACTOR), int((4 / 3) * SCALE_FACTOR)))
    draw_highscore(screen, highscore, sprites[0].score)
    pygame.display.update()


def draw_dots(win, dots):
    for i, row in enumerate(dots):
        for j, col in enumerate(row):
            if dots[i][j] == 1:
                win.blit(dot, (j * SCALE_FACTOR + (SCALE_FACTOR // 2.3), i * SCALE_FACTOR + (SCALE_FACTOR // 2.3)))
            elif dots[i][j] == 2:
                win.blit(powerup, (j * SCALE_FACTOR + (SCALE_FACTOR // 8), i * SCALE_FACTOR + (SCALE_FACTOR // 8)))


def draw_start(win, screen, bg, sprites, dots):
    screen.fill((0, 0, 0))
    win.blit(bg, (0, 0))
    draw_dots(win, dots.positions)
    draw_lives(screen)
    for sprite in sprites:
        sprite.draw(win)
    # draw_grid(win)
    screen.blit(WIN, (0, 3 * SCALE_FACTOR))
    draw_text(screen, f'SCORE: {sprites[0].get_score()}', font, int((2 / 3) * SCALE_FACTOR),
              (255, 255, 255), (int((1 / 3) * SCALE_FACTOR), int((4 / 3) * SCALE_FACTOR)))
    draw_text(screen, 'READY!', font, int((23 / 30) * SCALE_FACTOR), (255, 241, 24),
              (int(12 * SCALE_FACTOR), int(20 * SCALE_FACTOR)))
    draw_highscore(screen, highscore, sprites[0].score)
    pygame.display.update()


def draw_gameover(win, screen, bg, sprites, dots):
    screen.fill((0, 0, 0))
    win.blit(bg, (0, 0))
    draw_dots(win, dots.positions)
    draw_lives(screen)
    # draw_grid(win)
    screen.blit(WIN, (0, 3 * SCALE_FACTOR))
    draw_text(screen, f'SCORE: {sprites[0].get_score()}', font, int((2 / 3) * SCALE_FACTOR),
              (255, 255, 255), (int((1 / 3) * SCALE_FACTOR), int((4 / 3) * SCALE_FACTOR)))
    draw_text(screen, 'GAME OVER', font, int((23 / 30) * SCALE_FACTOR), (255, 0, 0),
              (int(10.6 * SCALE_FACTOR), int(20 * SCALE_FACTOR)))
    draw_highscore(screen, highscore, sprites[0].score)
    pygame.display.update()


def draw_lives(win):
    lives = pacman.get_lives()
    for i in range(lives):
        win.blit(life, ((i * SCALE_FACTOR * 1.2) + SCALE_FACTOR // 2, (34 * SCALE_FACTOR) + SCALE_FACTOR // 2))


if __name__ == '__main__':
    keys = {K_UP: "UP", K_DOWN: "DOWN", K_LEFT: "LEFT", K_RIGHT: "RIGHT"}
    while True:
        clock.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key in keys and not game_over:
                    pacman.update_next_direction(keys[event.key])
                elif event.key == K_SPACE and game_over:
                    start_animation = True
                    death_timer = False
                    end_timer = False
                    game_over = False
                    level = 0
                    pacman = Pacman(SCALE_FACTOR, 13.5, 23, MAX_VELOCITY, grid)
                    blinky = Blinky(SCALE_FACTOR, 13.5, 11, MAX_VELOCITY, grid)
                    inky = Inky(SCALE_FACTOR, 11.5, 14, MAX_VELOCITY, grid)
                    pinky = Pinky(SCALE_FACTOR, 13.5, 14, MAX_VELOCITY, grid)
                    clyde = Clyde(SCALE_FACTOR, 15.5, 14, MAX_VELOCITY, grid)
                    start_animation = True
                elif event.key == K_t:
                    pacman.level_end = True
                    end_timer = True

        if not start_animation and not game_over and not death_timer and not end_timer:
            draw(WIN, SCREEN, bg, [pacman, blinky, inky, pinky, clyde], dots)
            pacman.move()
            blinky.move(pacman, grid)
            inky.move(pacman, grid, blinky)
            pinky.move(pacman, grid)
            clyde.move(pacman, grid)
        elif end_timer and end_frames >= end_delay:
            end_timer = False
            end_frames = 0
            dots.reset_dots()
            blinky.reset_level()
            inky.reset_level()
            pinky.reset_level()
            clyde.reset_level()
            blinky.current_direction = 'LEFT'
            inky.current_direction = 'UP'
            pinky.current_direction = 'DOWN'
            clyde.current_direction = 'UP'
            pacman.reset(False)
            if level < 20:
                level += 1
            blinky.set_level(levels[level])
            inky.set_level(levels[level])
            pinky.set_level(levels[level])
            clyde.set_level(levels[level])
            pacman.set_level(levels[level])
            start_animation = True
        elif end_timer:
            draw(WIN, SCREEN, bg, [pacman], dots)
            end_frames += 1
        elif death_timer and death_frames >= death_delay:
            death_timer = False
            death_frames = 0
            blinky.reset()
            inky.reset()
            pinky.reset()
            clyde.reset()
            pacman.reset(True)
        elif death_timer:
            draw(WIN, SCREEN, bg, [pacman], dots)
            pacman.move()
            death_frames += 1
        elif game_over:
            draw_gameover(WIN, SCREEN, bg, [pacman], dots)
        elif start_frames <= start_delay // 2 and start_animation:
            draw_start(WIN, SCREEN, bg, [pacman], dots)
            start_frames += 1
        elif start_frames <= start_delay and start_animation:
            draw_start(WIN, SCREEN, bg, [pacman, blinky, inky, pinky, clyde], dots)
            start_frames += 1
        elif start_animation:
            start_animation = False
            start_frames = 0
            inky.alive = False
            pinky.alive = False
            clyde.alive = False
            inky.spawning = True
            pinky.spawning = True
            clyde.spawning = True
            blinky.current_direction = 'LEFT'
            inky.current_direction = 'UP'
            pinky.current_direction = 'DOWN'
            clyde.current_direction = 'UP'

        if pacman.start_reset:
            death_timer = True
            if pacman.lives > 0:
                start_animation = True
            else:
                highscore_file = open("./assets/highscore.txt", "w")
                if pacman.get_score() > int(highscore):
                    highscore = pacman.get_score()
                highscore_file.write(str(highscore))
                highscore_file.close()
                game_over = True
            pacman.start_reset = False

        if dots.is_empty():
            pacman.level_end = True
            end_timer = True

        if pinky.counting_dots and pinky.time_since_dot >= 240:
            pinky.dot_counter += 1
            inky.time_since_dot = 0
            clyde.time_since_dot = 0
        if inky.counting_dots and inky.time_since_dot >= 240:
            inky.dot_counter += 1
            clyde.time_since_dot = 0
        if clyde.counting_dots and clyde.time_since_dot >= 240:
            clyde.dot_counter += 1

        if blinky.has_left and not pinky.has_left:
            pinky.counting_dots = True
        elif pinky.has_left and not inky.has_left:
            inky.counting_dots = True
        elif inky.has_left and not clyde.has_left:
            clyde.counting_dots = True
