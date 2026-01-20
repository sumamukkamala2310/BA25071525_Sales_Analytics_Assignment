# Business Analytics Assignment
# Author: Suma Mukkamala (BA25071525)


def parse_transactions(raw_lines):
    """
    Parses raw sales data lines into clean transaction dictionaries.
    """

    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        if len(parts) != 8:
            continue

        tid, date, pid, pname, qty, price, cid, region = parts

        pname = pname.replace(",", "")
        qty = qty.replace(",", "")
        price = price.replace(",", "")

        try:
            qty = int(qty)
            price = float(price)
        except ValueError:
            continue

        transactions.append({
            "TransactionID": tid,
            "Date": date,
            "ProductID": pid,
            "ProductName": pname,
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": cid,
            "Region": region
        })

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0
    filtered_by_region = 0
    filtered_by_amount = 0

    required_fields = [
        "TransactionID", "Date", "ProductID",
        "ProductName", "Quantity", "UnitPrice",
        "CustomerID", "Region"
    ]

    for tx in transactions:
        if not all(field in tx for field in required_fields):
            invalid_count += 1
            continue

        if (
            tx["Quantity"] <= 0 or
            tx["UnitPrice"] <= 0 or
            not tx["TransactionID"].startswith("T") or
            not tx["ProductID"].startswith("P") or
            not tx["CustomerID"].startswith("C")
        ):
            invalid_count += 1
            continue

        amount = tx["Quantity"] * tx["UnitPrice"]

        if region and tx["Region"] != region:
            filtered_by_region += 1
            continue

        if min_amount and amount < min_amount:
            filtered_by_amount += 1
            continue

        if max_amount and amount > max_amount:
            filtered_by_amount += 1
            continue

        valid_transactions.append(tx)

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, summary

# =======================
# PART 2: ANALYTICS
# =======================

def calculate_total_revenue(transactions):
    total = 0.0
    for tx in transactions:
        total += tx["Quantity"] * tx["UnitPrice"]
    return total


def region_wise_sales(transactions):
    regions = {}
    total_revenue = calculate_total_revenue(transactions)

    for tx in transactions:
        region = tx["Region"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if region not in regions:
            regions[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        regions[region]["total_sales"] += amount
        regions[region]["transaction_count"] += 1

    for region in regions:
        regions[region]["percentage"] = round(
            (regions[region]["total_sales"] / total_revenue) * 100, 2
        )

    return dict(
        sorted(regions.items(), key=lambda x: x[1]["total_sales"], reverse=True)
    )


def top_selling_products(transactions, n=5):
    products = {}

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if name not in products:
            products[name] = {"quantity": 0, "revenue": 0.0}

        products[name]["quantity"] += qty
        products[name]["revenue"] += revenue

    return sorted(
        products.items(),
        key=lambda x: x[1]["quantity"],
        reverse=True
    )[:n]


def customer_analysis(transactions):
    customers = {}

    for tx in transactions:
        cid = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if cid not in customers:
            customers[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0
            }

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1

    for cid in customers:
        customers[cid]["avg_order_value"] = round(
            customers[cid]["total_spent"] / customers[cid]["purchase_count"], 2
        )

    return dict(
        sorted(customers.items(), key=lambda x: x[1]["total_spent"], reverse=True)
    )


def daily_sales_trend(transactions):
    daily = {}

    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily:
            daily[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily[date]["revenue"] += amount
        daily[date]["transaction_count"] += 1
        daily[date]["customers"].add(tx["CustomerID"])

    return {
        date: {
            "revenue": data["revenue"],
            "transactions": data["transaction_count"],
            "unique_customers": len(data["customers"])
        }
        for date, data in sorted(daily.items())
    }


def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    peak_date = None
    max_revenue = 0
    txn_count = 0

    for date, data in daily.items():
        if data["revenue"] > max_revenue:
            max_revenue = data["revenue"]
            txn_count = data["transactions"]
            peak_date = date

    return peak_date, max_revenue, txn_count


def low_performing_products(transactions, threshold=10):
    products = {}

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if name not in products:
            products[name] = {"quantity": 0, "revenue": 0.0}

        products[name]["quantity"] += qty
        products[name]["revenue"] += revenue

    return [
        (name, data["quantity"], data["revenue"])
        for name, data in products.items()
        if data["quantity"] < threshold
    ]

def enrich_sales_data(valid_transactions, product_mapping):
    """
    Enriches valid transactions with API product data.
    """
    enriched = []

    for tx in valid_transactions:
        enriched_tx = tx.copy()

        # Convert ProductID like 'P101' → 101
        try:
            product_num = int(tx["ProductID"][1:])
        except (ValueError, IndexError):
            product_num = None

        api_data = product_mapping.get(product_num)

        if api_data:
            enriched_tx["API_Category"] = api_data["category"]
            enriched_tx["API_Brand"] = api_data["brand"]
            enriched_tx["API_Rating"] = api_data["rating"]
            enriched_tx["API_Match"] = True
        else:
            enriched_tx["API_Category"] = None
            enriched_tx["API_Brand"] = None
            enriched_tx["API_Rating"] = None
            enriched_tx["API_Match"] = False

        enriched.append(enriched_tx)

    return enriched
