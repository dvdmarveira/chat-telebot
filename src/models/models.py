from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey 
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

# Cria a conexão com o banco
db = create_engine("sqlite:///database.db")

# Cria a base do banco de dados
Base = declarative_base()

# Cria as classes/tabelas do banco
# Clientes
class Customer(Base):
  __tablename__ = "customers"
  
  id = Column("id", Integer, primary_key=True, autoincrement=True)
  name = Column("name", String, nullable=False)
  age = Column("age", Integer)
  cpf = Column("cpf", String)
  number = Column("number", String, nullable=False)
  
  def __init__(self, name, age, cpf, number):
    self.name = name
    self.age = age
    self.cpf = cpf
    self.number = number
  
# Pedidos
class Order(Base):
  __tablename__ = "orders"
  
  ORDERS_STATUS = (
    ("PENDING", "PENDING"),
    ("FINALIZED", "FINALIZED"),
    ("CANCELLED", "CANCELLED"),
  )
  
  id = Column("id", Integer, primary_key=True, autoincrement=True)
  customer = Column("customer", ForeignKey("customers.id"))
  price = Column("price", Float)
  status = Column("status", ChoiceType(choices=ORDERS_STATUS)) # pendente, finalizado, cancelado
  # items = 
  
  def __init__(self, customer, price=0, status="PENDING"):
    self.customer = customer
    self.price = price
    self.status = status

# Itens de um pedido
class Order_Items(Base):
  __tablename__ = "order_items"

  FLAVOR_ITEMS = (
    ("CHOCOLATE", "CHOCOLATE"),
    ("MACAXEIRA", "MACAXEIRA"),
    ("COCO", "COCO"),
    ("MILHO", "MILHO"),
  )
  
  id = Column("id", Integer, primary_key=True, autoincrement=True)
  amount = Column("amount", Integer)
  flavor = Column("flavor", ChoiceType(choices=FLAVOR_ITEMS))
  unit_price = Column("unit_price", Float)
  order = Column("order", ForeignKey("orders.id"))
  
  def __init__(self, amount, flavor, unit_price, order):
    self.amount = amount
    self.flavor = flavor
    self.unit_price = unit_price
    self.order = order
    
# Executa a criação dos metadados do banco