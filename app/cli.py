from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from models import Customer, Product, Invoice, InvoiceLine, Payment, PaymentMethod
from database import session
import click



@click.group()
def cli():
    pass
    
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

@cli.command()
@click.option('--name', prompt=True, help="Customer name")
@click.option('--address', prompt=True, default="", help="Customer address")
@click.option('--city', prompt=True, default="", help="Customer city")
@click.option('--phone', prompt=True, default="", help="Customer phone")
def create_customer(name, address, city, phone):
    """Create a new customer"""
    click.echo("\n=== Create Customer ===")
    customer = Customer.create_customer(session, name, address, city, phone)
    click.echo(f"Customer '{customer.name}' created with ID {customer.id}")

@cli.command()
def list_customers():
    """List all customers"""
    click.echo("\n=== Customers ===")
    customers = session.query(Customer).all()
    for c in customers:
        click.echo(f"{c.id}: {c.name} | {c.city} | {c.phone}")

@cli.command()
@click.argument('customer_id', type=int)
@click.argument('new_city', type=str)
def update_customer_city(customer_id, new_city):
    """Update a customer's city"""
    click.echo("\n=== Update Customer City ===")
    customer = session.get(Customer, customer_id)
    if not customer:
        click.echo("Customer not found.")
        return
    customer.update_city(session, new_city)
    click.echo(f"Customer {customer.name} city updated to {new_city}")

@cli.command()
@click.argument('customer_id', type=int)
def delete_customer(customer_id):
    """Delete a customer"""
    click.echo("\n=== Delete Customer ===")
    customer = session.get(Customer, customer_id)
    if not customer:
        click.echo("Customer not found.")
        return
    customer.delete(session)
    click.echo(f"Customer {customer.name} deleted.")

@cli.command()
@click.option('--name', prompt=True, help="Product name")
@click.option('--price', prompt=True, type=float, help="Product price")
def create_product(name, price):
    """Create a new product"""
    click.echo("\n=== Create Product ===")
    product = Product.create_product(session, name, Decimal(str(price)))
    click.echo(f"Product '{product.name}' created with ID {product.id}")

@cli.command()
def list_products():
    """List all products"""
    click.echo("\n=== Products ===")
    products = session.query(Product).all()
    for p in products:
        click.echo(f"{p.id}: {p.name} | ${p.price}")

@cli.command()
@click.argument('product_id', type=int)
@click.argument('new_price', type=float)
def update_product_price(product_id, new_price):
    """Update the price of a product"""
    click.echo("\n=== Update Product Price ===")
    product = session.get(Product, product_id)
    if not product:
        click.echo("Product not found.")
        return
    product.update_price(session, new_price)
    click.echo(f"Product {product.name} price updated to ${new_price}")

@cli.command()
@click.argument('product_id', type=int)
def delete_product(product_id):
    """Delete a product"""
    click.echo("\n=== Delete Product ===")
    product = session.get(Product, product_id)
    if not product:
        click.echo("Product not found.")
        return
    product.delete(session)
    click.echo(f"Product {product.name} deleted.")

@cli.command()
@click.option('--name', prompt=True, help="Payment method name")
def create_payment_method(name):
    """Create a payment method"""
    click.echo("\n=== Create Payment Method ===")
    pm = PaymentMethod.create_payment_method(session, name)
    click.echo(f"Payment method '{pm.name}' created with ID {pm.id}")

@cli.command()
def list_payment_methods():
    """List all payment methods"""
    click.echo("\n=== Payment Methods ===")
    methods = session.query(PaymentMethod).all()
    for pm in methods:
        click.echo(f"{pm.id}: {pm.name}")

