from queue import PriorityQueue
from utils import get_direction, heuristic, print_result
import itertools  # Import thư viện itertools để sử dụng biến đếm counter cho Priority Queue.

def two_goals_astar(grid, start, goals, is_valid_move):
    """
    Thuật toán A* để tìm đường ghé qua tất cả các đích trong goals.
    """
    #List lưu trữ kết quả (goal_position, node_count, path)
    all_result = []

    total_path = []  # Lưu trữ toàn bộ đường đi qua tất cả các đích.
    total_directions = []  # Lưu trữ tất cả các hướng đi.
    total_nodes_expanded = 0  # Đếm tổng số nút đã mở rộng.
    total_goals_reached = [] #Lưu giữ lại các goal đã reach (vị trí goal đó, số node count, path)

    current_start = start  # Điểm bắt đầu của lần tìm kiếm hiện tại.
    remaining_goals = set(goals)  # Tập các đích cần ghé thăm.

    while remaining_goals:
        # Gọi A* để tìm đường từ current_start đến đích gần nhất.
        nearest_goal, nodes_expanded, directions = astar_single_goal(grid, current_start, remaining_goals, is_valid_move)

        if nearest_goal is None:
            print("Không thể tìm đường tới tất cả các đích.")
            all_result.append(None, total_nodes_expanded, [])  # Trả về nếu không thể tìm thấy đường.

        # Cập nhật thông tin đường đi.
        total_path.extend(directions)
        total_nodes_expanded += nodes_expanded

        # Loại bỏ đích đã ghé thăm và cập nhật điểm xuất phát.
        remaining_goals.remove(nearest_goal)
        current_start = nearest_goal

        #Lưu kết quả lại sau khi cập nhật thông tin đường đi
        all_result.append([current_start, total_nodes_expanded, total_path])
        print_result(current_start, total_nodes_expanded, total_path)
    return all_result

def astar_single_goal(grid, start, goals, is_valid_move):
    """
    Tìm đường từ start đến đích gần nhất trong goals.
    """
    open_set = PriorityQueue()
    open_set_counter = itertools.count()  # Tạo một biến đếm để đảm bảo khi f bằng nhau, ô nào được thêm trước sẽ được duyệt trước.
    open_set.put((0, next(open_set_counter), start))
    came_from = {}
    g_score = {start: 0}
    node_count = set()
    node_count.add(start)

    while not open_set.empty():
        _, _, current = open_set.get()

        if current in goals:
            #print(f"Đến đích rồi: {current}")
            path = reconstruct_path(came_from, current)
            directions = [get_direction(path[i], path[i + 1]) for i in range(len(path) - 1)]
            return current, len(node_count), directions

        for neighbor in get_neighbors(current, grid, is_valid_move):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                node_count.add(neighbor)
                #print(f"Node duyệt số {len(node_count)} từ {current} đến {neighbor}")
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goals)
                open_set.put((f_score, next(open_set_counter), neighbor))

        #print(f"Hết neighbor của {current} \n")

    return None, len(node_count), []

def get_neighbors(pos, grid, is_valid_move):
    x, y = pos
    neighbors = [(x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y)]
    return [n for n in neighbors if is_valid_move(grid, n)]

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.insert(0, current)
    return path
