from queue import PriorityQueue  # Import thư viện hàng đợi ưu tiên (PriorityQueue) để sử dụng trong thuật toán A*.
from utils import get_direction  # Import hàm get_direction từ file utils, dùng để lấy hướng đi từ một vị trí đến vị trí khác.
from utils import heuristic  # Import hàm heuristic từ file utils, đây là hàm đánh giá để tính toán khoảng cách từ điểm hiện tại đến mục tiêu.
import itertools  # Import thư viện itertools để sử dụng biến đếm counter cho Priority Queue.

def astar(grid, start, goals, is_valid_move):
    """
    Hàm thực hiện thuật toán A* tìm đường ngắn nhất từ điểm xuất phát 'start' đến một trong các điểm đích trong 'goals'.
    grid: Bản đồ (ma trận) lưới để tìm đường.
    start: Điểm xuất phát (tọa độ dưới dạng tuple (x, y)).
    goals: Tập hợp các điểm đích (là một danh sách các tọa độ).
    is_valid_move: Hàm kiểm tra xem có thể di chuyển đến một vị trí (ô) trong lưới hay không.
    """
    open_set = PriorityQueue()  # Khởi tạo hàng đợi ưu tiên để quản lý các ô sẽ được duyệt, theo thứ tự ưu tiên của hàm f.
    open_set_counter = itertools.count()  # Tạo một biến đếm để đảm bảo khi f bằng nhau, ô nào được thêm trước sẽ được duyệt trước.
    open_set.put((0, next(open_set_counter), start))  # Đưa điểm bắt đầu vào hàng đợi với chi phí là 0 và thêm biến đếm.
    came_from = {}  # Từ điển dùng để lưu lại bước đi trước của mỗi ô, giúp tái tạo lại đường đi.
    g_score = {start: 0}  # Từ điển lưu giá trị g (chi phí từ điểm xuất phát đến ô hiện tại) cho từng ô, g của start là 0.
    node_count = set()  # Biến đếm số lượng nút đã được mở rộng.
    node_count.add(start)

    while not open_set.empty():  # Vòng lặp tiếp tục cho đến khi hàng đợi trống.
        _, _, current = open_set.get()  # Lấy ô có giá trị f nhỏ nhất ra khỏi hàng đợi. _, current do chúng ta chỉ cần quan tâm đến vị trí current (f đã được sort theo giá trị từ bé nhất đến lớn nhất của f)
        
        if current in goals:  # Nếu ô hiện tại là một trong các điểm đích:
            path = reconstruct_path(came_from, current)  # Tái tạo lại đường đi từ điểm xuất phát đến điểm đích.
            directions = [get_direction(path[i], path[i+1]) for i in range(len(path)-1)]  # Lấy hướng đi cho từng bước trong đường đi.
            #print(node_count)
            return current, len(node_count), directions  # Trả về ô đích, số nút đã mở rộng, và các hướng đi.

        # Duyệt qua các ô lân cận của ô hiện tại.
        for neighbor in get_neighbors(current, grid, is_valid_move):  
            tentative_g_score = g_score[current] + 1  # Tính toán giá trị g tạm thời của ô lân cận.
            # Nếu ô lân cận chưa có g_score hoặc g mới nhỏ hơn g đã biết:
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                node_count.add(neighbor)  # Tăng biến đếm số lượng nút đã mở rộng.
                #print(f"Node duyệt số {len(node_count)} bắt đầu từ {current} đến {neighbor}")
                came_from[neighbor] = current  # Ghi nhận rằng ô hiện tại là bước trước của ô lân cận.
                g_score[neighbor] = tentative_g_score  # Cập nhật giá trị g của ô lân cận.
                f_score = tentative_g_score + heuristic(neighbor, goals)  # Tính toán giá trị f (g + h) của ô lân cận.
                open_set.put((f_score, next(open_set_counter), neighbor))  # Đưa ô lân cận vào hàng đợi ưu tiên với giá trị f mới và thứ tự thêm.
        #print(f"Hết neighbor của {current} \n")

    return None, node_count, []  # Nếu không tìm thấy đường đi, trả về None, số lượng nút đã mở rộng, và danh sách trống (không có hướng đi).

def get_neighbors(pos, grid, is_valid_move):
    """
    Hàm lấy danh sách các ô lân cận có thể di chuyển từ vị trí hiện tại.
    pos: Tọa độ hiện tại (tuple (x, y)).
    grid: Bản đồ (ma trận) lưới.
    is_valid_move: Hàm kiểm tra xem có thể di chuyển đến vị trí lân cận hay không.
    """
    x, y = pos  # Tách vị trí hiện tại thành tọa độ x, y.
    neighbors = [(x, y-1), (x-1, y), (x, y+1), (x+1, y)]  # Danh sách các ô lân cận (trên, trái, dưới, phải).
    return [n for n in neighbors if is_valid_move(grid, n)]  # Trả về các ô lân cận hợp lệ có thể di chuyển.

def reconstruct_path(came_from, current):
    """
    Hàm tái tạo lại đường đi từ điểm xuất phát đến điểm đích.
    came_from: Từ điển lưu lại thông tin ô trước đó của mỗi ô.
    current: Ô đích mà ta muốn tái tạo lại đường đi.
    """
    path = [current]  # Bắt đầu đường đi từ điểm đích.
    while current in came_from:  # Quay ngược lại từ điểm đích đến điểm xuất phát bằng cách nhìn vào từ điển came_from.
        current = came_from[current]  # Cập nhật current thành ô trước đó.
        path.insert(0, current)  # Chèn ô trước đó vào đầu danh sách đường đi.
    return path  # Trả về toàn bộ đường đi từ điểm xuất phát đến đích.
