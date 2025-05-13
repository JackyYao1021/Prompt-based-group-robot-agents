from robot import Robot
import random
import numpy as np
from scipy.optimize import linear_sum_assignment
from excavator import Excavator

class Controller(Robot):
    def __init__(self, position, robot_id):
        super().__init__(position, robot_id)
        self.excavators = []
        self.target_letters = {}
        self.command_history = []
        
    
    def add_excavator(self, excavator):
        self.excavators.append(excavator)
        self.command_history.append({
            'type': 'add_excavator',
            'excavator_id': excavator.robot_id
        })

    def assign_tasks(self, assignment_method='nearest'):
        tasks = []
        available_excavators = [e for e in self.excavators if not e.has_target]
            
        if assignment_method == 'nearest':
            tasks = self._assign_nearest(available_excavators)
        elif assignment_method == 'random':
            tasks = self._assign_random(available_excavators)
        elif assignment_method == 'simple_hungarian':
            tasks = self._assign_simple_hungarian(available_excavators)
        elif assignment_method == 'hungarian':
            tasks = self._assign_hungarian(available_excavators)
        elif assignment_method == 'bid':
            tasks = self._assign_bid_algorithm(available_excavators)
        return tasks
        
    def _assign_nearest(self, available_excavators):
        tasks = []
        for letter, target_pos in self.target_letters.items():
            if not available_excavators:
                break
                
            nearest_excavator = min(
                available_excavators,
                key=lambda e: self.calculate_distance(e.position, target_pos)
            )
            
            task = {
                'excavator': nearest_excavator,
                'target_letter': letter,
                'target_position': target_pos
            }
            tasks.append(task)
            
            nearest_excavator.set_task(task)
            
            available_excavators.remove(nearest_excavator)
            
        return tasks
        
    
    def _assign_random(self, available_excavators):
        tasks = []
        for letter, target_pos in self.target_letters.items():
            if not available_excavators:
                break
            
            excavator = random.choice(available_excavators)
            task = {
                'excavator': excavator,
                'target_letter': letter,
                'target_position': target_pos
            }
            tasks.append(task)
            
            excavator.set_task(task)
            
            available_excavators.remove(excavator)
            
        return tasks
        
        
    def _assign_simple_hungarian(self, available_excavators):
        tasks = []      

        cost_matrix = np.array([[self.calculate_distance(excavator.position, target) for target in self.target_letters.values()] for excavator in available_excavators])

        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        for excavator_index, letter_index in zip(row_ind, col_ind):
            task = {
                'excavator': available_excavators[excavator_index],
                'target_letter': list(self.target_letters.keys())[letter_index],
                'target_position': list(self.target_letters.values())[letter_index]
            }
            tasks.append(task)
            
            available_excavators[excavator_index].set_task(task)
            
        return tasks
    
    def _assign_hungarian(self, available_excavators):
        tasks = []
        
        def heuristic(excavator: Excavator, target):
            excavator.set_task({'target_letter': target[0], 'target_position': target[1]})
            return len(excavator.find_path())


        cost_matrix = np.array([[heuristic(excavator, target) for target in self.target_letters.items()] for excavator in available_excavators])

        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        for excavator_index, letter_index in zip(row_ind, col_ind):
            task = {
                'excavator': available_excavators[excavator_index],
                'target_letter': list(self.target_letters.keys())[letter_index],
                'target_position': list(self.target_letters.values())[letter_index]
            }
            tasks.append(task)
            
            available_excavators[excavator_index].set_task(task)
            
        return tasks
    
    def _assign_bid_algorithm(self, available_excavators):
        tasks = []
        unassigned_targets = list(self.target_letters.items())
        
        prices = {target[0]: 0 for target in unassigned_targets}
        
        while unassigned_targets and available_excavators:
            bids = {}
            
            for excavator in available_excavators:
                best_bid = float('inf')
                best_target = None
                
                for target in unassigned_targets:
                    excavator.set_task({'target_letter': target[0], 'target_position': target[1]})
                    path = excavator.find_path()
                    cost = len(path) if path else float('inf')
                    
                    bid = cost - prices[target[0]]
                    
                    if bid < best_bid:
                        best_bid = bid
                        best_target = target
                
                if best_target:
                    bids[excavator] = (best_target, best_bid)
            
            if not bids:
                break
            
            best_excavator = min(bids.items(), key=lambda x: x[1][1])[0]
            best_target, best_bid = bids[best_excavator]
            
            prices[best_target[0]] += best_bid
            
            task = {
                'excavator': best_excavator,
                'target_letter': best_target[0],
                'target_position': best_target[1]
            }
            tasks.append(task)
            
            available_excavators.remove(best_excavator)
            unassigned_targets.remove(best_target)
            
            best_excavator.set_task(task)
        
        return tasks

    def get_command_history(self):
        return self.command_history


    def calculate_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) 
    
    
    def recieve_target_letter(self, letters: dict):
        for letter, position in letters.items():
            if letter not in self.target_letters:
                self.target_letters[letter] = position
            else:
                print(f"Duplicate letter: {letter}")
                
                