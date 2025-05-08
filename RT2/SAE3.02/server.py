"""Create a server on port 127.0.0.1 which can search words on different \
    files depending on client inputs."""

import socket
import threading
import json
from functions import pdf, excel, txt, html

# Constants for file paths
PDF_PATH = "./pdf"
EXCEL_PATH = "./excel"
TXT_PATH = "./txt"
HTML_PATH = "./html"

# Server configuration
SERVER_HOST = "127.0.0.1"  # Localhost
SERVER_PORT = 65000  # Port number for the server
BUFFER_SIZE = 4096  # Buffer size for data transfer


def handle_client(client_socket):
    """Handle communication with the client."""
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            # Decode the JSON request from the client
            request = json.loads(data.decode('utf-8'))
            search_word = request.get("search_word")
            case_sensitive = request.get("case_sensitive", False)
            file_types = request.get("file_types", [])

            # Perform the search based on file types
            results = {}
            if "pdf" in file_types:
                results["pdf"] = pdf(PDF_PATH, search_word, case_sensitive)
            if "excel" in file_types:
                results["excel"] = excel(EXCEL_PATH, search_word, case_sensitive)
            if "txt" in file_types:
                results["txt"] = txt(TXT_PATH, search_word, case_sensitive)
            if "html" in file_types:
                results["html"] = html(HTML_PATH, search_word, case_sensitive)

            # Send the results back to the client as JSON
            client_socket.send(json.dumps(results).encode('utf-8'))
        except Exception as e:
            print(f"Error while handling client: {e}")
            break

    client_socket.close()


def start_server():
    """Start the server and listen for incoming connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        # Handle the client in a new thread
        client_thread = threading.Thread(target=handle_client,
                                        args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    # Start the server
    start_server()
