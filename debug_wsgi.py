import os
import sys

# Expected path for your app
EXPECTED_PATH = '/home/ariefisher/cycling_poster'

print(f"Current working directory: {os.getcwd()}")
print(f"System path: {sys.path}")

# Check if the path is in sys.path
if EXPECTED_PATH in sys.path:
    print(f"SUCCESS: {EXPECTED_PATH} is in sys.path")
else:
    print(f"ERROR: {EXPECTED_PATH} is NOT in sys.path")
    print("Did you update the WSGI file?")

# Check if app.py exists
if os.path.exists(os.path.join(EXPECTED_PATH, 'app.py')):
    print(f"SUCCESS: app.py found in {EXPECTED_PATH}")
else:
    print(f"ERROR: app.py NOT found in {EXPECTED_PATH}")
