import mysql.connector
import tkinter as tk
from tkinter import messagebox

my_db = connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password4341",
    database="banking_system"
)

cursor = my_db.cursor()

#allows user to look at account balance
def check_balance(account_id): 
      cursor.execute("SELECT current_balance FROM balance_info WHERE account_id = %s", (account_id,))
      result = cursor.fetchone()
      if result:
            return result[0]
      else:
            return 0.0

#allow users to deposit money
def deposit(account_id, amount): 
      n_balance = check_balance(account_id) + amount
      cursor.execute("UPDATE account_info SET account_balance = %s WHERE account_id = %s", (n_balance, account_id, ))
      cursor.execute("UPDATE balance_info SET current_balance = %s WHERE account_id = %s", (n_balance, account_id, ))
      my_db.commit()
      messagebox.showinfo("Deposit", "Deposit was successful.")

#withdrawal of money from specific account
def withdraw(account_id, amount):
      current_balance = check_balance(account_id)
      if amount > current_balance:
            messagebox.showerror("Error", "You have insufficent funds.")
      else:
            n_balance = current_balance - amount
            cursor.execute("UPDATE account_info SET account_balance = %s WHERE account_id = %s", (n_balance, account_id, ))
            cursor.execute("UPDATE balance_info SET current_balance = %s WHERE account_id = %s", (n_balance, account_id, ))
            my_db.commit()
            messagebox.showinfo("Withdrawl", "The withdrawl was successful.")

#account_id will be created automatically but takes in other information to add account to database
def add_account(name, password, DOB, p_number, start_balance):
      cursor.execute("INSERT INTO account_info (name, password, date_of_birth, phone_number, account_balance) VALUES(%s, %s, %s, %s, %s)", (name, password, DOB, p_number, start_balance))
      account_id = cursor.lastrowid
      cursor.execute("INSERT INTO balance_info (account_id, current_balance) VALUES(%s, %s)", (account_id, start_balance))
      my_db.commit()
      messagebox.showinfo("Account Creation", "The account has been created.")

#delete account based on the account's id
def delete_account(account_id):
      cursor.execute("DELETE FROM account_info WHERE account_id = %s", (account_id,))
      cursor.execute("DELETE FROM balance_info WHERE account_id = %s", (account_id, ))
      my_db.commit()
      messagebox.showinfo("Account Deletion", "The account has been deleted.")


#gives the user a chance to change the specifics of their account
def change_account(account_id, name=None, password=None, date_of_birth=None, phone_number=None):
      updates = []
      if name:
        updates.append(("name", name))
      if password:
            updates.append(("password", password))
      if DOB:
            updates.append(("date_of_birth", DOB))
      if phone_number:
            updates.append(("phone_number", phone_number))
      #helps in actually updating the given information into the database
      if updates:
            update_query = ", ".join([f"{col} = %s" for col, _ in updates])
            values = [val for _, val in updates]
            values.append(account_id)
            cursor.execute(f"UPDATE account_info SET {update_query} WHERE account_id = %s", values)
            my_db.commit()
            messagebox.showinfo("Account Update", "Account details updated successfully.")


#visuals for the user interface of the banking system's menu
def display_menu(root):
    root.geometry("400x300")
    root.title("C2C Banking System Menu")

    account_id_label = tk.Label(root, text="Enter Account ID:")
    account_id_label.pack(pady=10)
    account_id_entry = tk.Entry(root, width=30)
    account_id_entry.pack(pady=5)

    amount_label = tk.Label(root, text="Enter Amount:")
    amount_label.pack(pady=10)
    amount_entry = tk.Entry(root, width=30)
    amount_entry.pack(pady=5)

    def check_balance_command():
        account_id = int(account_id_entry.get())
        messagebox.showinfo("Balance", f"Current balance: ${check_balance(account_id)}")

    check_balance_btn = tk.Button(root, text="Check Balance", command=check_balance_command)
    check_balance_btn.pack(pady=10)

    def deposit_command():
        account_id = int(account_id_entry.get())
        amount = float(amount_entry.get())
        deposit(account_id, amount)

    deposit_btn = tk.Button(root, text="Deposit Funds", command=deposit_command)
    deposit_btn.pack(pady=10)

    def withdraw_command():
        account_id = int(account_id_entry.get())
        amount = float(amount_entry.get())
        withdraw(account_id, amount)

    withdraw_btn = tk.Button(root, text="Withdraw Funds", command=withdraw_command)
    withdraw_btn.pack(pady=10)

    def add_account_command():
        name = name_entry.get()
        password = password_entry.get()
        dob = dob_entry.get()
        phone_number = phone_entry.get()
        start_balance = float(balance_entry.get())
        add_account(name, password, dob, phone_number, start_balance)

    name_label = tk.Label(root, text="Name:")
    name_label.pack(pady=10)
    name_entry = tk.Entry(root, width=30)
    name_entry.pack(pady=5)

    password_label = tk.Label(root, text="Password:")
    password_label.pack(pady=10)
    password_entry = tk.Entry(root, width=30)
    password_entry.pack(pady=5)

    dob_label = tk.Label(root, text="Date of Birth (YYYY-MM-DD):")
    dob_label.pack(pady=10)
    dob_entry = tk.Entry(root, width=30)
    dob_entry.pack(pady=5)

    phone_label = tk.Label(root, text="Phone Number:")
    phone_label.pack(pady=10)
    phone_entry = tk.Entry(root, width=30)
    phone_entry.pack(pady=5)

    balance_label = tk.Label(root, text="Starting Balance:")
    balance_label.pack(pady=10)
    balance_entry = tk.Entry(root, width=30)
    balance_entry.pack(pady=5)

    add_account_btn = tk.Button(root, text="Add Account", command=add_account_command)
    add_account_btn.pack(pady=10)

    def delete_account_command():
        account_id = int(account_id_entry.get())
        delete_account(account_id)

    delete_account_btn = tk.Button(root, text="Delete Account", command=delete_account_command)
    delete_account_btn.pack(pady=10)

    def change_account_command():
        account_id = int(account_id_entry.get())
        change_account(account_id, name_entry.get(), password_entry.get(), dob_entry.get(), phone_entry.get())

    change_account_btn = tk.Button(root, text="Change Account Details", command=change_account_command)
    change_account_btn.pack(pady=10)

    exit_btn = tk.Button(root, text="Exit", command=root.destroy)
    exit_btn.pack(pady=0)

    root.mainloop()

#implements both the functionality and visuals of the C2C program 
def main():
    root = tk.Tk()
    display_menu(root)

                                   
if __name__ == "__main__":
    main()

#closes connection to database
cursor.close()
my_db.close()
            