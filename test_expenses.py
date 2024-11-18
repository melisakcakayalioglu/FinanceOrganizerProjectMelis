from expense import Expense #imports Expense class from expense.py
from Midterm import * 

# 
# https://www.w3schools.com/python/python_file_handling.asp general file interaction
# https://www.w3schools.com/python/python_file_open.asp different ways to read files
# https://www.w3schools.com/python/python_file_write.asp appending vs writing 
# 
# for exceptions: look up pytest.raises()

def test_clear_sheet():
    f = open("test_expenses.csv", "w")
    f.write("dfgh \n dfghjkl \hiaugfkbafm, \n")
    f.close()

    clear_sheet("test_expenses.csv")

    f = open("test_expenses.csv", "r")
    assert "ExpenseName,ExpenseAmount,ExpenseCategory,ExpenseDate\n" == f.read()



def test_save_expense_to_file():
    my_expense = Expense(name="bills", category="home", amount=5)
    save_expense_to_file(my_expense, "test_expenses.csv")

    f = open("test_expenses.csv", "r")

    assert f.readlines()[1] == "bills,5,home,2024/10/30\n"

    clear_sheet("test_expenses.csv")

def test_add_expense():
 
    #Test adding a new expense
  
    test_expense = Expense(name="Test Expense", category="test", amount=50.0)

    # Verify the attributes of the created expense
    assert test_expense.name == "Test Expense", "Expense name should match input."
    assert test_expense.category == "test", "Expense category should match input."
    assert test_expense.amount == 50.0, "Expense amount should match input."

    print("test_add_expense passed!")


def test_add_category():
  
    #Test adding a new category to the list of expense categories.
 
    # Resetting the categories for testing
    global expense_categories
    expense_categories = ["rent", "groceries", "health"]

    # Adding a new category
    new_category = "education"
    if new_category not in expense_categories:
        expense_categories.append(new_category)

    # Checking if the category is added
    assert "education" in expense_categories, "New category should be added to the list."

    print("test_add_category passed!")


def test_summarize_expenses():
   
    #Test summarizing expenses to ensure correct totals by category.
   
    # Create sample data
    sample_expenses = [
        Expense(name="Rent", category="rent", amount=500.0),
        Expense(name="Groceries", category="groceries", amount=150.0),
        Expense(name="Gym", category="health", amount=50.0),
        Expense(name="Dining", category="groceries", amount=100.0)
    ]

    # Summarize the expenses
    summary = {}
    for expense in sample_expenses:
        if expense.category in summary:
            summary[expense.category] += expense.amount
        else:
            summary[expense.category] = expense.amount

    # Validate summary results
    assert summary["rent"] == 500.0, "Rent total should be 500."
    assert summary["groceries"] == 250.0, "Groceries total should be 250."
    assert summary["health"] == 50.0, "Health total should be 50."

    print("test_summarize_expenses passed!")


def test_get_user_expense_direct():
    
    #Test the get_user_expense function by simulating user input directly.
    
    # Backing up the built-in input function
    original_input = __builtins__.input

    # Mocking user inputs
    mock_inputs = iter(["Test Expense", "100.0", "1"])  # Simulated inputs
    __builtins__.input = lambda _: next(mock_inputs)

    try:
        # Calling the function
        user_expense = get_user_expense()

        # Validating the returned expense
        assert user_expense.name == "Test Expense", "Expense name should match user input."
        assert user_expense.amount == 100.0, "Expense amount should match user input."
        assert user_expense.category == expense_categories[0], "Expense category should match the selected category."

        print("test_get_user_expense_direct passed!")
    finally:
        # Restoring the original input function
        __builtins__.input = original_input


def test_csv_file_operations():
 
    #Test saving an expense(or creating new sheet function)to a CSV file and reading it back.
   
    # Test file path
    test_file = "test_expenses.csv"

    # Creating a test expense
    test_expense = Expense(name="Test Expense", category="test", amount=25.0)

    # Save the expense to a CSV file
    with open(test_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            [test_expense.name, test_expense.amount, test_expense.category])

    # Reading the expense from the CSV file
    with open(test_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        lines = list(reader)

    # Validate the CSV content
    assert len(lines) == 1, "There should be one line in the file."
    assert lines[0] == ["Test Expense", "25.0",
                        "test"], "CSV content should match the saved expense."

    # Clean up test file
    os.remove(test_file)

    print("test_csv_file_operations passed!")



