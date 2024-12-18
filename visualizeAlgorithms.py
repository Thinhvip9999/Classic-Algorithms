import tkinter as tk
import time
import sys
from grid import read_input, create_grid, is_valid_move
from queue import PriorityQueue  # Import thư viện hàng đợi ưu tiên (PriorityQueue) để sử dụng trong thuật toán A*.
import itertools  # Import thư viện itertools để sử dụng biến đếm counter cho Priority Queue.
from utils import heuristic, get_direction
from astar import get_neighbors, reconstruct_path

CELL_SIZE = 100  # Kích thước ô trong lưới (pixels)
DELAY = 100  # Độ trễ giữa các bước (milliseconds)

# Hàm để vẽ grid với walls, start và goal
def draw_grid(canvas, grid, start, goals, walls):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            color = 'white'
            if grid[y][x] == '#':
                color = 'black'
            elif (x, y) == start:
                color = 'red'
            elif (x, y) in goals:
                color = 'green'
            canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill=color, outline='gray')

# Hàm để đánh dấu ô trong queue (màu vàng)
def mark_queue(canvas, pos):
    x, y = pos
    canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill='yellow', outline='gray')

# Hàm để đánh dấu ô đã di chuyển (màu xanh lá cây nhạt)
def mark_move(canvas, pos):
    x, y = pos
    canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill='lightgreen', outline='gray')

# Hàm để vẽ đường đi cuối cùng (màu xanh lá cây đậm)
def mark_path(canvas, path):
    for pos in path:
        x, y = pos
        canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill='darkgreen', outline='gray')

# Thuật toán BFS với visualize từng bước
def bfs_visualize(canvas, grid, start, goals):
    from collections import deque
    queue = deque([(start, [start])])  # Queue lưu các bước đi
    visited = set([start])  # Đánh dấu visited ngay khi thêm vào queue
    
    while queue:
        (x, y), path = queue.popleft()

        # Đánh dấu ô hiện tại trong queue (màu vàng)
        mark_queue(canvas, (x, y))
        canvas.update()  # Cập nhật canvas để hiện thay đổi
        time.sleep(DELAY / 1000.0)  # Tạm dừng để quan sát quá trình tìm kiếm

        # Kiểm tra nếu đã đến mục tiêu
        if (x, y) in goals:
            return path  # Trả về đường đi khi tìm thấy mục tiêu

        # Thử di chuyển đến các ô lân cận
        for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:  # Lên, trái, xuống, phải
            new_pos = (x + dx, y + dy)
            if new_pos not in visited and is_valid_move(grid, new_pos):
                visited.add(new_pos)
                queue.append((new_pos, path + [new_pos]))
                
                # Đánh dấu ô di chuyển (màu xanh lá cây nhạt)
                mark_move(canvas, new_pos)
                canvas.update()
                time.sleep(DELAY / 1000.0)

    return []  # Không tìm thấy đường đi

# Hàm chính để visualize BFS
def visualize_bfs(grid, start, goals, walls):
    root = tk.Tk()
    root.title("BFS Visualization")
    canvas = tk.Canvas(root, width=len(grid[0]) * CELL_SIZE, height=len(grid) * CELL_SIZE)
    canvas.pack()

    # Vẽ lưới ban đầu
    draw_grid(canvas, grid, start, goals, walls)
    
    # Bắt đầu BFS sau 1 giây để cho phép nhìn thấy lưới ban đầu
    root.after(1000, lambda: mark_path(canvas, bfs_visualize(canvas, grid, start, goals)))
    root.mainloop()


# Thuật toán DFS với visualize từng bước
def dfs_visualize(canvas, grid, start, goals):
    stack = [(start, [start])]  # Stack lưu các bước đi
    visited = set([start])  # Đánh dấu visited ngay khi thêm vào stack
    
    while stack:
        (x, y), path = stack.pop()
        visited.add((x, y))
        # Đánh dấu ô hiện tại trong stack (màu vàng)
        mark_queue(canvas, (x, y))
        canvas.update()  # Cập nhật canvas để hiện thay đổi
        time.sleep(DELAY / 1000.0)  # Tạm dừng để quan sát quá trình tìm kiếm

        # Kiểm tra nếu đã đến mục tiêu
        if (x, y) in goals:
            return path  # Trả về đường đi khi tìm thấy mục tiêu

        # Thử di chuyển đến các ô lân cận
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # Lên, trái, xuống, phải
            new_pos = (x + dx, y + dy)
            if new_pos not in visited and is_valid_move(grid, new_pos):
                stack.append((new_pos, path + [new_pos]))
                
                # Đánh dấu ô di chuyển (màu xanh lá cây nhạt)
                mark_move(canvas, new_pos)
                canvas.update()
                time.sleep(DELAY / 1000.0)

    return []  # Không tìm thấy đường đi

