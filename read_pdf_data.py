from pypdf import PdfReader
import re

file_path = 'FertilizersData.pdf'

def parse_pdf():
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        lines = text.split('\n')
        # Filter empty lines
        lines = [line.strip() for line in lines if line.strip()]
        
        parsed_data = []
        
        # Regex: Name (anything) space Weight (number) space Price (number)
        # We work backwards. Last token is price, second last is weight.
        
        for k, line in enumerate(lines):
            # Skip header
            if line.lower().startswith("name") and "weight" in line.lower():
                continue
                
            # Handle the 130 00 split case specifically or generic merge?
            # If line doesn't end with two numbers, maybe check next line?
            # But "130" looks like a number.
            
            parts = line.split()
            if len(parts) < 3:
                # meaningful partial line?
                continue
                
            # Check if last two are numbers
            try:
                price = float(parts[-1])
                weight = float(parts[-2])
                name = " ".join(parts[:-2])
                parsed_data.append({'name': name, 'weight': weight, 'price': price})
            except ValueError:
                # Maybe the price is split?
                # Case: "Krushiudhyog 20.10.10 50 130" (next line "00")
                # parts[-1] is 130. parts[-2] is 50. Name is "Krushiudhyog 20.10.10".
                # If we accept this, we record price as 130. That's wrong.
                # But typically PDF extraction joins text? 
                # Let's inspect the "00" line.
                pass
        
        # Correction logic:
        # If we see a very small line like "00" or just numbers, it might be a continuation.
        # But let's look at the raw output again.
        # "Krushiudhyog 20.10.10 50 130" -> Parsed as Name:..., W:50, P:130.
        # Next line: "00". len(parts)=1.
        # "DAP..."
        
        # A simple heuristic:
        # If we have a line that we parsed, but the next line is just a number (continuation of price), append it?
        # Or better: Normalize the text first.
        # "130\n00" -> "13000"? No.
        # "130\n0" -> "1300"
        
        # Let's try to just print what we parsed strictly first to see what's broken.
        for item in parsed_data:
            print(item)
            
    except Exception as e:
        print(f"Error: {e}")

parse_pdf()
