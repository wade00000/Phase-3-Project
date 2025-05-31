from datetime import date, datetime
from decimal import Decimal
from app.db.models import Customer, Product, Invoice, InvoiceLine, Payment, PaymentMethod
from app.database import Session
from app.helpers import cancelable_prompt,input_nonempty, input_decimal, input_int, input_date
import click
import shlex


session = Session() 

@click.group()
def cli():
    pass

# === CREATE CUSTOMER ===
@cli.command()
def create_customer():
    """Create a new customer"""
    click.echo("\n=== Create Customer ===")
    try:
        name = cancelable_prompt("Customer name")
        address = cancelable_prompt("Customer address", default="")
        city = cancelable_prompt("Customer city", default="")
        phone = cancelable_prompt("Customer phone", default="")
        customer = Customer.create_customer(session, name, address, city, phone)
        click.echo(f"Customer '{customer.name}' created with ID {customer.id}")
    except click.Abort:
        click.echo("⚠️ Command canceled.")

@cli.command()
def list_customers():
    """List all customers"""
    click.echo("\n=== Customers ===")
    customers = session.query(Customer).all()
    for c in customers:
        click.echo(f"{c.id}: {c.name} | {c.city} | {c.phone}")

@cli.command()
def update_customer_city():
    """Update a customer's city"""
    click.echo("\n=== Update Customer City ===")
    try:
        customer_id = cancelable_prompt("Customer ID", type_=int)
        new_city = cancelable_prompt("New city name")
        customer = session.get(Customer, customer_id)
        if not customer:
            click.echo("Customer not found.")
            return
        customer.update_city(session, new_city)
        click.echo(f"Customer {customer.name} city updated to {new_city}")
    except click.Abort:
        click.echo("⚠️ Command canceled.")

@cli.command()
def delete_customer():
    """Delete a customer"""
    click.echo("\n=== Delete Customer ===")
    try:
        customer_id = cancelable_prompt("Customer ID", type_=int)
        customer = session.get(Customer, customer_id)
        if not customer:
            click.echo("Customer not found.")
            return
        customer.delete(session)
        click.echo(f"Customer {customer.name} deleted.")
    except click.Abort:
        click.echo("⚠️ Command canceled.")

# === PRODUCT MANAGEMENT ===
@cli.command()
def create_product():
    """Create a new product"""
    click.echo("\n=== Create Product ===")
    try:
        name = cancelable_prompt("Product name")
        price = cancelable_prompt("Product price", type_=float)
        product = Product.create_product(session, name, Decimal(str(price)))
        click.echo(f"Product '{product.name}' created with ID {product.id}")
    except click.Abort:
        click.echo("⚠️ Command canceled.")

@cli.command()
def list_products():
    """List all products"""
    click.echo("\n=== Products ===")
    products = session.query(Product).all()
    for p in products:
        click.echo(f"{p.id}: {p.name} | ${p.price}")

@cli.command()
def update_product_price():
    """Update the price of a product"""
    click.echo("\n=== Update Product Price ===")
    try:
        product_id = cancelable_prompt("Product ID", type_=int)
        product = validate_id(session, Product, product_id)  # Replaces manual checks
        new_price = cancelable_prompt("New price", type_=float)
        product.update_price(session, new_price)
        click.echo(f"Price updated to ${new_price}")
    except click.Abort:
        click.echo("⚠️ Command canceled.")
    except click.BadParameter as e:  # Specific error
        click.secho(f"❌ {e}", fg="red")

@cli.command()
def delete_product():
    """Delete a product"""
    click.echo("\n=== Delete Product ===")
    try:
        product_id = cancelable_prompt("Product ID", type_=int)
        product = session.get(Product, product_id)
        if not product:
            click.echo("Product not found.")
            return
        product.delete(session)
        click.echo(f"Product {product.name} deleted.")
    except click.Abort:
        click.echo("⚠️ Command canceled.")

# === PAYMENT METHODS ===
@cli.command()
def create_payment_method():
    """Create a payment method"""
    click.echo("\n=== Create Payment Method ===")
    try:
        name = cancelable_prompt("Payment method name")
        pm = PaymentMethod.create_payment_method(session, name)
        click.echo(f"Payment method '{pm.name}' created with ID {pm.id}")
    except click.Abort:
        click.echo("⚠️ Command canceled.")

@cli.command()
def list_payment_methods():
    """List all payment methods"""
    click.echo("\n=== Payment Methods ===")
    methods = session.query(PaymentMethod).all()
    for pm in methods:
        click.echo(f"{pm.id}: {pm.name}")

# === INVOICE MANAGEMENT ===
@cli.command()
def create_invoice():
    """Create an invoice and add products interactively"""
    click.echo("\n=== Create Invoice ===")
    try:
        customer_id = cancelable_prompt("Customer ID", type_=int)
        number = cancelable_prompt("Invoice number")
        invoice_date = datetime.strptime(cancelable_prompt("Invoice date (YYYY-MM-DD)"), "%Y-%m-%d").date()
        due_date = datetime.strptime(cancelable_prompt("Due date (YYYY-MM-DD)"), "%Y-%m-%d").date()

        customer = session.get(Customer, customer_id)
        if not customer:
            click.echo("Customer not found.")
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
            prod_id = cancelable_prompt("Product ID to add (or 'done')", type_=str, default='done')
            if prod_id.lower() == 'done':
                break

            try:
                product_id = int(prod_id)
            except ValueError:
                click.echo("Invalid product ID.")
                continue

            product = session.get(Product, product_id)
            if not product:
                click.echo("Product not found.")
                continue

            quantity = cancelable_prompt("Quantity", type_=int)
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
    except click.Abort:
        click.echo("⚠️ Command canceled.")
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@cli.command()
def list_invoices():
    """List all invoices"""
    click.echo("\n=== Invoices ===")
    invoices = session.query(Invoice).all()
    for inv in invoices:
        click.echo(f"ID {inv.id}: {inv.number} | Customer ID {inv.customer_id} | Total ${inv.invoice_total} | Status: {inv.status}")

@cli.command()
def record_payment():
    """Record a payment for an invoice"""
    click.echo("\n=== Record Payment ===")
    try:
        invoice_id = cancelable_prompt("Invoice ID", type_=int)
        payment_method_id = cancelable_prompt("Payment Method ID", type_=int)
        amount = Decimal(str(cancelable_prompt("Payment amount", type_=float)))
        pay_date = datetime.strptime(cancelable_prompt("Payment date (YYYY-MM-DD)"), "%Y-%m-%d").date()

        invoice = session.get(Invoice, invoice_id)
        if not invoice:
            click.echo("Invoice not found.")
            return

        pm = session.get(PaymentMethod, payment_method_id)
        if not pm:
            click.echo("Payment method not found.")
            return

        if invoice.balance_due is None or amount > invoice.balance_due:
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
    except click.Abort:
        click.echo("⚠️ Command canceled.")
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
def shell():
    """Interactive CLI shell"""
    while True:
        try:
            cmd = input("billing > ").strip()
            if cmd.lower() in ("exit", "quit"):
                click.echo("Exiting shell.")
                break
            if not cmd:
                continue
            args = shlex.split(cmd)
            cli.main(args=args, standalone_mode=False)
        except KeyboardInterrupt:
            click.echo("\nExiting shell.")
            break
        except Exception as e:
            click.secho(f"Error: {e}", fg="red")

if __name__ == "__main__":
    cli()
