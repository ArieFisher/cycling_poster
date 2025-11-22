# Configuration for CycleMap2025
try:
    from app_secrets import API_KEY
except ImportError:
    API_KEY = None
    print("Warning: secrets.py not found. API_KEY is missing.")

# Default Map Parameters
STYLE = "klokantech-basic"
SCALE_FACTOR = 2
WIDTH = 3000
HEIGHT = 4000
ZOOM = 10.5
PITCH = 43
BEARING = 163

# Route Styling
LINE_COLOR = "#ff920d"
LINE_WIDTH = 3
LINE_OPACITY = 0.7