"""Creates an IHM to communicate with a server on 127.0.0.1:65000,\
    to search an inputed word for different file types (PDF, HTML, TXT or Excel)."""

import socket
import json
import tkinter as tk
from tkinter import messagebox, Checkbutton, IntVar
from tkinter.scrolledtext import ScrolledText

# Server configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65000
BUFFER_SIZE = 4096


class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Search Client")

        # Apply dark theme
        self.root.configure(bg="#2e2e2e")
        self.dark_bg = "#2e2e2e"
        self.dark_fg = "#ffffff"
        self.accent_color = "#00ff00"

        # Configure grid layout for resizing
        root.grid_rowconfigure(8, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # UI components
        tk.Label(root, text="Word to search:", bg=self.dark_bg, fg=self.dark_fg).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.search_word_entry = tk.Entry(root, width=30, bg="#3b3b3b", fg=self.dark_fg, insertbackground=self.dark_fg)
        self.search_word_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        self.case_sensitive_var = IntVar()
        Checkbutton(root, text="Case Sensitive", variable=self.case_sensitive_var, bg=self.dark_bg, fg=self.dark_fg, selectcolor=self.dark_bg).grid(row=1, column=0, columnspan=2, sticky="w")

        tk.Label(root, text="File Types:", bg=self.dark_bg, fg=self.dark_fg).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.file_types_vars = {
            "PDF": IntVar(),
            "Excel": IntVar(),
            "TXT": IntVar(),
            "HTML": IntVar()
        }
        for idx, (file_type, var) in enumerate(self.file_types_vars.items()):
            Checkbutton(root, text=file_type, variable=var, bg=self.dark_bg, fg=self.dark_fg, selectcolor=self.dark_bg).grid(row=3 + idx, column=0, columnspan=2, sticky="w")

        search_button = tk.Button(root, text="Search", command=self.search, bg=self.accent_color, fg=self.dark_fg, relief="flat")
        search_button.grid(row=7, column=0, columnspan=2, pady=10)

        # ScrolledText for dynamic resizing and better visualization of results
        self.results_text = ScrolledText(root, wrap=tk.WORD, bg="#3b3b3b", fg=self.dark_fg, insertbackground=self.dark_fg, state="disabled")
        self.results_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def format_results(self, results):
        """Format the search results for display in a structured and readable manner."""
        output = []
        for ftype, files in results.items():
            if files:  # Only include sections with results
                output.append(f"=== {ftype.upper()} ===")
                for file, matches in files.items():
                    if ftype == "pdf":
                        pages = ", ".join(map(str, matches))
                        output.append(f"{file} : Page {pages}")
                    elif ftype == "excel":
                        excel_matches = []
                        for match in matches:
                            excel_matches.append(f"{match['sheet']}, {match['cell']}")
                        output.append(f"{file} : " + " ".join(excel_matches))
                    elif ftype in ["txt", "html"]:
                        lines = ", ".join(map(str, matches))
                        output.append(f"{file} : Line {lines}")
                output.append("")  # Add a blank line for better readability
        return "\n".join(output)

    def search(self):
        """
        Send search parameters to the server and display the results.
        """
        search_word = self.search_word_entry.get()
        case_sensitive = bool(self.case_sensitive_var.get())
        file_types = [ftype.lower() for ftype, var in self.file_types_vars.items() if var.get()]

        if not search_word or not file_types:
            messagebox.showwarning("Invalid Input", "Please enter a word and \
                select at least one file type.")
            return

        # Prepare the request data
        request = {
            "search_word": search_word,
            "case_sensitive": case_sensitive,
            "file_types": file_types
        }

        try:
            # Connect to the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_HOST, SERVER_PORT))

            # Send the request to the server
            client_socket.send(json.dumps(request).encode('utf-8'))

            # Receive the response from the server
            response = client_socket.recv(BUFFER_SIZE)
            results = json.loads(response.decode('utf-8'))

            # Format and display the results
            formatted_results = self.format_results(results)
            self.results_text.configure(state="normal")
            self.results_text.delete(1.0, tk.END)
            if formatted_results:
                self.results_text.insert(tk.END, formatted_results)
            else:
                self.results_text.insert(tk.END, "No results found.")
            self.results_text.configure(state="disabled")

            client_socket.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to the server: {e}")


if __name__ == "__main__":
    # Start the client application
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
