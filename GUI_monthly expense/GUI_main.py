import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import file_manager
import pandas as pd
from PIL import Image, ImageTk 
import os 

# ------------- Window ----------
root = tk.Tk()
root.title("✨ Monthly Expense Tracker ✨")
root.state('zoomed') 

bg = "#f7f6ff"        
card_bg = "#ffffff"
accent = "#6C5CE7"    
muted = "#6b6b6b"
ok_color = "#00b894"
warn_color = "#fdcb6e"

# Global variable to hold the background image reference
background_photo = None
background_label = None


# ttk styling
style = ttk.Style(root)
style.theme_use("default")
style.configure("TButton", font=("Inter", 11, "bold"), padding=8)
style.configure("TLabel", font=("Inter", 11))
style.configure("Header.TLabel", font=("Inter", 18, "bold"), foreground=accent)
style.configure("Small.TLabel", font=("Inter", 9), foreground=muted)


# Emerald button style
def emerald_button(parent, text, command=None, width=None, pady=6, padx=6):
    btn = tk.Button(
        parent,
        text=text,
        fg="#F4F5F4",               
        bg="#387646",                 
        activebackground="#387646",
        activeforeground="#50C878",
        highlightbackground="#50C878",
        highlightcolor="#50C878",
        highlightthickness=4,      
        bd=1,                        
        width=width,
        font=("Inter", 14, "bold"),  
        command=command
    )
    btn.pack(padx=padx, pady=pady)
    return btn

def clear_frame():
    for w in root.winfo_children():
        w.destroy()
    global background_label
    if background_label:
        background_label.destroy()
        background_label = None

