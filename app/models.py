from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .database import Base  
from .database import Session  

session = Session()  


class BaseModel(Base):
    """Base model class providing common operations for all database models """
    __abstract__ = True #  Prevents SQLAlchemy from creating a table for this class.
    

    def save(self, session):
        """Save the current object to the database."""
        session.add(self)
        session.commit()

    def delete(self, session):
        """Delete the current object from the database."""
        session.delete(self)
        session.commit()
        
class Customer(BaseModel):
    
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)
    city = Column(String)
    phone = Column(String)

    invoices = relationship(
        'Invoice', 
        back_populates='customer',
        cascade='all, delete-orphan' # Ensures related invoices are deleted when customer is deleted
    )

    @classmethod
    def create_customer(cls, session, name, address, city, phone):
        
        customer = cls(name=name, address=address, city=city, phone=phone)
        customer.save(session)
        return customer

    @classmethod
    def get_customer_by_name(cls, session, name):
        
        return session.query(cls).filter_by(name=name).first()

    def update_city(self, session, new_city):
        self.city = new_city
        self.save(session)
        return self

    @property
    def total_due(self):
        """Calculate the total amount due across all invoices.
        
        Returns:
            Numeric: Sum of all unpaid invoice balances
        """
        return sum(invoice.balance_due for invoice in self.invoices if invoice.balance_due)

    @property
    def paid_in_full(self):
        """Check if all invoices are fully paid.
        
        Returns:
            bool: True if all invoices are paid, False otherwise
        """
        return all(invoice.is_paid for invoice in self.invoices)


class Invoice(BaseModel):
    
    
   
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    invoice_total = Column(Numeric(10, 2))
    payment_total = Column(Numeric(10, 2))
    invoice_date = Column(Date)
    due_date = Column(Date)
    payment_date = Column(Date)
    balance_due = Column(Numeric(10, 2))
    status = Column(String)

    customer = relationship(
        'Customer', 
        back_populates='invoices'
    )

    invoice_lines = relationship(
        'InvoiceLine', 
        back_populates='invoice',
        cascade='all, delete-orphan' # Ensures related invoice lines are deleted when invoice is deleted
    )
    payments = relationship(
        'Payment', 
        back_populates='invoice',
        cascade='all, delete-orphan' # Ensures related payments are deleted when invoice is deleted
    )

    @classmethod
    def create_invoice(cls, session, number, customer_id, invoice_total, payment_total, 
                     invoice_date, due_date, payment_date, balance_due, status):
        
        invoice = cls(
            number=number,
            customer_id=customer_id,
            invoice_total=invoice_total,
            payment_total=payment_total,
            invoice_date=invoice_date,
            due_date=due_date,
            payment_date=payment_date,
            balance_due=balance_due,
            status=status
        )
        invoice.save(session)
        return invoice

    @classmethod
    def get_invoice_by_number(cls, session, number):
        
        return session.query(cls).filter_by(number=number).first()

    def update_status(self, session, new_status):
        """Update the invoice status. """
        self.status = new_status
        self.save(session)
        return self

    @property
    def is_paid(self):
        """Check if invoice is fully paid.
        
        Returns:
            bool: True if balance_due is zero, False otherwise
        """
        return self.balance_due == 0

    @property
    def total_quantity(self):
        
        return sum(line.quantity for line in self.invoice_lines)


class Payment(BaseModel):
    
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    payment_method_id = Column(Integer, ForeignKey('payment_methods.id'))
    amount = Column(Numeric(10, 2))
    date = Column(Date)

    invoice = relationship('Invoice', back_populates='payments')
    payment_method = relationship('PaymentMethod', back_populates='payments')

    @classmethod
    def create_payment(cls, session, invoice_id, payment_method_id, amount, date):
        
        payment = cls(
            invoice_id=invoice_id,
            payment_method_id=payment_method_id,
            amount=amount,
            date=date
        )
        payment.save(session)
        return payment

    @classmethod
    def get_payment_by_id(cls, session, payment_id):
        
        return session.get(cls, payment_id)

    def update_amount(self, session, new_amount):
        
        self.amount = new_amount
        self.save(session)
        return self


class PaymentMethod(BaseModel):
    
    __tablename__ = 'payment_methods'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    payments = relationship(
        'Payment', 
        back_populates='payment_method',
        cascade='all, delete-orphan' # Ensures related payments are deleted when payment method is deleted
    )


    @classmethod
    def create_payment_method(cls, session, name):
        
        pay_method = cls(name=name)
        pay_method.save(session)
        return pay_method

    @classmethod
    def get_payment_method_by_name(cls, session, name):
       
        return session.query(cls).filter_by(name=name).first()

    def update_name(self, session, new_pm_name):
        
        self.name = new_pm_name
        self.save(session)
        return self


class Product(BaseModel):
    
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Numeric(10, 2))

    invoice_lines = relationship(
        'InvoiceLine', 
        back_populates='product',
        cascade='all, delete-orphan' # Ensures related invoice lines are deleted when product is deleted
   )


    @classmethod
    def create_product(cls, session, name, price):
        
        product = cls(name=name, price=price)
        product.save(session)
        return product

    @classmethod
    def get_product_by_name(cls, session, name):
       
        return session.query(cls).filter_by(name=name).first()

    @classmethod
    def get_product_by_id(cls, session, product_id):
        
        product = session.get(cls, product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} does not exist.")
        return product

    def update_price(self, session, new_price):
        
        self.price = new_price
        self.save(session)
        return self

    def update_name(self, session, new_name):
        
        self.name = new_name
        self.save(session)
        return self


class InvoiceLine(BaseModel):
    
    __tablename__ = 'invoice_lines'

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    unit_price = Column(Numeric(10, 2))
    total = Column(Numeric(10, 2))

    invoice = relationship('Invoice', back_populates='invoice_lines')
    product = relationship('Product', back_populates='invoice_lines')

    @classmethod
    def create_invoice_line(cls, session, invoice_id, product_id, quantity, unit_price, total):
        
        invoice_line = cls(
            invoice_id=invoice_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            total=total
        )
        invoice_line.save(session)
        return invoice_line

    @classmethod
    def get_invoice_line_by_id(cls, session, invoice_line_id):
        
        return session.get(cls, invoice_line_id)

    def update_quantity(self, session, new_quantity):
        """Update the line item quantity.
    
        """
        self.quantity = new_quantity
        self.save(session)
        return self

    @property
    def line_total(self):
        """Calculate the line total (quantity * unit_price).
        
        """
        return self.quantity * self.unit_price