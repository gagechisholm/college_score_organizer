import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import scrolledtext

class Reports:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        self.backup = {}

    def split_data(self):
        """Read the file and extract class names and scores (every 1st and 4th lines)."""
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                for index in range(0, len(lines), 4):  # Step 4 lines to extract class name and score
                    # Extract class name (line 1, 5, 9, ...)
                    class_name = lines[index].strip()
                    # Extract score (line 4, 8, 12, ...)
                    if index + 3 < len(lines):  # Check if there are enough lines for the score
                        try:
                            score = int(lines[index + 3].strip())  # Convert score to integer
                            self.data[class_name] = score  # Store class name and score as key-value pair
                        except ValueError:
                            print(f"Error: Could not convert score for {class_name}")
        except FileNotFoundError:
            print(f"Error: The file {self.filename} was not found.")
            return

    def show_data(self):
        """Return the formatted data as a string."""
        return "\n".join([f"Class: {key} | Score: {value}" for key, value in self.data.items()])

    def sort_data(self):
        """Sort the data by score in ascending order."""
        if not self.backup:  # If backup doesn't exist, create one
            self.backup = self.data.copy()
            self.data = dict(sorted(self.data.items(), key=lambda item: item[1]))  # Sort by score (ascending)
            return "Finished sorting."
        else:
            return "Data is already sorted."

    def undo_sort(self):
        """Undo the sort and restore the original data."""
        if not self.backup:
            return "Data sort already undone."
        else:
            self.data = self.backup
            self.backup.clear()
            return "Undo sort complete."

class ReportsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reports App")
        self.reports = None
        
        self.root.geometry("800x600")

        # File Selection
        self.file_label = tk.Label(root, text="Enter Filename (e.g., reports.txt):")
        self.file_label.pack(pady=5)

        self.filename_entry = tk.Entry(root, width=40)
        self.filename_entry.pack(pady=5)

        self.load_button = tk.Button(root, text="Load File", command=self.load_file)
        self.load_button.pack(pady=5)

        # Text area to display data
        self.data_display = scrolledtext.ScrolledText(root, width=90, height=20)
        self.data_display.pack(pady=10)

        # Action Buttons
        self.sort_button = tk.Button(root, text="Sort List", command=self.sort_list, state=tk.DISABLED)
        self.sort_button.pack(pady=5)

        self.undo_button = tk.Button(root, text="Undo Sort", command=self.undo_sort, state=tk.DISABLED)
        self.undo_button.pack(pady=5)

        self.show_button = tk.Button(root, text="Show Data", command=self.show_data, state=tk.DISABLED)
        self.show_button.pack(pady=5)

    def load_file(self):
        """Load the file and process the data."""
        filename = self.filename_entry.get()
        try:
            self.reports = Reports(filename)
            self.reports.split_data()
            # Enable buttons after file is loaded
            messagebox.showinfo("Success", f"File '{filename}' loaded successfully.")
            self.update_display()
            self.sort_button.config(state=tk.NORMAL)
            self.undo_button.config(state=tk.NORMAL)
            self.show_button.config(state=tk.NORMAL)
        except FileNotFoundError:
            messagebox.showerror("Error", f"File '{filename}' not found.")

    def show_data(self):
        """Display the loaded data in the text area."""
        if self.reports:
            data = self.reports.show_data()
            self.update_display(data)

    def sort_list(self):
        """Sort the data by score."""
        if self.reports:
            message = self.reports.sort_data()
            self.update_display(message)
            self.show_data()  # Display sorted data

    def undo_sort(self):
        """Undo the sorting."""
        if self.reports:
            message = self.reports.undo_sort()
            self.update_display(message)
            self.show_data()  # Display data after undo

    def update_display(self, message=""):
        """Update the text area with the given message."""
        self.data_display.delete(1.0, tk.END)  # Clear previous content
        if message:
            self.data_display.insert(tk.END, message)

# Main Tkinter window setup
root = tk.Tk()
app = ReportsApp(root)
root.mainloop()
