
import tkinter as tk


from tkinter import ttk, messagebox
from supabase import create_client, Client
import bcrypt

# 🔹 Supabase connection
SUPABASE_URL = ""   # your Supabase project URL
SUPABASE_KEY = ""              # your anon key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

root = tk.Tk()
root.title("Login & Register - Supabase")
root.geometry("400x300")
root.resizable(False, False)

# 🔹 Styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("TLabel", font=("Segoe UI", 11))
style.configure("TEntry", padding=5)

def show_frame(frame):
    frame.tkraise()

# ---------------- LOGIN FRAME ----------------
login_frame = ttk.Frame(root)
login_frame.place(relwidth=1, relheight=1)

ttk.Label(login_frame, text="Login", font=("Segoe UI", 16, "bold")).pack(pady=10)

ttk.Label(login_frame, text="Username:").pack(pady=5)
login_username = ttk.Entry(login_frame)
login_username.pack()

ttk.Label(login_frame, text="Password:").pack(pady=5)
login_password = ttk.Entry(login_frame, show="*")
login_password.pack()

def login():
    global current_user
    username = login_username.get().strip()
    password = login_password.get().encode("utf-8")

    if not username or not password:
        messagebox.showwarning("Warning", "Please fill in all fields!")
        return

    result = supabase.table("users").select("*").eq("username", username).execute()
    if result.data:
        stored_hash = result.data[0]["password"].encode("utf-8")
        if bcrypt.checkpw(password, stored_hash):
            current_user = username  # store the logged-in username
            welcome_label.config(text=f"Welcome, {current_user}!")  # update label
            show_frame(home_frame)
        else:
            messagebox.showerror("Error", "Invalid username or password!")
    else:
        messagebox.showerror("Error", "Invalid username or password!")

ttk.Button(login_frame, text="Login", command=login).pack(pady=10)
ttk.Button(login_frame, text="Register", command=lambda: show_frame(register_frame)).pack()

# ---------------- REGISTER FRAME ----------------
register_frame = ttk.Frame(root)
register_frame.place(relwidth=1, relheight=1)

ttk.Label(register_frame, text="Register", font=("Segoe UI", 16, "bold")).pack(pady=10)

ttk.Label(register_frame, text="Username:").pack(pady=5)
reg_username = ttk.Entry(register_frame)
reg_username.pack()

ttk.Label(register_frame, text="Password:").pack(pady=5)
reg_password = ttk.Entry(register_frame, show="*")
reg_password.pack()

def register():
    username = reg_username.get().strip()
    password = reg_password.get().encode("utf-8")

    if not username or not password:
        messagebox.showwarning("Warning", "Please fill in all fields!")
        return

    exists = supabase.table("users").select("*").eq("username", username).execute()
    if exists.data:
        messagebox.showerror("Error", "This username is already taken!")
        return

    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
    supabase.table("users").insert({"username": username, "password": hashed}).execute()
    messagebox.showinfo("Success", "Registration complete. You can now log in.")
    show_frame(login_frame)

ttk.Button(register_frame, text="Register", command=register).pack(pady=10)
ttk.Button(register_frame, text="Back to Login", command=lambda: show_frame(login_frame)).pack()

# ---------------- HOME FRAME ----------------
home_frame = ttk.Frame(root)
home_frame.place(relwidth=1, relheight=1)

# At the top of home frame
welcome_label = ttk.Label(home_frame, text="Welcome!", font=("Segoe UI", 16, "bold"))
welcome_label.pack(pady=20)

def logout():
    show_frame(login_frame)

ttk.Button(home_frame, text="Logout", command=logout).pack(pady=20)

show_frame(login_frame)

root.mainloop()