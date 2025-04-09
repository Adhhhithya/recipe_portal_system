import sqlite3

# --- DB Initialization ---
def connect_db():
    conn = sqlite3.connect("recipe_portal.db")
    return conn

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # Users Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        dietary_pref TEXT
    )""")

    # Recipes Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cuisine TEXT,
        difficulty TEXT,
        instructions TEXT
    )""")

    # Ingredients Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )""")

    # Recipe_Ingredients Junction Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recipe_ingredients (
        recipe_id INTEGER,
        ingredient_id INTEGER,
        FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
    )""")

    # Reviews Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        recipe_id INTEGER,
        rating INTEGER,
        comment TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
    )""")

    conn.commit()
    conn.close()

# --- Insert Functions ---
def add_user(username, dietary_pref):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, dietary_pref) VALUES (?, ?)", (username, dietary_pref))
    conn.commit()
    conn.close()

def add_recipe(name, cuisine, difficulty, instructions, ingredient_list):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO recipes (name, cuisine, difficulty, instructions) VALUES (?, ?, ?, ?)",
                (name, cuisine, difficulty, instructions))
    recipe_id = cur.lastrowid

    for ingredient in ingredient_list:
        # Check if ingredient exists
        cur.execute("SELECT ingredient_id FROM ingredients WHERE name = ?", (ingredient,))
        result = cur.fetchone()
        if result:
            ingredient_id = result[0]
        else:
            cur.execute("INSERT INTO ingredients (name) VALUES (?)", (ingredient,))
            ingredient_id = cur.lastrowid

        cur.execute("INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (?, ?)",
                    (recipe_id, ingredient_id))

    conn.commit()
    conn.close()

def add_review(user_id, recipe_id, rating, comment):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO reviews (user_id, recipe_id, rating, comment) VALUES (?, ?, ?, ?)",
                (user_id, recipe_id, rating, comment))
    conn.commit()
    conn.close()

def get_all_recipes():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipes")
    rows = cur.fetchall()
    conn.close()
    return rows

# --- Display DB Tables when run directly ---
def print_tables():
    conn = connect_db()
    cur = conn.cursor()
    tables = ['users', 'recipes', 'ingredients', 'recipe_ingredients', 'reviews']
    for table in tables:
        print(f"\n--- {table.upper()} ---")
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    conn.close()

# --- Main Execution for DB file ---
if __name__ == "__main__":
    create_tables()
    print("Tables created.")
    print_tables()
