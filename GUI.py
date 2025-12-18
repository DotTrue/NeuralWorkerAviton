import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

import brain

class DigitRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Распознавание цифр с визуализацией")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')

        # Переменные
        self.canvas_data = []
        self.drawing = False
        self.last_x = None
        self.last_y = None

        self.setup_ui()

    def setup_ui(self):
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Заголовок
        title_label = tk.Label(
            main_frame,
            text="Распознавание рукописных цифр",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=(0, 20))

        # Контейнер для двух кубиков
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(expand=True, fill='both')

        # Левый кубик - холст для рисования
        left_cube = tk.Frame(content_frame, bg='white', relief='solid', bd=2)
        left_cube.pack(side='left', expand=True, fill='both', padx=(0, 10))

        # Заголовок левого кубика
        left_title = tk.Label(
            left_cube,
            text="Нарисуйте цифру",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#444'
        )
        left_title.pack(pady=15)

        # Холст для рисования
        self.canvas = tk.Canvas(
            left_cube,
            bg='#f8f8f8',
            width=400,
            height=400,
            highlightthickness=1,
            highlightbackground='#ccc'
        )
        self.canvas.pack(pady=10, padx=20)

        # Привязка событий мыши
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)

        # Инструкция
        instruction = tk.Label(
            left_cube,
            text="Рисуйте цифру мышкой в области выше",
            font=('Arial', 10),
            bg='white',
            fg='#666'
        )
        instruction.pack(pady=(5, 15))

        # Кнопки под левым кубиком
        button_frame = tk.Frame(left_cube, bg='white')
        button_frame.pack(pady=(0, 20))

        # Кнопка "Распознать"
        recognize_btn = tk.Button(
            button_frame,
            text="РАСПОЗНАТЬ",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=30,
            pady=10,
            command=self.recognize_digit,
            relief='flat',
            cursor='hand2'
        )
        recognize_btn.pack(side='left', padx=5)

        # Кнопка "Очистить"
        clear_btn = tk.Button(
            button_frame,
            text="ОЧИСТИТЬ",
            font=('Arial', 12, 'bold'),
            bg='#f44336',
            fg='white',
            padx=30,
            pady=10,
            command=self.clear_canvas,
            relief='flat',
            cursor='hand2'
        )
        clear_btn.pack(side='left', padx=5)

        # Кнопка "Показать матрицу"
        matrix_btn = tk.Button(
            button_frame,
            text="МАТРИЦА 28x28",
            font=('Arial', 12, 'bold'),
            bg='#2196F3',
            fg='white',
            padx=30,
            pady=10,
            command=self.show_matrix_visualization,
            relief='flat',
            cursor='hand2'
        )
        matrix_btn.pack(side='left', padx=5)

        # Правый кубик - результат
        right_cube = tk.Frame(content_frame, bg='white', relief='solid', bd=2)
        right_cube.pack(side='right', expand=True, fill='both', padx=(10, 0))

        # Заголовок правого кубика
        right_title = tk.Label(
            right_cube,
            text="Результат распознавания",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#444'
        )
        right_title.pack(pady=30)

        # Большой дисплей для цифры
        self.result_display = tk.Label(
            right_cube,
            text="?",
            font=('Arial', 120, 'bold'),
            bg='white',
            fg='#2196F3'
        )
        self.result_display.pack(expand=True)

        # Вероятность
        self.probability_label = tk.Label(
            right_cube,
            text="Вероятность: --%",
            font=('Arial', 12),
            bg='white',
            fg='#666'
        )
        self.probability_label.pack(pady=(0, 30))

        # Информация о матрице
        self.matrix_info = tk.Label(
            right_cube,
            text="Матрица: --\nMin: -- Max: --\nMean: --",
            font=('Courier', 9),
            bg='#f5f5f5',
            fg='#333',
            relief='solid',
            bd=1,
            padx=10,
            pady=10
        )
        self.matrix_info.pack(fill='x', padx=20, pady=10)

        # Статус бар
        self.status_bar = tk.Label(
            main_frame,
            text="Готов к рисованию",
            font=('Arial', 10),
            bg='#e0e0e0',
            fg='#333',
            anchor='w',
            relief='sunken',
            bd=1
        )
        self.status_bar.pack(fill='x', pady=(20, 0))

    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        self.status_bar.config(text="Рисование...")

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            line = self.canvas.create_line(
                self.last_x, self.last_y, x, y,
                width=8,
                fill='black',
                capstyle='round',
                smooth=True
            )
            self.canvas_data.append(line)
            self.last_x = x
            self.last_y = y

    def stop_drawing(self, event):
        self.drawing = False
        self.status_bar.config(text="Рисование завершено")

    def clear_canvas(self):
        """Очищает холст"""
        for item in self.canvas_data:
            self.canvas.delete(item)
        self.canvas_data = []
        self.result_display.config(text="?", fg='#2196F3')
        self.probability_label.config(text="Вероятность: --%")
        self.matrix_info.config(text="Матрица: --\nMin: -- Max: --\nMean: --")
        self.status_bar.config(text="Холст очищен")

    def canvas_to_matrix(self):
        """Преобразует холст в матрицу 28x28"""
        # Создаём изображение
        img = Image.new('L', (400, 400), color=255)
        draw = ImageDraw.Draw(img)

        # Копируем линии с холста
        for item in self.canvas.find_all():
            coords = self.canvas.coords(item)
            if coords and len(coords) >= 4:
                draw.line(coords, fill=0, width=8)

        # Масштабируем и нормализуем
        img = img.resize((28, 28), Image.Resampling.LANCZOS)
        matrix = np.array(img, dtype=np.float32)
        matrix = 255 - matrix  # инвертируем
        matrix = matrix / 255.0  # нормализуем

        return matrix

    def recognize_digit(self):
        """Распознавание цифры"""
        if not self.canvas_data:
            self.status_bar.config(text="Ошибка: сначала нарисуйте цифру!")
            return

        self.status_bar.config(text="Распознавание...")
        self.root.after(100, self.show_recognition_result)

    def show_recognition_result(self):
        """Показывает результат распознавания"""
        # Получаем матрицу
        matrix = self.canvas_to_matrix()

        # ПРОСТАЯ ЛОГИКА РАСПОЗНАВАНИЯ (замените на вашу нейросеть)
        # Используем сумму пикселей для определения цифры
        digit,probability = brain.Predict(matrix)
        # Обновляем GUI
        self.result_display.config(text=str(digit), fg='#4CAF50')
        self.probability_label.config(text=f"Вероятность: {probability}%")

        # Обновляем информацию о матрице
        matrix_info_text = f"Матрица: 28×28\nMin: {matrix.min():.3f}\nMax: {matrix.max():.3f}\nMean: {matrix.mean():.3f}"
        self.matrix_info.config(text=matrix_info_text)

        self.status_bar.config(
            text=f"Распознано: цифра {digit} (вероятность {probability}%)"
        )

    def show_matrix_visualization(self):
        """Показывает визуализацию матрицы"""
        if not self.canvas_data:
            self.status_bar.config(text="Сначала нарисуйте цифру!")
            return

        matrix = self.canvas_to_matrix()

        # Создаём график
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))

        # 1. Градации серого
        im1 = axes[0, 0].imshow(matrix, cmap='gray', vmin=0, vmax=1)
        axes[0, 0].set_title("Матрица 28x28 (Grayscale)")
        axes[0, 0].axis('off')
        plt.colorbar(im1, ax=axes[0, 0])

        # 2. Heatmap
        im2 = axes[0, 1].imshow(matrix, cmap='hot')
        axes[0, 1].set_title("Heatmap")
        axes[0, 1].axis('off')
        plt.colorbar(im2, ax=axes[0, 1])

        # 3. С аннотациями (первые 14x14)
        axes[1, 0].imshow(matrix, cmap='gray', vmin=0, vmax=1)
        axes[1, 0].set_title("Значения пикселей")
        axes[1, 0].axis('off')

        for i in range(14):
            for j in range(14):
                val = matrix[i, j]
                if val > 0.1:
                    axes[1, 0].text(j, i, f'{val:.1f}',
                                    ha='center', va='center',
                                    color='white' if val < 0.5 else 'black',
                                    fontsize=6)

        # 4. Гистограмма распределения
        axes[1, 1].hist(matrix.flatten(), bins=20, alpha=0.7, color='blue', edgecolor='black')
        axes[1, 1].set_title("Распределение значений")
        axes[1, 1].set_xlabel("Значение")
        axes[1, 1].set_ylabel("Частота")

        # Добавляем статистику
        stats_text = f"""
        Min: {matrix.min():.3f}
        Max: {matrix.max():.3f}
        Mean: {matrix.mean():.3f}
        Std: {matrix.std():.3f}
        Sum: {matrix.sum():.1f}
        """
        axes[1, 1].text(0.05, 0.95, stats_text, transform=axes[1, 1].transAxes,
                        fontsize=9, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.suptitle("Визуализация матрицы 28x28", fontsize=14)
        plt.tight_layout()
        plt.show()

        self.status_bar.config(text="Визуализация матрицы показана")


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = DigitRecognizerApp(root)
    root.mainloop()