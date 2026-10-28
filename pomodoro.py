import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style

WORK_TIME = 25 * 60
SHORT_BREAK_TIME = 5 * 60
LONG_BREAK_TIME = 15 * 60

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x250")
        self.root.title("Pomodoro Timer")

        self.style = Style(theme="simplex")
        self.style.theme_use()

        self.timer_label = ttk.Label(self.root, text="", font=("TkDefaultFont", 40))
        self.timer_label.pack(pady=20)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(
            self.root, text="Stop", command=self.stop_timer, state=tk.DISABLED
        )
        self.stop_button.pack(pady=5)

        self.remaining = WORK_TIME
        self.is_work_time = True
        self.pomodoros_completed = 0
        self.is_running = False
        self.after_id = None

        self.update_label()

    def start_timer(self):
        if self.is_running:
            return
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.countdown()

    def stop_timer(self):
        self.is_running = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def countdown(self):
        if not self.is_running:
            return

        if self.remaining > 0:
            self.remaining -= 1
            self.update_label()
            self.after_id = self.root.after(1000, self.countdown)
        else:
            self.switch_session()

    def switch_session(self):
        if self.is_work_time:
            self.pomodoros_completed += 1
            if self.pomodoros_completed % 4 == 0:
                self.remaining = LONG_BREAK_TIME
                messagebox.showinfo("Pomodoro", "¡Descanso largo de 15 minutos!")
            else:
                self.remaining = SHORT_BREAK_TIME
                messagebox.showinfo("Pomodoro", "¡Descanso corto de 5 minutos!")
            self.is_work_time = False
        else:
            self.remaining = WORK_TIME
            self.is_work_time = True
            messagebox.showinfo("Pomodoro", "¡A trabajar! 25 minutos.")

        self.update_label()
        self.after_id = self.root.after(1000, self.countdown)

    def update_label(self):
        minutes, seconds = divmod(self.remaining, 60)
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

if __name__ == "__main__":
    app = PomodoroTimer()
    app.root.mainloop()
