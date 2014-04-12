from flask import Flask, send_file, render_template, g, abort, request
import os
import sqlite3

IMAGE_DIR = os.getcwd()
DATABASE = os.path.join(IMAGE_DIR, 'images.db')

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(_):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def initialize_db():
    with app.app_context():
        cursor = get_db().cursor()
        cursor.execute('create table if not exists images (filename text, description text, primary key (filename))')

@app.route("/images/<filename>")
def serve_file(filename):
    return send_file(os.path.join(IMAGE_DIR, filename))

@app.route("/")
def index():
    insert_new_files()
    remove_missing_files()
    return render_template('index.html', images=list_images())

def is_image(fn):
    lfn = fn.lower()
    return lfn.endswith('.jpg') or lfn.endswith('.png')
  
def list_images():
    cursor = get_db().execute('select filename, description from images')
    files = []
    for row in cursor: 
        files.append({'filename': row[0], 'description': row[1]})
    return files

def insert_new_files():
    conn = get_db()
    for fn in os.listdir(IMAGE_DIR):
        if is_image(fn):
            conn.execute("insert or ignore into images values(?, '')", [fn])
    conn.commit()

@app.route('/images/<filename>/description', methods=['PUT'])
def save_description(filename):
    db = get_db()
    db.execute('update images set description=? where filename=?', [request.form['description'], filename])
    db.commit()
    # api call
    return '', 200

def remove_missing_files():
    to_remove = []
    db = get_db()
    rows = db.execute('select filename from images')
    for row in rows:
        if not os.path.exists(os.path.join(IMAGE_DIR, row[0])):
            to_remove.append([row[0]])
    db.executemany('delete from images where filename=?', to_remove)

@app.route('/submit')
def submit(form):
    images = list_images()
    # TODO render image list in some ways and submit to blogging service
    return render_template('index.html', message='submitted')

if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)
