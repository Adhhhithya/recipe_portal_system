import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import random

# Initialize DB and insert data
def initialize_db():
    if os.path.exists('recipe_portal.db'):
        os.remove('recipe_portal.db')

    conn = sqlite3.connect('recipe_portal.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        dietary_pref TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        cuisine TEXT,
        dish_type TEXT,
        prep_time TEXT,
        difficulty TEXT,
        method TEXT,
        rating REAL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        stock_quantity TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS recipe_ingredients (
        recipe_id INTEGER,
        ingredient_id INTEGER,
        quantity TEXT,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id),
        FOREIGN KEY(ingredient_id) REFERENCES ingredients(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        user_id INTEGER,
        rating INTEGER,
        review TEXT,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    c.executemany("INSERT INTO users (name, dietary_pref) VALUES (?, ?)", [
        ('Alice', 'Vegetarian'),
        ('Bob', 'Vegan'),
        ('Charlie', 'Non-Vegetarian')
    ])

    ingredients = [
        ('Tomato', '120 pcs'), ('Onion', '80 pcs'), ('Garlic', '50 cloves'),
        ('Chicken', '30 kg'), ('Basil', '40 g'), ('Pasta', '60 packs'),
        ('Paneer', '25 blocks'), ('Spinach', '45 bundles'), ('Olive Oil', '100 ml'),
        ('Salt', '200 g'), ('Pepper', '90 g'), ('Chili Powder', '70 g'),
        ('Sugar', '150 g'), ('Flour', '1000 g'), ('Butter', '300 g'),
        ('Milk', '5 L'), ('Eggs', '60 pcs'), ('Cocoa Powder', '100 g')
    ]
    c.executemany("INSERT INTO ingredients (name, stock_quantity) VALUES (?, ?)", ingredients)

    recipes = [
        ('Spaghetti Pomodoro', 'Italian', 'Main Course', '30 mins', 'Easy', 'Boil pasta. Make tomato sauce with garlic, basil, and olive oil. Mix and serve.', 4.5),
        ('Palak Paneer', 'Indian', 'Main Course', '40 mins', 'Medium', 'Blend spinach. Fry paneer. Mix with spices and spinach puree.', 4.3),
        ('Garlic Chicken', 'Continental', 'Main Course', '45 mins', 'Medium', 'Marinate chicken in garlic and spices. Grill until cooked.', 4.7),
        ('Chocolate Cake', 'French', 'Dessert', '60 mins', 'Medium', 'Mix flour, sugar, cocoa, eggs, milk and bake.', 4.8),
        ('Bruschetta', 'Italian', 'Starter', '15 mins', 'Easy', 'Toast bread, top with tomato, basil, olive oil.', 4.2)
    ]

    sample_dish_names = [
        'Lemon Herb Quinoa', 'Mango Chutney Tofu', 'Creamy Broccoli Soup',
        'Grilled Zucchini Rolls', 'Spicy Chickpea Wraps', 'Avocado Lime Salad',
        'Stuffed Bell Peppers', 'Thai Peanut Noodles', 'Baked Falafel Pockets',
        'Mushroom Risotto', 'Tomato Basil Tart', 'Sweet Potato Curry',
        'Eggplant Parmesan', 'Pumpkin Lentil Soup', 'Garlic Butter Shrimp',
        'Coconut Rice Bowl', 'Pesto Pasta Delight', 'Zesty Black Bean Tacos',
        'Green Curry Vegetables', 'Cheesy Cauliflower Bake', 'Honey Glazed Carrots',
        'Kale Cranberry Salad', 'Tofu Stir Fry', 'Beetroot Hummus Wraps',
        'Peanut Butter Banana Toast', 'Almond Berry Smoothie'
    ]

    difficulties = ['Easy', 'Medium', 'Hard']
    cuisines = ['Indian', 'Italian', 'Mexican', 'Thai', 'Chinese', 'Greek', 'Fusion']

    for i in range(6, 51):
        name = random.choice(sample_dish_names)
        cuisine = random.choice(cuisines)
        difficulty = random.choice(difficulties)
        method = f"This is how you make {name}. Follow the traditional steps for a delicious result."
        recipes.append((name, cuisine, 'Main Course', '25 mins', difficulty, method, round(random.uniform(3.5, 4.9), 1)))

    c.executemany("INSERT INTO recipes (name, cuisine, dish_type, prep_time, difficulty, method, rating) VALUES (?, ?, ?, ?, ?, ?, ?)", recipes)

    conn.commit()
    conn.close()

class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍽 Cooking Recipe Portal")
        self.root.configure(bg="#f2f2f2")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), foreground="#fff", background="#4CAF50")
        style.configure("Treeview", font=('Arial', 11), rowheight=25, background="#fafafa", fieldbackground="#fafafa")

        self.tab_control = ttk.Notebook(self.root)
        self.recipe_tab = ttk.Frame(self.tab_control)
        self.summary_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.recipe_tab, text='🍲 Recipes')
        self.tab_control.add(self.summary_tab, text='📊 Summary')
        self.tab_control.pack(expand=1, fill='both')

        self.setup_recipe_tab()
        self.setup_summary_tab()

    def setup_recipe_tab(self):
        ttk.Label(self.recipe_tab, text="Recipe List", font=('Arial', 18, 'bold')).pack(pady=10)

        control_frame = ttk.Frame(self.recipe_tab)
        control_frame.pack(pady=5)

        ttk.Label(control_frame, text="Search: ").pack(side='left')
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var)
        search_entry.pack(side='left')
        search_entry.bind("<KeyRelease>", self.load_recipes)

        add_btn = ttk.Button(control_frame, text="➕ Add Recipe", command=self.add_recipe_dialog)
        add_btn.pack(side='right')

        cols = ('Name', 'Cuisine', 'Type', 'Prep Time', 'Difficulty', 'Rating')
        self.recipe_tree = ttk.Treeview(self.recipe_tab, columns=cols, show='headings')
        for col in cols:
            self.recipe_tree.heading(col, text=col)
            self.recipe_tree.column(col, width=130, anchor='center')
        self.recipe_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.load_recipes()

    def add_recipe_dialog(self):
        def save_recipe():
            name = name_var.get()
            cuisine = cuisine_var.get()
            dish_type = dish_type_var.get()
            prep_time = prep_time_var.get()
            difficulty = difficulty_var.get()
            method = method_text.get("1.0", tk.END).strip()
            rating = float(rating_var.get()) if rating_var.get() else 0.0

            conn = sqlite3.connect('recipe_portal.db')
            c = conn.cursor()
            c.execute("INSERT INTO recipes (name, cuisine, dish_type, prep_time, difficulty, method, rating) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (name, cuisine, dish_type, prep_time, difficulty, method, rating))
            conn.commit()
            conn.close()
            top.destroy()
            self.load_recipes()
            messagebox.showinfo("Success", "Recipe added successfully!")

        top = tk.Toplevel(self.root)
        top.title("Add New Recipe")
        top.geometry("400x500")

        name_var = tk.StringVar()
        cuisine_var = tk.StringVar()
        dish_type_var = tk.StringVar()
        prep_time_var = tk.StringVar()
        difficulty_var = tk.StringVar()
        rating_var = tk.StringVar()

        fields = [
            ("Recipe Name", name_var),
            ("Cuisine", cuisine_var),
            ("Dish Type", dish_type_var),
            ("Preparation Time", prep_time_var),
            ("Difficulty", difficulty_var),
            ("Rating", rating_var)
        ]

        for label, var in fields:
            ttk.Label(top, text=label).pack(pady=5)
            ttk.Entry(top, textvariable=var).pack(pady=5)

        ttk.Label(top, text="Method").pack(pady=5)
        method_text = tk.Text(top, height=5)
        method_text.pack(pady=5)

        ttk.Button(top, text="Save Recipe", command=save_recipe).pack(pady=10)

    def setup_summary_tab(self):
        ttk.Label(self.summary_tab, text="Recipe & Material Summary", font=('Arial', 18, 'bold')).pack(pady=10)
        summary_frame = ttk.Frame(self.summary_tab)
        summary_frame.pack(side='top', fill='both', expand=True, padx=10)

        ttk.Label(summary_frame, text="Recipes:", font=('Arial', 12)).grid(row=0, column=0, sticky='w')
        self.summary_tree = ttk.Treeview(summary_frame, columns=('Name', 'Cuisine', 'Difficulty', 'Method'), show='headings')
        for col in ('Name', 'Cuisine', 'Difficulty', 'Method'):
            self.summary_tree.heading(col, text=col)
        self.summary_tree.grid(row=1, column=0, sticky='nsew')

        ttk.Label(summary_frame, text="\nMaterials & Quantity:", font=('Arial', 12)).grid(row=2, column=0, sticky='w')
        self.inventory_tree = ttk.Treeview(summary_frame, columns=('Quantity'), show='headings')
        self.inventory_tree.heading('Quantity', text='Quantity in Stock')
        self.inventory_tree.grid(row=3, column=0, sticky='nsew')

        summary_frame.rowconfigure(1, weight=1)
        summary_frame.rowconfigure(3, weight=1)
        summary_frame.columnconfigure(0, weight=1)

        self.load_summary()

    def load_recipes(self, event=None):
        for i in self.recipe_tree.get_children():
            self.recipe_tree.delete(i)
        conn = sqlite3.connect('recipe_portal.db')
        c = conn.cursor()
        search_term = self.search_var.get()
        if search_term:
            c.execute("SELECT name, cuisine, dish_type, prep_time, difficulty, rating FROM recipes WHERE name LIKE ?", (f"%{search_term}%",))
        else:
            c.execute("SELECT name, cuisine, dish_type, prep_time, difficulty, rating FROM recipes")
        for row in c.fetchall():
            self.recipe_tree.insert('', 'end', values=row)
        conn.close()

    def load_summary(self):
        conn = sqlite3.connect('recipe_portal.db')
        c = conn.cursor()
        c.execute("SELECT name, cuisine, difficulty, method FROM recipes")
        for name, cuisine, difficulty, method in c.fetchall():
            self.summary_tree.insert('', 'end', values=(name, cuisine, difficulty, method))

        c.execute("SELECT name, stock_quantity FROM ingredients")
        for name, qty in c.fetchall():
            self.inventory_tree.insert('', 'end', text=name, values=(qty,))
        conn.close()

if __name__ == '__main__':
    initialize_db()
    root = tk.Tk()
    app = RecipeApp(root)
    root.geometry('1000x700')
    root.mainloop()
