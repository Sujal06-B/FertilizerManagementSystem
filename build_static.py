import os
import shutil
import sys
import django
from django.test import Client

# Add the project root to the python path
sys.path.append(os.getcwd())

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventorysystem4.settings')
django.setup()

# Create docs directory (standard for GitHub Pages)
output_dir = 'docs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize Client
client = Client()

def save_page(url, filename):
    print(f"Generating {filename} from {url}...")
    try:
        response = client.get(url)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Make static paths relative
            content = content.replace('/static/', './static/')
            
            # Disable dynamic links for the demo
            content = content.replace('href="/login/"', 'href="#" onclick="alert(\'Login is a dynamic feature and requires a backend server. It does not work on GitHub Pages static hosting.\')"')
            content = content.replace('href="/register/"', 'href="#" onclick="alert(\'Registration is a dynamic feature and requires a backend server. It does not work on GitHub Pages static hosting.\')"')
            
            with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Success: {filename}")
        else:
            print(f"Failed to get {url}: Status {response.status_code}")
    except Exception as e:
        print(f"Error generating {filename}: {e}")

# Generate Landing Page
save_page('/', 'index.html')

# Copy Static Files
source_static = 'static'
dest_static = os.path.join(output_dir, 'static')

if os.path.exists(dest_static):
    shutil.rmtree(dest_static)

if os.path.exists(source_static):
    print("Copying static files...")
    shutil.copytree(source_static, dest_static)
    print("Static files copied.")
else:
    print("Warning: Source static directory not found.")
