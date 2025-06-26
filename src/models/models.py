from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey 
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

# Cria a conexão com o banco
db = create_engine("sqlite:///banco.db")

# Cria a base do banco de dados
Base = declarative_base()

# Cria as classes/tabelas do banco
# Usuários
class User(Base):
  __tablename__ = "users"
  
  id = Column("id", Integer, primary_key=True, autoincrement=True)
  name = Column("name", String, nullable=False)
  email = Column("email", String, nullable=False)
  password = Column("password", String, nullable=False)
  gender = Column("gender", String)
  admin = Column("admin", Boolean, default=False)
  active = Column("active", Boolean, default=True)

  def __init__(self, name, email, password, gender, admin=False, active=True):
    self.name = name
    self.email = email
    self.password = password
    self.gender = gender
    self.admin = admin
    self.active = active
    
# Clientes
class Customer(Base):
  __tablename__ = "customers"
  
  id = Column("id", Integer, primary_key=True, autoincrement=True)
  name = Column("name", String, nullable=False)
  gender = Column("gender", String)
  address = Column("address", String)
  cellphone = Column("cellphone", String, nullable=False)
  
  def __init__(self, name, gender, address, cellphone):
    self.name = name
    self.gender = gender
    self.address = address
    self.cellphone = cellphone
  
# Pedidos
class Order(Base):
  __tablename__ = "orders"
  
  # ORDERS_STATUS = (
  #   ("PENDING", "PENDING"),
  #   ("FINALIZED", "COMPLETED"),
  #   ("CANCELLED", "CANCELLED"),
  # )
  
  id = Column("id", Integer, primary_key=True, autoincrement=True)
  customer = Column("customer", ForeignKey("customers.id"))
  user = Column("user", ForeignKey("users.id"))
  price = Column("price", Float)
  status = Column("status", String) # pendente, finalizado, cancelado
  items = relationship("Order_Items", cascade="all, delete")
  
  def __init__(self, customer, user, price=0, status="PENDING"):
    self.customer = customer
    self.user = user
    self.price = price
    self.status = status
    
  def calculate_price(self):
    # order_price = 0
    # for item in self.items:
    #   item_price = item.unit_price * item.amount
    #   order_price += item_price
    self.price = sum(item.unit_price * item.amount for item in self.items)

# Itens de um pedido
class Order_Items(Base):
  __tablename__ = "order_items"

  # FLAVOR_ITEMS = (
  #   ("CHOCOLATE", "CHOCOLATE"),
  #   ("MACAXEIRA", "MACAXEIRA"),
  #   ("COCO", "COCO"),
  #   ("MILHO", "MILHO"),
  # )
  
  id = Column("id", Integer, primary_key=True, autoincrement=True)
  amount = Column("amount", Integer)
  flavor = Column("flavor", String)
  unit_price = Column("unit_price", Float)
  order = Column("order", ForeignKey("orders.id"))
  
  def __init__(self, amount, flavor, unit_price, order):
    self.amount = amount
    self.flavor = flavor
    self.unit_price = unit_price
    self.order = order
    
# Executa a criação dos metadados do banco

# alembic revision --autogenerate -m "msg"
# alembic upgrade head