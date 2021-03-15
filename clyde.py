from ghost import Ghost
import pygame


class Clyde(Ghost):
    def __init__(self, sf, x, y, v, grid):
        self.scatter_coords = [(1, 29), (12, 29), (12, 26), (9, 26), (9, 23), (6, 23), (6, 26), (1, 26)]
        self.spawn_coords = 1
        self.spawn_dots = 60
        self.respawn_dots = 32
        self.current_direction = 'UP'
        self.image = pygame.transform.scale(pygame.image.load('./assets/orange_ghost/down_1.png'),
                                            (int(1.6 * sf), int(1.6 * sf)))
        self.sprites = {
            'NONE':
                [
                    pygame.transform.scale(pygame.image.load('./assets/orange_ghost/down_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/orange_ghost/down_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'UP':
                [
                    pygame.transform.scale(pygame.image.load('./assets/orange_ghost/up_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/orange_ghost/up_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'DOWN':
                [
                    pygame.transform.scale(pygame.image.load('./assets/orange_ghost/down_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/orange_ghost/down_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'LEFT':
                [
                    pygame.transform.scale(pygame.image.load('./assets/orange_ghost/left_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/orange_ghost/left_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'RIGHT':
                [
                    pygame.transform.scale(pygame.image.load('./assets/orange_ghost/right_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/orange_ghost/right_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'FRIGHTENED':
                [
                    pygame.transform.scale(pygame.image.load('./assets/other/vulnerable_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/other/vulnerable_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/other/vulnerable_3.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/other/vulnerable_4.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'DEAD':
                {
                    'UP': pygame.transform.scale(pygame.image.load('./assets/other/up_eyes.png'),
                                                 (int(1.6 * sf), int(1.6 * sf))),
                    'DOWN': pygame.transform.scale(pygame.image.load('./assets/other/down_eyes.png'),
                                                   (int(1.6 * sf), int(1.6 * sf))),
                    'LEFT': pygame.transform.scale(pygame.image.load('./assets/other/left_eyes.png'),
                                                   (int(1.6 * sf), int(1.6 * sf))),
                    'RIGHT': pygame.transform.scale(pygame.image.load('./assets/other/right_eyes.png'),
                                                    (int(1.6 * sf), int(1.6 * sf))),
                    'NONE': pygame.transform.scale(pygame.image.load('./assets/other/down_eyes.png'),
                                                   (int(1.6 * sf), int(1.6 * sf))),
                }
        }
        super().__init__(sf, x, y, v, grid)

    def get_target_pos(self, target, target2):
        x, y, _, _ = target.get_grid_coord((target.x, target.y))
        sx, sy, _ = self.get_grid_coord((self.x, self.y))
        diff = abs(sx - x) + abs(sy - y)
        if diff >= 8:
            tx, ty = x, y
        elif sx != 1 and sy != 29:
            tx, ty = 1, 29
        else:
            tx, ty = 9, 23
        return tx, ty

    def set_spawn_dots(self, id):
        if id == 1:
            self.spawn_dots = 60
        elif id == 2:
            self.spawn_dots = 50
        else:
            self.spawn_dots = 0
