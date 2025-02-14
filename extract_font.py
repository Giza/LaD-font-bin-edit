import struct
import sys
import csv
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Symbol:
    char_code: int
    hex_code: str
    char: str
    start_x: float
    start_y: float
    end_x: float
    end_y: float
    additional_data: List[int]  # Добавляем поле для дополнительных данных

def read_uint32(f) -> int:
    return struct.unpack('<I', f.read(4))[0]

def read_uint16(f) -> int:
    return struct.unpack('<H', f.read(2))[0]

def read_float(f) -> float:
    return struct.unpack('<f', f.read(4))[0]

def get_char_from_code(code: int) -> str:
    try:
        char = chr(code)
        if code > 0x7F:
            char_bytes = code.to_bytes(4, 'little')
            char = char_bytes.decode('utf-8', errors='ignore').strip('\x00')
        return char
    except:
        return '?'

def extract_font_data(filename: str) -> Tuple[List[Symbol], int, int, dict]:
    symbols = []
    texture_info = {}
    
    with open(filename, 'rb') as f:
        # Skip first 24 bytes
        f.seek(24)
        
        # Read offsets
        symbols_end_offset = read_uint32(f)
        f.seek(4, 1)  # Skip 4 bytes
        symbols_start_offset = read_uint32(f)
        f.seek(12, 1)  # Skip 12 bytes
        float_end_offset = read_uint32(f)
        f.seek(4, 1)  # Skip 4 bytes
        float_start_offset = read_uint32(f)
        f.seek(4, 1)  # Skip 4 bytes
        unknown3 = read_uint32(f)
        f.seek(4, 1)  # Skip 4 bytes
        unknown4 = read_uint32(f)

        texture_info['symbols_end_offset'] = symbols_end_offset
        texture_info['symbols_start_offset'] = symbols_start_offset
        texture_info['float_end_offset'] = float_end_offset
        texture_info['float_start_offset'] = float_start_offset
        texture_info['unknown3'] = unknown3
        texture_info['unknown4'] = unknown4

        # Read symbols
        f.seek(symbols_start_offset)
        symbol_count = (symbols_end_offset + 28 - symbols_start_offset) // 4
        symbol_codes = []
        
        for _ in range(symbol_count):
            symbol_codes.append(read_uint32(f))

        # Read texture info
        f.seek(4, 1)  # Skip 4 bytes
        unknown_data = read_uint32(f)
        texture_width = read_uint32(f)
        texture_height = read_uint32(f)
        unknown_short1 = read_uint16(f)
        unknown_short2 = read_uint16(f)

        texture_info['unknown_data'] = unknown_data
        texture_info['unknown_short1'] = unknown_short1
        texture_info['unknown_short2'] = unknown_short2

        # Read coordinates
        f.seek(float_start_offset)
        coord_count = (float_end_offset - float_start_offset) // 16

        coordinates = []
        for i in range(coord_count):
            start_x = read_uint32(f)
            start_y = read_uint32(f)
            end_x = read_uint32(f)
            end_y = read_uint32(f)
            coordinates.append((start_x, start_y, end_x, end_y))

        # Читаем дополнительные данные после всех координат
        additional_data_list = []
        for i in range(coord_count):
            data = []
            for _ in range(5):
                data.append(read_uint16(f))
            additional_data_list.append(data)
            
        # Собираем все данные вместе
        for i in range(coord_count):
            if i < len(symbol_codes):
                code = symbol_codes[i]
                start_x, start_y, end_x, end_y = coordinates[i]
                additional_data = additional_data_list[i]
                symbols.append(Symbol(
                    char_code=code,
                    hex_code=f"0x{code:08X}",
                    char=get_char_from_code(code),
                    start_x=start_x,
                    start_y=start_y,
                    end_x=end_x,
                    end_y=end_y,
                    additional_data=additional_data
                ))

    return symbols, texture_width, texture_height, texture_info

def save_to_csv(symbols: List[Symbol], width: int, height: int, texture_info: dict, output_file: str):
    # Сохраняем основную информацию о символах
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Записываем информацию о текстуре
        writer.writerow(['Texture Information'])
        writer.writerow(['Width', 'Height'])
        writer.writerow([width, height])
        writer.writerow([])

        # Записываем дополнительную информацию
        writer.writerow(['Additional Information'])
        for key, value in texture_info.items():
            if isinstance(value, int):
                writer.writerow([key, f"0x{value:08X}", value])
            else:
                writer.writerow([key, value])
        writer.writerow([])

        # Записываем заголовки для символов
        writer.writerow(['Symbol Data'])
        writer.writerow(['Character', 'Hex Code', 'Unicode', 'Start X', 'Start Y', 'End X', 'End Y', 
                        'Value1', 'Value2', 'Value3', 'Value4', 'Value5'])
        
        # Записываем данные о символах
        for symbol in symbols:
            writer.writerow([
                symbol.char,
                symbol.hex_code,
                symbol.char_code,
                f"{symbol.start_x}",
                f"{symbol.start_y}",
                f"{symbol.end_x}",
                f"{symbol.end_y}",
                *symbol.additional_data  # Распаковываем дополнительные данные
            ])

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <font_file>")
        sys.exit(1)

    font_file = sys.argv[1]
    output_file = font_file + ".csv"
    
    symbols, width, height, texture_info = extract_font_data(font_file)
    save_to_csv(symbols, width, height, texture_info, output_file)
    print(f"Data has been saved to {output_file}")

if __name__ == "__main__":
    main() 