# Требуется написать ООП с графическим интерфейсом в соответствии со своим вариантом.
# Должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
# Ввод данных из файла с контролем правильности ввода.
# Базы данных не использовать. При необходимости сохранять информацию в файлах, разделяя значения
# запятыми (CSV файлы) или пробелами. Для GUI использовать библиотеку tkinter (mathplotlib не использовать).
# Объекты – полукруги
# Функции:	сегментация
#           визуализация
#           раскраска
#           поворот вокруг заданного угла полукруга
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import math
import csv
from collections import Counter
import random


class Semicircle:
    def __init__(self, x, y, radius, color="blue"):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.angle = 0

    def draw(self, canvas):
        points = []
        for angle in range(0, 181, 5):
            rad = math.radians(angle)
            dx = self.radius * math.cos(rad)
            dy = self.radius * math.sin(rad)
            points.append((self.x + dx, self.y - dy))

        if self.angle != 0:
            rad_angle = math.radians(self.angle)
            cos_a = math.cos(rad_angle)
            sin_a = math.sin(rad_angle)
            rotated_points = []
            for x, y in points:
                x -= self.x
                y -= self.y
                new_x = x * cos_a - y * sin_a
                new_y = x * sin_a + y * cos_a
                rotated_points.append((new_x + self.x, new_y + self.y))
            points = rotated_points

        if points:
            canvas.create_polygon(points, fill=self.color, outline=self.color)

    def rotate(self, angle):
        self.angle = angle

    def change_color(self, new_color):
        self.color = new_color


def load_and_show_file(filename):
    """Загружает данные и отображает содержимое файла"""
    global semicircles


    semicircles = []
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)


            for item in file_content_tree.get_children():
                file_content_tree.delete(item)

            for i, row in enumerate(reader, 1):
                try:
                    if len(row) < 3:
                        raise ValueError("Недостаточно данных в строке")

                    x, y, radius = map(float, row[:3])
                    color = row[3] if len(row) > 3 else "blue"
                    semicircles.append(Semicircle(x, y, radius, color))

                    file_content_tree.insert('', 'end', values=(
                        f"{x:.2f}",
                        f"{y:.2f}",
                        f"{radius:.2f}",
                        color
                    ))

                except ValueError as e:
                    log_error(f"Ошибка в строке {i}: {row} - {e}")

        visualize_semicircles(semicircles, canvas)
        file_content_label.config(text=f"Файл: {filename.split('/')[-1]}")
        log_message(f"Успешно загружен файл: {filename}")
        show_original()  # Показываем исходную визуализацию

    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл {filename} не найден.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Неожиданная ошибка: {e}")


def open_file():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        load_and_show_file(filename)


def visualize_semicircles(semicircles, canvas):
    canvas.delete("all")
    for semicircle in semicircles:
        semicircle.draw(canvas)
    log_message(f"Отображено {len(semicircles)} полукругов")


def rotate_all():
    try:
        angle = float(angle_entry.get())
        for semicircle in semicircles:
            semicircle.rotate(angle)
        visualize_semicircles(semicircles, canvas)
        log_message(f"Все полукруги повернуты на угол {angle} градусов")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректный угол (число)")
        log_error("Ошибка ввода угла поворота")


def log_message(message):
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, message + "\n")
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)


def log_error(message):
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, "ОШИБКА: " + message + "\n", "error")
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)


def segment_by_radius():

    if not semicircles:
        messagebox.showwarning("Нет данных", "Сначала загрузите данные")
        return


    groups = {
        "Маленький (0-50)": lambda r: r <= 50,
        "Средний (50-100)": lambda r: 50 < r <= 100,
        "Большой (>100)": lambda r: r > 100
    }

    counts = {name: 0 for name in groups}

    for s in semicircles:
        for name, condition in groups.items():
            if condition(s.radius):
                counts[name] += 1
                break

    draw_pie_chart(counts, "Сегментация по радиусу", ["#ff9999", "#66b3ff", "#99ff99"])


def segment_by_color():

    if not semicircles:
        messagebox.showwarning("Нет данных", "Сначала загрузите данные")
        return

    color_counts = Counter(s.color for s in semicircles)

    palette = generate_color_palette(len(color_counts))

    draw_pie_chart(color_counts, "Сегментация по цвету", palette)


def generate_color_palette(n):
    colors = []
    for i in range(n):
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        colors.append(f"#{r:02x}{g:02x}{b:02x}")
    return colors


