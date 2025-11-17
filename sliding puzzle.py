import heapq

goal_state = [[1,2,3],
              [4,5,6],
              [7,8,0]]

moves = [(1,0), (-1,0), (0,1), (0,-1)]

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def is_goal(state):
    return state == goal_state

def manhattan_distance(state):
    d = 0
    for i in range(3):
        for j in range(3):
            v = state[i][j]
            if v != 0:
                gx = (v - 1) // 3
                gy = (v - 1) % 3
                d += abs(i - gx) + abs(j - gy)
    return d

def get_neighbors(state):
    neighbors = []
    x, y = find_blank(state)

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def a_star(start):
    pq = []
    heapq.heappush(pq, (manhattan_distance(start), start, []))
    visited = set()

    while pq:
        cost, state, path = heapq.heappop(pq)
        state_tuple = tuple(tuple(r) for r in state)

        if state_tuple in visited:
            continue

        visited.add(state_tuple)

        if is_goal(state):
            return path + [state]

        for n in get_neighbors(state):
            heapq.heappush(pq, (manhattan_distance(n), n, path + [state]))

    return None

def print_board(state):
    for row in state:
        print(row)
    print()

start_state = [[1,6,5],
               [7,3,8],
               [4,2,0]]

print("Solving puzzle...\n")
solution = a_star(start_state)

if solution:
    print("Solution Steps:")
    for step in solution:
        print_board(step)
else:
    print("This puzzle has NO solution.")