@cli.command()
@click.option('--customer_id', prompt=True, type=int, help="Customer ID")
@click.option('--number', prompt=True, help="Invoice number")
@click.option('--invoice_date', prompt=True, help="Invoice date (YYYY-MM-DD)")
@click.option('--due_date', prompt=True, help="Due date (YYYY-MM-DD)")
def create_invoice(customer_id, number, invoice_date, due_date):
    """Create an invoice and add products interactively"""
    click.echo("\n=== Create Invoice ===")
    customer = session.get(Customer, customer_id)
    if not customer:
        click.echo("Customer not found.")
        return

    try:
        invoice_date = datetime.strptime(invoice_date, "%Y-%m-%d").date()
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
    except ValueError:
        click.echo("Dates must be in YYYY-MM-DD format.")
        return

    invoice = Invoice.create_invoice(
        session,
        number=number,
        customer_id=customer_id,
        invoice_total=Decimal('0.00'),
        payment_total=Decimal('0.00'),
        invoice_date=invoice_date,
        due_date=due_date,
        payment_date=None,
        balance_due=Decimal('0.00'),
        status="Open"
    )

    click.echo(f"Invoice {invoice.number} created. Now add products.")

    total = Decimal('0.00')
    while True:
        product_id = click.prompt("Product ID to add (or 'done')", default='done')
        if str(product_id).lower() == 'done':
            break
        try:
            product_id = int(product_id)
        except ValueError:
            click.echo("Invalid product ID.")
            continue

        product = session.get(Product, product_id)
        if not product:
            click.echo("Product not found.")
            continue

        quantity = click.prompt("Quantity", type=int)
        unit_price = product.price
        line_total = unit_price * quantity

        InvoiceLine.create_invoice_line(
            session,
            invoice_id=invoice.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=unit_price,
            total=line_total
        )
        total += line_total
        click.echo(f"Added {quantity} x {product.name} at ${unit_price} each.")

    invoice.invoice_total = total
    invoice.balance_due = total
    session.commit()
    click.echo(f"Invoice {invoice.number} total updated to ${total}.")

@cli.command()
def list_invoices():
    """List all invoices"""
    click.echo("\n=== Invoices ===")
    invoices = session.query(Invoice).all()
    for inv in invoices:
        click.echo(f"ID {inv.id}: {inv.number} | Customer ID {inv.customer_id} | Total ${inv.invoice_total} | Status: {inv.status}")

@cli.command()
@click.option('--invoice_id', prompt=True, type=int, help="Invoice ID")
@click.option('--payment_method_id', prompt=True, type=int, help="Payment Method ID")
@click.option('--amount', prompt=True, type=float, help="Payment amount")
@click.option('--pay_date', prompt=True, help="Payment date (YYYY-MM-DD)")
def record_payment(invoice_id, payment_method_id, amount, pay_date):
    """Record a payment for an invoice"""
    click.echo("\n=== Record Payment ===")
    invoice = session.get(Invoice, invoice_id)
    if not invoice:
        click.echo("Invoice not found.")
        return

    pm = session.get(PaymentMethod, payment_method_id)
    if not pm:
        click.echo("Payment method not found.")
        return

    try:
        amount = Decimal(str(amount))
        pay_date = datetime.strptime(pay_date, "%Y-%m-%d").date()
    except Exception:
        click.echo("Invalid amount or date format.")
        return

    if amount > invoice.balance_due:
        click.echo(f"Payment amount ${amount} exceeds balance due ${invoice.balance_due}.")
        return

    Payment.create_payment(session, invoice_id, payment_method_id, amount, pay_date)
    invoice.payment_total += amount
    invoice.balance_due -= amount

    if invoice.balance_due == 0:
        invoice.status = "Paid"
        invoice.payment_date = pay_date

    session.commit()
    click.echo(f"Payment of ${amount} recorded for Invoice {invoice.number}. Remaining balance: ${invoice.balance_due}.")

if __name__ == "__main__":

    print("TEST")
    """A simple billing system"""
    click.secho(r"""
    ███╗   ███╗ ██████╗ ██╗   ██╗███╗   ██╗██╗   ██╗
    ████╗ ████║██╔═══██╗██║   ██║████╗  ██║██║   ██║
    ██╔████╔██║██║   ██║██║   ██║██╔██╗ ██║██║   ██║
    ██║╚██╔╝██║██║   ██║██║   ██║██║╚██╗██║╚██╗ ██╔╝
    ██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║ ╚████║ ╚████╔╝ 
    ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  
                Track it. Bill it. Bank it.

""", fg='red', bold=True)
    click.secho("\nWelcome to SimpleBilling CLI!", fg='green', bold=True)
    click.echo("Type '--help' to see available commands\n",)

    cli()
