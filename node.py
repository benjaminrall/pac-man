class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.t = 0
        self.forbidden_directions = [(12, 11), (12, 23), (15, 11), (15, 23)]
        self.neighbors = []
        self.previous = None

    def find_neighbors(self, node_grid, direction):
        x, y = self.x, self.y
        try:
            if self.t is not 1 or direction is not 'LEFT':
                for i in range(x + 1, len(node_grid[y])):
                    if node_grid[y][i] is not None:
                        if node_grid[y][i] is not 1:
                            self.neighbors.append(node_grid[y][i])
                        break
            if self.t is not 1 or direction is not 'UP':
                for i in range(y + 1, len(node_grid)):
                    if node_grid[i][x] is not None:
                        if node_grid[i][x] is not 1:
                            self.neighbors.append(node_grid[i][x])
                        break
            if self.t is not 1 or direction is not 'RIGHT':
                for i in range(x - 1, - 1, - 1):
                    if node_grid[y][i] is not None:
                        if node_grid[y][i] is not 1:
                            self.neighbors.append(node_grid[y][i])
                        break
            if (self.t is not 1 or direction is not 'DOWN') and not (self.x, self.y) in self.forbidden_directions:
                for i in range(y - 1, - 1, - 1):
                    if node_grid[i][x] is not None:
                        if node_grid[i][x] is not 1:
                            self.neighbors.append(node_grid[i][x])
                        break
        except:
            pass
