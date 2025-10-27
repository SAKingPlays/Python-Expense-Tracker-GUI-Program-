import customtkinter as ctk
from tkinter import messagebox, filedialog
import csv
from datetime import datetime

# Expense data storage
expenses = []

# Categories
CATEGORIES = ["Food", "Transport", "Bills", "Entertainment", "Other"]

# Initialize theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ExpenseTracker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Professional Expense Tracker")
        self.geometry("800x600")
        
        # Gradient background frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="💰 Expense Tracker",
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=10)

        # Input fields frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(fill="x", pady=10, padx=20)

        self.title_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Title")
        self.title_entry.grid(row=0, column=0, padx=5, pady=5)

        self.amount_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Amount")
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        self.category_option = ctk.CTkOptionMenu(self.input_frame, values=CATEGORIES)
        self.category_option.grid(row=0, column=2, padx=5, pady=5)

        self.date_entry = ctk.CTkEntry(self.input_frame, placeholder_text="YYYY-MM-DD")
        self.date_entry.grid(row=0, column=3, padx=5, pady=5)

        self.add_btn = ctk.CTkButton(self.input_frame, text="Add Expense", command=self.add_expense)
        self.add_btn.grid(row=0, column=4, padx=5, pady=5)

        # Expense listbox
        self.expense_list = ctk.CTkTextbox(self.main_frame, width=750, height=250)
        self.expense_list.pack(pady=10)

        # Summary
        self.summary_label = ctk.CTkLabel(self.main_frame, text="Total: $0.00", font=("Arial", 20, "bold"))
        self.summary_label.pack(pady=10)

        # Bottom buttons
        self.btn_frame = ctk.CTkFrame(self.main_frame)
        self.btn_frame.pack(pady=10)

        self.delete_btn = ctk.CTkButton(self.btn_frame, text="Delete Selected", command=self.delete_expense)
        self.delete_btn.grid(row=0, column=0, padx=5)

        self.save_btn = ctk.CTkButton(self.btn_frame, text="Save CSV", command=self.save_csv)
        self.save_btn.grid(row=0, column=1, padx=5)

        self.load_btn = ctk.CTkButton(self.btn_frame, text="Load CSV", command=self.load_csv)
        self.load_btn.grid(row=0, column=2, padx=5)

    def add_expense(self):
        title = self.title_entry.get()
        amount = self.amount_entry.get()
        category = self.category_option.get()
        date = self.date_entry.get() or datetime.today().strftime("%Y-%m-%d")

        if not title or not amount:
            messagebox.showwarning("Error", "Please enter title and amount.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Error", "Invalid amount.")
            return

        expense = {"title": title, "amount": amount, "category": category, "date": date}
        expenses.append(expense)
        self.refresh_list()

        # Clear fields
        self.title_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.date_entry.delete(0, "end")

    def refresh_list(self):
        self.expense_list.delete("1.0", "end")
        total = 0
        for i, exp in enumerate(expenses, start=1):
            self.expense_list.insert("end", f"{i}. {exp['title']} | ${exp['amount']:.2f} | {exp['category']} | {exp['date']}\n")
            total += exp["amount"]
        self.summary_label.configure(text=f"Total: ${total:.2f}")

    def delete_expense(self):
        try:
            selected = self.expense_list.get("sel.first", "sel.last")
            index = int(selected.split(".")[0]) - 1
            if 0 <= index < len(expenses):
                expenses.pop(index)
                self.refresh_list()
        except Exception:
            messagebox.showwarning("Error", "Select an expense to delete.")

    def save_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files","*.csv")])
        if file:
            with open(file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["title","amount","category","date"])
                writer.writeheader()
                writer.writerows(expenses)
            messagebox.showinfo("Saved", f"Expenses saved to {file}")

    def load_csv(self):
        file = filedialog.askopenfilename(filetypes=[("CSV Files","*.csv")])
        if file:
            with open(file, "r") as f:
                reader = csv.DictReader(f)
                expenses.clear()
                for row in reader:
                    expenses.append({
                        "title": row["title"],
                        "amount": float(row["amount"]),
                        "category": row["category"],
                        "date": row["date"]
                    })
            self.refresh_list()

if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()
