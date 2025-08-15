import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import csv
import matplotlib.pyplot as plt

# Setting up the database connection
def setup_database():
    connection = sqlite3.connect('expenses.db')
    c = connection.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    ''') # Create table if it doesn't exist
    connection.commit()
    connection.close()

# Database operations
# Fetching expenses from the database
# This function fetch all expenses from databse, ordered by date, lateset expense first.
def fetch_expenses():
    connection = sqlite3.connect('expenses.db')
    c = connection.cursor()
    c.execute('SELECT * FROM expenses order by date DESC')
    expenses = c.fetchall()
    connection.close()
    return expenses
# This function adds a new expense to the databse
def add_expense():
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid amount.")
        return
    category = category_var.get()
    description = description_entry.get()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    connection = sqlite3.connect('expenses.db')
    c = connection.cursor()
    c.execute('''
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, description, date))     
    connection.commit()
    connection.close()
    clear_entries() # Clear the input fields after adding expense
    refresh_expenses() # Refresh the displayed expenses
# deletes the selected expense from the databse
def delete_expense():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an expense to delete.")
        return
    item_id = tree.item(selected_item[0])['values'][0]
    
    connection = sqlite3.connect('expenses.db')
    c = connection.cursor()
    c.execute('DELETE FROM expenses WHERE id=?', (item_id,))
    connection.commit()
    connection.close()
    refresh_expenses()
# Exports all expenses to a CSV file
def export_expenses():  
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    expenses = fetch_expenses()
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Amount', 'Category', 'Description', 'Date'])
        for expense in expenses:
            writer.writerow(expense)
    
    messagebox.showinfo("Export", "Expenses exported successfully.")
# Plots the expenses by category in a pie chart
def plot_expenses():
    connection = sqlite3.connect('expenses.db')
    c = connection.cursor()
    c.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    data = c.fetchall()
    connection.close()
    if not data:
        messagebox.showwarning("No Data", "No expenses to plot.")
        return
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]
    plt.figure(figsize=(10, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title('Expenses by Category')
    plt.show()
# Refreshes the displayed expenses in the treeview
def refresh_expenses():
    update_tree(fetch_expenses())
# Updates the treeview with the latest expenses
def update_tree(expenses):
    tree.delete(*tree.get_children())
    for expense in expenses:
        tree.insert('', tk.END, values=expense)
# Clears the input fields and resets to default
def clear_entries():
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    category_var.set('Food')

# Main application setup
root = tk.Tk()
root.title("Daily Expense Tracker")
root.geometry("800x600")
# Input frame for adding expenses
frame = tk.LabelFrame(root, text="Add Expense", padx=10, pady=10)
frame.pack(padx=10, pady=5, fill="x")
# Input fields for amount
tk.Label(frame, text="Amount:").grid(row=0, column=0)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=0, column=1)
# Category dropdown frame
tk.Label(frame, text="Category:").grid(row=0, column=2)
category_var = tk.StringVar(value='Food')
categories = ['Food', 'Transport', 'Bills', 'Shopping', 'Utilities', 'Entertainment', 'Other']
category_menu = ttk.Combobox(frame, textvariable=category_var, values=categories, state='readonly')
category_menu.grid(row=0, column=3)
# Description input
tk.Label(frame, text="Description:").grid(row=0, column=4)
description_entry = tk.Entry(frame)
description_entry.grid(row=0, column=5)
# Add Expense button
tk.Button(frame, text="Add Expense", command=add_expense).grid(row=0, column=6, padx=5)
# Delete, Export, Plot buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10, padx=10, fill="x")

tk.Button(button_frame, text="Delete Expense", command=delete_expense).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Export Expenses", command=export_expenses).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Plot Expenses", command=plot_expenses).grid(row=0, column=2, padx=5)
# Treeview frame for displaying expenses
tree_frame = tk.Frame(root)
tree_frame.pack(padx=10, pady=5, fill="both", expand=True)

columm = ('ID', 'Amount', 'Category', 'Description', 'Date')
tree = ttk.Treeview(tree_frame, columns=columm, show='headings')
for col in columm:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill="both", expand=True)
# Initialize the databse and load data
setup_database()
refresh_expenses()

root.mainloop()

