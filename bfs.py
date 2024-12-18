# bfs.py
from utils import get_direction

def bfs(grid, start, goals, is_valid_move):
    from collections import deque
    queue = deque([(start, [start])])  # Dùng queue để lưu các bước đi vì queue phục vụ cho dạng FIFO
    visited = set([start])  # Đánh dấu visited ngay khi thêm vào queue

    while queue:
        (x, y), path = queue.popleft()
        # Kiểm tra nếu đã đến mục tiêu
        if (x, y) in goals:
            # Tạo danh sách hướng đi
            directions = [get_direction(path[i], path[i + 1]) for i in range(len(path) - 1)]
            return (x, y), len(visited), directions

        # Thử di chuyển đến các ô lân cận
        for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:  # Thứ tự ưu tiên: Lên, trái, xuống, phải
            new_pos = (x + dx, y + dy)
            if new_pos not in visited and is_valid_move(grid, new_pos):
                visited.add(new_pos)  # Đánh dấu visited ngay khi thêm vào queue
                queue.append((new_pos, path + [new_pos]))

    return None, len(visited), []  # Không tìm thấy đường đi

