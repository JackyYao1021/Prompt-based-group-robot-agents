from robot import Robot

class Controller(Robot):
    def __init__(self, position, robot_id):
        """
        Initialize the Controller robot
        :param position: (x, y) tuple representing the robot's position
        :param robot_id: Unique identifier for the robot
        """
        super().__init__(position, robot_id)
        self.excavators = []
        self.target_letters = {}
        self.task_queue = []
        self.command_history = []
        
    
    def add_excavator(self, excavator):
        """
        Add an excavator to the controller's management
        :param excavator: Excavator robot instance
        """
        self.excavators.append(excavator)
        self.command_history.append({
            'type': 'add_excavator',
            'excavator_id': excavator.robot_id
        })

    def assign_tasks(self, assignment_method='nearest'):
        """
        Assign tasks to excavators based on different assignment strategies
        :param assignment_method: Strategy for task assignment ('nearest', 'round_robin', 'load_balanced')
        :return: List of assigned tasks
        """
        tasks = []
        available_excavators = [e for e in self.excavators if not e.has_target]
        
        if not available_excavators or not self.target_letters:
            return tasks
            
        if assignment_method == 'nearest':
            tasks = self._assign_nearest(available_excavators)
        elif assignment_method == 'round_robin':
            tasks = self._assign_round_robin(available_excavators)
        elif assignment_method == 'load_balanced':
            tasks = self._assign_load_balanced(available_excavators)
            
        return tasks
        
    def _assign_nearest(self, available_excavators):
        """Assign tasks to the nearest available excavator"""
        tasks = []
        for letter, target_pos in self.target_letters.items():
            if not available_excavators:
                break
                
            # Find the nearest excavator to the target
            nearest_excavator = min(
                available_excavators,
                key=lambda e: self.calculate_distance(e.position, target_pos)
            )
            
            # Create and assign task
            task = {
                'excavator': nearest_excavator,
                'target_letter': letter,
                'target_position': target_pos
            }
            tasks.append(task)
            
            # Remove assigned excavator from available list
            available_excavators.remove(nearest_excavator)
            
        return tasks
        
    def _assign_round_robin(self, available_excavators):
        """Assign tasks in a round-robin fashion"""
        tasks = []
        excavator_index = 0
        
        for letter, target_pos in self.target_letters.items():
            if not available_excavators:
                break
                
            # Get next excavator in round-robin fashion
            excavator = available_excavators[excavator_index]
            
            task = {
                'excavator_id': excavator.robot_id,
                'target_letter': letter,
                'target_position': target_pos
            }
            tasks.append(task)
            
            # Update index for next assignment
            excavator_index = (excavator_index + 1) % len(available_excavators)
            
        return tasks
        
    def _assign_load_balanced(self, available_excavators):
        """Assign tasks to balance the workload among excavators"""
        tasks = []
        excavator_loads = {e.robot_id: 0 for e in available_excavators}
        
        for letter, target_pos in self.target_letters.items():
            if not available_excavators:
                break
                
            # Find excavator with minimum current load
            min_load_excavator = min(
                available_excavators,
                key=lambda e: excavator_loads[e.robot_id]
            )
            
            task = {
                'excavator_id': min_load_excavator.robot_id,
                'target_letter': letter,
                'target_position': target_pos
            }
            tasks.append(task)
            
            # Update load for the assigned excavator
            excavator_loads[min_load_excavator.robot_id] += 1
            
        return tasks

    def get_command_history(self):
        """
        Get the history of all commands issued
        :return: List of command records
        """
        return self.command_history

    def perform_task(self, maze):
        """
        Perform the controller's task of coordinating scouts and excavators
        :param maze: 2D list representing the maze
        :return: List of assigned tasks
        """
        if self.process_scout_reports():
            return self.assign_tasks()
        return []

    def calculate_distance(self, pos1, pos2):
        """
        Calculate Manhattan distance between two positions
        :param pos1: First position (x, y)
        :param pos2: Second position (x, y)
        :return: Manhattan distance
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) 
    
    
    def recieve_target_letter(self, letters: dict):
        for letter, position in letters.items():
            if letter not in self.target_letters:
                self.target_letters[letter] = position
            else:
                print(f"Duplicate letter: {letter}")
                
                