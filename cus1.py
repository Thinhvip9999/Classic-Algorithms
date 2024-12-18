from utils import get_direction

# Hàm tìm kiếm theo chiều sâu có giới hạn (Depth-Limited Search - DLS)
def depth_limited_search(node, goals, depth_limit, path, visited, is_valid_move, grid):
    # Nếu node hiện tại là một trong các mục tiêu, trả về đường đi
    if node in goals:
        return path  # Trả về đường đi nếu tìm thấy mục tiêu

    # Dừng nếu đã đạt tới giới hạn độ sâu
    if depth_limit == 0:
        return None

    # Thử di chuyển đến các ô lân cận theo thứ tự LÊN, TRÁI, XUỐNG, PHẢI
    for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        new_pos = (node[0] + dx, node[1] + dy)
        if new_pos not in visited and is_valid_move(grid, new_pos):
            #print(new_pos)
            visited.add(new_pos)  # Đánh dấu vị trí đã thăm
            result = depth_limited_search(new_pos, goals, depth_limit - 1, path + [new_pos], visited, is_valid_move, grid)
            if result:  # Nếu tìm thấy mục tiêu ở nhánh con
                return result

    return None  # Không tìm thấy kết quả trong độ sâu hiện tại

# Hàm tìm kiếm lặp theo chiều sâu (Iterative Deepening Search - IDS)
def iterative_deepening_search(grid, start, goals, is_valid_move):
    depth = 0  # Giới hạn độ sâu bắt đầu từ 0

    while True:
        visited = set([start])  # Reset tập hợp visited cho mỗi lần gọi DLS
        node_count = set([start])  # Đếm số lượng node đã duyệt trong mỗi lần gọi DLS
        #print(f"Đang thử với giới hạn độ sâu: {depth}")  # Debug: in ra độ sâu hiện tại

        # Gọi hàm DLS với giới hạn độ sâu hiện tại
        path = depth_limited_search(start, goals, depth, [start], visited, is_valid_move, grid)
        
        if path:  # Nếu tìm thấy đường đi tới một mục tiêu
            goal_node = path[-1]  # Lấy vị trí của mục tiêu
            directions = [get_direction(path[i], path[i + 1]) for i in range(len(path) - 1)]
            return goal_node, len(visited), directions  # Trả về vị trí, số node duyệt và hướng đi
        #print(f"Tăng giới hạn độ sâu: {depth}")
        depth += 1  # Tăng giới hạn độ sâu