# ---------------- Background Setup ----------------
def setup_background(image_path="background.png"):
    global background_photo, background_label
    
    root.update()
    screen_width = root.winfo_width()
    screen_height = root.winfo_height()
    
    # Construct the absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_image_path = os.path.join(script_dir, image_path)
    
    try:
        # 1. Load the image using PIL
        img = Image.open(full_image_path) 
        
        # 2. Resize the image to fit the current maximized window size
        img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        
        # 3. Convert the PIL image to a Tkinter PhotoImage object
        background_photo = ImageTk.PhotoImage(img)
        
        # 4. Create a Label to display the image
        background_label = tk.Label(root, image=background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        return background_label
        
    except FileNotFoundError:
        print(f"Error: Background image not found at '{full_image_path}'. Using default color.")
        return root 
    except Exception as e:
        print(f"An error occurred loading the background image: {e}. Using default color.")
        return root 


# ---------------- Home ----------------
def home_screen():
    clear_frame()
    
    bg_parent = setup_background("background.png") 

    btn_container = tk.Frame(bg_parent, bg='')
    btn_container.place(relx=0.35, rely=0.45, anchor="center") 
    
    btn_frame = tk.Frame(btn_container, bg='') 
    btn_frame.pack()

    # Buttons remain white/emerald to contrast the dark green background
    emerald_button(btn_frame, text="➕ Add Expense", command=add_menu_screen, width=28, pady=4, padx=4)
    emerald_button(btn_frame, text="📦 Add from Frequent", command=add_from_frequent_screen, width=28, pady=4, padx=4)
    emerald_button(btn_frame, text="📄 View Expenses", command=view_menu_screen, width=28, padx=8, pady=8)
    emerald_button(btn_frame, text="📈 Reports", command=reports_screen, width=28, padx=8, pady=8)


# ---------------- Add Menu ----------
def add_menu_screen():
    clear_frame()
    bg_parent = setup_background("background.png") 
    
    frame = tk.Frame(bg_parent, bg='') 
    frame.place(relx=0.35, rely=0.45, anchor="center")

    card = tk.Frame(frame, bg='')
    card.pack(padx=10, pady=10)

    emerald_button(frame, text="Add New Expense", command=add_expense_screen, width=28).pack(pady=8)
    ttk.Button(frame, text="⬅ Back", command=home_screen, width=20).pack(pady=12)


# ---------------- Add New Expense Screen ----------------
def add_expense_screen():
    clear_frame()
    bg_parent = setup_background("background.png") 
    
    frame = tk.Frame(bg_parent, bg='', padx=18, pady=18)
    frame.place(relx=0.35, rely=0.42, anchor="center")

    ttk.Label(frame, text="Add New Expense", style="Header.TLabel", background="#387646", foreground='#FFFFFF').pack(pady=4)

    form = tk.Frame(frame, bg='', padx=12, pady=8)
    form.pack(padx=10, pady=6)

    tk.Label(form, text="Category:", bg=card_bg).grid(row=0, column=0, sticky="w", pady=4)
    cat_entry = tk.Entry(form, width=36)
    cat_entry.grid(row=0, column=1, pady=4)

    tk.Label(form, text="Description:", bg=card_bg).grid(row=1, column=0, sticky="w", pady=4)
    desc_entry = tk.Entry(form, width=36)
    desc_entry.grid(row=1, column=1, pady=4)

    tk.Label(form, text="Amount (₹):", bg=card_bg).grid(row=2, column=0, sticky="w", pady=4)
    amt_entry = tk.Entry(form, width=36)
    amt_entry.grid(row=2, column=1, pady=4)

    use_today_var = tk.BooleanVar(value=True)
    tk.Checkbutton(form, text="Use today's date", variable=use_today_var, bg=card_bg).grid(row=3, column=1, sticky="w", pady=4)

    tk.Label(form, text="Not today? enter date:", bg=card_bg).grid(row=4, column=0, sticky="w", padx=6, pady=2)
    date_entry = tk.Entry(form, width=36)
    date_entry.insert(0, "DD/MM/YYYY")
    date_entry.grid(row=4, column=1, pady=4)

    def do_save():
        category = cat_entry.get().strip()
        description = desc_entry.get().strip()
        amt = amt_entry.get().strip()
        if not category or not description or not amt:
            messagebox.showerror("Invalid", "Please fill all fields")
            return
        try:
            amount = int(amt)
        except:
            messagebox.showerror("Invalid", "Amount must be a number")
            return

        if use_today_var.get():
            expense_date = date.today().strftime("%d-%b-%Y")
        else:
            raw = date_entry.get().strip()
            try:
                dd, mm, yyyy = raw.split("/")
                mm = int(mm); dd = int(dd); yyyy = int(yyyy)
                month_name = date(yyyy, mm, dd).strftime("%b")
                expense_date = f"{dd:02d}-{month_name}-{yyyy}"
            except Exception:
                messagebox.showerror("Invalid", "Date format should be DD/MM/YYYY")
                return

        # write and update frequent
        file_manager.write_to_current_csv(expense_date, category, description, amount)
        # build month_year
        _, mon, yr = expense_date.split("-")
        month_year = mon + yr
        month_df = file_manager.read_from_given_month(month_year)
        file_manager.write_to_freq_csv(category, description, amount, month_df)

        messagebox.showinfo("Saved", "Expense saved successfully")
        home_screen()

    emerald_button(frame, text="Save Expense", command=do_save, width=24).pack(pady=4)
    ttk.Button(frame, text="⬅ Back", command=add_menu_screen, width=10).pack(pady=2)


# ------------- Add From Frequent Screen -------------
def add_from_frequent_screen():
    clear_frame()
    bg_parent = setup_background("background.png") 
    
    frame = tk.Frame(bg_parent, bg='', padx=14, pady=14, width=200)
    frame.place(relx=0.35, rely=0.42, anchor="center")

    ttk.Label(frame, text="Add from Frequently Bought", style="Header.TLabel", background="#387646", foreground='#FFFFFF').grid(row=0, column=0, columnspan=2, pady=4)

    try:
        freq_df = file_manager.read_from_freq_csv()
    except Exception:
        freq_df = pd.DataFrame()

    if freq_df is None or freq_df.empty:
        tk.Label(frame, text="No frequent items found.", bg="#387646", fg="#FFFFFF").grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="⬅ Back", command=home_screen).grid(row=2, column=0, columnspan=2, pady=12)
        return

    listbox = tk.Listbox(frame, width=60, height=8)
    listbox.grid(row=1, column=0, columnspan=2, pady=6) 
    for idx, row in freq_df.iterrows():
        listbox.insert(tk.END, f"{idx+1}. {row['description']} ({row['category']}) - ₹{row.get('amount','')}")

    tk.Label(frame, text="Amount (or leave empty to use stored):", bg=card_bg).grid(row=2, column=0, sticky='w', pady=(8, 3))
    amt_entry = tk.Entry(frame, width=20)
    amt_entry.grid(row=2, column=1, padx=2, pady=3)

    use_today_var = tk.BooleanVar(value=True)
    tk.Checkbutton(frame, text="Use today's date", variable=use_today_var, bg=card_bg).grid(row=3, column=0, sticky='w', padx=2, pady=3) # sticky='w' for alignment
    date_entry = tk.Entry(frame, width=20)
    date_entry.insert(0, "DD/MM/YYYY")
    date_entry.grid(row=3, column=1, padx=2, pady=3)

    def add_selected():
        sel = listbox.curselection()
        if not sel:
            messagebox.showerror("Select", "Please select an item")
            return
        idx = sel[0]
        item = freq_df.iloc[idx]
        category = item["category"]
        description = item["description"]
        stored_amount = item.get("amount", None)
        amt_text = amt_entry.get().strip()
        if amt_text:
            try:
                amount = int(amt_text)
            except:
                messagebox.showerror("Invalid", "Amount must be a number")
                return
        else:
            try:
                amount = int(stored_amount)
            except:
                messagebox.showerror("Invalid", "No amount provided")
                return

        if use_today_var.get():
            expense_date = date.today().strftime("%d-%b-%Y")
        else:
            raw = date_entry.get().strip()
            try:
                dd, mm, yyyy = raw.split("/")
                month_name = date(int(yyyy), int(mm), int(dd)).strftime("%b")
                expense_date = f"{int(dd):02d}-{month_name}-{yyyy}"
            except Exception:
                messagebox.showerror("Invalid", "Date format should be DD/MM/YYYY")
                return

        file_manager.write_to_current_csv(expense_date, category, description, amount)
        _, mon, yr = expense_date.split("-")
        month_year = mon + yr
        df = file_manager.read_from_given_month(month_year)
        file_manager.write_to_freq_csv(category, description, amount, df)
        messagebox.showinfo("Added", f"Added {description} to {month_year}")
        home_screen()
 
    ttk.Button(frame, text="Add Selected", command=add_selected, width=20).grid(row=4, column=0, columnspan=2, pady=6)
    
    ttk.Button(frame, text="⬅ Back", command=home_screen).grid(row=5, column=0, columnspan=2, pady=4)

