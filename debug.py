# debug.py
from app.database import Base 

def print_tables():
    print("=== Tables registered in Base.metadata ===")
    for table_name in Base.metadata.tables.keys():
        print(f"- {table_name}")

if __name__ == "__main__":
    print_tables()






# MY TO DO LIST
# 1.add cascades in:
# Customer.invoices
# Invoice.invoice_lines
# Invoice.payments
# Product.invoice_lines
# PaymentMethod.payments
# 2.deal with multiple session commits