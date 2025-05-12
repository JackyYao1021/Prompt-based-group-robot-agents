import pandas as pd
import os
import re
from Utils import load_maze, find_start_position
from visualizer import MazeVisualizer
from matplotlib import pyplot as plt
from controller import Controller
from excavator import Excavator

def experiment_1():
    times_dict = {} 
    path_lengths_dict = {}
    for file in os.listdir("./results/experiment_1"):
        print(file)
        with open(f"./results/experiment_1/{file}", "r") as f:
            lines = f.readlines()
            times = []
            path_lengths = []
            for line in lines:
                if "maze" in line:
                    maze_number = int(line.split(" ")[1])
                if "time taken" in line:
                    time = float(line.split(":")[1].split(" ")[1])
                    times.append(time)
                if "path length" in line:
                    path_length = int(line.split(":")[1].strip())
                    path_lengths.append(path_length)
            times_dict[file] = times
            path_lengths_dict[file] = path_lengths

    print(times_dict)   
    print(path_lengths_dict)

    df_times = pd.DataFrame(times_dict)
    df_path_lengths = pd.DataFrame(path_lengths_dict)

    print(df_times.to_latex())
    print(df_path_lengths.to_latex())


def experiment_2():
    task_assignment_times = {}  
    pathfinding_times = {}      
    path_lengths = {}           
    
    for file in os.listdir("./results/experiment_2"):
        with open(f"./results/experiment_2/{file}", "r") as f:
            lines = f.readlines()
            maze_task_assignment_times = []
            maze_pathfinding_times = []
            maze_total_path_lengths = []
            
            for line in lines:
                if "maze" in line and "number of" not in line:
                    maze_number = int(line.split(" ")[1])
                
                if "Time for task assignment" in line:
                    time = float(line.split(":")[1].strip().split(" ")[0])
                    maze_task_assignment_times.append(time)

                if "Time for pathfinding" in line:
                    time = float(line.split(":")[1].strip().split(" ")[0])
                    maze_pathfinding_times.append(time)

                if "total path length" in line:
                    length = int(line.split(":")[1].strip())
                    maze_total_path_lengths.append(length)
                    
            task_assignment_times[file] = maze_task_assignment_times
            pathfinding_times[file] = maze_pathfinding_times
            path_lengths[file] = maze_total_path_lengths
            
    df_task_assignment_times = pd.DataFrame(task_assignment_times)
    df_pathfinding_times = pd.DataFrame(pathfinding_times)
    df_path_lengths = pd.DataFrame(path_lengths)

    print(df_task_assignment_times.to_latex())
    print(df_pathfinding_times.to_latex())
    print(df_path_lengths.to_latex())
    
def visualise_maze(maze_number):
    maze, _ = load_maze(f"./mazes/maze_{maze_number}.txt")
    
    start_position = find_start_position(maze)
    excavators = [Excavator(start_position, 0)]
    robots = {
        'excavators': excavators,
    }
    visualizer = MazeVisualizer(maze, robots)  
    while True: 
        visualizer.plot_maze()
        visualizer.plot_robots()
        plt.pause(0.2)


if __name__ == "__main__":
    # experiment_2()
    # visualise_maze(0)
