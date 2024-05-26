import tkinter as tk
from tkinter import ttk
from Main import MainWindow  # Import the main window class from main_window.py
import time

class LoadingScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x400")
        self.root.configure(bg="#1E1E1E")

        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width - 500) // 2
        y_coordinate = (screen_height - 500) // 2
        self.root.geometry(f"500x500+{x_coordinate}+{y_coordinate}")

        # Remove the title bar
        self.root.overrideredirect(True)

        # Loading image
        self.image_path = r"C:\Users\Admin\Downloads\Tkinter-Designer-master\Tkinter-Designer-master1\build\Screenshot_2024-05-08_112229-removebg-preview.png"
        self.image = tk.PhotoImage(file=self.image_path)
        self.image = self.image.subsample(2, 2) 
        self.image_label = tk.Label(self.root, image=self.image, bg="#1E1E1E")
        self.image_label.place(relx=0.5, rely=0.25, anchor="center")

        # Loading animation
        self.loading_label = tk.Label(self.root, text="Application Organizer Program", font=("Helvetica", 15, "bold"), fg="#9f0be3", bg="#1E1E1E")
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")

        # Loading bar
        self.loading_bar = ttk.Progressbar(self.root, orient="horizontal", mode="indeterminate", length=300)
        self.loading_bar.place(relx=0.5, rely=0.7, anchor="center")
        self.loading_bar.start(10)
        self.loading_animation()

    def loading_animation(self):
        loading_text = "Application Organizer Program"
        for char_index in range(len(loading_text)):
            animated_text = loading_text[:char_index+1]
            if self.root.winfo_exists():
                for _ in range(3):
                    for char in ".  .  .  ":
                        self.loading_label.config(text=animated_text + char)
                        self.root.update()
                        time.sleep(0.004)
        if self.root.winfo_exists():
            self.root.after(0, self.open_main_window)


    def open_main_window(self):
        self.root.destroy()  # Close the loading screen window
        main_window = MainWindow()  # Create an instance of the main window
        main_window.show()  # Show the main window


def main():
    loading_screen = LoadingScreen()
    loading_screen.root.mainloop()

if __name__ == "__main__":
    main()
