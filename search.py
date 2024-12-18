# search.py
import sys
from grid import read_input, create_grid, is_valid_move
from dfs import dfs
from bfs import bfs
from utils import print_result
from astar import astar
from gbfs import gbfs
from cus1 import iterative_deepening_search
from cus2 import ida_star
from two_goal_astar import two_goals_astar  # Thuật toán cần chỉnh sửa

if __name__ == "__main__":
    '''
    Command line:
    python search.py RobotNav-test.txt DFS
    python search.py RobotNav-test.txt BFS
    python search.py RobotNav-test.txt AS
    python search.py RobotNav-test.txt GBFS
    python search.py RobotNav-test.txt CUS1
    python search.py RobotNav-test.txt CUS2
    python search.py RobotNav-test.txt TWO_GOALS
    '''
    input_file = sys.argv[1]  # Ví dụ: RobotNav-test.txt
    method = sys.argv[2]  # Tên thuật toán: DFS, BFS, AS, ...

    # Đọc dữ liệu từ file đầu vào và khởi tạo grid
    grid_size, start_pos, goal_positions, walls = read_input(input_file)
    grid = create_grid(grid_size, walls)

    # Chạy thuật toán tương ứng và in kết quả
    if method == "DFS":
        goal_node, node_count, directions = dfs(grid, start_pos, goal_positions, is_valid_move)
        print_result(goal_node, node_count, directions)

    elif method == "BFS":
        goal_node, node_count, directions = bfs(grid, start_pos, goal_positions, is_valid_move)
        print_result(goal_node, node_count, directions)

    elif method == "AS":
        goal_node, node_count, directions = astar(grid, start_pos, goal_positions, is_valid_move)
        print_result(goal_node, node_count, directions)

    elif method == "GBFS":
        goal_node, node_count, directions = gbfs(grid, start_pos, goal_positions, is_valid_move)
        print_result(goal_node, node_count, directions)

    elif method == "CUS1":
        goal_node, node_count, directions = iterative_deepening_search(grid, start_pos, goal_positions, is_valid_move)
        print_result(goal_node, node_count, directions)

    elif method == "CUS2":
        goal_node, node_count, directions = ida_star(grid, start_pos, goal_positions, is_valid_move)
        print_result(goal_node, node_count, directions)

    elif method == "TWO_GOALS":
        # TWO_GOALS trả về danh sách các kết quả cho từng đích
        result = two_goals_astar(grid, start_pos, goal_positions, is_valid_move)
        
    else:
        print(f"Method {method} not recognized!")
        sys.exit(1)
