import os

def process_file_inplace(filename):
    with open(filename, 'rb+') as f:
        while True:
            chunk = f.read(4)  # читаем по 4 байта (int32)
            if not chunk:
                break
            number = int.from_bytes(chunk, 'little')
            if number % 7 == 0:
                new_value = number * 100 // (73 ** 2 + 29)
                f.seek(-4, os.SEEK_CUR)
                f.write(new_value.to_bytes(4, 'little'))

if __name__ == "__main__":
    # Создаём тестовый файл
    with open("resource/numbers.bin", "wb") as f:
        for n in [7, 14, 21, 5, 49]:
            f.write(n.to_bytes(4, 'little'))

    process_file_inplace("resource/numbers.bin")