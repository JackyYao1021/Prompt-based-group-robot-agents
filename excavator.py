from collections import deque
from robot import Robot
import heapq
from search_algorithms import BFSFinder, AStarFinder, DijkstraFinder, GBFSFinder, DFSFinder

class Excavator(Robot):
    def __init__(self, position, robot_id):
        """
        Initialize the Excavator robot
        :param position: (x, y) tuple representing the robot's position
        :param robot_id: Unique identifier for the robot
        """
        super().__init__(position, robot_id)
        self.id = robot_id
        self.target = None
        self.path = []
        self.has_target = False
        self.mission_history = []  # List to store mission history
        self.explored_nodes = []  # 记录探索过的节点
        self.maze = None
        self.path_finder = None
        
    def set_task(self, task):
        """
        Set the target position for the excavator
        :param target_position: (x, y) tuple representing the target position
        """
        self.target = task['target_position']
        self.path = []
        self.mission_history.append({
            'type': 'set_target',
            'target': task['target_letter'],
            'position': self.position
        })


    def set_maze(self, maze):
        """
        Set the maze for the excavator
        :param maze: 2D list representing the maze
        """
        self.maze = maze
        
    def set_path_finder(self, path_finder):
        """
        Set the path finder for the excavator
        :param path_finder: PathFinder object
        """
        if path_finder == "BFS":
            self.path_finder = BFSFinder(self.maze)
        elif path_finder == "AStar":
            self.path_finder = AStarFinder(self.maze)
        elif path_finder == "Dijkstra":
            self.path_finder = DijkstraFinder(self.maze)
        elif path_finder == "GBFS":
            self.path_finder = GBFSFinder(self.maze)
        elif path_finder == "DFS":
            self.path_finder = DFSFinder(self.maze)
        
    def find_path(self):
        """
        Find path to target using the path finder
        :return: List of positions representing the path to target
        """
        return self.path_finder.find_path(self.position, self.target)

    
    def move(self):
        """
        Move the excavator to the next position
        :param next_pos: (x, y) tuple representing the next position
        """
        next_pos = self.path[1] if len(self.path) > 1 else self.path[0]
        self.position = next_pos
        self.path.pop(0)        
        

    def grab_target(self):
        """
        Mark that the excavator has grabbed the target
        """
        self.has_target = True
        self.mission_history.append({
            'type': 'grab_target',
            'position': self.position,
            'target': self.target
        })

    def release_target(self):
        """
        Mark that the excavator has released the target
        """
        self.has_target = False
        self.mission_history.append({
            'type': 'release_target',
            'position': self.position
        })

    def get_mission_history(self):
        """
        Get the history of all missions performed
        :return: List of mission records
        """
        return self.mission_history

    def perform_task(self, maze):
        """
        Perform the excavator's task of finding and moving to target
        :param maze: 2D list representing the maze
        :return: List of positions representing the path to target
        """
        return self.find_path(maze)