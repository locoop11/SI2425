from searchPlus import *

# Define the grid representing the ice field
line1 = "## ## ## ## ## ## ## ## ##\n"
line2 = "## .. .. .. .. .. .. .. ##\n"
line3 = "## .. .. .. 00 .. .. .. ##\n"
line4 = "## .. .. .. .. .. .. .. ##\n"
line5 = "## .. .. () () () .. .. ##\n"
line6 = "## .. .. .. .. .. .. .. ##\n"
line7 = "## .. .. .. 01 .. .. .. ##\n"
line8 = "## .. .. .. .. .. .. .. ##\n"
line9 = "## ## ## ## ## ## ## ## ##\n"
grid = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9

class PenguinsPairs(Problem):
    """
    Represents a problem where penguins need to be paired on an ice grid.
    """
    def __init__(self, ice_map=grid):
        """Initializes the problem with the given ice map."""
        self.initial = self.parse_grid(ice_map)
        self.rows = len(self.initial)
        self.cols = len(self.initial[0])
        super().__init__(self.initial)  # Initialize the problem with the initial state
        self.visited = set()  # Track visited states to prevent loops


    def parse_grid(self, ice_map):
        """Parses the grid from a string format into a tuple representation."""
        return tuple(tuple(line.split()) for line in ice_map.strip().split("\n"))


    def actions(self, state):
        """Returns a list of valid moves for the penguins."""
        moves = []
        directions = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}
        penguins = [p for row in state for p in row if p.isdigit()]
        
        for penguin in penguins:
            for i, row in enumerate(state):
                for j, cell in enumerate(row):
                    if cell == penguin:
                        for direction, (di, dj) in directions.items():
                            ni, nj = i + di, j + dj
                            
                            # Check if the move is within bounds and not blocked
                            if not (0 <= ni < self.rows and 0 <= nj < self.cols) or state[ni][nj] in ('##', '()'):
                                continue

                            # Move in the given direction until an obstacle is encountered
                            while 0 <= ni < self.rows and 0 <= nj < self.cols and state[ni][nj] not in ('()', '##'):
                                if state[ni][nj].isdigit() and len(state[ni][nj]) == 2:
                                    break
                                ni += di
                                nj += dj
                            
                            if 0 <= ni < self.rows and 0 <= nj < self.cols and state[ni][nj] not in ('()', penguin):
                                moves.append((penguin, direction))
        
        return sorted(moves, key=lambda x: (int(x[0]), x[1]))


    def result(self, state, action):
        """Returns the new state after applying an action."""
        penguin, direction = action
        directions = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}
        di, dj = directions[direction]
        new_state = [list(row) for row in state]

        for i in range(self.rows):
            for j in range(self.cols):
                if new_state[i][j] == penguin:
                    ni, nj = i + di, j + dj
                    # Move until the penguin reaches an obstacle or another penguin
                    while 0 <= ni < self.rows and 0 <= nj < self.cols and new_state[ni][nj] == "..":
                        ni += di
                        nj += dj
                    ni -= di
                    nj -= dj

                    # Update the state with the new penguin position
                    new_state[i][j] = ".."
                    new_state[ni][nj] = penguin
                    new_state_tuple = tuple(tuple(row) for row in new_state)
                    
                    if new_state_tuple not in self.visited:
                        self.visited.add(new_state_tuple)
                        return new_state_tuple
                    else:
                        return state

        return state


    def goal_test(self, state):
        """Checks if all penguins are paired correctly."""
        penguin_positions = [(i, j) for i in range(self.rows) for j in range(self.cols) if state[i][j].isdigit()]
        paired = set()
        valid_pairs = True

        for i, j in penguin_positions:
            if state[i][j] in paired:
                continue
            # Check if a pair exists vertically
            if i + 1 < self.rows and state[i + 1][j].isdigit():
                if int(state[i][j]) >= int(state[i + 1][j]):
                    valid_pairs = False
                    break
                paired.add(state[i][j])
                paired.add(state[i + 1][j])
            else:
                valid_pairs = False
                break

        return len(paired) == len(penguin_positions) and len(paired) % 2 == 0 and valid_pairs


    def display(self, state):
        """Displays the current state of the grid."""
        return "\n".join(" ".join(row) for row in state) + "\n"
    

    def executa(self, state, actions_list, verbose=False):
        """Executa uma sequência de acções a partir do estado devolvendo o triplo formado pelo estado final, 
        pelo custo acumulado e pelo booleano que indica se o objectivo foi ou não atingido. Se o objectivo 
        for atingido antes da sequência ser atingida, devolve-se o estado e o custo corrente.
        Há o modo verboso e o não verboso, por defeito."""
        cost = 0
        for a in actions_list:
            seg = self.result(state,a)
            cost = self.path_cost(cost,state,a,seg)
            state = seg
            obj = self.goal_test(state)
            if verbose:
                print('Ação:', a)
                print(self.display(state),end='')
                print('Custo Total:',cost)
                print('Atingido o objectivo?', obj)
                print()
            if obj:
                break
        return (state, cost, obj)
