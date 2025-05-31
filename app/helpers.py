import click
from decimal import Decimal, InvalidOperation
from datetime import datetime


# Allows a user to cancel a prompt by typing 'cancel' or pressing Ctrl+C
def cancelable_prompt(text, type_=str, default=None):
    try:
        value = click.prompt(text, type=type_, default=default)
        if isinstance(value, str) and value.strip().lower() == 'cancel':
            raise click.Abort()
        return value
    except KeyboardInterrupt:
        raise click.Abort()

# === UTILITY INPUT VALIDATORS ===
def input_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")

def input_decimal(prompt):
    while True:
        try:
            value = Decimal(input(prompt).strip())
            if value >= 0:
                return value
            else:
                print("Value must be non-negative.")
        except InvalidOperation:
            print("Invalid decimal number.")

def input_int(prompt):
    while True:
        try:
            value = int(input(prompt).strip())
            if value >= 0:
                return value
            else:
                print("Value must be non-negative integer.")
        except ValueError:
            print("Invalid integer.")

def input_date(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            print("Date must be in YYYY-MM-DD format.")


def validate_id(session, model, id_):
    obj = session.get(model, id_)
    if not obj:
        raise click.BadParameter(f"{model.__name__} ID {id_} not found.")
    return obj

