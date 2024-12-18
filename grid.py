# grid.py
def read_input(filename):
    with open(filename, 'r') as file:
        grid_size = eval(file.readline().strip())  # [N, M]
        start_pos = eval(file.readline().strip())  # (x1, y1)
        goal_positions = [eval(pos.strip()) for pos in file.readline().strip().split('|')]  # List of goals (xG, yG)
        walls = [eval(line.strip()) for line in file.readlines()]  # List of walls (x, y, w, h)
    return grid_size, start_pos, goal_positions, walls

def create_grid(grid_size, walls):
    grid = [['.' for _ in range(grid_size[1])] for _ in range(grid_size[0])]
    
    for wall in walls:
        x, y, w, h = wall
        for i in range(h):
            for j in range(w):
                grid[y + i][x + j] = '#'
    
    return grid

def is_valid_move(grid, pos):
    x, y = pos
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid) and grid[y][x] == '.'
