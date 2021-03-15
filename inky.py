from ghost import Ghost
import pygame


class Inky(Ghost):
    def __init__(self, sf, x, y, v, grid):
        self.scatter_coords = [(26, 29), (15, 29), (15, 26), (18, 26), (18, 23), (21, 23), (21, 26), (26, 26)]
        self.spawn_coords = - 1
        self.spawn_dots = 30
        self.respawn_dots = 17
        self.current_direction = 'UP'
        self.image = pygame.transform.scale(pygame.image.load('./assets/blue_ghost/down_1.png'),
                                            (int(1.6 * sf), int(1.6 * sf)))
        self.sprites = {
            'NONE':
                [
                    pygame.transform.scale(pygame.image.load('./assets/blue_ghost/down_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/blue_ghost/down_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'UP':
                [
                    pygame.transform.scale(pygame.image.load('./assets/blue_ghost/up_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/blue_ghost/up_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'DOWN':
                [
                    pygame.transform.scale(pygame.image.load('./assets/blue_ghost/down_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/blue_ghost/down_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'LEFT':
                [
                    pygame.transform.scale(pygame.image.load('./assets/blue_ghost/left_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/blue_ghost/left_2.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                ],
            'RIGHT':
                [
                    pygame.transform.scale(pygame.image.load('./assets/blue_ghost/right_1.png'),
                                           (int(1.6 * sf), int(1.6 * sf))),
                    pygame.transform.scale(pygame.image.load('./assets/blue_ghost/right_2.png'),
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
        bx, by, _ = target2.get_grid_coord((target2.x, target2.y))
        px, py, _, _ = target.get_grid_coord((target.x, target.y))
        x, y = px + (target.directions[target.current_direction][0] * 2), py + (
                    target.directions[target.current_direction][1] * 2)
        tx, ty = bx + ((x - bx) * 2), by + ((y - by) * 2)
        if tx < 0:
            tx = 0
        if ty < 0:
            ty = 0
        if tx >= len(self.grid[0]):
            tx = len(self.grid[0]) - 1
        if ty >= len(self.grid):
            ty = len(self.grid) - 1
        while True:
            if self.grid[ty][tx] != 1:
                break
            else:
                if tx != px:
                    if tx > px:
                        tx -= 1
                    else:
                        tx += 1
                elif ty != py:
                    if ty > py:
                        ty -= 1
                    else:
                        ty += 1
        return tx, ty

    def set_spawn_dots(self, id):
        if id <= 1:
            self.spawn_dots = 30
        else:
            self.spawn_dots = 0

