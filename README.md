# 🥘 Recipe Portal App

A simple desktop application for browsing and managing recipes and ingredients using Python and SQLite. Designed with `tkinter` for an intuitive GUI, this app allows users to view recipe lists, see ingredient summaries, and search easily.

---

## 🎯 Aim of the Project

To create a functional and user-friendly desktop application for managing recipes and ingredient stock, allowing users to quickly access, search, and summarize food preparation data using a local database.

---

## 📦 Project Structure
Recipe Portal App/
│
├── recipe_portal.db          # SQLite3 database storing all recipes, ingredients, users, and reviews
├── main.py                   # Main Python file containing GUI and application logic
│
├── 📦 Modules & Components:
│   ├── initialize_db()       # Initializes the database and inserts default sample data
│   ├── RecipeApp class       # Manages the overall GUI layout and user interaction
│   │   ├── setup_recipe_tab()  # Recipe tab UI layout and logic
│   │   ├── setup_summary_tab() # Summary tab UI layout and logic
│   │   ├── load_recipes()      # Fetches and displays recipes in the UI
│   │   └── load_summary()      # Displays recipe and ingredient summaries
│
└── 📊 Tabs:
    ├── 🍲 Recipes Tab         # Displays recipes in a searchable table format
    ├── 📊 Summary Tab         # Summarizes all recipes and available stock items
    └── ➕ Add Recipe (Coming Soon) # Will allow users to add custom recipes through the GUI


---

## 🖥️ Technologies Used

- Python 3.x
- SQLite3
- Tkinter (for GUI)
- ttk Treeview

---

## 📚 Features

- 🧾 View a list of recipes with details like ingredients, preparation time, and chef.
- 🔍 Search functionality by recipe name or chef name.
- 📊 Summary tab to display total recipes and a list of all available ingredients.
- 🗃️ Backend database auto-generated with initial recipe and ingredient data.


---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/recipe-portal.git
cd recipe-portal
```
### 2. Run the App
```bash
python main.py
```
Make sure Python 3.x is installed on your system.
 ---

### Future Improvements
Add "Add Recipe" functionality via GUI.

Allow editing and deleting of existing recipes.

Export summary reports to PDF or CSV.

User authentication and favorites.
---

### License
This project is open-source and available under the MIT License.
---
