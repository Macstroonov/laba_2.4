import socket
import threading
import os
import json
import xml.etree.ElementTree as ET

KEY = 0x55

def encrypt(data):
    result = bytearray()
    for byte in data:
        shifted = ((byte << 2) | (byte >> 6)) & 0xFF
        result.append(shifted ^ KEY)
    return bytes(result)

def handle_client(conn):
    try:
        raw = conn.recv(1024).decode()
        if not raw:
            return

        parts = raw.split(":", 1)
        if len(parts) != 2:
            conn.send(b"ERROR: Invalid command")
            return

        command, filename = parts
        filename = filename.strip()

        if command == "UPLOAD":
            content = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                content += chunk

            print(f"Received file: {filename}, size: {len(content)} bytes")

            if filename.endswith(".json"):
                try:
                    json.loads(content.decode("utf-8"))
                    print("[OK] JSON valid")
                except Exception as e:
                    error_msg = f"ERROR: Invalid JSON - {e}".encode()
                    conn.send(error_msg)
                    return
            elif filename.endswith(".xml"):
                try:
                    ET.fromstring(content.decode("utf-8"))
                    print("[OK] XML valid")
                except Exception as e:
                    error_msg = f"ERROR: Invalid XML - {e}".encode()
                    conn.send(error_msg)
                    return
            else:
                conn.send(b"ERROR: Only .json or .xml allowed")
                return

            encrypted = encrypt(content)
            out_name = filename.replace(".json", ".bin").replace(".xml", ".bin")
            os.makedirs("resource", exist_ok=True)
            with open(f"resource/{out_name}", "wb") as f:
                f.write(encrypted)

            conn.send(f"OK: {out_name} saved".encode())

        elif command == "DOWNLOAD":
            bin_name = f"{filename}.bin"
            filepath = f"resource/{bin_name}"

            if not os.path.exists(filepath):
                conn.send(b"ERROR: File not found")
                return

            with open(filepath, "rb") as f:
                conn.sendfile(f)

        else:
            conn.send(b"ERROR: Unknown command")

    except Exception as e:
        print(f"Server error: {e}")
        try:
            conn.send(f"ERROR: Server error - {e}".encode())
        except:
            pass
    finally:
        conn.close()

def main():
    os.makedirs("resource", exist_ok=True)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 9999))
    server.listen(5)
    print("Server started on port 9999")

    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    main()