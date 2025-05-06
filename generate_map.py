import random

def generate_maze(width, height):
    # 保证奇数尺寸，方便迷宫生成
    width = width if width % 2 == 1 else width + 1
    height = height if height % 2 == 1 else height + 1

    maze = [['#'] * width for _ in range(height)]

    def carve(x, y):
        maze[y][x] = '.'
        dirs = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width-1 and 1 <= ny < height-1 and maze[ny][nx] == '#':
                maze[y + dy//2][x + dx//2] = '.'
                carve(nx, ny)

    # 从左下角开始
    carve(1, height-2)

    # 设置起点和终点
    maze[height-2][1] = 'S'
    maze[1][width-2] = 'E'
    return maze

def save_map(grid, filename):
    with open(filename, 'w') as f:
        for row in grid:
            f.write(' '.join(row) + '\n')

if __name__ == "__main__":
    width, height = 21, 21  # 建议用奇数
    maze = generate_maze(width, height)
    save_map(maze, 'map.txt')
    print("联通迷宫已生成并保存到 map.txt")