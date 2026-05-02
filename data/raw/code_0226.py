import re
import json

def extract_invoice_data(raw_text):
    """
    Simulates OCR text processing and extracts key invoice fields using regex.
    In a production environment, 'raw_text' would come from pytesseract.image_to_string().
    """
    
    # Regular expression patterns for common invoice fields
    patterns = {
        "invoice_number": r"(?:Invoice\s?#|Inv-)\s?(\w+)",
        "date": r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        "vendor": r"^(.*?)\n",  # Assumes vendor name is on the first line
        "total_amount": r"(?:Total|Amount Due):\s?\$?(\d+\.\d{2})",
        "items": r"(\d+)\s+([\w\s]+?)\s+\$?(\d+\.\d{2})"
    }

    data = {
        "vendor": re.search(patterns["vendor"], raw_text).group(1).strip() if re.search(patterns["vendor"], raw_text) else None,
        "invoice_number": re.search(patterns["invoice_number"], raw_text).group(1) if re.search(patterns["invoice_number"], raw_text) else None,
        "date": re.search(patterns["date"], raw_text).group(1) if re.search(patterns["date"], raw_text) else None,
        "total_amount": re.search(patterns["total_amount"], raw_text).group(1) if re.search(patterns["total_amount"], raw_text) else None,
        "line_items": []
    }

    # Extract multiple line items
    item_matches = re.finditer(patterns["items"], raw_text)
    for match in item_matches:
        data["line_items"].append({
            "quantity": match.group(1),
            "description": match.group(2).strip(),
            "price": match.group(3)
        })

    return data

def main():
    # Simulated output from an OCR engine (e.g., Tesseract)
    ocr_sample = """
    Tech Solutions Inc.
    123 Innovation Drive, CA
    Invoice #INV-99821
    Date: 04/23/2026

    Items:
    2 Wireless Mouse      $50.00
    1 Mechanical Keyboard $120.00
    3 USB-C Cables        $45.00

    Total Amount Due: $215.00
    """

    print("--- Processing Invoice OCR Text ---")
    invoice_details = extract_invoice_data(ocr_sample)
    
    # Output the digitized data as a JSON string for easy integration
    print(json.dumps(invoice_details, indent=4))

if __name__ == "__main__":
    main()