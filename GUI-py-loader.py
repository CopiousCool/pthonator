import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
from io import StringIO

class InteractiveTerminal:
    def __init__(self):
        self.dir_path = None  # initialize the directory path as None
        self.root = tk.Tk()
        self.root.title("Interactive Terminal")

        # Create frame for scripts
        self.scripts_frame = tk.Frame(self.root, bg="lightgray")
        self.scripts_frame.pack(side="top", fill="x")
        tk.Label(self.scripts_frame, text="Scripts", font="bold").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.scripts_frame, text="Actions", font="bold").grid(row=0, column=1, padx=5, pady=5)

        # Create frame for input/output terminal
        self.terminal_frame = tk.Frame(self.root)
        self.terminal_frame.pack(side="bottom", fill="both", expand=True)
        self.terminal = tk.Text(self.terminal_frame, bg="#222", fg="#ddd", insertbackground="#ddd")
        self.terminal.pack(side="left", fill="both", expand=True)
        self.terminal.bind("<Return>", self.run_command_from_input)
        scrollbar = tk.Scrollbar(self.terminal_frame, command=self.terminal.yview)
        scrollbar.pack(side="right", fill="y")
        self.terminal.config(yscrollcommand=scrollbar.set)

        # Create frame for input area
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(side="bottom", fill="x")
        self.input_label = tk.Label(self.input_frame, text="Input:", font="bold")
        self.input_label.pack(side="left", padx=5, pady=5)
        self.input = tk.Entry(self.input_frame, bg="#ddd", fg="#222")
        self.input.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.input.bind("<Return>", self.run_command_from_input)

        # Create buttons
        self.load_button = tk.Button(self.scripts_frame, text="Load Scripts", command=self.load_scripts)
        self.load_button.grid(row=0, column=2, padx=5, pady=5)

    def load_scripts(self):
        self.dir_path = filedialog.askdirectory()
        if not self.dir_path:
            return
        for widget in self.scripts_frame.winfo_children():
            widget.destroy()
        tk.Label(self.scripts_frame, text="Scripts", font="bold").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.scripts_frame, text="Actions", font="bold").grid(row=0, column=1, padx=5, pady=5)
        for i, file_name in enumerate(os.listdir(self.dir_path)):
            if not file_name.endswith(".py"):
                continue
            script_path = os.path.join(self.dir_path, file_name)
            tk.Label(self.scripts_frame, text=file_name).grid(row=i+1, column=0, padx=5, pady=5)
            button_frame = tk.Frame(self.scripts_frame)
            button_frame.grid(row=i+1, column=1, padx=5, pady=5)
            tk.Button(button_frame, text="Info", command=lambda path=script_path: self.show_info(path)).pack(side="left", padx=5, pady=5)
            tk.Button(button_frame, text="Run", command=lambda path=script_path: self.run_script(path)).pack(side="left", padx=5, pady=5)
            tk.Button(button_frame, text="Edit", command=lambda path=script_path: self.edit_script(path)).pack(side="left", padx=5, pady=5)

    def show_info(self, path):
        with open(path, "r") as file:
            messagebox.showinfo("Script Info", f"Script Name: {os.path.basename(path)}\n\n{file.read()}")

    def run_script(self, path):
        self.terminal.insert("end", f">>> Running script: {os.path.basename(path)}\n", "command")
        proc = subprocess.Popen([sys.executable, path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.dir_path)
        while True:
            output = proc.stdout.readline()
            if output == b"" and proc.poll() is not None:
                break
            if output:
                self.terminal.insert("end", output.decode(), "stdout")
        self.terminal.insert("end", f"\n>>> Script {os.path.basename(path)} completed.\n\n", "command")

    def edit_script(self, path):
        os.system(f'"{sys.executable}" -m idlelib "{path}"')

    def run_command_from_input(self, event):
        command = self.input.get()
        self.input.delete(0, "end")
        self.terminal.insert("end", f"{command}\n", "command")
        if command.startswith("cd "):
            self.change_directory(command[3:])
        else:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=self.dir_path)
            while True:
                output = proc.stdout.readline()
                if output == b"" and proc.poll() is not None:
                    break
                if output:
                    self.terminal.insert("end", output.decode(), "stdout")

    def change_directory(self, path):
        path = os.path.abspath(os.path.join(self.dir_path, path))
        if os.path.isdir(path):
            self.dir_path = path
            self.terminal.insert("end", f">>> Changed directory to: {self.dir_path}\n", "command")
        else:
            self.terminal.insert("end", f">>> Directory not found: {path}\n", "stderr")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = InteractiveTerminal()
    app.run()