import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime

db = sqlite3.connect("gas_bookings.db")
cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        status TEXT NOT NULL,
        booking_date TEXT NOT NULL
    )
""")
db.commit()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

def add_booking():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()
    qty = entry_qty.get()
    status = status_var.get()
    booking_date = datetime.now().strftime("%Y-%m-%d")

    if not name or not phone or not email or not address or not qty:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    try:
        qty_int = int(qty)
        if qty_int <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Input Error", "Quantity must be a positive number.")
        return

    cursor.execute(
        "INSERT INTO bookings (customer_name, phone, email, address, quantity, status, booking_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, phone, email, address, qty_int, status, booking_date)
    )
    db.commit()

    entry_name.delete(0, ctk.END)
    entry_phone.delete(0, ctk.END)
    entry_email.delete(0, ctk.END)
    entry_address.delete(0, ctk.END)
    entry_qty.delete(0, ctk.END)
    status_var.set("Pending")

    show_bookings()

def show_bookings():
    textbox.configure(state="normal")
    textbox.delete("1.0", ctk.END)

    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()
    for b in rows:
        textbox.insert(
            ctk.END,
            f"ID: {b[0]} | Name: {b[1]} | Phone: {b[2]} | Email: {b[3]} | Address: {b[4]} | Qty: {b[5]} | Status: {b[6]} | Date: {b[7]}\n"
        )

    textbox.configure(state="disabled")

def on_closing():
    db.close()
    root.destroy()

root = ctk.CTk()
root.title("🛢️ Gas Cylinder Booking System")
root.geometry("700x800")

title_label = ctk.CTkLabel(root, text="Gas Booking System", font=ctk.CTkFont(size=24, weight="bold"))
title_label.pack(pady=20)

entry_width = 500

entry_name = ctk.CTkEntry(root, placeholder_text="Customer Name", width=entry_width)
entry_name.pack(pady=10)

entry_phone = ctk.CTkEntry(root, placeholder_text="Phone Number", width=entry_width)
entry_phone.pack(pady=10)

entry_email = ctk.CTkEntry(root, placeholder_text="Email ID", width=entry_width)
entry_email.pack(pady=10)

entry_address = ctk.CTkEntry(root, placeholder_text="Address", width=entry_width)
entry_address.pack(pady=10)

entry_qty = ctk.CTkEntry(root, placeholder_text="Quantity (No. of Cylinders)", width=entry_width)
entry_qty.pack(pady=10)

status_var = ctk.StringVar(value="Pending")
status_menu = ctk.CTkOptionMenu(root, variable=status_var, values=["Pending", "Delivered", "Cancelled"], width=200)
status_menu.pack(pady=10)

add_btn = ctk.CTkButton(root, text="Add Booking", command=add_booking)
add_btn.pack(pady=20)

textbox = ctk.CTkTextbox(root, width=650, height=400)
textbox.pack(pady=10)

show_bookings()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
