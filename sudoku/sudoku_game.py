import random
import time  # Import the time module for timing


class SudokuGenerator:
    def __init__(self, size=9):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.initial_cells = set()
        self.generate_puzzle()

    def is_valid(self, num, row, col):
        for i in range(self.size):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.grid[i][j] == num:
                    return False
        return True

    def solve(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    for num in range(1, self.size + 1):
                        if self.is_valid(num, row, col):
                            self.grid[row][col] = num
                            if self.solve():
                                return True
                            self.grid[row][col] = 0
                    return False
        return True

    def generate_puzzle(self, num_holes=40):
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.solve()
        holes = random.sample(range(self.size * self.size), num_holes)
        self.initial_cells = set()
        for hole in holes:
            row, col = hole // self.size, hole % self.size
            self.initial_cells.add((row, col))
            self.grid[row][col] = 0

    def get_puzzle(self):
        return self.grid

    def get_initial_cells(self):
        return self.initial_cells


class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)

    def is_valid(self, num, row, col):
        for i in range(self.size):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.grid[i][j] == num:
                    return False
        return True

    def solve(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    for num in range(1, self.size + 1):
                        if self.is_valid(num, row, col):
                            self.grid[row][col] = num
                            if self.solve():
                                return True
                            self.grid[row][col] = 0
                    return False
        return True


def print_grid(grid):
    for row in grid:
        print(" ".join(str(num) if num != 0 else '.' for num in row))


def get_user_input():
    while True:
        try:
            row = int(input("Enter row (1-9): ")) - 1
            col = int(input("Enter column (1-9): ")) - 1
            num = int(input("Enter number (1-9): "))
            if row in range(9) and col in range(9) and num in range(1, 10):
                return row, col, num
            else:
                print("Invalid input. Please enter values in the correct range.")
        except ValueError:
            print("Invalid input. Please enter numerical values.")


def play_sudoku():
    points=0
    generator = SudokuGenerator()
    puzzle = generator.get_puzzle()
    initial_cells = generator.get_initial_cells()

    print("Sudoku Puzzle:")
    print_grid(puzzle)

    # Start timing
    start_time = time.time()

    move_count = 0  # Initialize move counter

    while True:
        row, col, num = get_user_input()
        if (row, col) not in initial_cells:
            print("Cannot change this cell. It was filled by the generator.")
        else:
            if puzzle[row][col]==0:
                points+=1
            else:
                points-=1
                if(points<0):
                    points=0
            puzzle[row][col] = num
            move_count += 1  # Increment move counter
            print("Updated Puzzle:")
            print_grid(puzzle)
            # Check if the grid is completely filled and valid
            solver = SudokuSolver(puzzle)
            if all(cell != 0 for row in puzzle for cell in row):
                # End timing
                end_time = time.time()
                elapsed_time = end_time - start_time
                if solver.solve():
                    print(f"Congratulations! You solved the Sudoku.")
                    print(f"POINTS: {points}")
                    print(f"Time taken: {elapsed_time:.2f} seconds")
                    print(f"Number of moves: {move_count}")
                else:
                    print("The current configuration is not valid. Best of luck next time.")
                break

if __name__ == "__main__":
    play_sudoku()
