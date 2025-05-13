from abc import ABC, abstractmethod
from collections import deque
import heapq
from typing import List, Tuple, Set, Optional

class PathFinder(ABC):
    def __init__(self, maze):
        self.maze = maze
        self.directions = [(-1,0), (1,0), (0,-1), (0,1)]
    
    @abstractmethod
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        pass
    
    def in_bounds(self, x, y):
        return 0 <= x < len(self.maze) and 0 <= y < len(self.maze[0])

    def is_walkable(self, x, y):
        return self.maze[x][y] != '#'

class BFSFinder(PathFinder):
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        queue = deque()
        queue.append((start, [start]))
        visited = set()
        
        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == goal:
                return path
                
            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and self.is_walkable(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        return []

class AStarFinder(PathFinder):
    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        heap = [(0 + self.heuristic(start, goal), 0, start)]
        visited = set()
        cost_so_far = {start: 0}
        came_from = {start: None}

        while heap:
            _, cost, current = heapq.heappop(heap)
            if current == goal:
                break
            if current in visited:
                continue
            visited.add(current)

            for dx, dy in self.directions:
                nx, ny = current[0] + dx, current[1] + dy
                if self.in_bounds(nx, ny) and self.is_walkable(nx, ny) and (nx, ny) not in visited:
                    new_cost = cost_so_far[current] + 1
                    neighbor = (nx, ny)
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        priority = new_cost + self.heuristic(neighbor, goal)
                        came_from[neighbor] = current
                        heapq.heappush(heap, (priority, new_cost, neighbor))

        path = []
        node = goal
        while node:
            path.append(node)
            node = came_from.get(node)
        return path[::-1] if goal in came_from else []
        

class DFSFinder(PathFinder):
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        stack = [(start, [start])]
        visited = set()
        
        while stack:
            (x, y), path = stack.pop()
            if (x, y) == goal:
                return path
                
            if (x, y) in visited:
                continue
                
            visited.add((x, y))
            
            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and self.is_walkable(nx, ny) and (nx, ny) not in visited:
                    stack.append(((nx, ny), path + [(nx, ny)]))
        return []
    
    
class DijkstraFinder(PathFinder):
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        heap = [(0, start)]
        visited = set()
        distances = {start: 0}
        previous = {start: None}
        
        while heap:
            current_distance, current = heapq.heappop(heap)
            
            if current == goal:
                break
                
            if current in visited:
                continue
                
            visited.add(current)
            
            for dx, dy in self.directions:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)
                if self.in_bounds(nx, ny) and self.is_walkable(nx, ny) and neighbor not in visited:
                    new_distance = current_distance + 1
                    if neighbor not in distances or new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current
                        heapq.heappush(heap, (new_distance, neighbor))
        
        path = []
        node = goal
        while node:
            path.append(node)
            node = previous.get(node)
        return path[::-1] if goal in previous else []

class GBFSFinder(PathFinder):
    def heuristic(self, a, b):  
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        heap = [(self.heuristic(start, goal), start)]
        came_from = {start: None}
        visited = set()

        while heap:
            _, current = heapq.heappop(heap)
            if current == goal:
                break
            visited.add(current)

            for dx, dy in self.directions:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)
                if self.in_bounds(nx, ny) and self.is_walkable(nx, ny) and neighbor not in visited:
                    if neighbor not in came_from:
                        came_from[neighbor] = current
                        heapq.heappush(heap, (self.heuristic(neighbor, goal), neighbor))
        path = []
        node = goal
        while node:
            path.append(node)
            node = came_from.get(node)
        return path[::-1] if goal in came_from else []
            