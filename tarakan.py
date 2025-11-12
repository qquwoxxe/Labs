import tkinter as tk
import random
from collections import deque


class GoodMaze:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Таракан в лабиринте")
        self.root.geometry("700x700")

        self.cell_size = 25
        self.width = 21
        self.height = 21

        self.create_widgets()
        self.generate_good_maze()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Новый лабиринт", command=self.generate_good_maze).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Найти выход", command=self.find_exit).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Очистить путь", command=self.draw_maze).pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(self.root, width=self.width * self.cell_size,
                                height=self.height * self.cell_size, bg='white')
        self.canvas.pack(pady=10)

    def find_exit_position(self):
        """Находит позицию выхода"""
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 'E':
                    return x, y
        return self.width - 2, self.height - 2

    def generate_good_maze(self):
        self.maze = [['#' for _ in range(self.width)] for _ in range(self.height)]

        start_x, start_y = 1, 1
        self.maze[start_y][start_x] = ' '

        frontiers = []
        for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
            nx, ny = start_x + dx, start_y + dy
            if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                frontiers.append((nx, ny, start_x, start_y))

        while frontiers:
            fx, fy, px, py = frontiers.pop(random.randint(0, len(frontiers) - 1))

            if self.maze[fy][fx] == '#':
                self.maze[fy][fx] = ' '
                self.maze[(fy + py) // 2][(fx + px) // 2] = ' '

                for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                    nx, ny = fx + dx, fy + dy
                    if 0 < nx < self.width - 1 and 0 < ny < self.height - 1 and self.maze[ny][nx] == '#':
                        frontiers.append((nx, ny, fx, fy))

        self.maze[1][1] = 'S'

        exit_x, exit_y = self.find_farthest_point(1, 1)
        self.maze[exit_y][exit_x] = 'E'

        self.draw_maze()

    def find_farthest_point(self, start_x, start_y):
        visited = set()
        queue = deque([(start_x, start_y, 0)])
        farthest_x, farthest_y = start_x, start_y
        max_distance = 0

        while queue:
            x, y, dist = queue.popleft()

            if (x, y) in visited:
                continue
            visited.add((x, y))

            if dist > max_distance and self.maze[y][x] == ' ':
                max_distance = dist
                farthest_x, farthest_y = x, y

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and
                        self.maze[ny][nx] != '#' and (nx, ny) not in visited):
                    queue.append((nx, ny, dist + 1))

        return farthest_x, farthest_y

    def draw_maze(self):
        self.canvas.delete("all")

        for y in range(self.height):
            for x in range(self.width):
                color = 'white'
                if self.maze[y][x] == '#':
                    color = 'black'
                elif self.maze[y][x] == 'S':
                    color = 'green'
                elif self.maze[y][x] == 'E':
                    color = 'red'

                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, outline='gray', width=1
                )

    def find_exit(self):
        visited = set()
        path = []

        def dfs(x, y):
            if (x < 0 or x >= self.width or y < 0 or y >= self.height or
                    self.maze[y][x] == '#' or (x, y) in visited):
                return False

            visited.add((x, y))
            path.append((x, y))

            self.canvas.create_oval(
                x * self.cell_size + 5, y * self.cell_size + 5,
                (x + 1) * self.cell_size - 5, (y + 1) * self.cell_size - 5,
                fill='blue', tags='path', outline='darkblue', width=2
            )
            self.root.update()
            self.root.after(50)

            if self.maze[y][x] == 'E':
                for px, py in path:
                    self.canvas.create_oval(
                        px * self.cell_size + 3, py * self.cell_size + 3,
                        (px + 1) * self.cell_size - 3, (py + 1) * self.cell_size - 3,
                        fill='lime', tags='solution', outline='green', width=2
                    )
                return True

            exit_x, exit_y = self.find_exit_position()

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            directions.sort(key=lambda d: abs((x + d[0]) - exit_x) + abs((y + d[1]) - exit_y))

            for dx, dy in directions:
                if dfs(x + dx, y + dy):
                    return True

            path.pop()
            self.canvas.create_rectangle(
                x * self.cell_size, y * self.cell_size,
                (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                fill='lightblue', outline='gray', tags='path', width=1
            )
            return False

        self.canvas.delete('path')
        self.canvas.delete('solution')
        dfs(1, 1)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    maze = GoodMaze()
    maze.run()