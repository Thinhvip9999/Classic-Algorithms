from queue import PriorityQueue  # Import hàng đợi ưu tiên (PriorityQueue) để quản lý các nút dựa trên giá trị heuristic.
from utils import get_direction  # Import hàm get_direction từ file utils, dùng để lấy hướng di chuyển từ một ô đến ô khác.
from utils import heuristic  # Import hàm heuristic từ file utils, đây là hàm đánh giá khoảng cách từ một điểm đến điểm đích.
import itertools  # Import thư viện itertools để sử dụng biến đếm counter cho Priority Queue.

def gbfs(grid, start, goals, is_valid_move):
    """
    Hàm thực hiện thuật toán Greedy Best-First Search (GBFS) tìm đường từ 'start' đến một trong các điểm đích trong 'goals'.
    grid: Bản đồ (ma trận) lưới để tìm đường.
    start: Điểm bắt đầu (tọa độ dạng tuple (x, y)).
    goals: Tập hợp các điểm đích (là một danh sách các tọa độ).
    is_valid_move: Hàm kiểm tra xem có thể di chuyển đến một vị trí trong lưới hay không.
    """
    open_set = PriorityQueue()  # Khởi tạo hàng đợi ưu tiên để lưu trữ các nút đang được xem xét, ưu tiên dựa trên giá trị heuristic.
    open_set_counter = itertools.count()  # Tạo một biến đếm để đảm bảo khi f bằng nhau, ô nào được thêm trước sẽ được duyệt trước.
    open_set_entries = set()  # Tập hợp để lưu các nút trong hàng đợi
    closed_set = set()  # Tập hợp các nút đã được mở rộng (đã duyệt qua).

    open_set.put((heuristic(start, goals), open_set_counter, start))  # Đưa điểm bắt đầu vào hàng đợi với giá trị heuristic.
    open_set_entries.add(start)  # Thêm điểm bắt đầu vào tập hợp

    came_from = {}  # Từ điển dùng để lưu lại nút trước đó của mỗi ô để có thể tái tạo lại đường đi.
    node_count = set()  # Biến đếm số lượng nút đã được mở rộng.
    node_count.add(start)

    # Vòng lặp chính của thuật toán
    while not open_set.empty():  # Tiếp tục cho đến khi hàng đợi ưu tiên trống.
        _, _, current = open_set.get()  # Lấy ô có giá trị heuristic nhỏ nhất ra khỏi hàng đợi.
        open_set_entries.remove(current)  # Xóa nó khỏi tập hợp

        if current in closed_set:  # Nếu ô hiện tại đã được xử lý, bỏ qua nó.
            continue
        closed_set.add(current)  # Thêm ô hiện tại vào tập hợp các ô đã được mở rộng (duyệt qua).

        if current in goals:  # Nếu ô hiện tại là một trong các điểm đích:
            path = reconstruct_path(came_from, current)  # Tái tạo lại đường đi từ điểm xuất phát đến đích.
            directions = [get_direction(path[i], path[i+1]) for i in range(len(path)-1)]  # Tính toán hướng di chuyển cho từng bước trong đường đi.
            return current, len(node_count), directions  # Trả về điểm đích, số nút đã duyệt, và danh sách các hướng đi.

        # Duyệt qua các ô lân cận của ô hiện tại
        for neighbor in get_neighbors(current, grid, is_valid_move):
            if neighbor not in closed_set:
                if neighbor not in open_set_entries:  
                    node_count.add(neighbor)  # Tăng biến đếm số lượng nút đã duyệt.
                    came_from[neighbor] = current  # Ghi nhận rằng ô hiện tại là bước đi trước của ô lân cận.
                    open_set.put((heuristic(neighbor, goals), next(open_set_counter), neighbor))  # Thêm ô lân cận vào hàng đợi với giá trị heuristic của nó.
                    open_set_entries.add(neighbor)  # Thêm neighbor vào tập hợp
    
    # Nếu không tìm được đường đi đến đích
    return None, node_count, []  # Trả về None nếu không tìm thấy đường đi, cùng với số nút đã duyệt và danh sách trống.

# Hàm để lấy các ô lân cận của nút hiện tại
def get_neighbors(pos, grid, is_valid_move):
    """
    Hàm này trả về danh sách các ô lân cận (neighbor) có thể di chuyển đến từ vị trí hiện tại.
    pos: Vị trí hiện tại (tọa độ tuple (x, y)).
    grid: Bản đồ (ma trận) lưới.
    is_valid_move: Hàm kiểm tra xem có thể di chuyển đến vị trí lân cận hay không.
    """
    x, y = pos  # Lấy tọa độ hiện tại (x, y).
    neighbors = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]  # Danh sách các ô lân cận (trên, trái, dưới, phải).
    return [n for n in neighbors if is_valid_move(grid, n)]  # Trả về các ô lân cận hợp lệ dựa trên hàm kiểm tra is_valid_move.

# Hàm để tái tạo lại đường đi từ điểm xuất phát đến đích
def reconstruct_path(came_from, current):
    """
    Hàm tái tạo lại đường đi sau khi đã tìm thấy điểm đích.
    came_from: Từ điển chứa thông tin ô trước đó của mỗi ô.
    current: Ô đích mà ta muốn tái tạo lại đường đi từ nó.
    """
    path = [current]  # Bắt đầu đường đi từ điểm đích.
    while current in came_from:  # Quay ngược lại từ điểm đích đến điểm xuất phát.
        current = came_from[current]  # Cập nhật current thành ô trước đó.
        path.insert(0, current)  # Chèn ô trước đó vào đầu danh sách đường đi.
    return path  # Trả về toàn bộ đường đi từ điểm xuất phát đến đích.
