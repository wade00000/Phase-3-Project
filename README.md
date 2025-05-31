# 💼 SimpleBilling CLI

> _Track it. Bill it. Bank it._  
A developer-focused time-tracking and invoicing tool, built entirely in Python and run via the command line. SimpleBilling allows you to log billable hours, manage clients, and generate invoices right from your terminal.

---

## 🚀 CLI Entry Point: `run_cli.py`

This is the **main entry point** of the application. When you run this script, you’re greeted with a colorful ASCII banner and a helpful welcome message. This script does two things:

1. Displays the app's identity and usage tips using `click.secho()`.
2. Launches an interactive CLI shell defined in `app/cli.py`, allowing the user to type commands directly.

> 💡 This file uses Python's `if __name__ == "__main__":` check to ensure the CLI only runs when executed directly — not when imported as a module.

---

## 🧠 CLI Command Shell: `app/cli.py`

This file defines the **core CLI logic** using Python’s `cmd.Cmd` class.

The `SimpleBillingShell` class is a custom command-line shell that handles user input and command execution. It supports the following commands:

### CLI Commands

| Command       | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `add_client`  | Create a new client with name, email, and rate.                            |
| `log_hours`   | Log billable hours for an existing client.                                 |
| `show_clients`| List all clients and their hourly rates.                                   |
| `generate_invoice` | View an invoice for a given client with total hours and amount.       |
| `exit` / `quit` | Cleanly exits the CLI shell.                                              |

The shell uses:
- `input()` prompts for interactive data collection
- SQLAlchemy sessions for ORM operations
- Helper functions to modularize logic and ensure clean code separation

---

## 🔧 Functions: `app/functions.py`

This file holds **helper functions** that encapsulate specific business logic used by the CLI.

### Notable Functions

- `create_client(name, email, rate)`  
  Creates and persists a new client object. Returns the created client or `None` if validation fails.

- `log_work(client_id, hours)`  
  Adds a work log entry for a specific client. Includes input validation for negative or zero hours.

- `get_all_clients()`  
  Retrieves a list of all clients in the database.

- `generate_invoice_for_client(client_id)`  
  Calculates total billable hours and returns a string-formatted invoice breakdown.

These functions ensure the CLI remains lean, while logic is modular and testable.

---

## 🧬 Models: `app/models.py`

The project uses SQLAlchemy ORM to define relational data models. The three main models are:

- **Client**  
  Attributes: `id`, `name`, `email`, `rate`  
  Has a one-to-many relationship with `WorkLog`.

- **WorkLog**  
  Attributes: `id`, `client_id`, `hours_logged`, `timestamp`  
  Belongs to a single client.

These models support foreign key constraints, backref relationships, and can be extended later for invoice history or project tracking.

---

## 📁 Project Structure

```
simplebilling/
├── app/
│   ├── cli.py           # CLI logic and command handler
│   ├── functions.py     # Helper functions for CRUD and invoice generation
│   ├── models.py        # SQLAlchemy models
│   └── __init__.py
├── run_cli.py           # Entry point script with welcome banner
├── db/                  # SQLite DB and migrations (Alembic, not documented here)
├── README.md            # You're reading it.
```

---

## 🛠️ Tech Stack

- Python 3.11
- SQLAlchemy ORM
- Click (for terminal text formatting)
- SQLite (lightweight, file-based database)
- Cmd module (interactive CLI shell)

---

## 🧾 Sample Output

```
█████╗ ███╗   ██╗ ██████╗ 
██╔══██╗████╗  ██║██╔═══██╗
███████║██╔██╗ ██║██║   ██║
██╔══██║██║╚██╗██║██║   ██║
██║  ██║██║ ╚████║╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
Track it. Bill it. Bank it.

Welcome to SimpleBilling CLI!
Type '--help' to see available commands
💡 Type 'cancel' or press Ctrl+C at any prompt to cancel a command.

> add_client
Client Name: Acme Inc.
Client Email: contact@acme.com
Hourly Rate: 75

> log_hours
Client ID: 1
Hours Worked: 4.5

> generate_invoice
Client ID: 1
--- Invoice for Acme Inc. ---
Total Hours: 4.5
Hourly Rate: $75.0
Total Due: $337.50
```

---

## 🔗 Resources & Inspiration

- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Python Cmd module](https://docs.python.org/3/library/cmd.html)
- [Click](https://click.palletsprojects.com/)
- [ASCII Art Generator](https://patorjk.com/software/taag/)

---

## 🧠 Future Features (Ideas)

- PDF export of invoices
- Tag work sessions by project
- Filter invoices by month
- Email invoices directly from CLI
- Optional web dashboard frontend (Flask?)

---

## 👤 Author

**Wade**  
Full Stack Software Engineer in the making  
Crafting tools that save time so you can make money 💸
