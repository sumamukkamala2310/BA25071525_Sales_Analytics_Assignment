"""
Report Generator
Author: Suma Mukkamala (BA25071525)
"""


from datetime import datetime
from collections import defaultdict
import os


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    if not transactions:
        print("No transactions available. Report not generated.")
        return

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    total_revenue = 0
    total_transactions = len(transactions)
    date_list = []

    region_sales = defaultdict(float)
    region_count = defaultdict(int)

    customer_spend = defaultdict(float)
    product_sales = defaultdict(lambda: {"qty": 0, "revenue": 0})

    daily_sales = defaultdict(lambda: {"revenue": 0, "transactions": 0, "customers": set()})

    enriched_count = 0
    failed_products = set()

    for tx in enriched_transactions:
        qty = tx["Quantity"]
        price = tx["UnitPrice"]
        amount = qty * price
        date = tx["Date"]
        region = tx["Region"]
        customer = tx["CustomerID"]
        product = tx["ProductName"]

        total_revenue += amount
        date_list.append(date)

        region_sales[region] += amount
        region_count[region] += 1

        customer_spend[customer] += amount
        product_sales[product]["qty"] += qty
        product_sales[product]["revenue"] += amount

        daily_sales[date]["revenue"] += amount
        daily_sales[date]["transactions"] += 1
        daily_sales[date]["customers"].add(customer)

        if tx.get("API_Match"):
            enriched_count += 1
        else:
            failed_products.add(product)

    avg_order_value = total_revenue / total_transactions if total_transactions else 0
    date_range = f"{min(date_list)} to {max(date_list)}"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("SALES ANALYTICS REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Records Processed: {total_transactions}\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 60 + "\n")
        for region in sorted(region_sales, key=region_sales.get, reverse=True):
            percent = (region_sales[region] / total_revenue) * 100
            f.write(
                f"{region}: ₹{region_sales[region]:,.2f} | "
                f"{percent:.2f}% | {region_count[region]} transactions\n"
            )

        f.write("\nTOP 5 PRODUCTS\n")
        f.write("-" * 60 + "\n")
        top_products = sorted(
            product_sales.items(),
            key=lambda x: x[1]["revenue"],
            reverse=True
        )[:5]

        for i, (prod, data) in enumerate(top_products, 1):
            f.write(f"{i}. {prod} | Qty: {data['qty']} | Revenue: ₹{data['revenue']:,.2f}\n")

        f.write("\nTOP 5 CUSTOMERS\n")
        f.write("-" * 60 + "\n")
        top_customers = sorted(
            customer_spend.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        for i, (cust, amt) in enumerate(top_customers, 1):
            f.write(f"{i}. {cust} | Total Spent: ₹{amt:,.2f}\n")

        f.write("\nDAILY SALES TREND\n")
        f.write("-" * 60 + "\n")
        for date in sorted(daily_sales):
            d = daily_sales[date]
            f.write(
                f"{date}: ₹{d['revenue']:,.2f} | "
                f"{d['transactions']} txns | "
                f"{len(d['customers'])} customers\n"
            )

        success_rate = (enriched_count / total_transactions) * 100 if total_transactions else 0

        f.write("\nAPI ENRICHMENT SUMMARY\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write("Products not enriched:\n")

        for p in failed_products:
            f.write(f"- {p}\n")

    print("Sales report generated successfully.")
