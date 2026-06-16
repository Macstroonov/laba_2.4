import struct

def parse_binary_file(filename):
    with open(filename, 'rb') as f:
        # Читаем заголовок
        signature = f.read(4)
        if signature != b'DATA':
            raise ValueError("Неверная сигнатура файла")

        version = struct.unpack('<H', f.read(2))[0]
        record_count = struct.unpack('<I', f.read(4))[0]

        print(f"Версия: {version}, Записей: {record_count}")

        total_temp = 0
        active_flags = 0

        for _ in range(record_count):
            timestamp = struct.unpack('<Q', f.read(8))[0]
            record_id = struct.unpack('<I', f.read(4))[0]
            temp_raw = struct.unpack('<h', f.read(2))[0]
            temp_celsius = temp_raw / 100
            flags = f.read(1)[0]

            total_temp += temp_celsius
            if flags & 0x01:  # проверяем младший бит
                active_flags += 1

        avg_temp = total_temp / record_count if record_count > 0 else 0
        print(f"Средняя температура: {avg_temp:.2f}°C")
        print(f"Активных флагов: {active_flags}")

# Пример использования
if __name__ == "__main__":
    parse_binary_file("resource/data.bin")