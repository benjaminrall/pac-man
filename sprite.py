import pygame


class Sprite:
    '''base class for all sprites'''

    def __init__(self, sf, x, y, v, grid):
        self.start_pos = (int((x * sf) + (sf // 2)), (y * sf) + (sf // 2))
        self.alive = True
        self.dying = False
        self.directions = {'LEFT': (-1, 0), 'RIGHT': (1, 0), 'UP': (0, -1), 'DOWN': (0, 1), 'NONE': (0, 0)}
        self.current_direction = 'NONE'
        self.next_direction = 'NONE'
        self.grid = grid
        self.v = v
        self.sf = sf
        self.tick = 0

        self.x = int((x * sf) + (sf // 2))
        self.y = (y * sf) + (sf // 2)

    def update_next_direction(self, direction):
        if direction == self.current_direction:
            return

        self.next_direction = direction

        nx, ny = self.directions[self.next_direction]
        cx, cy = self.directions[self.current_direction]

        if (nx + cx, ny + cy) == (0, 0):
            self.current_direction = self.next_direction
            self.next_direction = 'NONE'
        # print(self.current_direction)

    def is_alive(self):
        return self.alive == True

    def get_pos(self):
        return self.x, self.y

    def get_grid_coord(self, pos):
        x, y = pos
        centre = False
        extra = 2.5
        if ((self.sf // 2) + extra >= x % self.sf >= (self.sf // 2) - extra and self.directions[self.current_direction][1] == 0) or ((self.sf // 2) + extra >= y % self.sf >= (self.sf // 2) - extra and self.directions[self.current_direction][0] == 0):
            self.rect.center = self.get_pos()
            centre = True
        x = int(x // self.sf)
        y = int(y // self.sf)
        return x, y, centre

    def can_move(self, direction):
        x, y, centre, _ = self.get_grid_coord((self.x, self.y))
        cx, cy = self.directions[direction]
        newx = cx + x
        newy = cy + y
        if self.grid[newy][newx] == 1 and centre:
            return False
        else:
            return True

    def can_turn(self):
        x, y, centre, _ = self.get_grid_coord((self.x, self.y))
        if self.grid[y][x] == 2 and centre and self.can_move(self.next_direction):
            return True
        else:
            return False

    def kill(self):
        pass
