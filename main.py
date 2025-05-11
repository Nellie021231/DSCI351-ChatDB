from nl_sql import translate_to_sql
from db import run_sql_query
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from db import engine

def get_sample_questions(dataset):
    if dataset == "startup_investments":
        return [
            "List all funding round types.",
            "Which companies were acquired in 2020?",
            "Show IPO details with valuation above $1B.",
            "Find all people affiliated with Stanford."
        ]
    elif dataset == "grocery_sales":
        return [
            "Show top 5 selling products by quantity.",
            "List all employees hired after 2015.",
            "What is the average discount by product category?",
            "List all stores in a specific city."
        ]
    elif dataset == "customer_analysis":
        return [
            "List customers who churned in the last year.",
            "What is the average amount spent per transaction?",
            "Show marketing campaigns with the highest positive response rate.",
            "Find all customers older than 30 with income over 50k."
        ]
    return []

def main():
    print("Welcome to ChatDB! Let me know if you have any questions! You can use 'exit' to quit.\n")

    selected_dataset = None
    # dataset selection
    while not selected_dataset:
        print("Please select a dataset to work with:")
        print("1. Startup Investments – data on companies, funding rounds, acquisitions, and investor relationships.")
        print("2. Grocery Sales – transactional sales data, store/product/customer details from a retail environment.")
        print("3. Customer Analysis – customer behavior including purchases, subscriptions, and marketing responses.")
        choice = input("Enter the number of your choice: ").strip()

        if choice == '1':
            selected_dataset = "startup_investments"
        elif choice == '2':
            selected_dataset = "grocery_sales"
        elif choice == '3':
            selected_dataset = "customer_analysis"
        else:
            print("Invalid selection. Please enter number 1/2/3.\n")

    print(f"\nYou selected: {selected_dataset.replace('_', ' ').title()}\n")
    print("Here are some example questions you can try:")
    for q in get_sample_questions(selected_dataset):
        print(f"- {q}")
    print()

    # start chatDB
    while True:
        user_input = input(f"[{selected_dataset}] Question (type 'switch' to change dataset) > ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        if not user_input.strip():
            print("\nPlease enter a question.\n")
            continue

        if user_input.lower() in ['switch', 'change dataset']:
            selected_dataset = None
            while not selected_dataset:
                print("Please select a dataset to switch to:")
                print("1. Startup Investments – data on companies, funding rounds, acquisitions, and investor relationships.")
                print("2. Grocery Sales – transactional sales data, store/product/customer details from a retail environment.")
                print("3. Customer Analysis – customer behavior including purchases, subscriptions, and marketing responses.")
                choice = input("Enter the number of your choice: ").strip()
                if choice == '1':
                    selected_dataset = "startup_investments"
                elif choice == '2':
                    selected_dataset = "grocery_sales"
                elif choice == '3':
                    selected_dataset = "customer_analysis"
                else:
                    print("Invalid selection. Please enter number 1/2/3.\n")

            print(f"\nSwitched to: {selected_dataset.replace('_', ' ').title()}\n")
            print("Here are some example questions you can try:")
            for q in get_sample_questions(selected_dataset):
                print(f"- {q}")
            print()
            continue  # back to top of loop after switching

        try:
            sql_query = translate_to_sql(user_input, selected_dataset)
            print(f"\nGenerated SQL:\n{sql_query}\n")

            lowered = sql_query.strip().lower()
            if lowered.startswith(("insert", "update", "delete")):
                # Use direct execution for write operations
                with engine.connect() as conn:
                    conn.execute(text(sql_query))
                    conn.commit()
                print("Statement executed successfully.\n")

            else:
                # Use pandas for read queries
                result_df = run_sql_query(sql_query)

                if result_df.empty:
                    print("No results found.\n")
                else:
                    print("Result:")
                    print(result_df.to_string(index=False))
                    print()

        except SQLAlchemyError as db_err:
            print(f"Database Error: {db_err}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
