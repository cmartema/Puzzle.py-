path_to_goal = []  #the sequence of moves taken to reach the goal.
cost_of_path = 0       #the number of moves taken to reach the goal.
nodes_expanded = 0    #the number of nodes that have been expanded.
search_depth = 0      #the depth within the search tree when the goal node is found.
max_search_depth = 0  #the maximum depth of the search tree in the lifetime of the algorithm.
running_time = 0      #the total running time of the search instance, reported in seconds.
max_ram_usage = 0    #the maximum RAM usage in the lifetime of the process as measured by the ru maxrss attribute in the resource module, reported in megabytes.

def main():
    if len(sys.argv) < 2:
        print("Usage: puzzle.py <method> <board>")
        return
    
    method_type = ""
    board_setup = ""

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "bfs" or sys.argv[i] == "dfs" or sys.argv[i] == "ast":
            if sys.argv[i] == "bfs":
                method_type = "bfs"
                i += 1
            elif sys.argv[i] == "dfs":
                method_type = "dfs"
                i += 1
            else:
                method_type = "ast"
                i += 1
        else:
            print("Invalid Argument:",sys.argv[i])
            return
        if sys.argv[i] = 
        