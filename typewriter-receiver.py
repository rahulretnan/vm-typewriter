import socket
import threading
import pyautogui
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

typing = False
paused = False
text_to_type = ""
current_index = 0

def handle_client(client_socket):
    global typing, text_to_type, paused, current_index
    logging.info("Client handler started")
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                logging.info("Client disconnected")
                break
            if data == "START":
                typing = True
                paused = False
                logging.info("Received START command")
                threading.Thread(target=type_text).start()
            elif data == "STOP":
                typing = False
                logging.info("Received STOP command")
            elif data == "PAUSE":
                paused = True
                logging.info("Received PAUSE command")
            elif data == "CLEAR":
                text_to_type = ""
                current_index = 0
                logging.info("Received CLEAR command")
            else:
                text_to_type = data
                current_index = 0
    except Exception as e:
        logging.error(f"Error handling client: {e}")
    finally:
        client_socket.close()
        logging.info("Client handler terminated")
        logging.info("Waiting for connection...")


def type_text():
    global typing, text_to_type, paused, current_index
    while typing and current_index < len(text_to_type):
        if paused:
            pyautogui.sleep(0.1)
            continue
        pyautogui.typewrite(text_to_type[current_index])
        logging.info(f"Typed character: {text_to_type[current_index]}")
        current_index += 1
        pyautogui.sleep(0.05)  # Adjust the typing speed if necessary
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