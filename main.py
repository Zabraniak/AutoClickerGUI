import tkinter as tk
from tkinter import ttk
import pyautogui
import time
import threading
import tkinter.messagebox as messagebox


class AutoClickerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Auto Clicker")
        self.geometry("300x300")

        self.click_count = 0
        self.elapsed_time = 0.0
        self.is_running = False

        self.create_widgets()

    def create_widgets(self):
        # Delay Label and Entry
        delay_label = ttk.Label(self, text="Delay (seconds):")
        delay_label.pack()
        self.delay_entry = ttk.Entry(self)
        self.delay_entry.pack()

        # Number of Clicks Label and Entry
        num_clicks_label = ttk.Label(self, text="Number of Clicks:")
        num_clicks_label.pack()
        self.num_clicks_entry = ttk.Entry(self)
        self.num_clicks_entry.pack()

        # Start Button
        self.start_button = ttk.Button(self, text="Start", command=self.start_auto_clicker)
        self.start_button.pack()

        # Summary Label
        self.summary_label = ttk.Label(self, text="")
        self.summary_label.pack()

    def start_auto_clicker(self):
        if self.is_running:
            return

        # Reset click count and elapsed time
        self.click_count = 0
        self.elapsed_time = 0.0

        # Parse user input
        delay_str = self.delay_entry.get()
        num_clicks_str = self.num_clicks_entry.get()

        try:
            delay = float(delay_str)
            num_clicks = int(num_clicks_str)

            # Validate input values
            if not (1 <= delay <= 40):
                raise ValueError("Invalid delay value. Enter a value between 1 and 40.")
            if not (1 <= num_clicks <= 50000):
                raise ValueError("Invalid number of clicks. Enter a value between 1 and 50,000.")

            self.summary_label.config(text="Auto Clicker will start in {} seconds.\nPosition your cursor accordingly."
                                      .format(delay))

            # Disable user input while delay is in progress
            self.delay_entry.configure(state=tk.DISABLED)
            self.num_clicks_entry.configure(state=tk.DISABLED)
            self.start_button.configure(state=tk.DISABLED)

            # Start the delay timer in a separate thread
            delay_thread = threading.Thread(target=self.delay_timer, args=(delay, num_clicks))
            delay_thread.start()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def delay_timer(self, delay, num_clicks):
        time.sleep(delay)

        self.summary_label.config(text="Auto Clicker is running...")

        # Enable user input after delay is finished
        self.delay_entry.configure(state=tk.NORMAL)
        self.num_clicks_entry.configure(state=tk.NORMAL)
        self.start_button.configure(state=tk.NORMAL)

        # Start the auto clicker in a separate thread
        auto_clicker_thread = threading.Thread(target=self.auto_clicker, args=(num_clicks,))
        auto_clicker_thread.start()

    def auto_clicker(self, num_clicks):
        self.is_running = True

        # Get the current mouse position
        original_x, original_y = pyautogui.position()

        # Start the timer
        start_time = time.time()

        # Perform the clicks
        for _ in range(num_clicks):
            # Move the mouse to the original position
            pyautogui.moveTo(original_x, original_y)

            # Perform a click
            pyautogui.click()

            # Increment the click count
            self.click_count += 1

            # Delay between clicks
            time.sleep(1)

        # Calculate the elapsed time
        self.elapsed_time = time.time() - start_time

        # Display the summary
        self.show_summary()

        self.is_running = False

    def show_summary(self):
        summary_text = f"Auto Clicker Summary:\n"
        summary_text += f"Clicks performed: {self.click_count}\n"
        summary_text += f"Elapsed time: {self.elapsed_time:.2f} seconds\n"
        summary_text += f"Clicks per second: {self.click_count / self.elapsed_time:.2f}"

        self.summary_label.config(text=summary_text)


if __name__ == "__main__":
    app = AutoClickerApp()
    app.mainloop()
