import pandas as pd
import os
import re
from Utils import load_maze, find_start_position
from visualizer import MazeVisualizer
from matplotlib import pyplot as plt
from controller import Controller
from excavator import Excavator
import numpy as np

def experiment_1():
    times_dict = {} 
    path_lengths_dict = {}
    for file in os.listdir("./results/experiment_1"):
        # print(file)
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
            times_dict[file.split(".")[0]] = times
            path_lengths_dict[file.split(".")[0]] = path_lengths

    # print(times_dict)   
    # print(path_lengths_dict)

    df_times = pd.DataFrame(times_dict)
    df_path_lengths = pd.DataFrame(path_lengths_dict)

    # print(df_times.to_latex())
    # print(df_path_lengths.to_latex())
    return df_times, df_path_lengths


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
                    
            task_assignment_times[file.split(".")[0]] = maze_task_assignment_times
            pathfinding_times[file.split(".")[0]] = maze_pathfinding_times
            path_lengths[file.split(".")[0]] = maze_total_path_lengths
            
    df_task_assignment_times = pd.DataFrame(task_assignment_times)
    df_pathfinding_times = pd.DataFrame(pathfinding_times)
    df_path_lengths = pd.DataFrame(path_lengths)

    print(df_task_assignment_times.to_latex())
    print(df_pathfinding_times.to_latex())
    print(df_path_lengths.to_latex())
    
    return df_task_assignment_times, df_pathfinding_times, df_path_lengths
    
def visualise_maze(maze_number, save_path=None):
    maze, _ = load_maze(f"./mazes/maze_{maze_number}.txt")
    
    start_position = find_start_position(maze)
    excavators = [Excavator(start_position, 0)]
    robots = {
        'excavators': excavators,
    }
    visualizer = MazeVisualizer(maze, robots)  
    visualizer.plot_maze()
    visualizer.plot_robots()
    # while True: 
    #     visualizer.plot_maze()
    #     visualizer.plot_robots()
    #     plt.pause(0.2)
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def visualize_execution_times(time_data, log_scale=False, title="Execution Time of Algorithms Across Mazes"):
    time_data = time_data.T
    algorithms = time_data.index.tolist()
    n_algorithms = len(algorithms)
    n_mazes = time_data.shape[1]
    x = np.arange(n_algorithms)
    bar_width = 0.05
    
    offsets = np.linspace(-bar_width*5, bar_width*5, n_mazes)
    
    plt.figure(figsize=(12, 6))
    if log_scale:
        plt.yscale('log')
    for i in range(n_mazes):
        plt.bar(x + offsets[i], time_data.iloc[:, i], width=bar_width, label=f'Maze {i}')
    
    plt.xticks(x, algorithms)
    plt.xlabel('Algorithm')
    plt.ylabel('Execution Time (seconds)')
    plt.title(title)
    plt.legend(title='Maze', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # experiment_2()
    # visualise_maze(0)
    # time, path = experiment_1()
    
    ## experiment 2
    # df_task_assignment_times, df_pathfinding_times, df_path_lengths = experiment_2()
    # print(df_task_assignment_times)
    # visualize_execution_times(df_task_assignment_times, log_scale=True, title="Execution Time of Task Assignment Algorithms Across 10 Mazes")
    # visualize_execution_times(df_pathfinding_times, "Execution Time of Pathfinding Algorithms Across 10 Mazes")
    
    
    ## experiment 1
    # time = time.iloc[:-2, :]
    # visualize_execution_times(time, "Execution Time of Pathfinding Algorithms Across 10 Mazes")
    
    for i in range(10):
        visualise_maze(i, f"./diagrams/maze_{i}.png")
    
