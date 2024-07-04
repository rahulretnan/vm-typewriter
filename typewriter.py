import tkinter as tk
import socket
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CHAR_LIMIT = 500  # Character limit for the text input

def enforce_char_limit(event=None):
    current_text = text_field.get("1.0", tk.END)
    if len(current_text) > CHAR_LIMIT:
        text_field.delete("1.0", tk.END)
        text_field.insert("1.0", current_text[:CHAR_LIMIT])
        logging.info("Character limit reached")

def send_text():
    if client_socket:
        text = text_field.get("1.0", tk.END)
        client_socket.sendall(text.encode('utf-8'))
        logging.info("Sent text to VM")
    else:
        logging.error("Not connected to VM")

def send_command(command):
    if client_socket:
        client_socket.sendall(command.encode('utf-8'))
        logging.info(f"Sent command: {command}")
    else:
        logging.error("Not connected to VM")

def start_typing():
    send_command("START")

def stop_typing():
    send_command("STOP")

def clear_text():
    text_field.delete("1.0", tk.END)
    logging.info("Text field cleared")

def pause_typing():
    send_command("PAUSE")

def connect_to_vm():
    global client_socket
    ip_address = ip_entry.get()
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, 12345))
        logging.info(f"Connected to VM at {ip_address}")
        connect_button.config(text="Disconnect", command=disconnect_from_vm)
    except socket.error as e:
        logging.error(f"Failed to connect to VM: {e}")
        client_socket = None

def disconnect_from_vm():
    global client_socket
    if client_socket:
        client_socket.close()
        logging.info("Disconnected from VM")
        connect_button.config(text="Connect", command=connect_to_vm)
        client_socket = None
    else:
        logging.error("Not connected to VM")

# Set up the GUI
root = tk.Tk()
root.title("Typewriter Sender")
root.attributes('-topmost', True)  # Make the window stay on top

# IP address input field and connect button frame
ip_frame = tk.Frame(root)
ip_frame.pack(pady=10)

ip_label = tk.Label(ip_frame, text="Enter VM IP Address:")
ip_label.pack(side=tk.LEFT)

ip_entry = tk.Entry(ip_frame)
ip_entry.insert(0, '192.168.186.129')  # Set default IP address
ip_entry.pack(side=tk.LEFT, padx=5)

connect_button = tk.Button(ip_frame, text="Connect", command=connect_to_vm)
connect_button.pack(side=tk.LEFT)

text_field = tk.Text(root, height=20, width=100)
text_field.pack(pady=10)

text_field.bind("<<Modified>>", enforce_char_limit)  # Bind the function to the <<Modified>> event

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

send_button = tk.Button(button_frame, text="Send Text", command=send_text)
send_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

start_button = tk.Button(button_frame, text="Start Typing", command=start_typing)
start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

stop_button = tk.Button(button_frame, text="Stop Typing", command=stop_typing)
stop_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

clear_button = tk.Button(button_frame, text="Clear Text", command=clear_text)
clear_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

pause_button = tk.Button(button_frame, text="Pause Typing", command=pause_typing)
pause_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

# Initialize the socket as None
client_socket = None

root.mainloop()
if client_socket:
    client_socket.close()
logging.info("Connection closed")