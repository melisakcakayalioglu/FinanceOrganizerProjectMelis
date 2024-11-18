import csv # this allows us to read and write on the csv (comma seperated values) file
import os # imports os library for managing files in the operating system
from datetime import datetime # allows work with date and time functions
from expense import Expense #imports Expense class from expense.py

# Global variable to store user-defined expense categories
expense_categories = [
    "rent", "home", "groceries", "dining out",
    "clothing", "health", "transportation", "other"
]

def main() -> None:
    print("Running Expense Tracker!")
    expense_file_path = 'expenses.csv' # sets a variable for the file path where expenses will be stored

    while True: # infinite loop until the user responds / gives users an option to choose an action by typing a number from 1 to 6
        action = input("Choose an action: [1] Add Expense [2] View Summary [3] Add Category [4] Clear Sheet [5] New Sheet [6] Exit: ")
        if action == '1': # if the number 1 is typed, the code inside this if block will run
            user_expense = get_user_expense()
            save_expense_to_file(user_expense, expense_file_path) # user_expense includes the expense data, expense_file_path specifies the file to save it in
        elif action == '2':
            summarize_expenses(expense_file_path)
        elif action == '3':
            add_expense_category()
        elif action == '4': # calls a function to delete all expenses in expenses.csv
            clear_sheet(expense_file_path)
        elif action == '5':
            expense_file_path = create_new_sheet() #creates a new CSV file
        elif action == '6':
            print("Exiting Expense Tracker.")
            break
        else: #if the input does not match numbers between 1 to 6, then it will give this message
            print("Invalid action, please try again.")

def get_user_expense() -> Expense: # to define a function named get_user_expense that returns an Expense object
    print('Getting User Expense')
    expense_name = input('Enter expense name: ')
    try: # code that may contain an error (if anything besides a number is entered)
        expense_amount = float(input('Enter expense amount: ')) # float will convert the user expense amount into decimals
    except ValueError: # code that handles error
        print("Invalid amount. Please enter a number.") # If a user enters a text instead of a number, this message is printed
        return get_user_expense() # function will restart

    print('Current Categories:')
    for i, category_name in enumerate(expense_categories): # for loop to go through each category in expense_categories
        print(f" {i + 1}. {category_name}")

    while True: # loop that keeps asking user to pick a category until they enter a correct response
        action = input("Choose a category by number or type 'new' to add a new category: ")
        if action.isdigit() and 1 <= int(action) <= len(expense_categories): # makes sure users typed a number in the given range
            selected_category = expense_categories[int(action) - 1] # selected category is saved
            break
        elif action.lower() == 'new': # if the users typed 'new', it calls add_expense_category() to add a new category
            selected_category = add_expense_category()
            break
        else: # If the user does not matches the options above
            print("Invalid input. Please enter a valid number or 'new'.")

    return Expense(name=expense_name, category=selected_category, amount=expense_amount) # creates and returns an Expense object with the name, category, amount.

def add_expense_category() -> str:
    new_category = input("Enter a new expense category: ")
    if new_category and new_category not in expense_categories: # cheks if it is a new and valid category
        expense_categories.append(new_category) # adds the new category to our list
        print(f'Category "{new_category}" added successfully.')
        return new_category # If the user input already exists or it is blank
    else:
        print("Invalid or already existing category.")
        return add_expense_category()

def save_expense_to_file(expense: Expense, expense_file_path: str) -> None:
    # Check if the file exists and is not empty to add header if needed
    file_exists = os.path.isfile(expense_file_path) and os.path.getsize(expense_file_path) > 0

    # Get the current date in yyyy/mm/dd format
    current_date = datetime.now().strftime("%Y/%m/%d")

    print(f'Saving expense: {expense.name}, {expense.amount}, {expense.category}, {current_date} to {expense_file_path}')
    try:
        with open(expense_file_path, 'a', newline='') as f: # Append for adding data without deleting the old ones
            writer = csv.writer(f)
            # Write header if file does not exist or is empty
            if not file_exists:
                writer.writerow(['ExpenseName', 'ExpenseAmount', 'ExpenseCategory', 'ExpenseDate'])
            # Write the expense details with the current date
            writer.writerow([expense.name, expense.amount, expense.category, current_date])
    except IOError as e:
        print(f"Error saving to file: {e}")

def summarize_expenses(expense_file_path: str) -> None:
    print('Summarizing expenses...')
    expenses = []

    try:
        with open(expense_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header row
            for line in reader:
                if len(line) == 4:  # Ensure each line has four items
                    expense_name, expense_amount, expense_category, expense_date = line
                    try:
                        line_expense = Expense(
                            name=expense_name,
                            amount=float(expense_amount),
                            category=expense_category,
                        )
                        expenses.append(line_expense)
                    except ValueError:
                        print(f"Skipping invalid data: {line}")
    except FileNotFoundError:
        print('No expenses recorded yet.')
        return
    except IOError as e:
        print(f"Error reading file: {e}")
        return

    # Summarize by category
    amount_by_category = {}
    for exp in expenses:
        if exp.category in amount_by_category:
            amount_by_category[exp.category] += exp.amount
        else:
            amount_by_category[exp.category] = exp.amount

    print("Expenses by category:")
    for key, amount in amount_by_category.items():
        print(f"{key}: ${amount:.2f}")

    total_spent = sum(exp.amount for exp in expenses)
    print(f'Total spent: ${total_spent:.2f}')


def clear_sheet(expense_file_path: str) -> None:
    # Clears all data in the specified CSV file, keeping only the header.
    try:
        with open(expense_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ExpenseName', 'ExpenseAmount', 'ExpenseCategory', 'ExpenseDate'])
        print("Sheet cleared successfully.")
    except IOError as e:
        print(f"qsheet: {e}")

def create_new_sheet() -> str:
    # Creates a new CSV file (sheet) with the required header structure.
    new_sheet_name = input("Enter a name for the new sheet (e.g., 'expenses_may.csv'): ")
    try:
        with open(new_sheet_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ExpenseName', 'ExpenseAmount', 'ExpenseCategory', 'ExpenseDate'])
        print(f"New sheet '{new_sheet_name}' created successfully.")
    except IOError as e:
        print(f"Error creating new sheet: {e}")
        return 'expenses.csv'  # Default to main sheet if creation fails
    return new_sheet_name



if __name__ == "__main__":
    main()
