import os
import django
import re
from pypdf import PdfReader

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventorysystem4.settings')
django.setup()

from dashboard.models import Product

def get_category(name):
    name_upper = name.upper()
    if 'UREA' in name_upper:
        return 'Urea'
    if 'DAP' in name_upper:
        return 'DAP'
    if 'MURIATE' in name_upper or 'MOP' in name_upper:
        return 'MOP'
    if any(x in name_upper for x in ['18.18.10', '20.10.10', '19.19.19', '10.26.26', '24:24:0', '15.15.15', '18.46.0', 'NPK', '20/20']):
        return 'NPK'
    # Generic NPK detection (3 numbers separated by dot or colon or slash)
    if re.search(r'\d{2}[\.:/]\d{2}[\.:/]\d{2}', name):
        return 'NPK'
    if any(x in name_upper for x in ['SAGARIKA', 'HUMIC', 'ORGANIC', 'COMPOST']):
        return 'Organic'
    if 'SEEDS' in name_upper:
        return 'Seeds'
    if 'PESTICIDE' in name_upper:
        return 'Pesticide'
    return 'Bio-Fertilizer' # Default

def update_products_from_pdf():
    file_path = 'FertilizersData.pdf'
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        raw_lines = text.split('\n')
        lines = []
        
        # Pre-process to merge split lines (like 130 \n 00)
        i = 0
        while i < len(raw_lines):
            line = raw_lines[i].strip()
            if not line:
                i += 1
                continue
                
            # If next line is just digits and short, merge it
            if i + 1 < len(raw_lines):
                next_line = raw_lines[i+1].strip()
                if re.match(r'^\d+$', next_line) and len(next_line) <= 3:
                     # Heuristic: if current line ends with digits (price part 1) or looks like it's missing the price
                     # Append next line
                     line = line + next_line
                     i += 1 # Skip next line
            
            lines.append(line)
            i += 1
            
        print(f"Processed {len(lines)} lines.")
        
        count = 0
        for line in lines:
            if 'Name' in line and 'weight' in line:
                continue
                
            # Parse logic
            parts = line.split()
            if len(parts) < 3:
                continue
            
            # Try to grab last two as numbers
            try:
                # Handle cases like "Urea 46.- -"
                # If price is valid float
                price_str = parts[-1]
                weight_str = parts[-2]
                
                # Check if price is float
                price = float(price_str)
                
                # Check if weight is float
                # If "Urea 46.- - 50 266", parts[-1]=266, parts[-2]=50. Correct.
                weight = float(weight_str)
                
                name = " ".join(parts[:-2])
                
                # Clean up name if it has trailing junk?
                # "Urea 46.- -" -> Name.
                
                print(f"Found: {name} | W: {weight} | P: {price}")
                
                category = get_category(name)
                
                product, created = Product.objects.get_or_create(name=name)
                product.weight = weight
                product.price = price
                product.category = category
                
                if created:
                    product.quantity = 100 # Default quantity for new products
                    print(f"Created: {name}")
                else:
                    print(f"Updated: {name}")
                
                product.save()
                    
                count += 1
                
            except ValueError:
                # Maybe fallback or log
                print(f"Skipping malformed line: {line}")
                
        print(f"Successfully updated {count} products.")

    except Exception as e:
        print(f"Error updating from PDF: {e}")

if __name__ == '__main__':
    update_products_from_pdf()