def draw_pie_chart(data, title, palette):
    canvas.delete("all")
    total = sum(data.values())
    if total == 0:
        return

    # Получаем размеры холста
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if width < 10 or height < 10:
        width, height = 600, 400

    cx, cy = width // 2, height // 2
    radius = min(width, height) * 0.35

    canvas.create_text(cx, 30, text=title, font=("Arial", 16, "bold"))

    start_angle = 0
    items = list(data.items())

    for i, (label, count) in enumerate(items):
        angle = 360 * count / total

        canvas.create_arc(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            start=start_angle, extent=angle,
            fill=palette[i % len(palette)], outline="white", width=2
        )

        percent = count / total * 100
        mid_angle = start_angle + angle / 2
        rad_angle = math.radians(mid_angle)
        label_radius = radius * 0.7
        x = cx + label_radius * math.cos(rad_angle)
        y = cy - label_radius * math.sin(rad_angle)

        if angle > 10:
            canvas.create_text(x, y, text=f"{percent:.1f}%", font=("Arial", 10))

        start_angle += angle

    legend_x = cx + radius + 20
    legend_y = cy - radius + 20

    for i, (label, count) in enumerate(items):
        y = legend_y + i * 30
        canvas.create_rectangle(
            legend_x, y,
            legend_x + 20, y + 20,
            fill=palette[i % len(palette)], outline="black"
        )
        canvas.create_text(
            legend_x + 25, y + 10,
            text=f"{label}: {count} ({count / total * 100:.1f}%)",
            anchor="w", font=("Arial", 10)
        )

    log_message(f"Построена круговая диаграмма: {title}")


def show_original():
    if semicircles:
        visualize_semicircles(semicircles, canvas)
    else:
        canvas.delete("all")
        canvas.create_text(300, 200, text="Загрузите данные для визуализации",
                           font=("Arial", 14), fill="gray")


root = tk.Tk()
root.title("Визуализатор полукругов с сегментацией")
root.geometry("1400x800")

main_container = tk.PanedWindow(root, orient=tk.HORIZONTAL)
main_container.pack(fill=tk.BOTH, expand=True)

left_panel = tk.Frame(main_container)
main_container.add(left_panel)

control_frame = tk.Frame(left_panel)
control_frame.pack(fill=tk.X, pady=5)

tk.Button(control_frame, text="Открыть файл", command=open_file).pack(side=tk.LEFT, padx=5)

tk.Label(control_frame, text="Угол поворота:").pack(side=tk.LEFT, padx=(10, 2))
angle_entry = tk.Entry(control_frame, width=5)
angle_entry.pack(side=tk.LEFT)
angle_entry.insert(0, "0")

tk.Button(control_frame, text="Применить поворот", command=rotate_all).pack(side=tk.LEFT, padx=5)

segment_frame = tk.Frame(control_frame)
segment_frame.pack(side=tk.LEFT, padx=(20, 0))

tk.Label(segment_frame, text="Сегментация:").pack(side=tk.LEFT)
tk.Button(segment_frame, text="По радиусу", command=segment_by_radius).pack(side=tk.LEFT, padx=5)
tk.Button(segment_frame, text="По цвету", command=segment_by_color).pack(side=tk.LEFT, padx=5)
tk.Button(segment_frame, text="Исходная визуализация", command=show_original).pack(side=tk.LEFT, padx=5)

canvas_frame = tk.Frame(left_panel)
canvas_frame.pack(fill=tk.BOTH, expand=True)
canvas = tk.Canvas(canvas_frame, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)


def on_canvas_resize(event):
    if semicircles:
        visualize_semicircles(semicircles, canvas)


canvas.bind("<Configure>", on_canvas_resize)

output_frame = tk.Frame(left_panel)
output_frame.pack(fill=tk.BOTH, expand=False)

output_label = tk.Label(output_frame, text="Журнал событий:")
output_label.pack(anchor=tk.W)

output_text = tk.Text(output_frame, height=8, wrap=tk.WORD)
output_text.pack(fill=tk.BOTH, expand=True)
output_text.tag_config("error", foreground="red")

scrollbar = ttk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)
output_text.config(state=tk.DISABLED)

right_panel = tk.Frame(main_container)
main_container.add(right_panel)

file_content_frame = tk.Frame(right_panel)
file_content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

file_content_label = tk.Label(file_content_frame, text="Данные из файла")
file_content_label.pack(anchor=tk.W)

file_content_tree = ttk.Treeview(file_content_frame,
                                 columns=("X", "Y", "Радиус", "Цвет"),
                                 show="headings",
                                 height=30)
file_content_tree.pack(fill=tk.BOTH, expand=True)

columns = [
    ("X", "Координата X", 120),
    ("Y", "Координата Y", 120),
    ("Радиус", "Радиус", 100),
    ("Цвет", "Цвет", 100)
]

for col_id, col_text, width in columns:
    file_content_tree.heading(col_id, text=col_text)
    file_content_tree.column(col_id, width=width, anchor='center')

scrollbar = ttk.Scrollbar(file_content_frame,
                          orient="vertical",
                          command=file_content_tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
file_content_tree.configure(yscrollcommand=scrollbar.set)

semicircles = []
show_original()

root.mainloop()