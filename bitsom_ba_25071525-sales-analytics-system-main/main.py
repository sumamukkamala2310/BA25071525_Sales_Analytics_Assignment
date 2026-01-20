"""
Sales Analytics System
Business Analytics Assignment
Author: Suma Mukkamala (Roll No: BA25071525)
"""


from file_handler import read_sales_data, save_enriched_data
from data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    enrich_sales_data
)
from utils.api_handler import fetch_all_products, create_product_mapping
from report_generator import generate_sales_report


def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # [1/10] Read sales data
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data("data\sales_data.txt")
        print(f"Successfully read {len(raw_lines)} transactions")

        # [2/10] Parse and clean data
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"Parsed {len(transactions)} records")

        # [3/10] Display filter options
        print("[3/10] Filter Options Available:")
        regions = sorted(set(tx["Region"] for tx in transactions))
        print(f"Regions: {', '.join(regions)}")
        print("Amount Range: ₹500 - ₹500,000")

        # [4/10] Ask user for filters
        choice = input("Do you want to filter data? (y/n): ").lower()

        region = None
        min_amt = None
        max_amt = None

        if choice == "y":
            region = input("Enter region (or press Enter to skip): ").strip() or None

            min_amt_input = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amt_input = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amt = float(min_amt_input) if min_amt_input else None
            max_amt = float(max_amt_input) if max_amt_input else None

        # [4/10 continued] Validate and filter
        print("[4/10] Validating transactions...")
        valid_tx, invalid_count, summary = validate_and_filter(
            transactions,
            region=region,
            min_amount=min_amt,
            max_amount=max_amt
        )

        print(f"Valid: {summary['final_count']} | Invalid: {summary['invalid']}")

        # [5/10] Perform analytics
        print("[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_tx)
        print(f"Total Revenue: ₹{total_revenue:,.2f}")
        print("Analysis complete")

        # [6/10] Fetch product data from API
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"Fetched {len(api_products)} products")

        # [7/10] Enrich sales data
        print("[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_tx = enrich_sales_data(valid_tx, product_mapping)

        matched = sum(1 for tx in enriched_tx if tx.get("API_Match"))
        success_rate = (matched / len(valid_tx)) * 100 if valid_tx else 0
        print(f"Enriched {matched}/{len(valid_tx)} transactions ({success_rate:.1f}%)")

        # [8/10] Save enriched data
        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched_tx)
        print("Saved to: data/enriched_sales_data.txt")

        # [9/10] Generate report
        print("[9/10] Generating report...")
        generate_sales_report(valid_tx, enriched_tx)
        print("Report saved to: output/sales_report.txt")

        # [10/10] Completion
        print("[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("❌ Error occurred:", e)


if __name__ == "__main__":
    main()
