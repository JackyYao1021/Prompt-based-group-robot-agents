from excavator import Excavator
from controller import Controller
from visualizer import MazeVisualizer
from matplotlib import pyplot as plt
import random
from Utils import save_maze, find_start_position, find_valid_positions, generate_maze, ask_target_letters

def main():
    # Generate or load maze
    width, height = 21, 21
    maze, letter_positions = generate_maze(width, height, 4)
    save_maze(maze, "maze.txt")
    # Find start position
    start_pos = find_start_position(maze)
    
    valid_positions = find_valid_positions(maze)
    
    number_of_excavators = 5
    
    controller = Controller(start_pos, "C1")
    excavators = []
    for i in range(number_of_excavators):
        random_position = random.choice(valid_positions)
        excavator = Excavator(random_position, f"E{i+1}")
        excavators.append(excavator)
        controller.add_excavator(excavator)
    
    # Create visualizer
    robots = {
        'excavators': excavators,
        'controller': controller
    }
    
    visualizer = MazeVisualizer(maze, robots)
    
    # Simulate search process
    while letter_positions:
        target_letters = ask_target_letters(letter_positions)
        
        controller.recieve_target_letter(target_letters)
        
        tasks = controller.assign_tasks()
        for task in tasks:
            excavator = task['excavator']
            excavator.find_path(maze)
            if excavator.path:
                next_pos = excavator.path[1] if len(excavator.path) > 1 else excavator.path[0]
                excavator.move(next_pos)
        
        # Update visualization
        visualizer.plot_maze()
        visualizer.plot_robots()
        plt.pause(0.1)  
    
    plt.show()

if __name__ == "__main__":
    main() 