#------------- View Menu -------------
def view_menu_screen():
    clear_frame()
    bg_parent = setup_background("background.png") 
    
    # Frame for the entire view menu block
    frame = tk.Frame(bg_parent, bg='')
    frame.place(relx=0.35, rely=0.42, anchor="center")

    btn_frame = tk.Frame(frame, bg='')
    btn_frame.pack(pady=6)

    emerald_button(btn_frame, text="View by Month", command=view_by_month_screen, width=25).pack(pady=4)
    emerald_button(btn_frame, text="Search by Date", command=view_by_date_screen, width=25).pack(pady=4)
    emerald_button(btn_frame, text="Search by Category", command=view_by_category_screen, width=25).pack(pady=4)
    emerald_button(btn_frame, text="Most Frequent this Month", command=show_most_frequent_this_month, width=25).pack(pady=4)

    ttk.Button(frame, text="⬅ Back", command=home_screen).pack(pady=6)


# ------------- View by Month -------------
def view_by_month_screen():
    clear_frame()
    bg_parent = setup_background("background.png") 
    
    frame = tk.Frame(bg_parent, bg='', padx=12, pady=12)
    frame.place(relx=0.35, rely=0.45, anchor="center")

    ttk.Label(frame, text="View by Month", style="Header.TLabel", background="#387646", foreground='#FFFFFF').pack(pady=8)

    month_entry = tk.Entry(frame, width=8); month_entry.insert(0, date.today().strftime("%b").upper())
    month_entry.pack(pady=6)
    year_entry = tk.Entry(frame, width=8); year_entry.insert(0, date.today().strftime("%Y"))
    year_entry.pack(pady=6)

    def load():
        month_year = month_entry.get().upper() + year_entry.get()
        df = file_manager.read_from_given_month(month_year)
        display_df_table(df, title=f"Data for {month_year}")

    emerald_button(frame, text="Load", command=load, width=10).pack(pady=8)
    ttk.Button(frame, text="⬅ Back", command=view_menu_screen).pack(pady=6)


# ------------- View by Date -------------
def view_by_date_screen():
    clear_frame()
    bg_parent = setup_background("background.png") 
    
    frame = tk.Frame(bg_parent, bg='', padx=12, pady=12)
    frame.place(relx=0.35, rely=0.45, anchor="center")

    ttk.Label(frame, text="Search by Date (day)", style="Header.TLabel", background="#387646", foreground='#FFFFFF').pack(pady=8)
    day_entry = tk.Entry(frame, width=8); day_entry.insert(0, "03")
    day_entry.pack(pady=6)

    month_entry = tk.Entry(frame, width=8); month_entry.insert(0, date.today().strftime("%b").upper())
    month_entry.pack(pady=6)
    year_entry = tk.Entry(frame, width=8); year_entry.insert(0, date.today().strftime("%Y"))
    year_entry.pack(pady=6)

    def load():
        day = day_entry.get().zfill(2)
        month_year = month_entry.get().upper() + year_entry.get()
        df = file_manager.read_from_given_month(month_year)
        if df.empty:
            messagebox.showinfo("No data", "No data for this month")
            return
        df["day"] = df["date"].str.split("-").str[0]
        out = df[df["day"] == day]
        display_df_table(out, title=f"Data for {day}-{month_year}")

    emerald_button(frame, text="Search", command=load, width=20).pack(pady=8)
    ttk.Button(frame, text="⬅ Back", command=view_menu_screen).pack(pady=6)


