from pymongo import MongoClient
from config import MONGODB_URI, DATABASE_NAME

class Database:
  def __init__(self):
    self.client = MongoClient(MONGODB_URI)
    self.db = self.client[DATABASE_NAME]

  def get_categorias(self):
    return list(self.db.categorias.find())

  def get_produtos_por_categoria(self, categoria_id):
   return list(self.db.produtos.find({"categoria_id": categoria_id}))

  def get_produto(self, produto_id):
    return self.db.produtos.find_one({"_id": produto_id})