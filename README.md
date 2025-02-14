# Инструменты для работы с файлами шрифтов SDF / SDF Font File Tools

[English version below](#sdf-font-file-tools)

Набор инструментов для работы с бинарными файлами шрифтов в формате SDF (Signed Distance Field).

## Описание

Этот проект содержит набор Python-скриптов для:
- Извлечения данных из бинарных файлов шрифтов SDF
- Обновления координат символов
- Упаковки координат обратно в бинарный файл
- Анализа структуры файла с помощью шаблона 010 Editor

## Структура проекта

- `extract_font.py` - Извлекает данные о символах, координатах и текстуре из бинарного файла шрифта в CSV
- `update_coordinates.py` - Обновляет координаты символов на основе файла сопоставлений
- `pack_coordinates.py` - Упаковывает обновленные координаты обратно в бинарный файл
- `template.bt` - Шаблон для анализа структуры бинарного файла в 010 Editor
- `chars.csv` - Файл сопоставлений для замены символов

## Использование

### Извлечение данных из файла шрифта

```bash
python extract_font.py <font_file>
```

Создает CSV файл с данными о:
- Размерах текстуры
- Смещениях в файле
- Символах и их координатах
- Дополнительных параметрах

### Обновление координат

```bash
python update_coordinates.py
```

Обновляет координаты символов в CSV файле на основе сопоставлений из `chars.csv`.

### Упаковка координат

```bash
python pack_coordinates.py <original_font_file> <csv_file> <output_font_file>
```

Записывает обновленные координаты обратно в бинарный файл шрифта.

## Формат файла шрифта

Бинарный файл шрифта имеет следующую структуру:

1. Заголовок (24 байта)
2. Таблица смещений
   - symbols_end_offset
   - symbols_start_offset
   - float_end_offset
   - float_start_offset
   - unknown3
   - unknown4
3. Данные о символах
4. Информация о текстуре
   - Ширина
   - Высота
   - Дополнительные параметры
5. Координаты символов
6. Дополнительные данные символов

## Требования

- Python 3.6+
- 010 Editor (для использования шаблона анализа)

---

# SDF Font File Tools

A set of tools for working with SDF (Signed Distance Field) binary font files.

## Description

This project contains a set of Python scripts for:
- Extracting data from SDF binary font files
- Updating symbol coordinates
- Packing coordinates back into binary file
- Analyzing file structure using 010 Editor template

## Project Structure

- `extract_font.py` - Extracts symbol data, coordinates, and texture information from binary font file to CSV
- `update_coordinates.py` - Updates symbol coordinates based on mapping file
- `pack_coordinates.py` - Packs updated coordinates back into binary file
- `template.bt` - Template for analyzing binary file structure in 010 Editor
- `chars.csv` - Mapping file for symbol replacement

## Usage

### Extracting Data from Font File

```bash
python extract_font.py <font_file>
```

Creates a CSV file containing:
- Texture dimensions
- File offsets
- Symbols and their coordinates
- Additional parameters

### Updating Coordinates

```bash
python update_coordinates.py
```

Updates symbol coordinates in the CSV file based on mappings from `chars.csv`.

### Packing Coordinates

```bash
python pack_coordinates.py <original_font_file> <csv_file> <output_font_file>
```

Writes updated coordinates back into the binary font file.

## Font File Format

The binary font file has the following structure:

1. Header (24 bytes)
2. Offset table
   - symbols_end_offset
   - symbols_start_offset
   - float_end_offset
   - float_start_offset
   - unknown3
   - unknown4
3. Symbol data
4. Texture information
   - Width
   - Height
   - Additional parameters
5. Symbol coordinates
6. Symbol additional data

## Requirements

- Python 3.6+
- 010 Editor (for using analysis template)

## License

MIT 
