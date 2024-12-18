# dfs.py
from utils import get_direction

def dfs(grid, start, goals, is_valid_move):
    stack = [(start, [start])]  # Dùng stack để lưu các bước đi
    visited = set([start])
    node_count = set([start])

    while stack:
        (x, y), path = stack.pop()

        # Thêm vị trí hiện tại vào visited
        visited.add((x, y))
        
        # Kiểm tra nếu đã đến mục tiêu
        if (x, y) in goals:
            # Tạo danh sách hướng đi
            directions = [get_direction(path[i], path[i + 1]) for i in range(len(path) - 1)]
            return (x, y), len(node_count), directions

        # Thử di chuyển đến các ô lân cận
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # Vì là stack nên phải viết ngược lại theo thứ tự ưu tiên ưu tiên(Trên trái dưới phải) >> thứ tự theo stack (phải dưới trái trên) theo LIFO
            new_pos = (x + dx, y + dy)
            if new_pos not in visited and is_valid_move(grid, new_pos):
                stack.append((new_pos, path + [new_pos]))
                #print(f"{len(node_count)}: {new_pos}")
                node_count.add(new_pos)

    return None, len(visited), []  # Không tìm thấy đường đi
