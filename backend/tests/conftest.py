import sys
import os

# Make backend the root (so app.main can be imported)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

print("PYTHONPATH updated ->", ROOT_DIR)
