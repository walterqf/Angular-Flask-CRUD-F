from flask import Flask, jsonify, request, send_file
from pymysql import connect, cursors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

host = 'localhost'
port = 3307
dbname = 'productos'
username = 'root'
password = 'password'


def get_connection():
    conn = connect(host=host, port=port, db=dbname,
                   user=username, password=password)
    return conn


@app.get('/')
def getAll():
    conn=get_connection()
    cur=conn.cursor(cursors.DictCursor) 
    cur.execute("SELECT id, parent_id, nivel, referencia, (SELECT COALESCE(SUM(stock), 0) FROM productos p2  WHERE p2.nivel LIKE CONCAT(p1.nivel, '%')) AS stock FROM productos p1 ORDER BY nivel ASC;")
    result = cur.fetchall()
    #print(result)
    cur.close()
    conn.close()
    #print(jsonify(result))
    return jsonify(result)


@app.post('/')
def create_product():
    # print(request.get_json())
    new_product = request.get_json()
    referencia = new_product['referencia']
    parent_id = new_product['parent_id']
    stock=new_product['stock']
    nivel=new_product['nivel']
    conn = get_connection()
    cur = conn.cursor(cursors.DictCursor)
    cur.execute('INSERT INTO productos (referencia, stock, parent_id, nivel) VALUES (%s, %s, %s, %s)', (referencia, stock, parent_id, nivel))
    new_product = cur.fetchone()
    print(new_product)
    conn.commit()
    inserted_id = cur.lastrowid

    # Fetch the inserted data using the last inserted ID
    new_product=cur.execute(
        'SELECT * FROM productos WHERE id = %s',
        (inserted_id,)
    )

    # Fetch the single row that matches the inserted ID
    new_product = cur.fetchone()

    cur.close()
    conn.close()
    #print(username, email, password)
    return jsonify(new_product)


@app.delete('/<id>')
def delete_product(id):
    conn = get_connection()
    cur = conn.cursor(cursors.DictCursor)
    new_product1=cur.execute(
        'SELECT * FROM productos WHERE id = %s',
        (id)
    )
    new_product1 = cur.fetchone()
    cur.execute('delete from productos where id=%s', (id,))
    new_product = cur.fetchone()
    conn.commit()
    
    #inserted_id = cur.lastrowid
    
        # Fetch the single row that matches the inserted ID
    # Fetch the inserted data using the last inserted ID
    cur.close()
    conn.close()
  
    if new_product1 is None:
        return jsonify({'Message': 'Product not found'})
    #print(user)
    return jsonify(new_product1)


@app.put('/<id>')
def update_product(id):
    conn = get_connection()
    cur = conn.cursor(cursors.DictCursor)
    new_product = request.get_json()
    referencia = new_product['referencia']
    parent_id= new_product['parent_id']
    stock = new_product['stock']
    nivel = new_product['nivel']
    cur.execute(
        'update productos set referencia = %s, stock = %s, parent_id=%s, nivel=%s where id = %s', (referencia, stock, parent_id, nivel, id))
    product_updated = cur.fetchone()
    conn.commit()
    

    # Fetch the inserted data using the last inserted ID
    product_updated=cur.execute(
        'SELECT * FROM productos WHERE id = %s',
        (id)
    )

    # Fetch the single row that matches the inserted ID
    product_updated = cur.fetchone()
    cur.close()
    conn.close()
    print(product_updated)
    if product_updated is None:
        return jsonify({'Message': 'Product not found'}), 404
    print(product_updated)
    return jsonify(product_updated)


@app.get('/<id>')
def get_product(id):
    print(id)
    conn = get_connection()
    cur = conn.cursor(cursors.DictCursor)
    cur.execute('select * from productos where id = %s', (id,))
    product = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if product is None:
        return jsonify({'Message': 'Product not found'}), 404
    print(product)
    return jsonify(product)

"""@app.get('/')
def home():
    return send_file('static/index.html')

"""
if __name__ == '__main__':
    app.run(debug=True)