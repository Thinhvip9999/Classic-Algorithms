# check_map.py
import argparse
from grid import read_input, create_grid

def mark_position(grid, position, symbol):
    """Đánh dấu vị trí trên lưới với ký hiệu cụ thể."""
    x, y = position
    grid[y][x] = symbol

def print_grid(grid):
    """In lưới ra màn hình."""
    for row in grid:
        print(' '.join(row))

def main():
    # Thiết lập đối số dòng lệnh
    parser = argparse.ArgumentParser(description='Check and print the map.')
    parser.add_argument('input_file', type=str, help='Path to the input file')
    args = parser.parse_args()

    # Đọc dữ liệu từ tệp được cung cấp qua dòng lệnh
    grid_size, start_pos, goal_positions, walls = read_input(args.input_file)

    # Tạo lưới và thêm tường
    grid = create_grid(grid_size, walls)

    # Đánh dấu vị trí khởi đầu (ô màu đỏ)
    mark_position(grid, start_pos, 'S')

    # Đánh dấu các vị trí đích (ô màu xanh)
    for goal in goal_positions:
        mark_position(grid, goal, 'G')

    # In lưới ra để kiểm tra
    print_grid(grid)

if __name__ == "__main__":
    main()
