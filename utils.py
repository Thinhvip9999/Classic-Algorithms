# utils.py
def get_direction(current, next):
    x1, y1 = current
    x2, y2 = next
    if x2 > x1:
        return 'right'
    elif x2 < x1:
        return 'left'
    elif y2 > y1:
        return 'down'
    elif y2 < y1:
        return 'up'

def print_result(goal_node, node_count, directions):
    if directions:
        print(f"<Node {goal_node}> {node_count}")
        print(directions)
    else:
        print(f"No path found after exploring {node_count} nodes.")

# Thêm hàm heuristic
def heuristic(pos, goals):
    # Mặc định sử dụng Manhattan distance
    return min(abs(pos[0] - g[0]) + abs(pos[1] - g[1]) for g in goals)
