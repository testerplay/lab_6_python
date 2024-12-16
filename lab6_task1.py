from tkinter.filedialog import askopenfile, asksaveasfile
from PIL import Image, ImageFilter

def process_image_pil():
    # Открываем файл в бинарном режиме используя диалог tkinter
    f = askopenfile(mode='rb', defaultextension=".jpg",
                    filetypes=(("Image files", "*.jpg"), ("All files", "*.*")))
    if f is None:
        print("Error file open")  # Если файл не выбран
        return

    img = Image.open(f)  # Передаем объект файла
    print("Original image size:", img.size)  # Получаем размер изображения
    print("Original image format:", img.format)  # Выводим формат изображения

    # 1. Поворот на 180 градусов
    img = img.rotate(180, expand=True)
    
    # 2. Применение фильтра SMOOTH_MORE
    img = img.filter(ImageFilter.SMOOTH_MORE)
    
    # 3. Преобразование изображения в 32-битный формат с целыми числами
    img = img.convert("RGBA")
    
    # 4. Вставка изображения по центру
    img_width, img_height = img.size
    bg_width = img_width + 20  # Фон больше изображения на 20 пикселей по ширине
    bg_height = img_height + 20  # Фон больше изображения на 20 пикселей по высоте
    
    # Создаем фоновое изображение
    bg_img = Image.new('RGBA', (bg_width, bg_height), (255, 255, 255, 255))
    
    # Вставляем изображение по центру фона
    position = ((bg_width - img_width) // 2, (bg_height - img_height) // 2)
    bg_img.paste(img, position, img)
    
    # Отображаем результирующее изображение
    bg_img.show()

    # Сохраняем результирующее изображение
    save_path = asksaveasfile(defaultextension=".png",
                              filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    if save_path:
        bg_img.save(save_path)
        print("Image saved to:", save_path.name)
    
    f.close()  # Закрываем файл

# Вызов функции
process_image_pil()
