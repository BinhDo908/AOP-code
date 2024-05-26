import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import csv
from datetime import datetime
import psutil
from PIL import Image, ImageTk
import customtkinter as ctk

class RunningAppsWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Running Apps")
        self.window.geometry("400x400")
        self.window.iconbitmap(r"C:\Users\Admin\Downloads\Tkinter-Designer-master\Tkinter-Designer-master1\build\moai_1f5ff.ico")

        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(self.window, textvariable=self.search_var)
        self.search_entry.pack(fill="x", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self.start_search_timer)

        self.canvas = tk.Canvas(self.window, bg="#1E1E1E")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        background_image_path_RA = r"C:\Users\Admin\Downloads\6194995_1_.png"
        self.background_image_RA = tk.PhotoImage(file=background_image_path_RA)
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_image_RA)

        self.frame = tk.Frame(self.canvas, bg="#1E1E1E")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.app_labels = []
        self.search_timer = None
        self.search_delay = 500
        self.running_apps_snapshot = None
        self.update_running_apps()

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def update_running_apps(self):
        for label in self.app_labels:
            label.destroy()

        search_query = self.search_var.get().lower()

        if search_query == "":
            if self.running_apps_snapshot is not None:
                running_apps = self.running_apps_snapshot
            else:
                running_apps = self.get_running_apps()
        else:
            if self.running_apps_snapshot == None:
                self.running_apps_snapshot = self.get_running_apps()
            running_apps = [app_name for app_name in self.running_apps_snapshot if search_query in app_name.lower()]

        unique_running_apps = set(running_apps)

        if unique_running_apps:
            for i, app_name in enumerate(unique_running_apps):
                label = tk.Label(self.frame, text=app_name, anchor="w", bg="#1E1E1E", fg="white")
                label.grid(row=i, column=0, sticky="we")
                self.app_labels.append(label)

                label.bind("<Button-1>", lambda event, app_name=app_name: self.open_app(app_name))
                label.bind("<Button-3>", lambda event, app_name=app_name: self.confirm_end_task(app_name))
        else:
            label = tk.Label(self.frame, text="No matching apps", anchor="w", bg="#1E1E1E", fg="white")
            label.grid(row=0, column=0, sticky="we")
            self.app_labels.append(label)

        self.window.after(1000, self.update_running_apps)

    def open_app(self, app_name):
        app_path = self.find_app_path(app_name)
        if app_path:
            app_tracker = AppUsageTracker(app_name, app_path)

    def find_app_path(self, app_name):
        for proc in psutil.process_iter(['name', 'exe']):
            try:
                if proc.info['name'] == app_name:
                    return proc.info['exe']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return None

    def confirm_end_task(self, app_name):
        confirm = messagebox.askyesno("End Task", f"Are you sure you want to end the task for {app_name}?")
        if confirm:
            try:
                for proc in psutil.process_iter():
                    if proc.name() == app_name:
                        proc.terminate()
                        break
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

            self.app_labels = [label for label in self.app_labels if label.cget("text") != app_name]
            self.update_running_apps()

    def start_search_timer(self, event):
        if self.search_timer:
            self.window.after_cancel(self.search_timer)
        self.search_timer = self.window.after(self.search_delay, self.update_running_apps)

    def get_running_apps(self):
        user_name = psutil.Process().username()
        running_apps = []
        for proc in psutil.process_iter(['name', 'username', 'create_time']):
            try:
                if proc.info['username'] == user_name and proc.info['name'].endswith('.exe'):
                    running_apps.append(proc.info['name'])
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
        return running_apps

    def show(self):
        self.window.mainloop()

