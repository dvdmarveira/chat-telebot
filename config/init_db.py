from database import Database
from bson import ObjectId

def init_db():
       db = Database()
       
       # Inserir categorias
       categorias = [
           {"nome": "Bolos", "emoji": "🍰"},
           {"nome": "Cupcakes", "emoji": "🧁"},
           {"nome": "Brownies", "emoji": "🍫"}
       ]
       
       for categoria in categorias:
           categoria_id = db.db.categorias.insert_one(categoria).inserted_id
           
           # Inserir produtos da categoria
           if categoria["nome"] == "Bolos":
               produtos = [
                   {"categoria_id": categoria_id, "nome": "Bolo de chocolate", "preco": 10.00},
                   {"categoria_id": categoria_id, "nome": "Bolo de milho", "preco": 10.00},
               ]
               db.db.produtos.insert_many(produtos)