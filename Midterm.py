import csv
import expense
from expense import Expense

# Global variable to store user-defined expense categories
expense_categories = [
    "rent", "home", "groceries", "dining out",
    "clothing", "health", "transportation", "other"
]

def main() -> None:
    print("Running Expense Tracker! ")
    expense_file_path = 'expenses.csv'

    while True:
        action = input("Choose an action: [1] Add Expense [2] View Summary [3] Add Category [4] Exit: ")
        if action == '1':
            user_expense = get_user_expense()
            save_expense_to_file(user_expense, expense_file_path)
        elif action == '2':
            summarize_expenses(expense_file_path)
        elif action == '3':
            add_expense_category()
        elif action == '4':
            print("Exiting Expense Tracker.")
            break
        else:
            print("Invalid action, please try again.")

def get_user_expense() -> Expense:
    print('Getting User Expense')
    expense_name = input('Enter expense name: ')
    try:
        expense_amount = float(input('Enter expense amount: '))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return get_user_expense()

    print('Current Categories:')
    for i, category_name in enumerate(expense_categories):
        print(f" {i + 1}. {category_name}")

    while True:
        action = input("Choose a category by number or type 'new' to add a new category: ")
        if action.isdigit() and 1 <= int(action) <= len(expense_categories):
            selected_category = expense_categories[int(action) - 1]
            break
        elif action.lower() == 'new':
            selected_category = add_expense_category()
            break
        else:
            print("Invalid input. Please enter a valid number or 'new'.")

    return Expense(name=expense_name, category=selected_category, amount=expense_amount)

def add_expense_category() -> str:
    new_category = input("Enter a new expense category: ")
    if new_category and new_category not in expense_categories:
        expense_categories.append(new_category)
        print(f'Category "{new_category}" added successfully.')
        return new_category
    else:
        print("Invalid or already existing category.")
        return add_expense_category()

def save_expense_to_file(expense: Expense, expense_file_path: str) -> None:
    print(f'Saving expense: {expense.name}, {expense.amount}, {expense.category} to {expense_file_path}')
    try:
        with open(expense_file_path, 'a') as f:
            f.write(f'{expense.name}, {expense.amount}, {expense.category}')
            #writer = csv.writer(f)
            #writer.writerow([expense.name, expense.amount, expense.category])
    except IOError as e:
        print(f"Error saving to file: {e}")

def summarize_expenses(expense_file_path: str) -> None:
    print('Summarizing expenses...')
    expenses = []

    try:
        with open(expense_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for line in reader:
                if len(line) == 3:  # Ensure that each line contains three items
                    expense_name, expense_amount, expense_category = line
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

if __name__ == "__main__":
    main()


