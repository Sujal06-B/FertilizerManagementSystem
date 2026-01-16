import os
import django
import pandas as pd

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventorysystem4.settings')
django.setup()

from dashboard.models import Product

def update_products():
    file_path = 'Fertilizers .xlsx'
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        df = pd.read_excel(file_path)
        # Rename columns for clarity based on previous inspection
        # Previous inspection: 0->Name, 1->weight, 2->price
        # DataFrame columns were Unnamed: 0, Unnamed: 1, Unnamed: 2 with row 0 as header
        
        # Reload with header=1 if the first row (index 0) is actually the header
        # Based on "0 Name weight price", it seems the first row in the dataframe was the header.
        # Let's inspect again carefully.
        # "0 Name weight price" -> row 0 values.
        # The actual header was Unnamed.
        # So we should read with header=1? No, header=0 reads the first line as header.
        # If the output was:
        #               Unnamed: 0 Unnamed: 1 Unnamed: 2
        # 0                   Name    weight       price
        # 1       Krushisanjeevani         50       1250
        
        # This means the very first line of the file is empty or has "Unnamed" or pandas didn't detect it.
        # It looks like the file has the header in the first row of data (index 0).
        
        df = pd.read_excel(file_path, header=None)
        
        # Iterate over rows starting from index 1 (since 0 is the header "Name", "weight", "price")
        # Adjust column indices: 0 -> Name, 1 -> Weight, 2 -> Price
        
        for index, row in df.iterrows():
            if index == 0:
                continue # Skip header row
            
            name = row[0]
            try:
                weight = float(row[1])
            except:
                weight = 0.0
            
            try:
                price = float(row[2])
            except:
                price = 0.0

            if pd.isna(name):
                continue
                
            print(f"Processing: {name}, Weight: {weight}, Price: {price}")
            
            product, created = Product.objects.get_or_create(name=name)
            
            product.weight = weight
            product.price = price
            
            if created:
                product.quantity = 100 # Default
                product.category = 'Bio-Fertilizer' # Default
                product.company = 'Gen' # Default
                print(f"Created new product: {name}")
            else:
                print(f"Updated existing product: {name}")
            
            product.save()
            
        print("Database updated successfully.")

    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == '__main__':
    update_products()
