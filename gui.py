import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import os

# Get the absolute path to students.txt in the same directory as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "students.txt")

# ---- COLOR SCHEME -----
BG_COLOR = "#f0f2f5"
PRIMARY_COLOR = "#4a90e2"
PRIMARY_DARK = "#357abd"
ACCENT_COLOR = "#50c878"
TEXT_COLOR = "#2c3e50"
BUTTON_HOVER = "#357abd"

def register_student():
    # Ask for student ID
    student_id = simpledialog.askstring("Register Student", "Enter student ID:")
    if not student_id:
        return

    # Ask for student name
    name = simpledialog.askstring("Register Student", "Enter student name:")
    if not name:
        return

    # Save to students.txt
    try:
        with open(DB_FILE, "a") as f:
            f.write(f"{student_id} = {name}\n")
        messagebox.showinfo("Success", f"✓ Student registered:\n{name} (ID: {student_id})")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save student:\n{str(e)}")

def start_scanner():
    if not os.path.exists("scan.py"):
        messagebox.showerror("Error", "scan.py not found!")
        return

    # Run scanner script
    subprocess.Popen(["python", "scan.py"])
    messagebox.showinfo("Scanner Started", "Camera scanner is now running!\nPress Q to exit.")

def on_button_enter(button, color):
    button.config(bg=color)

def on_button_leave(button, color):
    button.config(bg=color)

# ---- GUI WINDOW -----
root = tk.Tk()
root.title("Attendance Scanner")
root.geometry("450x350")
root.config(bg=BG_COLOR)
root.resizable(False, False)

# Center window on screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

# ---- HEADER -----
header_frame = tk.Frame(root, bg=PRIMARY_COLOR, height=80)
header_frame.pack(fill=tk.X)

title_label = tk.Label(header_frame, text="📋 Attendance System", 
                       font=("Segoe UI", 24, "bold"), 
                       bg=PRIMARY_COLOR, fg="white")
title_label.pack(pady=20)

subtitle_label = tk.Label(header_frame, text="Manage student attendance with ease",
                          font=("Segoe UI", 10),
                          bg=PRIMARY_COLOR, fg="#e8f0ff")
subtitle_label.pack(pady=(0, 10))

# ---- BUTTON FRAME -----
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=40, padx=30, fill=tk.BOTH, expand=True)

# Register Student Button
btn_register = tk.Button(button_frame, text="👤 Register Student", 
                        font=("Segoe UI", 13, "bold"),
                        bg=PRIMARY_COLOR, fg="white",
                        command=register_student,
                        relief=tk.FLAT,
                        padx=30, pady=15,
                        cursor="hand2",
                        activebackground=PRIMARY_DARK,
                        activeforeground="white")
btn_register.pack(pady=12, fill=tk.X)

# Start Scanner Button
btn_start = tk.Button(button_frame, text="📷 Start Scanner", 
                     font=("Segoe UI", 13, "bold"),
                     bg=ACCENT_COLOR, fg="white",
                     command=start_scanner,
                     relief=tk.FLAT,
                     padx=30, pady=15,
                     cursor="hand2",
                     activebackground="#45b870",
                     activeforeground="white")
btn_start.pack(pady=12, fill=tk.X)

# ---- FOOTER -----
footer_frame = tk.Frame(root, bg="#e8e8e8", height=50)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

footer_label = tk.Label(footer_frame, text="© 2025 StudentScan | Ready to scan",
                       font=("Segoe UI", 9),
                       bg="#e8e8e8", fg="#666666")
footer_label.pack(pady=12)

root.mainloop()
