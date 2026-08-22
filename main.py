from database import get_connection
from fastapi import FastAPI
#import psycopg
from pydantic import BaseModel

app = FastAPI()

conn = get_connection()

@app.get("/")
def home():
 return {"message": "Stock API is running"}



@app.get("/products")
def get_products():
    conn = get_connection()

    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return {"products": products}





class Product(BaseModel):
    name: str
    stock: int
    price: float


@app.post("/products")
def create_product(product: Product):
    conn = get_connection()
    dbname="stock_db",
    user="postgres",
    password="your_password_here",
    host="localhost",
    port=5432



    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO products (name, stock, price)
        VALUES (%s, %s, %s)
        """,
        (product.name, product.stock, product.price)
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Product created"}


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    conn = get_connection()
    dbname="stock_db",
    user="postgres",
    password="your_password_here",
    host="localhost",
    port=5432


    cur = conn.cursor()

    cur.execute(
        """
        UPDATE products
        SET name = %s, stock = %s, price = %s
        WHERE id = %s
        """,
        (product.name, product.stock, product.price, product_id)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Product updated"}


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = get_connection()
    dbname="stock_db",
    user="postgres",
    password="your_password_here",
    host="localhost",
    port=5432


    cur = conn.cursor()

    cur.execute(
        "DELETE FROM products WHERE id = %s",
        (product_id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Product deleted"}




class ProductUpdate(BaseModel):
    name: str | None = None
    stock: int | None = None
    price: float | None = None


@app.patch("/products/{product_id}")
def patch_product(product_id: int, product: ProductUpdate):
    conn = get_connection()
    dbname="stock_db",
    user="postgres",
    password="your_password_here",
    host="localhost",
    port=5432


    cur = conn.cursor()

    if product.name is not None:
        cur.execute(
            "UPDATE products SET name = %s WHERE id = %s",
            (product.name, product_id)
        )

    if product.stock is not None:
        cur.execute(
            "UPDATE products SET stock = %s WHERE id = %s",
            (product.stock, product_id)
        )

    if product.price is not None:
        cur.execute(
            "UPDATE products SET price = %s WHERE id = %s",
            (product.price, product_id)
        )

    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Product updated"}


