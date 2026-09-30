# expense_tracker
The Following Repo is about my Academic Project on a simple programme which can be used to track your monthly expenses in detail with options to preceisely log how and when the Expense was made. The Programme Is Built Entirely using Python and runs inside the terminal itself. GUI and cool stuff not learned yet :/ 



## What you need

Python 3.6 or newer. Nothing else has to be installed.


## How to run it

Put the file expense_tracker.py in a folder, open a terminal in that folder, and type:

    python expense_tracker.py

On some computers the command is python3 instead of python.

The first time you run it, the program creates a file called expenses.db in the same folder. This is where all your expenses are stored. You do not have to create it yourself.


## Using the program

When the program starts, it shows a menu with numbered options. You type a number and press Enter. The options let you add an expense, view expenses, search, edit, delete, set a budget, check your budgets, see a monthly summary, manage categories, and export everything to a CSV file. Option 0 closes the program.

A few things are good to know while using it.

Dates are typed as year, month and day, like 2026-09-30. If you just press Enter, today's date is used. Dates in the future are not accepted.

Months are typed as year and month, like 2026-09. Pressing Enter uses the current month.

Categories can be chosen by typing either their number or their name. There are nine to begin with, including Food, Transport and Housing, and you can add your own from the Categories menu.

When you edit an expense, pressing Enter on any question keeps the old value.

Amounts may include commas, so 1,500 works.

If you press Ctrl and C at the same time, the current action is cancelled and you go back to the menu.


## Budgets

You can set a monthly limit for any category. After that, every time you add an expense to that category, the program checks how much of the limit has been used this month. When you reach 80 percent it gives you a warning, and when you go past the limit it tells you the budget has been exceeded.


## A small example

After setting a budget of 2000 for Food and adding a few expenses, the monthly summary looks like this:

    Summary for 2026-09
    ==============================
    Total spent : Rs. 2250.00
    Expenses    : 3
    Average     : Rs. 750.00

    By category:
      Food              1950.00   86.7%  #################
      Transport          300.00   13.3%  ##


## Files

expense_tracker.py is the program itself.

expenses.db is your saved data. It appears after the first run.

expenses_export.csv appears when you use the export option. You can open it in Excel or Google Sheets.


## Changing the settings

Near the top of expense_tracker.py there are a few settings you can change. CURRENCY is the symbol shown next to amounts, and it is set to Rs. by default. WARNING_PERCENT is how full a budget must be before you get a warning, and it is set to 80. DB_FILE and CSV_FILE are the names of the database and export files.


## Backing up or starting over

To back up your data, copy the expenses.db file somewhere safe. To start fresh, close the program and delete expenses.db. A new empty one will be created the next time you run it.


## Limitations

Categories can be added, but they cannot be renamed or deleted. Budget warnings only appear when you add an expense, not when you edit one. The program is for one person and works only in the terminal.


## Ideas for the future

Recurring expenses, income tracking, comparing one month with another, and a graphical or web version.


This was made as a learning project, my first programming project.