# Hàm chính để visualize DFS
def visualize_dfs(grid, start, goals, walls):
    root = tk.Tk()
    root.title("DFS Visualization")
    canvas = tk.Canvas(root, width=len(grid[0]) * CELL_SIZE, height=len(grid) * CELL_SIZE)
    canvas.pack()

    # Vẽ lưới ban đầu
    draw_grid(canvas, grid, start, goals, walls)
    
    # Bắt đầu DFS sau 1 giây để cho phép nhìn thấy lưới ban đầu
    root.after(1000, lambda: mark_path(canvas, dfs_visualize(canvas, grid, start, goals)))
    root.mainloop()

# Thuật toán A* với visualize từng bước
def astar_visualize(canvas, grid, start, goals):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    open_set_counter = itertools.count()
    
    while not open_set.empty():
        _, current = open_set.get()

        # Đánh dấu ô hiện tại trong hàng đợi (màu vàng)
        mark_queue(canvas, current)
        canvas.update()  # Cập nhật canvas để hiện thay đổi
        time.sleep(DELAY / 1000.0)  # Tạm dừng để quan sát quá trình tìm kiếm

        if current in goals:
            path = reconstruct_path(came_from, current)  # Tạo đường đi từ start đến goal
            mark_path(canvas, path)
            return

        for neighbor in get_neighbors(current, grid, is_valid_move):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goals)
                open_set.put((f_score, neighbor))

                # Đánh dấu ô đã di chuyển (màu xanh lá cây nhạt)
                mark_move(canvas, neighbor)
                canvas.update()
                time.sleep(DELAY / 1000.0)

# Hàm chính để visualize A*
def visualize_astar(grid, start, goals, walls):
    root = tk.Tk()
    root.title("A* Visualization")
    canvas = tk.Canvas(root, width=len(grid[0]) * CELL_SIZE, height=len(grid) * CELL_SIZE)
    canvas.pack()

    # Vẽ lưới ban đầu
    draw_grid(canvas, grid, start, goals, walls)

    # Bắt đầu A* sau 1 giây để cho phép nhìn thấy lưới ban đầu
    root.after(1000, lambda: astar_visualize(canvas, grid, start, goals))
    root.mainloop()

def gbfs_visualize(canvas, grid, start, goals):
    """
    Hàm thực hiện thuật toán Greedy Best-First Search (GBFS) và visual hóa nó trên canvas.
    """
    open_set = PriorityQueue()  # Khởi tạo hàng đợi ưu tiên để lưu trữ các nút đang được xem xét.
    open_set_counter = itertools.count()  # Đếm để xử lý các nút có giá trị heuristic bằng nhau.
    open_set_entries = set()  # Tập hợp để lưu các nút trong hàng đợi.
    closed_set = set()  # Tập hợp các nút đã được mở rộng.

    open_set.put((heuristic(start, goals), next(open_set_counter), start))  # Đưa điểm bắt đầu vào hàng đợi với giá trị heuristic.
    open_set_entries.add(start)  # Thêm điểm bắt đầu vào tập hợp.

    came_from = {}  # Từ điển dùng để lưu lại nút trước đó của mỗi ô.
    node_count = set()  # Biến đếm số lượng nút đã được mở rộng.

    while not open_set.empty():  # Tiếp tục cho đến khi hàng đợi ưu tiên trống.
        _, _, current = open_set.get()  # Lấy ô có giá trị heuristic nhỏ nhất ra khỏi hàng đợi.
        if current in open_set_entries:
            open_set_entries.remove(current)  # Xóa khỏi tập hợp nếu có.

        if current in closed_set:  # Nếu ô hiện tại đã được xử lý, bỏ qua nó.
            continue
        closed_set.add(current)  # Thêm ô hiện tại vào tập hợp các ô đã được duyệt qua.

        # Đánh dấu ô hiện tại trong hàng đợi (màu vàng)
        mark_queue(canvas, current)
        canvas.update()
        time.sleep(DELAY / 1000.0)

        if current in goals:  # Nếu tìm thấy mục tiêu:
            path = reconstruct_path(came_from, current)  # Tái tạo đường đi từ điểm xuất phát đến mục tiêu.
            mark_path(canvas, path)  # Vẽ đường đi cuối cùng (màu xanh lá cây đậm).
            return  # Kết thúc hàm.

        # Duyệt qua các ô lân cận
        for neighbor in get_neighbors(current, grid, is_valid_move):
            if neighbor not in closed_set and neighbor not in open_set_entries:
                node_count.add(neighbor)  # Tăng biến đếm số lượng nút đã duyệt.
                came_from[neighbor] = current  # Ghi nhận bước trước của ô lân cận.
                open_set.put((heuristic(neighbor, goals), next(open_set_counter), neighbor))  # Thêm ô lân cận vào hàng đợi.
                open_set_entries.add(neighbor)  # Thêm neighbor vào tập hợp.

                # Đánh dấu ô di chuyển (màu xanh lá cây nhạt)
                mark_move(canvas, neighbor)
                canvas.update()
                time.sleep(DELAY / 1000.0)

    # Nếu không tìm thấy đường đi
    print("No path found")
    return None