class AppUsageTracker:
    def __init__(self, app_name):
        self.app_name = app_name
        self.start_time = datetime.now()
        self.window = tk.Toplevel()
        self.window.geometry("250x100")
        self.window.title("App Usage Tracker")
        self.window.configure(bg="#1E1E1E")
        self.window.resizable(False, False)
        self.window.iconbitmap(r"C:\Users\Admin\Downloads\Tkinter-Designer-master\Tkinter-Designer-master1\build\moai_1f5ff.ico")

        self.label = tk.Label(self.window, text=f"Tracking time for {self.app_name}...", fg="#9f0be3", bg="#1E1E1E")
        self.label.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.stop_timer)
        self.update_timer()

    def update_timer(self):
        current_time = datetime.now()
        duration = current_time - self.start_time
        self.label.config(text=f"Time spent on {self.app_name}: {duration}", fg="#9f0be3", bg="#1E1E1E")
        self.window.after(1000, self.update_timer)

    def stop_timer(self):
        self.window.destroy()
    
    def close(self):
        self.stop_timer()

class TodoApp(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.configure(bg="#1E1E1E")
        self.title("AOP To-Do List")
        self.geometry("600x600")
        self.iconbitmap(r"C:\Users\Admin\Downloads\Tkinter-Designer-master\Tkinter-Designer-master1\build\moai_1f5ff.ico")
        self.tasks = []

        self.setup_ui()
        self.load_tasks()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="AOP To-Do List", font=("Helvetica", 24))
        self.title_label.pack(pady=20)

        self.task_entry = ctk.CTkEntry(self, placeholder_text="Enter a new task")
        self.task_entry.pack(pady=10, padx=20, fill='x')

        self.add_task_button = ctk.CTkButton(self, text="Add Task", command=self.add_task, fg_color="#9f0be3", hover_color="#62078c")
        self.add_task_button.pack(pady=10)

        self.tasks_frame = ctk.CTkFrame(self)
        self.tasks_frame.pack(pady=10, padx=20, fill='both', expand=True)

        self.update_tasks()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.task_entry.delete(0, 'end')
            self.update_tasks()
            self.save_tasks()
        else:
            messagebox.showwarning("Error", "Task cannot be empty")

    def delete_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            self.update_tasks()
            self.save_tasks()

    def update_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        for task in self.tasks:
            task_frame = ctk.CTkFrame(self.tasks_frame)
            task_frame.pack(fill='x', pady=5)

            task_label = ctk.CTkLabel(task_frame, text=task, anchor='w')
            task_label.pack(side='left', fill='x', expand=True, padx=10)

            delete_button = ctk.CTkButton(task_frame, text="Delete", width=80, command=lambda t=task: self.delete_task(t), fg_color="#9f0be3", hover_color="#62078c")
            delete_button.pack(side='right', padx=10)

    def save_tasks(self):
        with open('SavedTasks.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for task in self.tasks:
                writer.writerow([task])

    def load_tasks(self):
        if os.path.exists('SavedTasks.csv'):
            with open('SavedTasks.csv', 'r') as file:
                reader = csv.reader(file)
                self.tasks = [row[0] for row in reader]
                self.update_tasks()

class NoteApp(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("AOP Note-Taking App")
        self.geometry("600x400")
        self.iconbitmap(r"C:\Users\Admin\Downloads\Tkinter-Designer-master\Tkinter-Designer-master1\build\moai_1f5ff.ico")
        self.configure(bg="#ffffff")
        
        self.create_widgets()

    def create_widgets(self):
        self.text_area = tk.Text(self, bg="#1E1E1E", fg="white", insertbackground="white", wrap="word")
        self.text_area.pack(fill="both", expand=True)

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)

    def show(self):
        self.mainloop()

class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1000x800")
        self.window.configure(bg="#1E1E1E")
        self.window.title("Application Organizer Program")
        self.window.resizable(False, False)
        self.window.iconbitmap(r"C:\Users\Admin\Downloads\Tkinter-Designer-master\Tkinter-Designer-master1\build\moai_1f5ff.ico")
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = (screen_width - 1000) // 2
        y_coordinate = (screen_height - 800) // 2
        background_image_path = r"C:\Users\Admin\Downloads\6194995_1_.png"
        self.background_image = tk.PhotoImage(file=background_image_path)
        self.window.geometry(f"1000x800+{x_coordinate}+{y_coordinate}")

        self.canvas = tk.Canvas(
            self.window,
            bg="#1E1E1E",
            height=800,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)

        self.image_path_1 = r"C:\Users\Admin\Downloads\Tkinter-Designer-master\Tkinter-Designer-master1\build\Screenshot_2024-05-08_112229-removebg-preview.png"
        self.image_1 = tk.PhotoImage(file=self.image_path_1)
        self.image_1 = self.image_1.subsample(5, 5)
        self.canvas.create_image(10, 15, anchor="nw", image=self.image_1)

        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(self.window, textvariable=self.search_var, font=("Helvetica", 15), width=700, height=40, placeholder_text="Search")
        self.search_entry.place(x=100, y=32)
        self.search_entry.bind("<KeyRelease>", self.debounce(self.search_apps, 300))
        self.window.bind("<KeyRelease>", self.debounce(self.search_apps, 300))
        self.search_entry.focus_set()

        self.apps = []
        self.app_labels = []
        self.app_icons = []
        self.load_apps()

        self.browser = ctk.CTkButton(self.window, text="Browse", command=self.browseFiles, width=110, height=35, fg_color="#9f0be3", font=("Helvetica", 14, "bold"), hover_color="#62078c", corner_radius=10)
        self.browser.place(x=40, y=660)
        self.add_tooltip(self.browser, "Browse")

        self.run = ctk.CTkButton(self.window, text="Run All Apps", command=self.runApps, width=110, height=35, fg_color="#9f0be3", font=("Helvetica", 14, "bold"), hover_color="#62078c", corner_radius=10)
        self.run.place(x=40, y=700)
        self.add_tooltip(self.run, "Run All Apps")

        self.delete_mode = False
        self.delete_button = ctk.CTkButton(self.window, text="Delete App", command=self.deleteApp, width=110, height=35, fg_color="#9f0be3", font=("Helvetica", 14, "bold"), hover_color="#62078c", corner_radius=10)
        self.delete_button.place(x=160, y=660)
        self.add_tooltip(self.delete_button, "Delete App")

        self.running_apps_button = ctk.CTkButton(self.window, text="Running Apps", width=110, height=35, command=lambda: RunningAppsWindow(), fg_color="#9f0be3", font=("Helvetica", 14, "bold"), hover_color="#62078c", corner_radius=10)
        self.running_apps_button.place(x=160, y=700)
        self.add_tooltip(self.running_apps_button, "Running Apps")

        menu_options = ["Browse", "Run All Apps", "Delete App", "Running Apps","To-do List", "Note","Help"]
        self.menu_var = tk.StringVar(value="Menu")
        self.option_menu = ctk.CTkOptionMenu(self.window, values=menu_options, variable=self.menu_var, command=self.handleMenuOption, width=150, fg_color="#9f0be3", button_hover_color="#62078c", dropdown_fg_color="#62078c", button_color="#1E1E1E")
        self.option_menu.place(x=830, y=38)

    def debounce(self, func, wait):
        def debounced_func(*args, **kwargs):
            if hasattr(debounced_func, '_timer'):
                self.window.after_cancel(debounced_func._timer)
            debounced_func._timer = self.window.after(wait, lambda: func(*args, **kwargs))
        return debounced_func

    def handleMenuOption(self, selected_option):
        menu_actions = {
            "Browse": self.browseFiles,
            "Run All Apps": self.runApps,
            "Delete App": self.deleteApp,
            "Running Apps": lambda: RunningAppsWindow(),
            "To-do List": self.todoList,
            "Note": self.note,
            "Help": self.open_help_file
        }
        action = menu_actions.get(selected_option)
        if action:
            action()

    def add_tooltip(self, widget, text):
        tooltip = tk.Label(self.window, text=text, bg="#1E1E1E", fg="#9f0be3", borderwidth=1, relief="solid", wraplength=150)
        tooltip.place_forget()

        def show_tooltip(event):
            x = event.x_root - self.window.winfo_rootx() + 20
            y = event.y_root - self.window.winfo_rooty() + 20
            tooltip.place(x=x, y=y)

        def hide_tooltip(event):
            tooltip.place_forget()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def note(self):
        note_window = NoteApp()
        note_window.show()

    def search_apps(self, event):
        search_query = self.search_var.get().lower()
        matched_apps = []

        for app in self.apps:
            if search_query in app[1].lower():  
                matched_apps.append(app)

        self.clear_app_labels()

        if matched_apps:
            self.display_apps(matched_apps)
        else:
            no_result_label = ctk.CTkLabel(self.canvas, text="No results found", bg_color="#1E1E1E", fg_color="#9f0be3", corner_radius=50)
            no_result_label.place(x=500, y=400, anchor="center")
            self.app_labels.append(no_result_label)

    def clear_app_labels(self):
        for label in self.app_labels:
            label.destroy()
        self.app_labels = []
        self.app_icons = []

    def open_help_file(self):
        try:
            file_path = r"C:\Users\Admin\Downloads\Tkinter-Designer-master\Tkinter-Designer-master1\build\help_text.txt"
            with open(file_path, 'r') as file:
                content = file.read()

            text_window = tk.Toplevel(self.window)
            text_window.title("Help")
            text_window.geometry("400x250")

            text_widget = tk.Text(text_window, wrap="word", bg="#1E1E1E", fg="#ffffff", font=("Arial", 12))
            text_widget.insert("1.0", content)
            text_widget.configure(state="disabled")
            text_widget.pack(expand=True, fill="both")

        except FileNotFoundError:
            messagebox.showerror("Error", "The help file was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                              filetypes=(("executables", "*.exe"), ("all files", "*.*")))
        if filename:
            display_name = os.path.basename(filename)

            icon_path = filedialog.askopenfilename(initialdir="/", title="Select Icon",
                                                   filetypes=(("images", "*.png;*.jpg;*.jpeg;*.ico"), ("all files", "*.*")))
            if icon_path:
                self.apps.append((filename, display_name, icon_path))
                self.update_app_labels()
                self.save_apps()

    def runApps(self):
        for app in self.apps:
            os.startfile(app[0])

    def update_app_labels(self):
        self.clear_app_labels()
        self.display_apps(self.apps)

    def display_apps(self, apps):
        max_columns = 7
        x_start = 70
        y_start = 230
        x_gap = 130
        y_gap = 100

        for i, app in enumerate(apps):
            display_name = app[1]
            icon_path = app[2]

            row = i // max_columns
            column = i % max_columns
            x_position = x_start + column * x_gap
            y_position = y_start + row * y_gap

            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((43, 43), Image.LANCZOS)
            icon = ImageTk.PhotoImage(icon_image)
            self.app_icons.append(icon)

            icon_label = tk.Label(self.canvas, image=icon, bg="#1E1E1E")
            icon_label.place(x=x_position + 10, y=y_position - 70)

            label = ctk.CTkLabel(self.canvas, text=display_name, wraplength=80, justify='center', anchor='w', bg_color="transparent", fg_color="transparent", corner_radius=50, text_color="#9f0be3")
            label.place(x=x_position, y=y_position - 15)
            label.bind("<Button-3>", lambda event, i=i: self.renameApp(i))
            label.bind("<Button-1>", lambda event, i=i: self.runSingleApp(i))
            label.bind("<Button-2>", lambda event, i=i: self.onDelete(event, i))
            self.app_labels.append(label)

    def deleteApp(self):
        self.delete_mode = not self.delete_mode
        if self.delete_mode:
            self.delete_button.configure(text="Cancel Delete")
        else:
            self.delete_button.configure(text="Delete App")

    def save_apps(self):
        with open("savedApps.csv", "w", newline="") as saved:
            writer = csv.writer(saved)
            writer.writerows(self.apps)

    def load_apps(self):
        self.apps = []
        try:
            with open("savedApps.csv", "r", newline="") as saved:
                reader = csv.reader(saved)
                for row in reader:
                    if len(row) == 3:
                        self.apps.append((row[0], row[1], row[2]))
            self.update_app_labels()
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
            self.apps[index] = (self.apps[index][0], new_name, self.apps[index][2])
            self.update_app_labels()
            self.save_apps()

    def runSingleApp(self, index):
        os.startfile(self.apps[index][0])
        AppUsageTracker(self.apps[index][1])

    def todoList(self):
        TodoApp()

    def show(self):
        self.window.mainloop()

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.show()
