import os
import sys

# Menambahkan root folder ke sys.path agar Vercel dapat mengimpor app.py
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app

# Vercel mencari WSGI callable dengan nama 'app'
app = app

