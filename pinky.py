from ghost import Ghost
import pygame


class Pinky(Ghost):
    def __init__(self, sf, x, y, v, grid):
        self.scatter_coords = [(1, 1), (1, 5), (6, 5), (6, 1)]
        self.spawn_coords = 0
        self.spawn_dots = 0
        self.respawn_dots = 7
        self.current_direction = 'DOWN'
        self.image = pygame.transform.scale(pygame.image.load('./assets/pink_ghost/down_1.png'),
                                            (int(1.6 * sf), int(1.6 * sf)))
        self.sprites = {
            'NONE':
                [
                    pygame.transform.scale(pygame.image.load('./assets/pink_ghost/down_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pink_ghost/down_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'UP':
                [
                    pygame.transform.scale(pygame.image.load('./assets/pink_ghost/up_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pink_ghost/up_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'DOWN':
                [
                    pygame.transform.scale(pygame.image.load('./assets/pink_ghost/down_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pink_ghost/down_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'LEFT':
                [
                    pygame.transform.scale(pygame.image.load('./assets/pink_ghost/left_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pink_ghost/left_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'RIGHT':
                [
                    pygame.transform.scale(pygame.image.load('./assets/pink_ghost/right_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/pink_ghost/right_2.png'),
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
        tx, ty, _, _ = target.get_grid_coord((target.x, target.y))
        for i in range(4, -1, -1):
            x, y = tx + (target.directions[target.current_direction][0] * i), ty + (target.directions[target.current_direction][1] * i)
            try:
                if self.grid[y][x] != 1:
                    tx, ty, = x, y
                    break
            except:
                pass
        return tx, ty

    def set_spawn_dots(self, id):
        self.spawn_dots = 0
