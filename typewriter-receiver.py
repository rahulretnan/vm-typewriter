import socket
import threading
import pyautogui
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

typing = False
text_to_type = ""
current_index = 0
typing_speed = 0  # Default typing speed

def handle_client(client_socket):
    global typing, text_to_type, current_index, typing_speed
    logging.info("Client handler started")
    try:
        while True:
            data = client_socket.recv(10240).decode('utf-8')  # Increased buffer size to 10240 bytes
            if not data:
                logging.info("Client disconnected")
                break
            if data == "START":
                typing = True
                logging.info("Received START command")
                threading.Thread(target=type_text, args=(typing_speed,)).start()
            elif data == "STOP":
                typing = False
                logging.info("Received STOP command")
            elif data == "CLEAR":
                text_to_type = ""
                current_index = 0
                logging.info("Received CLEAR command")
            elif data.startswith("SPEED"):
                try:
                    speed = float(data.split()[1])
                    typing_speed = speed
                    logging.info(f"Received SPEED command: {speed}")
                except (IndexError, ValueError):
                    logging.error("Invalid SPEED command format")
            else:
                text_to_type = data
                current_index = 0
    except Exception as e:
        logging.error(f"Error handling client: {e}")
    finally:
        client_socket.close()
        logging.info("Client handler terminated")
        logging.info("Waiting for connection...")

def type_text(speed):
    global typing, text_to_type, current_index
    while typing and current_index < len(text_to_type):
        pyautogui.typewrite(text_to_type[current_index])
        logging.info(f"Typed character: {text_to_type[current_index]}")
        current_index += 1
        pyautogui.sleep(speed)  # Use the customizable typing speed
        if not typing:
            break  # Exit the loop if typing is stopped
    if current_index >= len(text_to_type):
        typing = False  # Ensure typing stops after the text ends
        logging.info("Finished typing text")

# Set up the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(1)

logging.info("Server started, waiting for connections...")

while True:
    client_socket, addr = server_socket.accept()
    logging.info(f"Connected to {addr}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()