# ------------- View by Category -------------
def view_by_category_screen():
    clear_frame()
    bg_parent = setup_background("background.png") 
    
    frame = tk.Frame(bg_parent, bg='', padx=12, pady=12)
    frame.place(relx=0.35, rely=0.45, anchor="center")

    ttk.Label(frame, text="Search by Category", style="Header.TLabel", background="#387646", foreground='#FFFFFF').pack(pady=8)
    month_entry = tk.Entry(frame, width=10); month_entry.insert(0, date.today().strftime("%b").upper())
    month_entry.pack(pady=6)
    year_entry = tk.Entry(frame, width=10); year_entry.insert(0, date.today().strftime("%Y"))
    year_entry.pack(pady=6)
    cat_entry = tk.Entry(frame, width=10); cat_entry.insert(0, "category")
    cat_entry.pack(pady=6)

    def load():
        month_year = month_entry.get().upper() + year_entry.get()
        df = file_manager.read_from_given_month(month_year)
        if df.empty:
            messagebox.showinfo("No data", "No data for this month")
            return
        out = df[df["category"].str.lower() == cat_entry.get().strip().lower()]
        display_df_table(out, title=f"Category results for {month_year}")

    emerald_button(frame, text="Search", command=load, width=20).pack(pady=8)
    ttk.Button(frame, text="⬅ Back", command=view_menu_screen).pack(pady=6)


# ------------- Most frequent this month -------------
def show_most_frequent_this_month():
    today = date.today()
    month_year = today.strftime("%b").upper() + today.strftime("%Y")
    df = file_manager.read_from_given_month(month_year)
    if df.empty:
        messagebox.showinfo("No data", "No data for this month")
        return
    try:
        item_counts = df["description"].value_counts()
        most_item = item_counts.idxmax()
        count = item_counts.max()
        messagebox.showinfo("Most frequent", f"{most_item}\nBought {count} times this month")
    except Exception:
        messagebox.showerror("Error", "Could not compute frequent item.")


# ------------- small table display helper -------------
def display_df_table(df, title="Results"):
    clear_frame()
    bg_parent = setup_background("background.png") 
    
    frame = tk.Frame(bg_parent, bg='', padx=12, pady=12)
    frame.place(relx=0.34, rely=0.42, anchor="center")

    ttk.Label(frame, text=title, style="Header.TLabel", background="#387646", foreground='#FFFFFF').pack(pady=8)

    if df.empty:
        tk.Label(frame, text="No records found.", bg=card_bg).pack(pady=8)
    else:
        cols = list(df.columns)
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c.title())
            tree.column(c, width=100, anchor="center")
        for _, row in df.iterrows():
            values = [row[c] for c in cols]
            tree.insert("", tk.END, values=values)
        tree.pack(expand=True, fill="both", padx=6, pady=4)

    ttk.Button(frame, text="⬅ Back", command=view_menu_screen).pack(pady=6)
    


# ------------- Reports (White background maintained for readability) -------------
def reports_screen():
    clear_frame()
    bg_parent = setup_background("background.png") 
    
    frame = tk.Frame(bg_parent, bg='#387646', padx=12, pady=12)
    frame.place(relx=0.35, rely=0.45, anchor="center")
    
    ttk.Label(frame, text="Reports", style="Header.TLabel", foreground="#FFFFFF", background="#387646").pack(pady=8)
    ttk.Label(frame, text="Total spend this month:", foreground='#FFFFFF', background="#387646").pack(pady=8)

    today = date.today()
    month_year = today.strftime("%b").upper() + today.strftime("%Y")
    df = file_manager.read_from_given_month(month_year)
    total = 0
    if not df.empty:
        total = df["amount"].sum()
    ttk.Label(frame, text=f"₹ {total}", font=("Inter", 16, "bold"), foreground="#FFFFFF", background="#387646").pack(pady=6)

    ttk.Button(frame, text="⬅ Back", command=home_screen).pack(pady=10)


# --------------------------- start ---------------------------
home_screen()
root.mainloop()