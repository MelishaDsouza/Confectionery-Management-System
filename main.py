import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Install Pillow library for image handling
import mysql.connector
from datetime import date

# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="confectionery"
    )

# Add a new cake to the database
def add_cake():
    name = name_entry.get()
    flavor = flavor_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()
    date_added = date.today()  # Get the current date

    if not (name and flavor and price and quantity):
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        price = float(price)
        quantity = int(quantity)
        total_bill = price * quantity
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cakes (name, flavor, price, quantity, date_added, total_bill) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, flavor, price, quantity, date_added, total_bill))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Cake added successfully")
        refresh_table()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Refresh the table
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cakes")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to cancel an order by ID
def cancel_order():
    order_id = cancel_id_entry.get()
    if not order_id:
        messagebox.showerror("Error", "Please enter an Order ID")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cakes WHERE id = %s", (order_id,))
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Order ID not found")
        else:
            conn.commit()
            messagebox.showinfo("Success", "Order cancelled successfully")
        cursor.close()
        conn.close()
        refresh_table()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to resize the background image
def resize_bg_image(event):
    new_width = event.width
    new_height = event.height
    resized_image = bg_image.resize((new_width, new_height), Image.LANCZOS)
    new_bg_photo = ImageTk.PhotoImage(resized_image)
    bg_label.config(image=new_bg_photo)
    bg_label.image = new_bg_photo  # Keep a reference to prevent garbage collection

# Main window
root = tk.Tk()
root.title("Confectionery Inventory Management")
root.geometry("800x600")  # Set the initial size of the window

# Load and set the background image
bg_image = Image.open("back.png")  # Replace with your image file name
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Cover the entire window

# Bind the resize event to the resize_bg_image function
root.bind("<Configure>", resize_bg_image)

# Create a frame for the entry fields
entry_frame = tk.Frame(root, bg="#DEB887", bd=2, relief=tk.RAISED)
entry_frame.place(relx=0.5, rely=0.15, anchor=tk.CENTER, relwidth=0.8, height=150)

# Labels and entries for cake details
tk.Label(entry_frame, text="Name", bg="#DEB887").grid(row=0, column=0, padx=10, pady=5)
tk.Label(entry_frame, text="Flavor", bg="#DEB887").grid(row=1, column=0, padx=10, pady=5)
tk.Label(entry_frame, text="Price", bg="#DEB887").grid(row=2, column=0, padx=10, pady=5)
tk.Label(entry_frame, text="Quantity", bg="#DEB887").grid(row=3, column=0, padx=10, pady=5)

name_entry = tk.Entry(entry_frame)
flavor_entry = tk.Entry(entry_frame)
price_entry = tk.Entry(entry_frame)
quantity_entry = tk.Entry(entry_frame)

name_entry.grid(row=0, column=1, padx=10, pady=5)
flavor_entry.grid(row=1, column=1, padx=10, pady=5)
price_entry.grid(row=2, column=1, padx=10, pady=5)
quantity_entry.grid(row=3, column=1, padx=10, pady=5)

# Create a frame for the buttons
button_frame = tk.Frame(root, bg="#BC8F8F", bd=2, relief=tk.RAISED)
button_frame.place(relx=0.5, rely=0.35, anchor=tk.CENTER, relwidth=0.2, height=50)

# Buttons
tk.Button(button_frame, text="Add Cake", command=add_cake).pack(padx=10, pady=5)

# Create a frame for cancel order
cancel_frame = tk.Frame(root, bg="#D2B48C", bd=2, relief=tk.RAISED)
cancel_frame.place(relx=0.5, rely=0.50, anchor=tk.CENTER, relwidth=0.4, height=120)

tk.Label(cancel_frame, text="Order ID", bg="#D2B48C").pack(padx=10, pady=5)
cancel_id_entry = tk.Entry(cancel_frame)
cancel_id_entry.pack(padx=10, pady=5)

cancel_button = tk.Button(cancel_frame, text="Cancel Order", command=cancel_order)
cancel_button.pack(pady=10)  # Added padding to separate the button from the entry field

# Create a frame for the treeview
tree_frame = tk.Frame(root, bg="#D2B48C", bd=2, relief=tk.RAISED)
tree_frame.place(relx=0.5, rely=0.80, anchor=tk.CENTER, relwidth=0.9, relheight=0.2)


# Treeview for displaying inventory
columns = ("ID", "Name", "Flavor", "Price", "Quantity", "Date Added", "Total Bill")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True)

# Load initial data
refresh_table()

root.mainloop()
