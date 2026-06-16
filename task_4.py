import os

def serialize_json(obj, indent=0):
    """Превращает словарь/список в JSON строку"""
    if isinstance(obj, dict):
        items = []
        for k, v in obj.items():
            items.append(f'{indent}  "{k}": {serialize_json(v, indent)}')
        return '{\n' + ',\n'.join(items) + f'\n{indent}}}'
    elif isinstance(obj, list):
        items = [serialize_json(v, indent) for v in obj]
        return '[\n' + ',\n'.join(items) + '\n]'
    elif isinstance(obj, str):
        return f'"{obj}"'
    elif isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif obj is None:
        return 'null'
    else:
        return str(obj)

def deserialize_json(json_str):
    """Превращает JSON строку в Python объект (через eval)"""
    return eval(json_str)

def validate_json(json_str):
    try:
        eval(json_str)
        return True, "OK"
    except Exception as e:
        return False, str(e)

def main():
    json_file = "resource/test_1.json"

    # 1. Читаем файл
    if not os.path.exists(json_file):
        print("Файл не найден")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        json_str = f.read()

    print("Содержимое файла:")
    print(json_str)
    print("\n" + "="*50 + "\n")

    # 2. Проверяем валидность
    valid, msg = validate_json(json_str)
    print(f"Валидация: {valid} - {msg}")

    if valid:
        # 3. Десериализация
        obj = deserialize_json(json_str)
        print("\n Десериализованный объект:")
        print(obj)

        # 4. Вывод с отступами (Pretty Print)
        print("\n С отступами:")
        print(serialize_json(obj, indent=2))

if __name__ == "__main__":
    main()