def visualize_gbfs(grid, start, goals, walls):
    root = tk.Tk()
    root.title("GBFS Visualization")
    canvas = tk.Canvas(root, width=len(grid[0]) * CELL_SIZE, height=len(grid) * CELL_SIZE)
    canvas.pack()

    # Vẽ lưới ban đầu
    draw_grid(canvas, grid, start, goals, walls)

    # Bắt đầu GBFS sau 1 giây để cho phép nhìn thấy lưới ban đầu
    root.after(1000, lambda: gbfs_visualize(canvas, grid, start, goals))
    root.mainloop()

def depth_limited_search_visualize(canvas, node, goals, depth_limit, path, visited, is_valid_move, grid):
    # Nếu node hiện tại là mục tiêu
    if node in goals:
        return path  # Trả về đường đi nếu tìm thấy mục tiêu

    # Dừng nếu đã đạt tới giới hạn độ sâu
    if depth_limit == 0:
        return None

    # Đánh dấu node hiện tại đang được kiểm tra (màu vàng)
    mark_queue(canvas, node)
    canvas.update()
    time.sleep(DELAY / 1000.0)

    # Thử di chuyển đến các ô lân cận theo thứ tự LÊN, TRÁI, XUỐNG, PHẢI
    for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        new_pos = (node[0] + dx, node[1] + dy)
        if new_pos not in visited and is_valid_move(grid, new_pos):
            visited.add(new_pos)  # Đánh dấu vị trí đã thăm
            
            # Đánh dấu node đã di chuyển (màu xanh lá cây nhạt)
            mark_move(canvas, new_pos)
            canvas.update()
            time.sleep(DELAY / 1000.0)

            # Gọi lại hàm tìm kiếm giới hạn độ sâu
            result = depth_limited_search_visualize(canvas, new_pos, goals, depth_limit - 1, path + [new_pos], visited, is_valid_move, grid)
            if result:  # Nếu tìm thấy mục tiêu
                return result

    return None  # Không tìm thấy kết quả trong độ sâu hiện tại

def iterative_deepening_search_visualize(canvas, grid, start, goals, is_valid_move):
    depth = 0  # Giới hạn độ sâu bắt đầu từ 0

    while True:
        visited = set([start])  # Reset tập hợp visited cho mỗi lần gọi DLS
        node_count = set([start])  # Đếm số lượng node đã duyệt trong mỗi lần gọi DLS
        
        # Gọi hàm DLS với giới hạn độ sâu hiện tại
        path = depth_limited_search_visualize(canvas, start, goals, depth, [start], visited, is_valid_move, grid)
        
        if path:  # Nếu tìm thấy đường đi tới mục tiêu
            goal_node = path[-1]  # Lấy vị trí của mục tiêu
            directions = [get_direction(path[i], path[i + 1]) for i in range(len(path) - 1)]

            # Đánh dấu đường đi cuối cùng (màu xanh lá cây đậm)
            mark_path(canvas, path)
            return goal_node, len(visited), directions  # Trả về vị trí đích, số node đã duyệt và hướng đi
        
        # Tăng giới hạn độ sâu
        depth += 1

# Hàm chính để visualize CUS1
def visualize_cus1(grid, start, goals, walls):
    root = tk.Tk()
    root.title("CUS1 (IDS) Visualization")
    canvas = tk.Canvas(root, width=len(grid[0]) * CELL_SIZE, height=len(grid) * CELL_SIZE)
    canvas.pack()

    # Vẽ lưới ban đầu
    draw_grid(canvas, grid, start, goals, walls)

    # Bắt đầu thuật toán sau 1 giây để nhìn thấy lưới ban đầu
    root.after(1000, lambda: iterative_deepening_search_visualize(canvas, grid, start, goals, is_valid_move))
    root.mainloop()

