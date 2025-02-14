import struct
import sys
import csv
from typing import List, Tuple

#def read_coordinates_from_csv(csv_file: str) -> List[Tuple[float, float, float, float]]:
def read_coordinates_from_csv(csv_file: str) -> List[Tuple[int, int, int, int, List[int]]]:
    coordinates = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Пропускаем секции до данных о символах
        for row in reader:
            if row and row[0] == 'Symbol Data':
                break
        
        # Пропускаем заголовки
        next(reader)
        
        # Читаем координаты и дополнительные данные
        for row in reader:
            if row:  # Проверяем, что строка не пустая
                try:
                    start_x = int(row[3])
                    start_y = int(row[4])
                    end_x = int(row[5])
                    end_y = int(row[6])
                    # Читаем 5 дополнительных значений
                    additional_data = [int(x) for x in row[7:12]]
                    coordinates.append((start_x, start_y, end_x, end_y, additional_data))
                except (IndexError, ValueError):
                    continue
    
    return coordinates

def read_header_offsets(data: bytearray) -> Tuple[int, int]:
    # Пропускаем первые 24 байта
    pos = 24
    
    # Пропускаем symbols_end_offset и 4 байта
    pos += 8
    
    # Пропускаем symbols_start_offset и 12 байт
    pos += 16
    
    # Читаем float_end_offset
    float_end_offset = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 8  # Пропускаем 4 байта после
    
    # Читаем float_start_offset
    float_start_offset = struct.unpack('<I', data[pos:pos+4])[0]
    
    return float_start_offset, float_end_offset

def pack_coordinates(input_file: str, csv_file: str, output_file: str):
    # Читаем оригинальный файл
    with open(input_file, 'rb') as f:
        data = bytearray(f.read())
    
    # Читаем координаты из CSV
    coordinates = read_coordinates_from_csv(csv_file)
    
    # Получаем смещения из заголовка
    float_start_offset, float_end_offset = read_header_offsets(data)
    
    # Проверяем, что у нас достаточно координат
    coord_count = (float_end_offset - float_start_offset) // 16
    if len(coordinates) > coord_count:
        coordinates = coordinates[:coord_count]
    
    # Записываем координаты
    for i, (start_x, start_y, end_x, end_y, _) in enumerate(coordinates):
        pos = float_start_offset + i * 16
        if pos + 16 <= len(data):
            data[pos:pos+4] = struct.pack('<I', start_x)
            data[pos+4:pos+8] = struct.pack('<I', start_y)
            data[pos+8:pos+12] = struct.pack('<I', end_x)
            data[pos+12:pos+16] = struct.pack('<I', end_y)
    
    # Записываем дополнительные данные после всех координат
    additional_data_offset = float_start_offset + coord_count * 16
    for i, (_, _, _, _, additional_data) in enumerate(coordinates):
        pos = additional_data_offset + i * 10  # 10 = 5 значений * 2 байта
        if pos + 10 <= len(data):
            for j, value in enumerate(additional_data):
                data[pos+j*2:pos+j*2+2] = struct.pack('<H', value)
    
    # Сохраняем измененный файл
    with open(output_file, 'wb') as f:
        f.write(data)

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <original_font_file> <csv_file> <output_font_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    csv_file = sys.argv[2]
    output_file = sys.argv[3]
    
    try:
        pack_coordinates(input_file, csv_file, output_file)
        print(f"Coordinates have been packed and saved to {output_file}")
        print("Original file structure has been preserved")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 