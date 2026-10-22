# Підключаємо шляхи до файлів і папок.
from pathlib import Path
# Підключаємо копіювання файлів.
import shutil
# Підключаємо перевірку цілісності зображень.
from PIL import Image
# У цій папці знаходиться розпакована навчальна частина Kaggle.
data_dir = Path('/content/dogs_source/train')
# У цю папку записуємо підготовлений набір даних.
base_dir = Path('/content/cats_dogs')
# В одному класі оригінального набору є 12500 зображень.
nb_images = 12500
# Для перевірки виділяємо 15 відсотків зображень кожного класу.
val_data_portion = 0.15
# Для остаточного тестування виділяємо ще 15 відсотків.
test_data_portion = 0.15
# Обчислюємо індекс початку перевірочної вибірки.
start_val = int(nb_images * (1 - val_data_portion - test_data_portion))
# Обчислюємо індекс початку тестової вибірки.
start_test = int(nb_images * (1 - test_data_portion))
# Задаємо три діапазони індексів без перетинів.
splits = [('train', 0, start_val), ('val', start_val, start_test), ('test', start_test, nb_images)]
# Збираємо рядки для текстового опису структури каталогів.
structure = []
# По черзі створюємо навчальний, перевірочний і тестовий набори.
for split, start, end in splits:
    # Обробляємо окремо котів і собак.
    for prefix, category in [('cat', 'cats'), ('dog', 'dogs')]:
        # Визначаємо папку поточного класу та вибірки.
        dest_dir = base_dir / split / category
        # Створюємо каталог, якщо його ще немає.
        dest_dir.mkdir(parents=True, exist_ok=True)
        # Починаємо підрахунок придатних зображень.
        count = 0
        # Беремо тільки індекси поточної вибірки.
        for index in range(start, end):
            # Будуємо назву вихідного файла, наприклад cat.0.jpg.
            source = data_dir / f'{prefix}.{index}.jpg'
            # Відкриваємо зображення для перевірки.
            with Image.open(source) as picture:
                # Перевіряємо, чи файл не пошкоджений.
                picture.verify()
            # Копіюємо файл до відповідного класу поточної вибірки.
            shutil.copy2(source, dest_dir / source.name)
            # Збільшуємо кількість скопійованих зображень.
            count += 1
        # Записуємо назву папки та фактичну кількість файлів.
        structure.append(f'{split}/{category}: {count} JPG')
# Показуємо готову структуру каталогів.
print('\n'.join(structure))
# Зберігаємо структуру також в окремий текстовий файл.
Path('/content/lab7_directory_structure.txt').write_text('\n'.join(structure), encoding='utf-8')
