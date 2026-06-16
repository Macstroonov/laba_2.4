import os

def serialize_xml(obj, root="root", level=0):
    """Превращает словарь/список в XML строку"""
    spaces = "  " * level
    if isinstance(obj, dict):
        lines = [f'{spaces}<{root}>']
        for k, v in obj.items():
            lines.append(serialize_xml(v, k, level + 1))
        lines.append(f'{spaces}</{root}>')
        return "\n".join(lines)
    elif isinstance(obj, list):
        lines = [f'{spaces}<{root}>']
        for v in obj:
            lines.append(serialize_xml(v, "item", level + 1))
        lines.append(f'{spaces}</{root}>')
        return "\n".join(lines)
    else:
        return f'{spaces}<{root}>{obj}</{root}>'

def deserialize_xml(xml_str):
    # Простейший парсер XML — просто убирает теги
    import re
    return re.sub(r'<[^>]+>', '', xml_str).strip()

def validate_xml(xml_str):
    # Проверяем, что все теги закрыты
    if xml_str.count('<') == xml_str.count('</'):
        return True, "OK"
    return False, "Не закрыты теги"

def main():
    xml_file = "resource/test_1.xml"

    # 1. Читаем файл
    if not os.path.exists(xml_file):
        print(" Файл не найден")
        return

    with open(xml_file, "r", encoding="utf-8") as f:
        xml_str = f.read()

    print(" Содержимое файла:")
    print(xml_str)
    print("\n" + "="*50 + "\n")

    # 2. Проверяем валидность
    valid, msg = validate_xml(xml_str)
    print(f" Валидация: {valid} - {msg}")

    if valid:
        # 3. Десериализация
        obj = deserialize_xml(xml_str)
        print("\n Десериализованный объект:")
        print(obj)

        # 4. Вывод с отступами (Pretty Print)
        print("\n С отступами:")
        print(serialize_xml(obj, root="root"))

if __name__ == "__main__":
    main()