# todo_list

# 📝 Modern To-Do List with Calendar & Notifications

A desktop To-Do application built with **Tkinter** and **ttk**, featuring:

- Add / Delete / Mark Done tasks  
- Priority tags (Low, Normal, High)  
- Due-Date picker (calendar widget)  
- Automatic desktop notifications for tasks due within the next hour  
- Sorted task list: earliest due date first, then High→Normal→Low priority  
- Clean shutdown of background notification thread when you close the window  

---
📦 Features
1. Task Management
   - Input a task description.  
   - Pick a due date via a calendar.  
   - Assign a priority (Low, Normal, High).  
   - Mark tasks as done or delete them when completed.  

2. Persistence  
   - Tasks are saved in `tasks.json` automatically.  
   - On launch, existing tasks are loaded (missing due dates default to today).  

3. Notifications
   - Runs a background loop checking every 5 minutes.  
   - If a task is due within the next hour (and not yet notified), you’ll get a desktop alert.  
   - Loop stops cleanly when you close the app.

4. Sorted Display
   - Tasks sorted by due date (earliest first).  
   - Same-day tasks ordered by priority: High → Normal → Low.

5. Themed UI (ttk / clam)
   - Uses the built-in `clam` theme for a modern look.  
   - Scrollable task list via a `Canvas` + `Scrollbar`.  

## 🔧 Libraries & Installation

This project relies on these Python packages:

| Library     | Purpose                                                | Install Command                |
|-------------|--------------------------------------------------------|--------------------------------|
| `tkcalendar`| Provides the `DateEntry` calendar widget               | `pip install tkcalendar`       |
| `plyer`     | Cross-platform desktop notifications                   | `pip install plyer`            |
| `tkinter`   | Built-in Python GUI toolkit (no install required)      | Comes with Python             |
| `ttk`       | Themed widgets shipped with Tkinter                    | Comes with Python             |

---

### 🎯 Quick Setup

1. Install dependencies

   ```bash
   pip install tkcalendar plyer
   ```
2. Run the app

   ```bash
   python todo_app.py
   ```

---

## 🚀 Packaging as a Standalone Executable

To share the app without requiring Python on the target machine, use **PyInstaller**:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "tasks.json;." todo_app.py
```
to run the project and get an offline file
# Windows
python -m venv venv
venv\Scripts\activate

cd "S:\test\todo_offline"

Get-ChildItem *.py
# You should see todo_app.py

pyinstaller --onefile --windowed --add-data "tasks.json;." --hidden-import=tkcalendar --hidden-import=plyer.platforms.win.notification todo_app.py

final file will in these path
.\dist\todo_app.exe



---

## 👥 Contributing

Feel free to open issues or submit pull requests for enhancements—e.g.,

* Task editing in-place
* Search & filter
* Themed light/dark toggle
* CSV/PDF export

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
