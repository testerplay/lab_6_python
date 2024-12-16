from tkinter.filedialog import askopenfile, asksaveasfile
import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_image(title, image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(8, 6))
    plt.imshow(image_rgb)
    plt.title(title)
    plt.axis('off')
    plt.show()

def process_image_opencv():
    # Загрузка изображения
    f = askopenfile(mode='rb', defaultextension=".jpg",
                    filetypes=(("Image files", "*.jpg"), ("All files", "*.*")))
    if f:
        file_path = f.name
        img = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)
        f.close()

        # Проверка, что изображение было загружено успешно
        if img is None:
            print("Ошибка загрузки изображения.")
            return

        # Показ оригинального изображения
        show_image("Original", img)

        # Вертикальный сдвиг изображения
        rows, cols, _ = img.shape
        M = np.float32([[1, 0, 0], [0, 1, 50]])  # Сдвиг на 50 пикселей вниз
        shifted_img = cv2.warpAffine(img, M, (cols, rows))
        show_image("Shifted", shifted_img)

        # Применение Гауссового размытия с маской 7x7
        blurred_img = cv2.GaussianBlur(shifted_img, (7, 7), 0)
        show_image("Gaussian Blur", blurred_img)

        # Преобразование в оттенки серого
        gray = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)
        plt.figure(figsize=(8, 6))
        plt.imshow(gray, cmap='gray')
        plt.title("Gray")
        plt.axis('off')
        plt.show()

        # Детектирование углов методом Ши-Томаси
        corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)
        corners = np.int0(corners)

        # Отображение углов
        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(blurred_img, (x, y), 5, (255, 0, 0), -1)
        show_image("Shi-Tomasi Corners", blurred_img)

        # Сохранение результата
        save_f = asksaveasfile(defaultextension=".jpg",
                               filetypes=(("Image files", "*.jpg"), ("All files", "*.*")))
        if save_f:
            cv2.imwrite(save_f.name, blurred_img)

process_image_opencv()
