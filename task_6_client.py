import socket
import os
import time

def upload_file(filename):
    filepath = os.path.join("resource", filename)
    if not os.path.exists(filepath):
        print(f"File {filename} not found in resource folder")
        return

    with open(filepath, "rb") as f:
        content = f.read()

    print(f"Sending file: {filename}, size: {len(content)} bytes")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9999))

    sock.send(f"UPLOAD:{filename}".encode())
    time.sleep(0.2)
    sock.send(content)
    sock.shutdown(socket.SHUT_WR)

    response = sock.recv(1024).decode()
    print(response)
    sock.close()

def download_file(filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9999))

    sock.send(f"DOWNLOAD:{filename}".encode())

    os.makedirs("resource", exist_ok=True)
    out_path = os.path.join("resource", f"downloaded_{filename}.bin")

    with open(out_path, "wb") as f:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            f.write(chunk)

    print(f"File saved as {out_path}")
    sock.close()

def main():
    print("1. Upload file (.json or .xml)")
    print("2. Download file (.bin)")
    choice = input("Select action (1/2): ")

    if choice == "1":
        name = input("File name (e.g. test_1.json): ")
        upload_file(name)
    elif choice == "2":
        name = input("File name without extension (e.g. test_1): ")
        download_file(name)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()