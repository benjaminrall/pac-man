from sprite import Sprite
from node import Node
import random
from grid import dots
import pygame


class Ghost(Sprite):

    def __init__(self, sf, x, y, v, grid):
        super().__init__(sf, x, y, v, grid)
        self.rect = self.image.get_rect()
        self.rect.center = (self.get_pos())
        self.current_direction = 'LEFT'
        self.previous_direction = 'NONE'
        self.scatter = True
        self.scatter_timings = [420, 1200, 420, 1200, 300, 1200, 300]
        self.scatter_frame = 0
        self.scatter_tick = 0
        self.scatter_step = 0
        self.frightened = False
        self.frightened_flash = 5
        self.frightened_ticks = 0
        self.frightened_velocity = 0.5
        self.reached_scatter = False
        self.previous_state = 'NORMAL'
        self.change_direction = False
        self.tunnel_velocity = 0.4
        self.velocity_modifier = 0.75
        self.dying_velocity = 1.5
        self.dead_velocity = 0.5
        self.alive = True
        self.dying = False
        self.respawning = False
        self.spawning = False
        self.counting_dots = False
        self.dot_counter = 0
        self.previous_dots = 0
        self.time_since_dot = 0
        self.global_dots = 0
        self.has_left = False

    def set_level(self, level):
        self.velocity_modifier = level.gs
        self.tunnel_velocity = level.gts
        self.frightened_velocity = level.gfs
        self.frightened_flash = level.flashes
        self.scatter_timings = level.scatter_timings
        self.set_spawn_dots(level.id)

    def draw(self, win):
        if not self.dying:
            if not self.frightened:
                images = self.sprites[self.current_direction]
                if self.tick >= 8:
                    image = images[1]
                else:
                    image = images[0]
            else:
                images = self.sprites["FRIGHTENED"]
                if self.frightened_ticks >= self.frightened_flash * 30:
                    if self.tick >= 8:
                        image = images[1]
                    else:
                        image = images[0]
                else:
                    if self.frightened_ticks % 30 > 15:
                        if self.tick >= 8:
                            image = images[1]
                        else:
                            image = images[0]
                    else:
                        if self.tick >= 8:
                            image = images[3]
                        else:
                            image = images[2]
        else:
            image = self.sprites['DEAD'][self.current_direction]

        win.blit(image, self.rect)

    def find_path(self, ex, ey, grid):
        open_set = []
        closed_set = []
        node_grid = []
        for i, row in enumerate(grid):
            x = []
            for j, col in enumerate(row):
                if col == 2:
                    x.append(Node(j, i))
                elif col == 1:
                    x.append(1)
                else:
                    x.append(None)
            node_grid.append(x)

        sx, sy, _ = self.get_grid_coord((self.x, self.y))
        start = Node(sx, sy)
        end = Node(ex, ey)
        node_grid[sy][sx] = start
        node_grid[ey][ex] = end
        path = []
        open_set.append(node_grid[sy][sx])

        start.t = 1

        for row in node_grid:
            for node in row:
                if node is not None and node is not 1:
                    node.find_neighbors(node_grid, self.previous_direction)

        while len(open_set) > 0:
            winner = 0
            for i in range(len(open_set)):
                if open_set[i].f < open_set[winner].f:
                    winner = i

            current = open_set[winner]
            if current == end:

                path = []
                temp = current
                path.append(temp)
                while temp.previous is not None:
                    path.append(temp.previous)
                    temp = temp.previous
                break

            closed_set.append(current)
            open_set.pop(winner)

            for neighbor in current.neighbors:
                if neighbor not in closed_set:
                    diff = abs(neighbor.x - current.x) + abs(neighbor.y - current.y)
                    temp_g = current.g + diff
                    if neighbor not in open_set:
                        open_set.append(neighbor)
                    elif temp_g < neighbor.g:
                        neighbor.g = temp_g
                    neighbor.previous = current
                    neighbor.h = abs(neighbor.x - end.x) + abs(neighbor.y - end.y)
                    neighbor.f = neighbor.g + neighbor.h

        direction = 'NONE'
        if len(path) != 0:
            next_node = path[len(path) - 2]
            if next_node.x > sx:
                direction = 'RIGHT'
            elif next_node.x < sx:
                direction = 'LEFT'
            elif next_node.y > sy:
                direction = 'DOWN'
            elif next_node.y < sy:
                direction = 'UP'
        return direction

    def move(self, target, grid, target2=None):
        x, y, centre = self.get_grid_coord(self.get_pos())
        if target.activated_powered:
            self.frightened = True
        elif not target.powered:
            self.frightened = False
        if target.dot_counter > self.previous_dots and self.counting_dots:
            self.previous_dots = target.dot_counter
            self.time_since_dot = 0
            if self.counting_dots and not (self.global_dots > 0):
                self.dot_counter += 1
            elif self.global_dots > 0:
                self.global_dots -= 1
        elif self.time_since_dot < 240 and self.counting_dots:
            self.time_since_dot += 1
        elif not self.counting_dots:
            self.time_since_dot = 0

        self.frightened_ticks = target.powered_ticks
        if self.alive:
            collision = self.collide(target)
            if self.previous_state == 'NORMAL' and self.scatter:
                self.previous_state = 'SCATTER'
                self.change_direction = True
            elif self.previous_state == 'NORMAL' and self.frightened:
                self.previous_state = 'FRIGHTENED'
                self.change_direction = True
            elif self.previous_state == 'SCATTER' and self.frightened:
                self.previous_state = 'FRIGHTENED'
                self.change_direction = True
            elif self.previous_state == 'SCATTER' and not self.scatter:
                self.previous_state = 'NORMAL'
                self.change_direction = True
            elif self.previous_state == 'FRIGHTENED' and not (self.scatter or self.frightened):
                self.previous_state = 'NORMAL'
            elif self.previous_state == 'FRIGHTENED' and self.scatter and not self.frightened:
                self.previous_state = 'SCATTER'

            if not self.frightened:
                if 'TURN' in collision:
                    if not self.scatter:
                        self.reached_scatter = False
                        self.scatter_frame = 0
                        tx, ty = self.get_target_pos(target, target2)
                    elif not self.reached_scatter:
                        tx, ty = self.scatter_coords[self.scatter_frame]
                        if x == tx and y == ty:
                            self.reached_scatter = True
                            self.scatter_frame += 1
                            tx, ty = self.scatter_coords[self.scatter_frame % len(self.scatter_coords)]
                    else:
                        self.scatter_frame += 1
                        tx, ty = self.scatter_coords[self.scatter_frame % len(self.scatter_coords)]
                    self.current_direction = self.find_path(tx, ty, grid)
                if self.change_direction and centre:
                    self.change_direction = False
                    for direction in self.directions:
                        if direction != self.current_direction:
                            dx, dy = x + self.directions[direction][0], y + self.directions[direction][1]
                            if grid[dy][dx] != 1:
                                self.current_direction = direction
                                break
                if 'COLLIDE' in collision:
                    target.kill()
                if self.current_direction is not 'NONE':
                    self.previous_direction = self.current_direction
                d = self.directions[self.current_direction]
                if y == 14 and (x <= 5 or x >= 22):
                    v = self.v * self.tunnel_velocity
                else:
                    v = self.v * self.velocity_modifier
                self.x += d[0] * v
                self.y += d[1] * v
                self.rect.center = self.get_pos()
            else:
                if 'TURN' in collision:
                    directions = []
                    if self.current_direction == 'UP' or self.current_direction == 'DOWN':
                        directions = ['LEFT', 'RIGHT']
                    elif self.current_direction == 'LEFT' or self.current_direction == 'RIGHT':
                        directions = ['UP', 'DOWN']
                    random.shuffle(directions)
                    for i in range(len(directions)):
                        direction = self.directions[directions[i]]
                        if grid[y + direction[1]][x + direction[0]] != 1:
                            self.current_direction = directions[i]
                            break
                if self.change_direction and centre:
                    self.change_direction = False
                    for direction in self.directions:
                        if direction != self.current_direction:
                            dx, dy = x + self.directions[direction][0], y + self.directions[direction][1]
                            if grid[dy][dx] != 1:
                                self.current_direction = direction
                                break
                if 'COLLIDE' in collision:
                    self.dying = True
                    self.alive = False
                    self.frightened = False
                if self.current_direction is not 'NONE':
                    self.previous_direction = self.current_direction
                d = self.directions[self.current_direction]
                v = self.v * self.frightened_velocity
                self.x += d[0] * v
                self.y += d[1] * v
                self.rect.center = self.get_pos()

            if self.x <= 0:
                self.x = 28 * self.sf
                self.rect.centerx = self.x
            elif self.x >= 28 * self.sf:
                self.x = 0
                self.rect.centerx = self.x

            if not self.has_left:
                diff = abs(y - 11) + abs(x - 13.5)
                if diff > 2.5:
                    self.has_left = True
            else:
                self.counting_dots = False

        elif self.spawning:
            if self.dot_counter >= self.spawn_dots and self.counting_dots and self.global_dots <= 0:
                if self.x / self.sf < 14 and 14.6 > self.y / self.sf > 14.4:
                    self.current_direction = 'RIGHT'
                    v = self.v * self.dead_velocity
                    self.x += self.directions[self.current_direction][0] * v
                    self.y = 14.5 * self.sf
                    self.rect.center = self.get_pos()
                elif self.x / self.sf > 14 and 14.6 > self.y / self.sf > 14.4:
                    self.current_direction = 'LEFT'
                    v = self.v * self.dead_velocity
                    self.x += self.directions[self.current_direction][0] * v
                    self.y = 14.5 * self.sf
                    self.rect.center = self.get_pos()
                elif round(self.y / self.sf) > 11:
                    self.current_direction = 'UP'
                    v = self.v * self.dead_velocity
                    self.y += self.directions[self.current_direction][1] * v
                    self.rect.center = self.get_pos()
                else:
                    self.current_direction = 'LEFT'
                    self.counting_dots = False
                    self.spawning = False
                    self.alive = True
            else:
                if y >= 15:
                    self.current_direction = 'UP'
                elif y <= 13:
                    self.current_direction = 'DOWN'
                v = self.v * self.dead_velocity
                self.y += self.directions[self.current_direction][1] * v
                self.rect.center = self.get_pos()
        elif self.dying:
            collision = self.collide(target)
            self.previous_state = 'NORMAL'
            # ABOVE GHOST HOUSE
            if 14.1 >= self.x / self.sf >= 13.9 and 14.5 > self. y / self.sf >= 10.5:
                self.x = 14 * self.sf
                self.current_direction = 'DOWN'
            # IN GHOST HOUSE
            elif 15 > self.x / self.sf > 12 and 15 > self.y / self.sf > 13:
                self.y = 14.5 * self.sf
                if self.spawn_coords == 0:
                    self.current_direction = 'NONE'
                    self.dying = False
                    self.spawning = True
                    self.counting_dots = True
                elif self.spawn_coords < 0:
                    if self.x / self.sf > 12.5:
                        self.current_direction = 'LEFT'
                    else:
                        self.x = 12.5 * self.sf
                        self.dying = False
                        self.spawning = True
                        self.counting_dots = True
                else:
                    if self.x / self.sf < 14.5:
                        self.current_direction = 'RIGHT'
                    else:
                        self.x = 14.5 * self.sf
                        self.dying = False
                        self.spawning = True
                        self.counting_dots = True
            # NOT IN GHOST HOUSE OR ABOVE IT
            else:
                if 'TURN' in collision:
                    self.current_direction = self.find_path(14, 11, grid)

            if self.current_direction is not 'NONE':
                self.previous_direction = self.current_direction
            d = self.directions[self.current_direction]
            v = self.v * self.dying_velocity
            self.x += d[0] * v
            self.y += d[1] * v
            self.rect.center = self.get_pos()

            if self.x <= 0:
                self.x = 28 * self.sf
                self.rect.centerx = self.x
            elif self.x >= 28 * self.sf:
                self.x = 0
                self.rect.centerx = self.x

        elif self.respawning:
            pass

        if not self.frightened:
            self.scatter_tick += 1
            try:
                if self.scatter_tick > self.scatter_timings[self.scatter_step]:
                    self.scatter_step += 1
                    self.scatter_tick = 0
                    self.scatter = not self.scatter
            except:
                self.scatter = False

        if self.tick < 16:
            self.tick += 1
        else:
            self.tick = 0
        if self.frightened_ticks > 0:
            self.frightened_ticks -= 1
        else:
            self.frightened = False

    def collide(self, target):
        x, y, centre = self.get_grid_coord(self.get_pos())
        tx, ty, _, _ = target.get_grid_coord(target.get_pos())
        response = []
        if self.grid[y][x] == 2 and centre:
            response.append('TURN')
        if x == tx and y == ty and target.alive:
            response.append('COLLIDE')
        return response

    def reset_level(self):
        self.x, self.y = self.start_pos
        self.rect.center = (self.get_pos())
        self.current_direction = 'NONE'
        self.frightened = False
        self.frightened_ticks = 0
        self.previous_state = 'NORMAL'
        self.scatter = True
        self.scatter_frame = 0
        self.scatter_tick = 0
        self.scatter_step = 0
        self.has_left = False
        self.counting_dots = False
        self.dot_counter = 0
        self.previous_dots = 0
        self.time_since_dot = 0
        self.global_dots = 0
        self.dying = False

    def reset(self):
        self.x, self.y = self.start_pos
        self.rect.center = (self.get_pos())
        self.current_direction = 'NONE'
        self.frightened = False
        self.frightened_ticks = 0
        self.previous_state = 'NORMAL'
        self.time_since_dot = 0
        self.global_dots = self.respawn_dots
        self.has_left = False
        self.counting_dots = False
        self.previous_dots = 0
        self.dying = False
