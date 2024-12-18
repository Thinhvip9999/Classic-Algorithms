from utils import get_direction, heuristic  # Hàm tính khoảng cách heuristic (Manhattan distance)

# Hàm kiểm tra IDA* với vòng lặp
def ida_star(grid, start, goals, is_valid_move):
    # Ngưỡng ban đầu là giá trị heuristic từ điểm bắt đầu đến một trong các mục tiêu
    threshold = heuristic(start, goals)
    path = [start]  # Khởi tạo đường đi với điểm xuất phát
    all_nodes = set([start])  # Lưu tất cả các node duy nhất đã gặp

    while True:
        visited = set([start])  # Reset tập visited cho mỗi lần lặp với ngưỡng mới
        stack = [(start, 0, path)]  # Sử dụng stack để mô phỏng quá trình duyệt DFS
        min_threshold = float('inf')  # Ngưỡng nhỏ nhất cho lần lặp tiếp theo
        all_nodes = set([start])  # Lưu tất cả các node duy nhất đã gặp

        #print(f"\nĐang thử với ngưỡng: {threshold}")  # Debug: In ra ngưỡng hiện tại

        while stack:
            node, g, current_path = stack.pop()  # Lấy phần tử trên cùng của stack
            f = g + heuristic(node, goals)  # Tính f(n) = g(n) + h(n)
            visited.add(node)  # Đánh dấu đã thăm

            # Nếu f(n) vượt ngưỡng, cập nhật min_threshold và bỏ qua nhánh này
            if f > threshold:
                min_threshold = min(min_threshold, f)
                #print(f"Hiện tại {node} đang vượt quá với cost là {f} \nNhánh {current_path} dừng mở rộng \n")
                continue

            # Nếu đã tìm thấy mục tiêu, trả về đường đi
            if node in goals:
                goal_node = node
                directions = [get_direction(current_path[i], current_path[i + 1]) 
                              for i in range(len(current_path) - 1)]
                #print(all_nodes)
                return goal_node, len(all_nodes), directions

            # Duyệt các ô lân cận theo thứ tự LÊN, TRÁI, XUỐNG, PHẢI
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                new_pos = (node[0] + dx, node[1] + dy)
                if new_pos not in visited and is_valid_move(grid, new_pos):
                    all_nodes.add(new_pos)  # Thêm vào tập các node duy nhất
                    #print(f"Bắt đầu từ {node} có cost là {f} đến {new_pos} có cost là {g + 1 + heuristic(new_pos, goals)}")
                    # Thêm trạng thái mới vào stack để tiếp tục duyệt
                    stack.append((new_pos, g + 1, current_path + [new_pos]))
            #print(f"Hết hàng xóm của {node}\n")
            #print(f"Số phần tử còn lại trong stack là {len(stack)}")
            #print(f"Số phần tử có trong visited là {len(visited)}")

        # Nếu không tìm thấy lời giải trong lần này, cập nhật ngưỡng cho lần tiếp theo
        if min_threshold == float('inf'):
            return None, len(all_nodes), []  # Không có lời giải

        threshold = min_threshold  # Cập nhật ngưỡng mới
