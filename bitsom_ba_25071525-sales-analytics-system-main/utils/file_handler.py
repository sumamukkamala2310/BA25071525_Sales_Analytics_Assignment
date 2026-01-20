# Business Analytics Assignment
# Author: Suma Mukkamala (BA25071525)


def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns list of raw data lines (strings).
    """

    encodings = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            with open(filename, "r", encoding=encoding) as file:
                lines = [line.strip() for line in file if line.strip()]

                # Skip header
                if lines and lines[0].lower().startswith("transactionid"):
                    lines = lines[1:]

                return lines

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print("Error: File not found.")
            return []

    print("Error: Unable to read file due to encoding issues.")
    return []

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched sales transactions to a pipe-delimited text file.
    """

    try:
        with open(filename, "w", encoding="utf-8") as file:
            # Header
            header = (
                "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
                "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
            )
            file.write(header)

            for tx in enriched_transactions:
                row = (
                    f"{tx.get('TransactionID')}|{tx.get('Date')}|"
                    f"{tx.get('ProductID')}|{tx.get('ProductName')}|"
                    f"{tx.get('Quantity')}|{tx.get('UnitPrice')}|"
                    f"{tx.get('CustomerID')}|{tx.get('Region')}|"
                    f"{tx.get('API_Category')}|{tx.get('API_Brand')}|"
                    f"{tx.get('API_Rating')}|{tx.get('API_Match')}\n"
                )
                file.write(row)

        print("Enriched sales data saved successfully.")

    except Exception as e:
        print("Error saving enriched data:", e)