def ida_star_visualize(canvas, grid, start, goals, is_valid_move):
    # Ngưỡng ban đầu là giá trị heuristic từ điểm bắt đầu đến một trong các mục tiêu
    threshold = heuristic(start, goals)
    path = [start]  # Khởi tạo đường đi với điểm xuất phát
    visited_all = set()  # Lưu tất cả các vị trí đã thăm trong toàn bộ quá trình
    all_nodes = set([start])  # Lưu tất cả các node duy nhất đã gặp

    while True:
        visited = set([start])  # Reset tập visited cho mỗi lần lặp với ngưỡng mới
        stack = [(start, 0, path)]  # Sử dụng stack để mô phỏng quá trình duyệt DFS
        min_threshold = float('inf')  # Ngưỡng nhỏ nhất cho lần lặp tiếp theo
        all_nodes = set([start])  # Lưu tất cả các node duy nhất đã gặp

        #print(f"\nĐang thử với ngưỡng: {threshold}")  # Debug: In ra ngưỡng hiện tại

        while stack:
            node, g, current_path = stack.pop()  # Lấy phần tử trên cùng của stack
            visited.add(node)  # Đánh dấu đã thăm
            f = g + heuristic(node, goals)  # Tính f(n) = g(n) + h(n)

            # Nếu f(n) vượt ngưỡng, cập nhật min_threshold và bỏ qua nhánh này
            if f > threshold:
                min_threshold = min(min_threshold, f)
                continue

            # Nếu đã tìm thấy mục tiêu, trả về đường đi
            if node in goals:
                goal_node = node
                directions = [get_direction(current_path[i], current_path[i + 1]) 
                              for i in range(len(current_path) - 1)]
                mark_path(canvas, current_path)  # Đánh dấu đường đi cuối cùng
                return goal_node, len(all_nodes), directions

            # Đánh dấu node hiện tại đang được kiểm tra (màu vàng)
            mark_queue(canvas, node)
            canvas.update()
            time.sleep(DELAY / 1000.0)

            # Duyệt các ô lân cận theo thứ tự LÊN, TRÁI, XUỐNG, PHẢI
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                new_pos = (node[0] + dx, node[1] + dy)
                if new_pos not in visited and is_valid_move(grid, new_pos):
                    all_nodes.add(new_pos)  # Thêm vào tập các node duy nhất
                    #print(f"Bắt đầu từ {node} đến {new_pos}")
                    
                    # Đánh dấu node đã di chuyển (màu xanh lá cây nhạt)
                    mark_move(canvas, new_pos)
                    canvas.update()
                    time.sleep(DELAY / 1000.0)

                    # Thêm trạng thái mới vào stack để tiếp tục duyệt
                    stack.append((new_pos, g + 1, current_path + [new_pos]))

        # Nếu không tìm thấy lời giải trong lần này, cập nhật ngưỡng cho lần tiếp theo
        if min_threshold == float('inf'):
            return None, len(all_nodes), []  # Không có lời giải

        threshold = min_threshold  # Cập nhật ngưỡng mới

# Hàm chính để visualize CUS2 (IDA*)
def visualize_cus2(grid, start, goals, walls):
    root = tk.Tk()
    root.title("CUS2 (IDA*) Visualization")
    canvas = tk.Canvas(root, width=len(grid[0]) * CELL_SIZE, height=len(grid) * CELL_SIZE)
    canvas.pack()

    # Vẽ lưới ban đầu
    draw_grid(canvas, grid, start, goals, walls)

    # Bắt đầu thuật toán sau 1 giây để nhìn thấy lưới ban đầu
    root.after(1000, lambda: ida_star_visualize(canvas, grid, start, goals, is_valid_move))
    root.mainloop()

# Chương trình bắt đầu từ đây
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python visualize.py <input_file> <algorithm>")
        sys.exit(1)
    
    filename = sys.argv[1]  # Đọc tên file từ dòng lệnh
    algorithm = sys.argv[2].upper()  # Đọc thuật toán từ dòng lệnh và chuyển thành chữ in hoa

    # Đọc input và khởi tạo grid
    grid_size, start_pos, goal_positions, walls = read_input(filename)
    grid = create_grid(grid_size, walls)

    # Visualize thuật toán
    if algorithm == "BFS":
        visualize_bfs(grid, start_pos, goal_positions, walls)
    elif algorithm == "DFS":
        visualize_dfs(grid, start_pos, goal_positions, walls)
    elif algorithm == "AS":
        visualize_astar(grid, start_pos, goal_positions, walls)
    elif algorithm == "GBFS":
        visualize_gbfs(grid, start_pos, goal_positions, walls)
    elif algorithm == "CUS1":
        visualize_cus1(grid, start_pos, goal_positions, walls)
    elif algorithm == "CUS2":
        visualize_cus2(grid, start_pos, goal_positions, walls)
    else:
        print(f"Unsupported algorithm: {algorithm}")
        sys.exit(1)
