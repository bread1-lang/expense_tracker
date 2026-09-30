# expense_tracker
The Following Repo is about my Academic Project on a simple programme which can be used to track your monthly expenses in detail with options to preceisely log how and when the Expense was made. The Programme Is Built Entirely using Python and runs inside the terminal itself. GUI and cool stuff not learned yet :/ 


## Features

- **Add, view, search, edit and delete** expenses
- **Monthly budgets** per category, with a warning at 80% and an alert when you go over
- **Monthly summary** with total, average, and a category breakdown
- **Categories**: nine built-in ones, and you can add your own
- **CSV export** for opening in Excel or Google Sheets
- **Input checking**: bad amounts, dates or empty answers are rejected and asked again, so it won't crash on typos

## Requirements

- Python 3.6 or newer (uses only the standard library: `sqlite3`, `csv`, `datetime`)

## How to run

1. Put `expense_tracker.py` in any folder.
2. Open a terminal in that folder.
3. Run:

   ```
   python expense_tracker.py
   ```

   On some systems you may need `python3` instead of `python`.

The first time you run it, a file called `expenses.db` is created automatically in the same folder. This is where all your data is saved.

## Using the program

You'll see a menu like this:

```
1. Add expense
2. View expenses
3. Search expenses
4. Edit expense
5. Delete expense
6. Set budget
7. Budget status
8. Monthly summary
9. Categories
10. Export to CSV
0. Exit
```

Type a number and press Enter. Some tips:

- **Dates** use the format `YYYY-MM-DD` (for example `2026-09-30`). Press Enter to use today. Future dates aren't allowed.
- **Months** use the format `YYYY-MM` (for example `2026-09`). Press Enter for the current month.
- **Categories** can be picked by number or by name.
- **Editing**: press Enter on any field to keep its old value.
- **Amounts** can include commas, so `1,500` works.
- **Ctrl+C** cancels the current action and takes you back to the menu.

### Example

```
Saved expense #2: Rs. 1500.00 on Food.
! Warning: 98% of the Food budget is used.

Summary for 2026-09
==============================
Total spent : Rs. 2250.00
Expenses    : 3
Average     : Rs. 750.00

By category:
  Food              1950.00   86.7%  #################
  Transport          300.00   13.3%  ##
```

## Files

| File | What it is |
|------|------------|
| `expense_tracker.py` | The program |
| `expenses.db` | Your data (created on first run) |
| `expenses_export.csv` | Created when you use "Export to CSV" |

## Settings

These are at the top of `expense_tracker.py` and are easy to change:

| Setting | Default | Meaning |
|---------|---------|---------|
| `CURRENCY` | `"Rs."` | Symbol shown next to amounts |
| `WARNING_PERCENT` | `80` | Warn when this % of a budget is used |
| `DB_FILE` | `"expenses.db"` | Name of the database file |
| `CSV_FILE` | `"expenses_export.csv"` | Name of the export file |
| `DEFAULT_CATEGORIES` | Food, Transport, Housing, ... | Categories created on first run |

## Backing up or resetting

- **Backup:** copy `expenses.db` somewhere safe.
- **Start fresh:** close the program and delete `expenses.db`. A new empty one is created next time.

## Known limitations

- Categories can be added but not renamed or deleted.
- Budget warnings only appear when adding an expense (not when editing).
- Single user, text interface only.

## Ideas for later

Recurring expenses, income tracking, month-to-month comparison, and a graphical or web version.

---

Made as a learning project (first programming project).
