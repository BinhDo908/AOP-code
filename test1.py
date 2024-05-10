import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import os
import csv
from datetime import datetime
import customtkinter 

class AppUsageTracker:
    def __init__(self):
        self.start_time = datetime.now()
        self.window = tk.Tk()
        self.window.geometry("250x100")
        self.window.title("App Usage Tracker")
        self.window.configure(bg="#1E1E1E")
        self.window.resizable(False, False)
        self.window.iconbitmap(r"C:\Users\Admin\Downloads\moai_1f5ff.ico")

        self.label = tk.Label(self.window, text="Application is running...", fg="#9f0be3", bg="#1E1E1E")
        self.label.pack()

        self.update_timer()

    def update_timer(self):
        current_time = datetime.now()
        duration = current_time - self.start_time
        self.label.config(text=f"Duration: {duration}", fg="#9f0be3", bg="#1E1E1E")
        self.window.after(1000, self.update_timer)

class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("700x500")
        self.window.configure(bg="#1E1E1E")
        self.window.title("Application Organizer Program")
        self.window.resizable(False, False)
        self.window.iconbitmap(r"C:\Users\Admin\Downloads\moai_1f5ff.ico")

        # Center the window on the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = (screen_width - 700) // 2
        y_coordinate = (screen_height - 500) // 2
        self.window.geometry(f"700x500+{x_coordinate}+{y_coordinate}")

        self.canvas = tk.Canvas(
            self.window,
            bg="#1E1E1E",
            height=500,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Add image at top left corner
        self.image_path_1 = r"C:\Users\Admin\Downloads\Screenshot_2024-05-08_112229-removebg-preview.png"
        self.image_1 = tk.PhotoImage(file=self.image_path_1)
        self.image_1 = self.image_1.subsample(5, 5)  # Resize the image by a factor of 2 in both dimensions
        self.canvas.create_image(10, 10, anchor="nw", image=self.image_1)
        self.canvas.create_rectangle(100, 32, 599, 66, fill="#ffffff")
        self.canvas.create_text(120, 49, text="Search", fill="#9f0be3", anchor="w", font=("Helvetica", 10, "bold"))

        self.image_path_2 = r"C:\Users\Admin\Downloads\depositphotos_80563786-stock-illustration-stack-flat-white-color-rounded-removebg-preview.png"
        self.image_2 = tk.PhotoImage(file=self.image_path_2)
        self.image_2 = self.image_2.subsample(10, 10)  # Resize the image by a factor of 2 in both dimensions
        self.image_2_id = self.canvas.create_image(670, 20, anchor="ne", image=self.image_2)
        self.canvas.tag_bind(self.image_2_id, "<Button-1>", self.showMenu)
        self.menu_shown = False
        self.menu_items = []

        self.app_label_positions = [
            (70, 110),
            (170, 110),
            (270, 110),
            (370, 110),
            (470, 110),
            (570, 110),
            (70, 100)
            # Add more positions as needed
        ]

        self.apps = []
        self.app_labels = []
        self.load_apps()

        self.browser = ttk.Button(self.window, text="Browse", style="Blue.TButton", command=self.browseFiles)
        self.browser.place(x=40, y=400)
        self.run = ttk.Button(self.window, text="Run All Apps", style="Blue.TButton", command=self.runApps)
        self.run.place(x=40, y=440)
        self.delete_mode = False
        self.delete_button = ttk.Button(self.window, text="Delete App", style="Blue.TButton", command=self.deleteApp)
        self.delete_button.place(x=140, y=440)

        self.window.tk_setPalette(background="#1E1E1E", foreground="#9f0be3", activeForeground="#9f0be3")

        self.style = ttk.Style()
        self.style.configure("Blue.TButton", background="#9f0be3", foreground="#9f0be3", borderwidth=0, font=("Helvetica", 10,"bold"),
                             padding=5, relief="flat", borderradius=10)
        self.style.configure("Delete.TButton", background="#9f0be3", foreground="#9f0be3", borderwidth=0,
                             font=("Arial", 10), padding=5, relief="flat", borderradius=10)
        
    def showMenu(self, event):
        if not self.menu_shown:
            # Calculate menu position
            icon_x, icon_y = self.canvas.coords(self.image_2_id)
            icon_width = self.image_2.width()
            icon_height = self.image_2.height()
            menu_x = icon_x + icon_width // 2 - 46  # Adjusted to center the menu horizontally
            menu_y = icon_y + icon_height

            # Create menu items
            for i, item_text in enumerate(["Browse", "Run All Apps", "Delete App"]):
                menu_item = tk.Label(self.canvas, text=item_text, bg="#ffffff", fg="#9f0be3")
                menu_item.place(x=menu_x, y=menu_y + i * 30, anchor="n")
                menu_item.bind("<Button-1>", self.handleMenuItemClick)
                self.menu_items.append(menu_item)
            self.menu_shown = True
        else:
            # Remove menu items
            for menu_item in self.menu_items:
                menu_item.destroy()
            self.menu_items = []
            self.menu_shown = False
    


    def handleMenuItemClick(self, event):
        clicked_item_text = event.widget.cget("text")
        if clicked_item_text == "Browse":
            self.browseFiles()
        elif clicked_item_text == "Run All Apps":
            self.runApps()
        elif clicked_item_text == "Delete App":
            self.deleteApp()

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                              filetypes=(("executables", "*.exe"), ("all files", "*.*")))
        if filename:
            self.apps.append(filename)
            self.update_app_labels()
            self.save_apps()

    def runApps(self):
        for app in self.apps:
            os.startfile(app)

    def update_app_labels(self):
        for label in self.app_labels:
            label.destroy()

        for i, app in enumerate(self.apps):
            label = tk.Label(self.canvas, text=os.path.basename(app), bg="#B9B9B9", wraplength=80, justify='center',
                             anchor='w', fg="#9f0be3")
            label.place(x=self.app_label_positions[i][0], y=self.app_label_positions[i][1])
            label.bind("<Button-3>", lambda event, i=i: self.renameApp(i))
            label.bind("<Button-1>", lambda event, i=i: self.runSingleApp(i))
            label.bind("<Button-2>", lambda event, i=i: self.onDelete(event, i))
            self.app_labels.append(label)

    def deleteApp(self):
        self.delete_mode = not self.delete_mode
        if self.delete_mode:
            self.delete_button.config(text="Cancel Delete")
        else:
            self.delete_button.config(text="Delete App")

    def save_apps(self):
        with open("savedApps.csv", "w", newline="") as saved:
            writer = csv.writer(saved)
            writer.writerow(self.apps)

    def load_apps(self):
        self.apps = []  # Clear the existing list
        try:
            with open("savedApps.csv", "r", newline="") as saved:
                reader = csv.reader(saved)
                for row in reader:
                    self.apps.extend(row)
        except FileNotFoundError:
            pass

    def onDelete(self, event, index):
        if self.delete_mode:
            confirm = messagebox.askyesno("Delete App", "Are you sure you want to delete this app?")
            if confirm:
                del self.apps[index]
                self.update_app_labels()
                self.save_apps()

    def renameApp(self, index):
        new_name = simpledialog.askstring("Rename App", "Enter a new name for the app:")
        if new_name:
            self.app_labels[index].config(text=new_name)
            self.save_apps()

    def runSingleApp(self, index):
        os.startfile(self.apps[index])
        tracker = AppUsageTracker()  # Start tracking usage time when app is run

    def show(self):
        self.window.mainloop()


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.show()
