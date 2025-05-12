from abc import ABC

class Robot(ABC):
    def __init__(self, position, robot_id):
        """
        Initialize the base Robot
        :param position: (x, y) tuple representing the robot's position
        :param robot_id: Unique identifier for the robot
        """
        self.position = position
        self.robot_id = robot_id
        self.is_active = True
        

    def move(self, new_position):
        """
        Move the robot to a new position
        :param new_position: (x, y) tuple representing the new position
        """
        self.position = new_position

    def get_position(self):
        """
        Get the current position of the robot
        :return: (x, y) tuple
        """
        return self.position