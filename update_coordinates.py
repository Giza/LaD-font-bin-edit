import csv

def update_coordinates():
    # Читаем маппинг замен
    replacements = {}
    with open('chars.csv', 'r', encoding='utf-8-sig') as f:  # используем utf-8-sig для автоматической обработки BOM
        for line in f:
            line = line.strip()
            if line:
                source, target = line.split(',')
                source = source.strip()  # очищаем от возможных пробелов
                target = target.strip()
                source = '0x0000' + source  # Преобразуем в формат как в файле
                target = '0x0000' + target.replace('0x', '')
                replacements[source] = target
    
    print(f"Загружено {len(replacements)} пар для замены")
    print("Все пары замен:")
    for source, target in replacements.items():
        print(f"{source} -> {target}")

    # Читаем файл данных
    with open('system_main_en_all_sdf.bin.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"Прочитано {len(lines)} строк из файла")

    # Создаем словарь для хранения данных каждой строки по hex коду
    hex_to_data = {}
    hex_to_line_number = {}
    
    # Сначала находим все строки с данными
    for i, line in enumerate(lines):
        parts = line.strip().split(',')
        if len(parts) > 2 and parts[1].startswith('0x'):
            hex_code = parts[1].strip()  # очищаем от возможных пробелов
            hex_to_data[hex_code] = parts[3:12]  # Сохраняем только координаты и значения
            hex_to_line_number[hex_code] = i

    print(f"Найдено {len(hex_to_data)} строк с hex-кодами")
    print("Примеры найденных hex-кодов:", list(hex_to_data.keys())[:3])

    # Для отладки: проверяем наличие первой пары замен
    first_source = list(replacements.keys())[0]
    first_target = replacements[first_source]
    print(f"\nПроверка первой пары замен:")
    print(f"Исходный код: {first_source}")
    print(f"Целевой код: {first_target}")
    print(f"Исходный код найден: {first_source in hex_to_data}")
    print(f"Целевой код найден: {first_target in hex_to_line_number}")
    if first_source in hex_to_data:
        print(f"Данные исходного кода: {hex_to_data[first_source]}")
    if first_target in hex_to_line_number:
        line_num = hex_to_line_number[first_target]
        print(f"Строка целевого кода: {lines[line_num].strip()}")

    # Выполняем замены
    replacements_made = 0
    not_found = []
    for source_hex, target_hex in replacements.items():
        if source_hex in hex_to_data:
            if target_hex in hex_to_line_number:
                source_data = hex_to_data[source_hex]
                line_number = hex_to_line_number[target_hex]
                parts = lines[line_number].strip().split(',')
                old_values = parts[3:121]
                parts[3:12] = source_data
                lines[line_number] = ','.join(parts) + '\n'
                print(f"Заменено {target_hex}: {old_values} -> {source_data}")
                replacements_made += 1
            else:
                not_found.append(f"Не найден целевой код: {target_hex}")
        else:
            not_found.append(f"Не найден исходный код: {source_hex}")

    print(f"\nВсего выполнено замен: {replacements_made}")
    if not_found:
        print("\nНе выполненные замены:")
        for msg in not_found:
            print(msg)

    # Записываем обновленный файл
    with open('system_main_en_all_sdf.bin.csv', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("\nФайл успешно обновлен")

if __name__ == '__main__':
    update_coordinates() 