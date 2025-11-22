# Configuration for CycleMap2025
try:
    from app_secrets import API_KEY
except ImportError:
    API_KEY = None
    print("Warning: secrets.py not found. API_KEY is missing.")

# Default Map Parameters
STYLE = "klokantech-basic"
SCALE_FACTOR = 2
WIDTH = 4000
HEIGHT = 3000
ZOOM = 14
PITCH = 45
BEARING = 160

# Route Styling
LINE_COLOR = "#ff920d"
LINE_WIDTH = 3
LINE_OPACITY = 0.7
