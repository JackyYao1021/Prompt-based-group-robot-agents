import random
import string

def generate_maze(width, height, num_letters, extra_paths=0):
    
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

    carve(1, height-2)
    
    walls = find_walls(maze)
    for i in range(extra_paths):
        random_wall = random.choice(walls)
        maze[random_wall[1]][random_wall[0]] = '.'  
        print(f"Extra path {i+1} carved at ({random_wall[0]}, {random_wall[1]})")
        
    letters = insert_letters(maze, num_letters)
    
    maze[height-2][1] = 's'
    
    return maze, letters


def insert_letters(maze, num_letters):
    height = len(maze)
    width = len(maze[0])
    
    empty_cells = [(x, y) for y in range(height) for x in range(width) if maze[y][x] == '.']
    
    chosen_cells = random.sample(empty_cells, min(num_letters, len(empty_cells)))
    
    letters = string.ascii_uppercase[:len(chosen_cells)]
    letter_positions = {}
    for (x, y), letter in zip(chosen_cells, letters):
        print(f"Inserting letter {letter} at ({x}, {y})")
        maze[y][x] = letter
        letter_positions[letter] = (x, y)
    return letter_positions


def load_maze(filename):
    """
    Load maze from file
    :param filename: Name of the map file
    :return: 2D list representing the maze
    """
    with open(filename, 'r') as f:
        maze = [line.strip().split() for line in f.readlines()]
        letters = find_letters(maze)
    return maze, letters

def save_maze(maze, filename):
    """
    Save the maze to a file
    :param maze: 2D list representing the maze
    :param filename: Name of the file to save the maze
    """
    with open(filename, 'w') as f:
        for row in maze:
            f.write(' '.join(str(cell) for cell in row) + '\n')
            
def find_start_position(maze):
    """
    Find the start position (S) in the maze
    :param maze: 2D list representing the maze
    :return: (x, y) tuple of start position
    """
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 's':
                return (i, j)
    return (1, 1) 

def get_valid_moves(maze, current_pos):
    """
    Get valid moves from current position
    :param maze: 2D list representing the maze
    :param current_pos: Current position (x, y)
    :return: List of valid moves
    """
    x, y = current_pos
    valid_moves = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < len(maze) and 
            0 <= new_y < len(maze[0]) and 
            maze[new_x][new_y] != '#'):
            valid_moves.append((new_x, new_y))
    return valid_moves

def find_valid_positions(maze):
    """
    Find all valid positions in the maze
    :param maze: 2D list representing the maze
    :return: List of valid positions
    """
    return [(i, j) for i in range(len(maze)) for j in range(len(maze[0])) if maze[i][j] != '#']

def find_walls(maze):
    """
    Find all walls inside the maze
    :param maze: 2D list representing the maze
    :return: List of walls
    """
    return [(i, j) for i in range(1,len(maze)-1) for j in range(1,len(maze[0])-1) if maze[i][j] == '#']


def find_letters(maze):
    """
    Find all letters in the maze
    :param maze: 2D list representing the maze
    :return: List of letters
    """
    letters = {}
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] in string.ascii_uppercase:
                letters[maze[i][j]] = (i, j)
    return letters


def ask_target_letters(letter_positions):
    
    # letters = input("Please enter the target letters: ").upper()
    letters = "A"
    if letters in letter_positions:
        letters = {letters: letter_positions[letters]}
        return letters
    else:
        print(f"Invalid letter! Available letters: {', '.join(sorted(letter_positions.keys()))}")
        return ask_target_letters()
