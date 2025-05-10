from robot import Robot

class Scout(Robot):
    def __init__(self, position, robot_id, radar_range=3):
        """
        Initialize the Scout robot
        :param position: (x, y) tuple representing the robot's position
        :param robot_id: Unique identifier for the robot
        :param radar_range: The range within which the scout can detect letters
        """
        super().__init__(position, robot_id)
        self.radar_range = radar_range
        self.detected_letters = {}  # Dictionary to store detected letters and their positions
        self.scan_history = []  # List to store historical scan results
        self.visited_positions = {position}  # Set to store visited positions

    def get_unvisited_moves(self, valid_moves):
        """
        Get moves that haven't been visited yet
        :param valid_moves: List of valid moves
        :return: List of unvisited valid moves
        """
        return [pos for pos in valid_moves if pos not in self.visited_positions]
    
    def move(self, new_position):
        """
        Move the robot to a new position
        :param new_position: (x, y) tuple representing the new position
        """
        super().move(new_position)
        self.visited_positions.add(new_position)

    def scan_area(self, maze):
        """
        Scan the surrounding area for letters within radar range
        :param maze: 2D list representing the maze
        :return: Dictionary of detected letters and their positions
        """

        self.detected_letters.clear()
        x, y = self.position
        
        # Scan in a square around the robot
        for i in range(max(0, x - self.radar_range), min(len(maze), x + self.radar_range + 1)):
            for j in range(max(0, y - self.radar_range), min(len(maze[0]), y + self.radar_range + 1)):
                if maze[i][j].isalpha() and maze[i][j] != '#':
                    self.detected_letters[maze[i][j]] = (i, j)
        
        # Record scan history
        self.scan_history.append({
            'position': self.position,
            'detected_letters': self.detected_letters.copy()
        })
        
        return self.detected_letters

    def get_scan_history(self):
        """
        Get the history of all scans performed
        :return: List of scan results
        """
        return self.scan_history

    def perform_task(self, maze):
        """
        Perform the scout's task of scanning the area
        :param maze: 2D list representing the maze
        :return: Dictionary of detected letters and their positions
        """
        return self.scan_area(maze) 