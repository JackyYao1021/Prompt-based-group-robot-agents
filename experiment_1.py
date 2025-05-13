from Utils import generate_maze, save_maze, load_maze, find_start_position, find_valid_positions, ask_target_letters
from visualizer import MazeVisualizer
from controller import Controller
from excavator import Excavator
from matplotlib import pyplot as plt    
import random
import time 


def maze_preparation(width, height, number_of_targets, extra_paths=0):
    """
    Generate 10 mazes with different number of targets and save them to a file
    """
    for i in range(10):
        maze, letters_positions = generate_maze(width, height, number_of_targets, extra_paths)
        save_maze(maze, f"./mazes/maze_{i}.txt")


# if __name__ == "__main__":
#     maze_preparation(21, 21, 20, extra_paths=60)

show_animation = True
note_results = False

if __name__ == "__main__":
    
    path_finders = ["DFS", "BFS", "AStar", "Dijkstra", "GBFS"]
    
    for path_finder in path_finders:
    
        number_of_excavators = 1
        if note_results:
            with open(f"./results/{path_finder}.txt", "w") as f:
                f.write(f"")
            
        total_time = 0
            
        for i in range(10):
            maze, letters_positions = load_maze(f"./mazes/maze_{i}.txt")
            start_pos = find_start_position(maze)
            controller = Controller(start_pos, "C1")
            valid_positions = find_valid_positions(maze)
            excavators = []
            for j in range(number_of_excavators):
                excavator = Excavator(start_pos,f"E{j+1}")
                excavator.set_maze(maze)
                excavator.set_path_finder(path_finder)
                excavators.append(excavator)
                controller.add_excavator(excavator)
                
            robots = {
                'excavators': excavators,
                'controller': controller
            }

            visualizer = MazeVisualizer(maze, robots)
            
            letters = ask_target_letters(letters_positions)
            print(letters)
            controller.recieve_target_letter(letters)

            tasks = controller.assign_tasks()
            print(tasks)
        
            for task in tasks:
                print(task)
                excavator = task['excavator']
                excavator.set_task(task)
                start_time = time.time()
                excavator.path = excavator.find_path()
                end_time = time.time()
                total_time += end_time - start_time
                print(len(excavator.path))
                if note_results:
                    with open(f"./results/{path_finder}.txt", "a") as f:
                        f.write(f"maze {i}\n")
                        f.write(f"time taken: {end_time - start_time} seconds\n")
                    f.write(f"excavator {excavator.id} path length: {len(excavator.path)}\n")
                    f.write(f"excavator {excavator.id} path: {excavator.path}\n")
                    
                while excavator.path:
                    # print(excavator.path)
                    visualizer.plot_maze()
                    visualizer.plot_robots()
                            
                    excavator.move()
                    if show_animation:
                        plt.pause(0.5)
            plt.close()
        if note_results:
            with open(f"./results/{path_finder}.txt", "a") as f:
                f.write(f"Total time taken: {total_time} seconds\n")
                f.write(f"Average time taken: {total_time / 10} seconds\n")

