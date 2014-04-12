import unittest
import tempfile
import os
import app

class Tests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)
        app.IMAGE_DIR = self.tempdir
        app.DATABASE = os.path.join(app.IMAGE_DIR, 'images.db')
        app.initialize_db()
        self.files = ['images.db']
    
    def tearDown(self):
        print self.files
        for fn in self.files:
            os.remove(os.path.join(self.tempdir, fn))
        self.files = []
        os.rmdir(self.tempdir)
    
    def touch(self, fn):
        self.files.append(fn)
        open(os.path.join(self.tempdir, fn), 'w').close()
    
    def remove(self, fn):
        self.files.remove(fn)
        os.remove(os.path.join(self.tempdir, fn))

    def test_assert_empty_database_on_init(self):
        with app.app.app_context():
            db = app.get_db()
            rows = db.execute('select * from images').fetchall()
            self.assertEqual(0, len(rows), 'expected no images in database')

    def test_can_add_file(self):
        with app.app.app_context():
            self.touch('foo.jpg')
            app.insert_new_files()
            db = app.get_db()
            rows = db.execute('select filename from images').fetchall()
            self.assertEqual('foo.jpg', rows[0][0], 'expected foo.jpg in database')

    def test_can_remove_file(self):
        with app.app.app_context():
            self.touch('foo.jpg')
            app.insert_new_files()
            self.remove('foo.jpg')
            app.remove_missing_files()
            db = app.get_db()
            rows = db.execute('select filename from images').fetchall()
            self.assertEqual(0, len(rows), 'expected no images in database')
