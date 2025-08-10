#Welcome to my Daily Expense Tracker!
print("Welcome to the Daily Expense Tracker!")
# This program allows users to track their daily expenses, view them, calculate totals and averages, and clear the list of expenses.
print("Menu:"
      "\n1. Add a new Expense"
      "\n2. View all Expenses"
      "\n3. Calculate Total and Average Expense"
      "\n4. Clear all Expenses"
      "\n5. Exit")
# Initialize an empty list to store expenses
Expenses_List = []
# The user can choose an option from the menu
while True:
    choice = input("Enter your choice (1-5): ")
    # Choice 1 allows the user to add a new expense
    if choice == '1':
        Expense = float(input("Enter the expense amount: "))
        Note = input("Enter a small remainder for this transaction: ")
        Expenses_List.append(Expense)
    # Choice 2 allows the user to view all recorded expenses
    elif choice == '2':
        if len(Expenses_List) == 0:
            print("No expenses recorded yet.")
        else:
            print("Your Expenses:")
            for i, expense in enumerate(Expenses_List, start=1):
                print(f"{i}. {expense}")
    # Choice 3 calculates the total and average of the expenses
    elif choice == '3':
        if len(Expenses_List) == 0:
            print("No expenses to calculate the total and average.")
        else:
            Total_Expenses = sum(Expenses_List)
            Average_Expense = Total_Expenses / len(Expenses_List)
            print(f"Total Expense: {Total_Expenses:.2f}")
            print(f"Average Expense: {Average_Expense:.2f}")
    # Choice 4 clears all recorded expenses
    elif choice == '4':
        Expenses_List.clear()
        print("All expenses cleared.")
    # Choice 5 exits the program
    elif choice == '5':
        print("Exiting the Daily Expense Tracker. Thank you!")
        break
    # The user need to enter a valid choice i.e., a number between 1 and 5
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")