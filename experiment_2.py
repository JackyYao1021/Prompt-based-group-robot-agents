import pandas as pd
from controller import Controller
from excavator import Excavator

from Utils import load_maze, find_start_position, find_valid_positions
import random   
import time 
from visualizer import MazeVisualizer
import matplotlib.pyplot as plt

random.seed(0)  

number_of_excavators = 10
show_animation = True
note_results = False

if __name__ == "__main__":
    task_assign_methods = ["random", "nearest", "simple_hungarian", "hungarian", "bid"]
            
    for task_assign_method in task_assign_methods:
        if note_results:
            with open(f"./results/experiment_2/{task_assign_method}.txt", "w") as f:
                f.write("Experiment 2\n")
                f.write(f"number of excavators: {number_of_excavators}\n")
                f.write(f"number of mazes: 10\n")
                f.write(f"number of task assign methods: {len(task_assign_methods)}\n")
            
    for i in range(10):
        maze, letters_positions = load_maze(f"./mazes/maze_{i}.txt")
        valid_positions = find_valid_positions(maze)
        controller_start_pos = find_start_position(maze)
        excavators_start_positions = random.sample(valid_positions, number_of_excavators)   
        letters = random.sample(letters_positions.keys(), number_of_excavators)
        
        for task_assign_method in task_assign_methods:
            controller = Controller(controller_start_pos, "C1")   
        
            letters_positions = {letter: letters_positions[letter] for letter in letters}
            controller.recieve_target_letter(letters_positions)
            
            for j in range(number_of_excavators):
                excavator = Excavator(excavators_start_positions[j], f"E{j+1}")
                excavator.set_maze(maze)
                excavator.set_path_finder("AStar")
                controller.add_excavator(excavator)
                
            if note_results:
                with open(f"./results/experiment_2/{task_assign_method}.txt", "a") as f:
                    f.write(f"maze {i}\n")
                    f.write(f"number of excavators: {number_of_excavators}\n")
                    f.write(f"letters: {letters}\n")
                    f.write(f"letters positions: {letters_positions}\n")
                
            time_start = time.time()
            controller.assign_tasks(task_assign_method)
            time_end = time.time()
            
            if note_results:
                with open(f"./results/experiment_2/{task_assign_method}.txt", "a") as f:
                    f.write(f"Time for task assignment: {time_end - time_start} seconds\n")
                    for excavator in controller.excavators:
                        f.write(f"excavator {excavator.id} current position: {excavator.position}\n")
                        f.write(f"excavator {excavator.id} target letter: {excavator.target}\n")
                
            time_start = time.time()    
            for excavator in controller.excavators:
                excavator.path = excavator.find_path()
            time_end = time.time()
            if note_results:
                with open(f"./results/experiment_2/{task_assign_method}.txt", "a") as f:
                    f.write(f"Time for pathfinding: {time_end - time_start} seconds\n")

            if note_results:
                with open(f"./results/experiment_2/{task_assign_method}.txt", "a") as f:
                    total_path_length = 0
                    for excavator in controller.excavators:
                        f.write(f"excavator {excavator.id} path: {excavator.path}\n")
                        f.write(f"excavator {excavator.id} path length: {len(excavator.path)}\n")
                        total_path_length += len(excavator.path)
                    f.write(f"total path length: {total_path_length}\n")
                    
            if show_animation:        
                robots = {
                    'excavators': controller.excavators,
                    'controller': controller
                }
            
            
                visualizer = MazeVisualizer(maze, robots)
                while True: 
                    visualizer.plot_maze()
                    visualizer.plot_robots()
                    
                    plt.pause(0.2)
                    for excavator in controller.excavators:
                        excavator.move()
                    if all(not excavator.has_target for excavator in controller.excavators):
                        break
                plt.close()
                    
                
                    
                    
