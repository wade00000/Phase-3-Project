# app/seed.py


from faker import Faker
from decimal import Decimal
from datetime import  timedelta
import random


from app.db.models import Customer, Product, PaymentMethod, Invoice, InvoiceLine, Payment
from database import Session

session = Session()  
fake = Faker()

def seed_customers(n=10):
    customers = []
    for _ in range(n):
        customer = Customer.create_customer(
            session,
            name=fake.name(),
            address=fake.street_address(),
            city=fake.city(),
            phone=fake.phone_number(),
        )
        customers.append(customer)
    return customers

def seed_products():
    products = []
    for _ in range(10):
        product = Product.create_product(
            session,
            name=fake.word().capitalize(),
            price=Decimal(random.uniform(5, 100)).quantize(Decimal("0.01")),
        )
        products.append(product)
    return products

def seed_payment_methods():
    methods = ["Credit Card", "Cash", "Check", "Bank Transfer", "PayPal"]
    payment_methods = []
    for name in methods:
        pm = PaymentMethod.create_payment_method(session, name=name)
        payment_methods.append(pm)
    return payment_methods

def seed_invoices(customers, products, payment_methods, n=20):
    invoices = []
    for _ in range(n):
        customer = random.choice(customers)
        invoice_date = fake.date_between(start_date='-90d', end_date='today')
        due_date = invoice_date + timedelta(days=30)
        
        invoice_lines = []
        invoice_total = Decimal("0.00")
        
        # Add between 1-5 lines
        line_count = random.randint(1, 5)
        for _ in range(line_count):
            product = random.choice(products)
            quantity = random.randint(1, 10)
            unit_price = product.price
            total = (unit_price * quantity).quantize(Decimal("0.01"))
            invoice_total += total
            
            # We create invoice lines after invoice creation, so just collect data here
            invoice_lines.append({
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "total": total,
            })
        
        payment_total = Decimal("0.00")
        status = "Unpaid"
        payment_date = None
        balance_due = invoice_total
        
        # 50% chance the invoice is partially or fully paid
        if random.choice([True, False]):
            payment_total = invoice_total if random.choice([True, False]) else (invoice_total / 2).quantize(Decimal("0.01"))
            balance_due = (invoice_total - payment_total).quantize(Decimal("0.01"))
            status = "Paid" if balance_due == 0 else "Partial"
            payment_date = invoice_date + timedelta(days=random.randint(1, 30))
        
        # Create Invoice
        invoice = Invoice.create_invoice(
            session,
            number=fake.unique.bothify(text="INV-####"),
            customer_id=customer.id,
            invoice_total=invoice_total,
            payment_total=payment_total,
            invoice_date=invoice_date,
            due_date=due_date,
            payment_date=payment_date,
            balance_due=balance_due,
            status=status,
        )
        
        # Create InvoiceLines linked to invoice
        for line in invoice_lines:
            InvoiceLine.create_invoice_line(
                session,
                invoice_id=invoice.id,
                product_id=line["product"].id,
                quantity=line["quantity"],
                unit_price=line["unit_price"],
                total=line["total"],
            )
        
        # Create payments if any
        if payment_total > 0:
            # Split payment_total among 1 or 2 payments randomly
            num_payments = random.choice([1, 2])
            amounts = []
            if num_payments == 1:
                amounts = [payment_total]
            else:
                first_amount = (payment_total * Decimal(random.uniform(0.3, 0.7))).quantize(Decimal("0.01"))
                second_amount = payment_total - first_amount
                amounts = [first_amount, second_amount]
            
            for amt in amounts:
                pm = random.choice(payment_methods)
                Payment.create_payment(
                    session,
                    invoice_id=invoice.id,
                    payment_method_id=pm.id,
                    amount=amt,
                    date=payment_date or invoice_date,
                )
        
        invoices.append(invoice)
    return invoices

def seed():
    print("Seeding customers...")
    customers = seed_customers(20)
    print("Seeding products...")
    products = seed_products()
    print("Seeding payment methods...")
    payment_methods = seed_payment_methods()
    print("Seeding invoices with lines and payments...")
    seed_invoices(customers, products, payment_methods, 30)
    print("Seeding completed!")

if __name__ == "__main__":
    seed()
