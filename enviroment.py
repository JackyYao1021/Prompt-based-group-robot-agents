class Environment:
    def __init__(self, map_file):
        self.grid = self.load_map(map_file)
        self.start_positions = self.find_positions('S')
        self.end_position = self.find_positions('E')[0]
        # 可扩展：self.targets = self.find_positions('f')

    def load_map(self, map_file):
        with open(map_file, 'r') as f:
            return [list(line.strip()) for line in f.readlines()]

    def find_positions(self, symbol):
        positions = []
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == symbol:
                    positions.append((x, y))
        return positions

    def is_free(self, x, y):
        return self.grid[y][x] in ('.', 'S', 'E', 'f')