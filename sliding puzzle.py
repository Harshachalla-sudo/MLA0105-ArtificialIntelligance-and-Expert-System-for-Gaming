import collections


class Board:
    """Represents the 8-puzzle board state and provides movement logic."""
    
    GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    
    def __init__(self, tiles):
        self.tiles = tiles

    def __eq__(self, other):
        """Used for checking if two board states are the same."""
        return self.tiles == other.tiles

    def __hash__(self):
        """Used for storing board states in sets/dictionaries (for visited states)."""
        return hash(self.tiles)

    def __str__(self):
        """A friendly string representation of the board."""
        s = ""
        for i in range(9):
            if i % 3 == 0 and i != 0:
                s += "\n"
            s += str(self.tiles[i]) if self.tiles[i] != 0 else " "
            s += " "
        return s

    def get_empty_index(self):
        """Finds the index (0-8) of the empty space (0)."""
        return self.tiles.index(0)

    def get_neighbors(self):
        """Generates all valid next board states by moving the empty space."""
        neighbors = []
        empty_index = self.get_empty_index()
        row, col = divmod(empty_index, 3)

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # Calculate the new index
                new_index = new_row * 3 + new_col
                
                new_tiles_list = list(self.tiles)
                new_tiles_list[empty_index], new_tiles_list[new_index] = \
                    new_tiles_list[new_index], new_tiles_list[empty_index]
                
                neighbors.append(Board(tuple(new_tiles_list)))
                
        return neighbors


def is_solvable(tiles):
    """
    Checks if the given initial state is solvable based on the number of inversions.
    An 8-puzzle is solvable if the number of inversions is EVEN.
    """
    inversions = 0
    puzzle_list = [tile for tile in tiles if tile != 0]
    n = len(puzzle_list)
    
    for i in range(n):
        for j in range(i + 1, n):
            if puzzle_list[i] > puzzle_list[j]:
                inversions += 1
                
    return inversions % 2 == 0

def solve_puzzle(initial_tiles):
    """
    Finds the shortest sequence of moves from initial_tiles to the goal state
    using Breadth-First Search (BFS).
    """
    initial_state = Board(initial_tiles)
    goal_state = Board(Board.GOAL_STATE)

    if initial_state == goal_state:
        return [initial_state]
    
    if not is_solvable(initial_tiles):
        print("❌ Initial state is NOT solvable. Cannot reach the goal.")
        return None

    queue = collections.deque([(initial_state, [initial_state])])
    visited = {initial_state}

    while queue:
        current_board, path = queue.popleft()

        for neighbor_board in current_board.get_neighbors():
            
            if neighbor_board == goal_state:
                return path + [neighbor_board]
            
            if neighbor_board not in visited:
                visited.add(neighbor_board)
                new_path = path + [neighbor_board]
                queue.append((neighbor_board, new_path))
    
    return None
 
def run_solver(initial_tiles):
    """Utility function to run the solver and print the results."""
    print("=" * 30)
    print("🧩 INITIAL BOARD STATE:")
    print(Board(initial_tiles))
    print("=" * 30)
    
    solution_path = solve_puzzle(initial_tiles)

    if solution_path:
        print(f"✅ Solution Found in {len(solution_path) - 1} moves!")
        print("-" * 25)
        print("--- Detailed Solution Path ---")
        for i, board in enumerate(solution_path):
            if i == 0:
                print(f"Start (Move 0):")
            else:
                print(f"Move {i}:")
            print(board)
            print("-" * 5)
    else:
        pass

solvable_tiles_1 = (1, 2, 3, 4, 0, 5, 7, 8, 6)
run_solver(solvable_tiles_1)

print("\n" + "#" * 50 + "\n")

solvable_tiles_2 = (8, 6, 7, 2, 5, 4, 3, 0, 1)
run_solver(solvable_tiles_2)

print("\n" + "#" * 50 + "\n")
