from __future__ import division
from __future__ import print_function


import sys
import math
import time
import queue as Q
import resource


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)


    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index >= self.n:  # Check if blank tile can move up by verifying its not on the top row of the board (n needs to be )
            config_copy = self.config[:]
            new_blank_index = self.blank_index - self.n
            config_copy[self.blank_index], config_copy[new_blank_index] = config_copy[new_blank_index],config_copy[self.blank_index]

            return PuzzleState(config_copy, self.n, self,"Up", self.cost + 1)
        
        #print("Invalid Move on up")
        return None

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index < (self.n * (self.n - 1)):  # Check if blank tile can move down by checking if the index is less than the first tile of the last row
            config_copy = self.config[:]
            new_blank_index = self.blank_index + self.n
            config_copy[self.blank_index], config_copy[new_blank_index] = config_copy[new_blank_index], config_copy[self.blank_index]
            
            return PuzzleState(config_copy, self.n, self,"Down", self.cost + 1)
        
        #print("Invalid Move on down")
        return None
        
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n != 0: # Check if blank tile can move left
            config_copy = self.config[:]
            new_blank_index = self.blank_index - 1
            config_copy[self.blank_index], config_copy[new_blank_index] = config_copy[new_blank_index], config_copy[self.blank_index]

            return PuzzleState(config_copy, self.n, self,"Left", self.cost + 1)

        #print("Invalid Move on left")
        return None
    
    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if (self.blank_index + 1) % self.n != 0:  # Check if blank tile can move right
            config_copy = self.config[:]
            new_blank_index = self.blank_index + 1
            config_copy[self.blank_index], config_copy[new_blank_index] = config_copy[new_blank_index], config_copy[self.blank_index]

            return PuzzleState(config_copy, self.n, self,"Right", self.cost + 1)

        #print("Invalid Move on right")
        return None
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(state, depth, nodes, running_time, max_ram_usage):
    curr_state = state
    path_to_goal = []
    cost_of_path = state.cost
    nodes_expanded = nodes
    search_depth = 0
    max_search_depth = depth
    while curr_state is not None:
        if curr_state.action != "Initial":
            path_to_goal.append(curr_state.action)
        curr_state = curr_state.parent
    path_to_goal.reverse()
    search_depth = len(path_to_goal)

    print("Path_to_goal:", path_to_goal)
    print("cost_of_path:", cost_of_path)
    print("nodes_expanded:", nodes_expanded)
    print("Search Depth:", search_depth)
    print("max_search_depth:", max_search_depth)
    print("running_time:", running_time)
    print("max_ram_usage:", max_ram_usage)

    file_name = "output.txt"
    with open(file_name, "w") as file:
        file.write(f"path_to_goal: {path_to_goal}\n")
        file.write(f"cost_of_path: {cost_of_path}\n")
        file.write(f"nodes_expanded: {nodes_expanded}\n")
        file.write(f"search_depth: {search_depth}\n")
        file.write(f"max_search_depth: {max_search_depth}\n")
        file.write(f"running_time: {running_time:.8f}\n")
        file.write(f"max_ram_usage: {max_ram_usage:.8f}\n")
    
def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    frontier = Q.Queue()
    frontier_config = set()
    frontier.put((initial_state, 0)) #queue set as tuple (state, depth)
    frontier_config.add(tuple(initial_state.config)) #Initializing tuple to hold the config and the state. Runs on O(1)
    explored = set()
    max_depth = 0
    nodes_expanded = 0
    
    while not frontier.empty():
        state_depth = frontier.get() #dequeue tuple (state, depth)
        state = state_depth[0]
        curr_depth = state_depth[1]
        explored.add(state)

        if test_goal(state) == True:
            return state, max_depth, nodes_expanded
          
        child = state.expand()
        nodes_expanded += 1
        for neighbor in child:
            neighbor_config = tuple(neighbor.config)
            if neighbor_config not in frontier_config and neighbor_config not in explored:
                frontier.put((neighbor, curr_depth + 1)) #Increment depth by 1
                frontier_config.add(neighbor_config)
                max_depth = max(max_depth, curr_depth + 1) #Update the max_depth
    return None

        
def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    pass

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    pass

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    pass

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    pass

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    goal_list = sorted(puzzle_state.config[:])
    config_copy = puzzle_state.config[:]
    if goal_list == config_copy:
        return True
    
    return False

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()

    dfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    if   search_mode == "bfs": state, max_depth, nodes_expanded = bfs_search(hard_state)
    elif search_mode == "dfs": state, max_depth, nodes_expanded = dfs_search(hard_state)
    elif search_mode == "ast": state, max_depth, nodes_expanded = A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")

    dfs_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss-dfs_start_ram)/(2**2) 
    
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

    running_time = end_time-start_time

    
    writeOutput(state, max_depth, nodes_expanded, running_time, dfs_ram)

if __name__ == '__main__':
    main()
