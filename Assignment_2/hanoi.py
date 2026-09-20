import time

class TowerOfHanoi:
    """Representation of the Tower of Hanoi Puzzle
       Link: https://en.wikipedia.org/wiki/Tower_of_Hanoi

       There are three pegs, numbers 1-number of disks are used instead of disks, 
       where a bigger number is a bigger disk.

       Example initial state with 3 disks:
       Peg 0: [3, 2, 1]
       Peg 1: []
       Peg 2: []

       Goal state for example:
       Peg 0: []
       Peg 1: []
       Peg 2: [3, 2, 1]
    """

    def __init__(self, number_of_disks = 4):
        """Constructor for TowerOfHanoi

        Args:
            number_of_disks (int, optional): The number of disks for the game. Defaults to 4.
        """
        self.number_of_disks = number_of_disks 
        self.reset()

    def move(self, source, destination):
        """ Moves the top disk from a source peg to the destiniation peg.
            No bigger disk may be placed on stop of a smaller one. 
 
        Args:
            source (int): The number of the peg to move a disk from. Possible values are 0, 1, or 2.
            destination (int): The number of the peg to move a disk to. Possible values are 0, 1, or 2.
 
        Returns:
            boolean: Returns True if the move was made and False otherwise.
        """
        top_disk = self.pegs[source][-1]

        if source not in (0, 1, 2) or destination not in (0, 1, 2):
            return False
 
        if source == destination:
            return False
 
        if len(self.pegs[source]) == 0:
            return False
 
        if len(self.pegs[destination]) > 0 and self.pegs[destination][-1] < disk:
            return False
 
        self.pegs[source].pop()
        self.pegs[destination].append(disk)
        return True

    def print_state(self):
        """Prints the state of each peg on one line each.
        """
        for i in range(len(self.pegs)):
            print("Peg " + str(i) + ": " + str(self.pegs[i]))

    def is_goal(self):
        """Checks whether the current state of the puzzle is the goal state.

        Returns:
            boolean: Returns True if disks (numbers) are in descending order on the third peg and False otherwise.
        """
        goal = list(range(self.number_of_disks, 0, -1))
        return self.pegs[2] == goal

    def reset(self):
        """Resets the Tower of Hanoi to the initial state.
        """
        self.pegs = [[], [], []]
        for disk in range(self.number_of_disks, 0, -1):
            self.pegs[0].append(disk)

    def get_state(self):
        """Returns the current state of the Tower.

        Returns:
            list: List containing three lists representing each peg in ascending order of peg number.
        """
        state = []
        for peg in self.pegs:
            state.append(list(peg))
        return state


class TTTowerOfHanoi(TowerOfHanoi):
 
    def is_goal(self):
        goal = []
        for size in range(self.number_of_disks, 0, -1):
            for copy in range(3):
                goal.append(size)
        return self.pegs[2] == goal
 
    def reset(self):
        self.pegs = [[], [], []]
 
        for size in range(self.number_of_disks, 0, -1):
            for copy in range(3):
                self.pegs[0].append(size)
