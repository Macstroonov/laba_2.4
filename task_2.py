def xor_encrypt_decrypt(data, key):
    result = bytearray()
    for byte in data:
        # Циклический сдвиг влево на 2 бита
        shifted = ((byte << 2) | (byte >> 6)) & 0xFF
        # XOR с ключом
        encrypted = shifted ^ key
        result.append(encrypted)
    return bytes(result)

def process_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()
    processed = xor_encrypt_decrypt(data, key)
    with open(output_file, 'wb') as f:
        f.write(processed)

if __name__ == "__main__":
    key = 0x55  # ключ шифрования
    process_file("resource/data.bin", "resource/data_encrypted.bin", key)
    process_file("resource/data_encrypted.bin", "resource/data_decrypted.bin", key)