import time  # For measuring execution time
import os    # For file path operations
from typing import List, Tuple, Set  # For type hints

class Nono_Solver:
    """Class that solves Nonogram puzzles using constraint propagation and backtracking."""
    
    def __init__(self, filename: str):
        """ Initialize the Nonogram solver with puzzle from file. """
        # Read puzzle constraints from file
        self.row_constraints, self.col_constraints = self.read_puzzle(filename)
        # Set grid dimensions
        self.height = len(self.row_constraints)
        self.width = len(self.col_constraints)
        # Initialize empty grid with None values
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        # Generate initial possible configurations for rows and columns
        self.row_domains = self._generate_domains(self.row_constraints, self.width)
        self.col_domains = self._generate_domains(self.col_constraints, self.height)

    def read_puzzle(self, filename: str) -> Tuple[List[List[int]], List[List[int]]]:
        """ Read puzzle clues from file with format: row constraints, blank line, column constraints. """
        try:
            # Read and split file contents
            with open(filename, 'r') as f:
                lines = f.read().strip().split('\n')
            
            # Find empty line separating row and column constraints
            separator_idx = lines.index('')
            
            # Parse constraints into lists of integers
            row_constraints = [list(map(int, line.split())) for line in lines[:separator_idx]]
            col_constraints = [list(map(int, line.split())) for line in lines[separator_idx+1:]]
            
            return row_constraints, col_constraints
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            exit(1)
        except Exception as e:
            print(f"Error reading puzzle file: {str(e)}")
            exit(1)

    def generate_line_possibilities(self, blocks: List[int], length: int) -> List[List[int]]:
        """ Generate all possible line configurations for given blocks. """
        # Handle empty blocks case
        if not blocks:
            return [[0] * length]
        
        # Calculate space requirements
        total_blocks = sum(blocks)
        total_gaps = len(blocks) - 1  # Gaps between blocks
        remaining_space = length - (total_blocks + total_gaps)
        
        # Check if configuration is possible
        if remaining_space < 0:
            return []

        def generate_positions(pos: int, current_blocks: List[int]) -> List[List[int]]:
            """ Recursive helper function to generate valid block positions. """
            # Base case: all blocks placed
            if not current_blocks:
                line = [0] * length
                for p in pos_list:
                    for i in range(p[1]):
                        line[p[0] + i] = 1
                return [line]
            
            block = current_blocks[0]
            results = []
            start = pos
            max_start = length - sum(current_blocks) - (len(current_blocks) - 1)
            
            # Try placing current block at different positions
            while start <= max_start:
                if all(p[0] + p[1] <= start for p in pos_list):
                    pos_list.append((start, block))
                    results.extend(generate_positions(start + block + 1, current_blocks[1:]))
                    pos_list.pop()
                start += 1
                
            return results

        pos_list = []  # Track block positions
        return generate_positions(0, blocks)

    def _generate_domains(self, constraints: List[List[int]], length: int) -> List[Set[tuple]]:
        """ Generate Possible configurations for each line """
        return [set(map(tuple, self.generate_line_possibilities(blocks, length))) 
                for blocks in constraints]

    def _update_domains(self) -> bool:
        """ Update domains based on current grid state using constraint propagation. """
        changed = True
        while changed:
            changed = False
            
            # Update row domains based on current grid values
            for i in range(self.height):
                new_domain = set()
                for possibility in self.row_domains[i]:
                    valid = True
                    for j, value in enumerate(possibility):
                        if self.grid[i][j] is not None and self.grid[i][j] != value:
                            valid = False
                            break
                    if valid:
                        new_domain.add(possibility)
                
                # Check for inconsistency
                if not new_domain:
                    return False
                if new_domain != self.row_domains[i]:
                    changed = True
                    self.row_domains[i] = new_domain
            
            # Update column domains similarly
            for j in range(self.width):
                new_domain = set()
                for possibility in self.col_domains[j]:
                    valid = True
                    for i, value in enumerate(possibility):
                        if self.grid[i][j] is not None and self.grid[i][j] != value:
                            valid = False
                            break
                    if valid:
                        new_domain.add(possibility)
                
                if not new_domain:
                    return False
                if new_domain != self.col_domains[j]:
                    changed = True
                    self.col_domains[j] = new_domain
            
            # Find and propagate certain values
            for i in range(self.height):
                for j in range(self.width):
                    if self.grid[i][j] is None:
                        row_values = {poss[j] for poss in self.row_domains[i]}
                        col_values = {poss[i] for poss in self.col_domains[j]}
                        common_values = row_values & col_values
                        if len(common_values) == 1:
                            self.grid[i][j] = common_values.pop()
                            changed = True
        
        return True

    def solve(self) -> bool:
        """ Solve the nonogram puzzle using constraint propagation and backtracking. """
        # Update domains and check consistency
        if not self._update_domains():
            return False

        # Find cell with smallest domain intersection (Most constrained variable)
        min_options = float('inf')
        best_pos = None
        best_values = None

        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] is None:
                    row_values = {poss[j] for poss in self.row_domains[i]}
                    col_values = {poss[i] for poss in self.col_domains[j]}
                    common_values = row_values & col_values
                    if len(common_values) < min_options:
                        min_options = len(common_values)
                        best_pos = (i, j)
                        best_values = common_values

        # If no empty cells, solution found
        if not best_pos:
            return True

        # Try each possible value for the chosen cell
        i, j = best_pos
        for value in best_values:
            self.grid[i][j] = value
            if self.solve():  # Recursive solving
                return True
            self.grid[i][j] = None  # Backtrack if no solution

        return False

    def print_solution(self):
        """Print the solved nonogram grid"""
        if not any(None in row for row in self.grid):
            for row in self.grid:
                print(''.join('██' if cell == 1 else '  ' for cell in row))
        else:
            print("No solution found")

def get_puzzle_file() -> str:
    """ Get and validate puzzle file path from user input. """
    while True:
        file_path = input("Enter the path to your puzzle file: ").strip()
        
        # Validate file path
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                return file_path
            else:
                print("Error: The specified path is not a file.")
        else:
            print("Error: The specified file does not exist.")
        
        # Ask to retry or exit
        retry = input("Would you like to try again? (y/n): ").strip().lower()
        if retry != 'y':
            print("Exiting program.")
            exit(0)

def main():
    """Main program entry point."""
    print("Welcome to the Nonogram Solver!")
    file_path = get_puzzle_file()
    
    print("\nSolving puzzle...")
    solver = Nono_Solver(file_path)
    start_time = time.perf_counter()
    
    if solver.solve():
        end_time = time.perf_counter()
        print("\nSolution found:\n")
        solver.print_solution()
        print(f"\nTime taken: {end_time - start_time:.2f} seconds")
    else:
        print("\nNo solution exists for this puzzle.")

if __name__ == "__main__":
    main()