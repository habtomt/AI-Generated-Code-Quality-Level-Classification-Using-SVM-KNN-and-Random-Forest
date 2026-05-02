import re
import json

def digitize_identity_card(raw_ocr_text):
    """
    Simulates the extraction of Personal Identifiable Information (PII) from 
    an ID card's OCR output using specialized regex patterns.
    """
    
    # regex patterns for common ID fields
    patterns = {
        "full_name": r"Name:\s*([A-Z\s]+)\n",
        "birth_date": r"DOB:\s*(\d{2}/\d{2}/\d{4})",
        "id_number": r"ID No:\s*([A-Z0-9-]+)",
        "address": r"Address:\s*(.*(?:\n.*)?)",
        "expiry_date": r"Expiry:\s*(\d{2}/\d{2}/\d{4})"
    }

    extracted_data = {}

    for field, pattern in patterns.items():
        match = re.search(pattern, raw_ocr_text, re.MULTILINE)
        if match:
            extracted_data[field] = match.group(1).strip()
        else:
            extracted_data[field] = "NOT_FOUND"

    return extracted_data

def verify_identity(data):
    """
    Simple validation logic for authentication purposes.
    """
    if data["id_number"] == "NOT_FOUND" or data["full_name"] == "NOT_FOUND":
        return False, "Missing critical identification fields."
    return True, "Verification Successful."

def main():
    # Simulated OCR result from a scanned ID card
    scanned_id_text = """
    REPUBLIC IDENTITY CARD
    Name: JANE DOE
    DOB: 12/05/1992
    ID No: 8821-X993-00
    Address: 742 Evergreen Terrace,
    Springfield, IL 62704
    Expiry: 01/01/2030
    """

    print("--- ID Card Digitization Process ---")
    
    # 1. Extraction
    digitized_data = digitize_identity_card(scanned_id_text)
    
    # 2. Display formatted output
    print(json.dumps(digitized_data, indent=4))
    
    # 3. Authentication check
    is_valid, message = verify_identity(digitized_data)
    print(f"\nStatus: {message}")

if __name__ == "__main__":
    main()