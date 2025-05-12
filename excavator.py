from collections import deque
from robot import Robot
import heapq
from search_algorithms import BFSFinder, AStarFinder, DijkstraFinder, GBFSFinder, DFSFinder

class Excavator(Robot):
    def __init__(self, position, robot_id):
        super().__init__(position, robot_id)
        self.id = robot_id
        self.target = None
        self.path = []
        self.has_target = False
        self.mission_history = []
        self.explored_nodes = []
        self.maze = None
        self.path_finder = None
        
    def set_task(self, task):
        self.target = task['target_position']
        self.path = []
        self.mission_history.append({
            'type': 'set_target',
            'target': task['target_letter'],
            'position': self.position
        })
        self.has_target = True


    def set_maze(self, maze):
        self.maze = maze
        
    def set_path_finder(self, path_finder):
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
        if self.path:
            next_pos = self.path[1] if len(self.path) > 1 else self.path[0]
            self.position = next_pos
            self.path.pop(0)  
        else:
            self.has_target = False
        

    def grab_target(self):
        self.has_target = True
        self.mission_history.append({
            'type': 'grab_target',
            'position': self.position,
            'target': self.target
        })

    def release_target(self):
        self.has_target = False
        self.mission_history.append({
            'type': 'release_target',
            'position': self.position
        })

    def get_mission_history(self):
        return self.mission_history