import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class MazeVisualizer:
    def __init__(self, maze, robots):
        """
        Initialize the maze visualizer
        :param maze: 2D list representing the maze
        :param robots: Dictionary of robots with their types as keys
        """
        self.maze = maze
        self.robots = robots
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.animation = None
        
        # Define colors for different elements
        self.colors = {
            'wall': '#000000',  # Black for walls
            'path': '#808080',  # Gray for paths
            'scout': '#FF0000',  # Red for scouts
            'excavator': '#0000FF',  # Blue for excavators
            'controller': '#00FF00',  # Green for controller
            'target': '#FFA500',  # Orange for target
            'radar': '#FFD700'  # Gold for radar range
        }

    def plot_maze(self):
        """
        Plot the initial state of the maze
        """
        self.ax.clear()
        maze_array = np.array(self.maze)
        
        # Plot walls
        walls = maze_array == '#'
        self.ax.imshow(walls, cmap='binary')
        
        # Plot paths
        paths = maze_array == ' '
        self.ax.imshow(paths, cmap='Greys', alpha=0.3)
        
        # Plot letters (targets)
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j].isalpha():
                    self.ax.text(j, i, self.maze[i][j], 
                               color=self.colors['target'],
                               ha='center', va='center',
                               fontsize=15, fontweight='bold')

    def plot_robots(self):
        """
        Plot all robots and their states
        """
        # Plot scouts
        for scout in self.robots.get('scouts', []):
            if scout.is_active:
                x, y = scout.position
                # Plot radar range
                radar = plt.Circle((y, x), scout.radar_range, 
                                 color=self.colors['radar'], 
                                 alpha=0.2)
                self.ax.add_patch(radar)
                # Plot scout
                self.ax.plot(y, x, 'o', color=self.colors['scout'], 
                           markersize=10, label='Scout')
                # Plot detected letters
                for letter, pos in scout.detected_letters.items():
                    self.ax.text(pos[1], pos[0], letter,
                               color=self.colors['target'],
                               ha='center', va='center',
                               fontsize=12)

        # Plot excavators
        for excavator in self.robots.get('excavators', []):
            if excavator.is_active:
                x, y = excavator.position
                self.ax.plot(y, x, 's', color=self.colors['excavator'],
                           markersize=10, label='Excavator')
                # Plot path if exists
                if excavator.path:
                    path = np.array(excavator.path)
                    self.ax.plot(path[:, 1], path[:, 0], '--',
                               color=self.colors['excavator'],
                               alpha=0.5)

        # Plot controller
        # controller = self.robots.get('controller')
        # if controller and controller.is_active:
        #     x, y = controller.position
        #     self.ax.plot(y, x, '^', color=self.colors['controller'],
        #                 markersize=12, label='Controller')

    def update(self, frame):
        """
        Update function for animation
        """
        self.plot_maze()
        self.plot_robots()
        self.ax.set_title(f'Frame {frame}')
        self.ax.legend(loc='upper right')
        return self.ax,

    def animate(self, frames=100, interval=500):
        """
        Create and show the animation
        :param frames: Number of frames to animate
        :param interval: Interval between frames in milliseconds
        """
        self.animation = animation.FuncAnimation(
            self.fig, self.update,
            frames=frames,
            interval=interval,
            blit=True
        )
        plt.show()

    def save_animation(self, filename, frames=100, interval=500):
        """
        Save the animation to a file
        :param filename: Name of the output file
        :param frames: Number of frames to animate
        :param interval: Interval between frames in milliseconds
        """
        self.animation = animation.FuncAnimation(
            self.fig, self.update,
            frames=frames,
            interval=interval,
            blit=True
        )
        self.animation.save(filename, writer='pillow') 