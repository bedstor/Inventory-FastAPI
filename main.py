from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3


app = FastAPI()

class Item(BaseModel):
    name: str
    quantity: int
    price: int
    


@app.post("/items")
async def add_item(item: Item):
    db = sqlite3.connect("inventory_con.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO inventory (item_name, price, quantity) VALUES (?, ?, ?)",
    (item.name, item.price, item.quantity))
    db.commit()
    return {"message" : "Товар успешно добавлен", "item_name" : item.name}


@app.delete("/items/{item_id}")
async def del_item(item_id: int):
    db = sqlite3.connect("inventory_con.db")
    cursor = db.cursor()
    cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,) )
    db.commit()
    db.close()
    return {"message" : "товар удалён"}


@app.put("/items/{item_id}")
async def put_item(item_id: int, item: Item):
    db = sqlite3.connect("inventory_con.db")
    cursor = db.cursor()
    cursor.execute("""UPDATE inventory SET item_name = ?, quantity = ?, price = ?
    WHERE id = ?""", (item.name, item.quantity, item.price, item_id))
    db.commit()
    db.close()
    return {"message" : "Данные о товаре обновлены"}

