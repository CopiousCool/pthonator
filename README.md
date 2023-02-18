# pythonator
A Python GUI app with interactive Terminal that executes scripts and commands. Also loads scrips from local or specified directory as buttons with info / code on each and an ability to launch an editor to edit the code

This code defines a class InteractiveTerminal that creates a simple GUI for running Python scripts and command-line commands. The user can load Python scripts from a directory, view their contents, and run them. Additionally, they can enter command-line commands to be run and view their output.

The class creates a tkinter window that contains several frames, including one for the loaded scripts and another for the input/output terminal. When the load_scripts method is called, a dialog box is opened to allow the user to select a directory of Python scripts. The method then creates labels for each script found in the directory, along with buttons for running the script, viewing its contents, and editing it.

The show_info method opens a message box that displays the contents of the selected script file. The run_script method executes the script using the subprocess module, capturing its output and displaying it in the terminal frame. The edit_script method opens the selected script file in the IDLE editor using the os.system function.

When the user types a command in the input frame and presses enter, the run_command_from_input method is called. If the command is a cd command, the change_directory method is called to update the current directory. Otherwise, the method executes the command using subprocess, capturing its output and displaying it in the terminal frame.

Overall, this code provides a basic, interactive interface for running Python scripts and command-line commands.
