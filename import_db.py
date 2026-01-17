import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventorysystem4.settings')
django.setup()

from django.contrib.auth.models import User

def load_data():
    if User.objects.count() == 0:
        print("Database is empty. Loading initial data from db_dump.json...")
        try:
            call_command('loaddata', 'db_dump.json')
            print("Data loaded successfully.")
        except Exception as e:
            print(f"Error loading data: {e}")
    else:
        print("Database already contains data. Skipping initial data load.")

if __name__ == '__main__':
    load_data()
