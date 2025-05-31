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


## 🧬 Models: `app/models.py`

The project uses SQLAlchemy ORM to define relational data models. Two examples of the models are:

- **Customers**  
  Attributes: `id`, `name`, `email`, `rate`  
  Has a one-to-many relationship with `Invoices`.

- **Invoices**  
  Attributes: `id`,`invoice_id`, `client_id`, `invice_total`, `payment_total`  
  Belongs to a single customer.


---

## 📁 Project Structure

```
.
├── Pipfile
├── Pipfile.lock
├── README.md
├── alembic
│   ├── README
│   ├── env.py
│   └── script.py.mako
├── alembic.ini
├── app
│   ├── __init__.py
│   ├── cli.py
│   ├── database.py
│   ├── db
│   │   ├── models.py
│   │   └── seed.py
│   └── helpers.py
|
├── debug.py
├── main.py
└── run_cli.py

```

---

## 🛠️ Tech Stack

- Python 3.11
- SQLAlchemy ORM
- Click (for terminal text formatting)
- SQLite (lightweight, file-based database)
- Cmd module (interactive CLI shell)


---

## 🔗 Resources & Inspiration

- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Python Cmd module](https://docs.python.org/3/library/cmd.html)
- [Click](https://click.palletsprojects.com/)
- [ASCII Art Generator](https://patorjk.com/software/taag/)

---
## 🛠️ Setup & Installation

#### 1. **Clone the repo**

```bash
git clone https://github.com/your-username/simplebilling-cli.git
cd simplebilling-cli
```

#### 2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### 3. **Install dependencies**

```bash
pip install -r requirements.txt
```

> 🧪 If you're developing or testing, you might want to install dev dependencies too:
> 
> ```bash
> pip install -r dev-requirements.txt
> ```

#### 4. **Initialize the database**

```bash
alembic upgrade head
```

> This runs migrations and sets up the SQLite database schema.

#### 5. **Run the CLI**

```bash
python run_cli.py
```

You’ll see a welcome banner and can immediately begin using the app.

---



## 👤 Author

**Wade**  
Full Stack Software Engineer in the making  
Crafting tools that save time so you can make money 💸
