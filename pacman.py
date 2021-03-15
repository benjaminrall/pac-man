import pygame
from sprite import Sprite
from grid import dots


class Pacman(Sprite):
    def __init__(self, sf, x, y, v, grid):
        super().__init__(sf, x, y, v, grid)
        self.image = pygame.transform.scale(pygame.image.load('./assets/pacman/up_full.png'),
                                            (int(1.9 * sf), int(1.9 * sf)))
        self.rect = self.image.get_rect()
        self.rect.center = (self.get_pos())
        self.score = 0
        self.start_reset = False
        self.powered = False
        self.activated_powered = False
        self.powered_ticks = 0
        self.powered_flash = 5
        self.max_powered_ticks = 360 + self.powered_flash * 30
        self.velocity_modifier = 0.8
        self.temp_velocity_modifier = 0.8
        self.powered_velocity = 0.9
        self.temp_powered_velocity = 0.9
        self.level_end = False
        self.dot_counter = 0
        self.sprites = {
            'NONE':
                [
                    pygame.transform.scale(pygame.image.load('./assets/pacman/up_full.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/up_full.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/up_full.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/up_full.png'),
                                           (int(1.9 * sf), int(1.9 * sf)))
                ],
            'UP':
                [
                    pygame.transform.scale(pygame.image.load('./assets/pacman/up_full.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/up_half.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/up_open.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/up_half.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                ],
            'DOWN':
                [
                    pygame.transform.scale(pygame.image.load('./assets/pacman/down_full.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/down_half.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/down_open.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/down_half.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                ],
            'LEFT':
                [
                    pygame.transform.scale(pygame.image.load('./assets/pacman/left_full.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/left_half.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/left_open.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/left_half.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                ],
            'RIGHT':
                [
                    pygame.transform.scale(pygame.image.load('./assets/pacman/right_full.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/right_half.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/right_open.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/right_half.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                ],
            'DEATH':
                [
                    pygame.transform.scale(pygame.image.load('./assets/pacman/death_0.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/death_1.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/death_2.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/death_3.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/death_4.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/death_5.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/death_6.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/death_7.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/death_8.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pacman/death_9.png'),
                                           (int(1.9 * sf), int(1.9 * sf))),
                ]
        }

        self.lives = 2

    def set_level(self, level):
        self.velocity_modifier = level.ps
        self.powered_velocity = level.pfs
        self.powered_flash = level.flashes
        if level.ft > 0:
            self.max_powered_ticks = level.ft + (self.powered_flash * 30)
        else:
            self.max_powered_ticks = 1

    def draw(self, win):
        if self.alive and not self.level_end:
            images = self.sprites[self.current_direction]
            if self.tick >= 15:
                image = images[3]
            elif self.tick >= 10:
                image = images[2]
            elif self.tick >= 5:
                image = images[1]
            else:
                image = images[0]
        elif self.dying and not self.level_end:
            images = self.sprites['DEATH']
            if self.tick >= 70:
                self.dying = False
            if self.tick >= 63:
                image = images[9]
            elif self.tick >= 56:
                image = images[8]
            elif self.tick >= 49:
                image = images[7]
            elif self.tick >= 42:
                image = images[6]
            elif self.tick >= 35:
                image = images[5]
            elif self.tick >= 28:
                image = images[4]
            elif self.tick >= 21:
                image = images[3]
            elif self.tick >= 14:
                image = images[2]
            elif self.tick >= 7:
                image = images[1]
            else:
                image = images[0]
        else:
            images = self.sprites[self.current_direction]
            image = images[0]

        if self.dying or self.alive:
            win.blit(image, self.rect)
        else:
            self.start_reset = True

    def reset(self, r_lives):
        if r_lives:
            self.lives -= 1
        self.x, self.y = self.start_pos
        self.rect.center = (self.get_pos())
        self.alive = True
        self.current_direction = 'NONE'
        self.next_direction = 'NONE'
        self.powered = False
        self.powered_ticks = 0
        self.dot_counter = 0
        self.level_end = False

    def get_score(self):
        return self.score

    def collide(self, grid_pos):
        if dots.is_dot(grid_pos[0], grid_pos[1]):
            dots.eat_dot(grid_pos[0], grid_pos[1])
            self.score += 10
            self.temp_velocity_modifier = 0
            self.temp_powered_velocity = 0
            self.dot_counter += 1
        elif dots.is_super(grid_pos[0], grid_pos[1]):
            dots.eat_dot(grid_pos[0], grid_pos[1])
            self.score += 50
            self.temp_velocity_modifier = 0
            self.temp_powered_velocity = 0
            self.powered = True
            self.powered_ticks = self.max_powered_ticks
            self.activated_powered = True
            self.dot_counter += 1
        elif self.max_powered_ticks - self.powered_ticks > 3 and self.max_powered_ticks != 1:
            self.temp_velocity_modifier = self.velocity_modifier
            self.temp_powered_velocity = self.powered_velocity
        else:
            self.temp_velocity_modifier = self.velocity_modifier
            self.temp_powered_velocity = self.powered_velocity


    def kill(self):

        self.alive = False
        self.dying = True
        self.tick = 0

    def get_lives(self):
        return self.lives

    def get_grid_coord(self, pos):
        x, y = pos
        turn_difference = 0.375 * self.sf
        can_turn = False
        if self.current_direction == 'UP' and (self.sf // 2) + turn_difference >= y % self.sf >= self.sf // 2:
            can_turn = True
        elif self.current_direction == 'DOWN' and self.sf // 2 >= y % self.sf >= (self.sf // 2) - turn_difference:
            can_turn = True
        elif self.current_direction == 'LEFT' and (self.sf // 2) + turn_difference >= x % self.sf >= self.sf // 2:
            can_turn = True
        elif self.current_direction == 'RIGHT' and self.sf // 2 >= x % self.sf >= (self.sf // 2) - turn_difference:
            can_turn = True
        elif self.current_direction == 'NONE':
            can_turn = True
        distance = (int((x % self.sf) - self.sf // 2), int((y % self.sf) - self.sf // 2))
        x = int(x // self.sf)
        y = int(y // self.sf)
        return x, y, can_turn, distance

    def move(self):
        if self.alive:
            if self.can_turn():
                if self.next_direction != 'NONE':
                    self.current_direction = self.next_direction

            if self.can_move(self.current_direction):
                _, _, _, distance = self.get_grid_coord(self.get_pos())
                dx, dy = 0, 0
                if distance[0] != 0 and self.directions[self.current_direction][0] == 0 and not self.can_turn():
                    dx = (-1 * distance[0])
                elif distance[1] != 0 and self.directions[self.current_direction][1] == 0 and not self.can_turn():
                    dy = (-1 * distance[1])

                if self.powered:
                    v = self.v * self.temp_powered_velocity
                else:
                    v = self.v * self.temp_velocity_modifier
                self.x += self.directions[self.current_direction][0] * v
                self.y += self.directions[self.current_direction][1] * v
                self.x += dx
                self.y += dy
                self.rect.center = self.get_pos()

                if self.activated_powered:
                    self.activated_powered = False

                if self.x <= 0:
                    self.x = 28 * self.sf
                    self.rect.centerx = self.x
                elif self.x >= 28 * self.sf:
                    self.x = 0
                    self.rect.centerx = self.x

                if self.tick < 20:
                    self.tick += 1
                else:
                    self.tick = 0
            elif self.tick < 5:
                self.tick = 5

            self.collide(self.get_grid_coord(self.get_pos()))
            if self.powered_ticks > 0:
                self.powered_ticks -= 1
            else:
                self.powered = False
        elif self.dying:
            self.tick += 1
