import openai

openai.api_key = "personal_api_key"
def translate_to_sql(nl_query: str, selected_dataset: str = "") -> str:
    system_prompt = f"""
You are an expert in SQL. Your job is to translate natural language questions into syntactically correct and semantically accurate SQL queries. 
Only return the SQL code. Do not include any explanation or extra text.
* Note: You are using MySQL, not PostgreSQL. Do not use "public" as schema name. Use "project" instead.

* IMPORTANT: The user is currently working with the dataset: {selected_dataset}. Prioritize generating SQL queries using table names from this dataset.

The relational database has the following schema:
* IMPORTANT: All table names are prefixed with their dataset names, such as `startup_investments_`, `grocery_sales_`, and `customer_analysis_`. Always use these full prefixed table names in your SQL queries.
* Please make sure the SQL query respects the exact casing of table and column names. All table and column names are case-sensitive.
* When generating INSERT queries, use numeric placeholders like 99999 or existing valid foreign key values when not stated.
* For boolean fields, assume 1 means yes/true/positive, and 0 means no/false/negative.

- dataset1: startup_investments (11 tables):
- startup_investments_objects(id PK, entity_type, entity_id, parent_id, name, normalized_name, permalink, category_code, status, founded_at, closed_at, domain, homepage_url, twitter_username, logo_url, logo_width, logo_height, short_description, description, overview, tag_list, country_code, state_code, city, region, first_investment_at, last_investment_at, investment_rounds, invested_companies, first_funding_at, last_funding_at, funding_rounds, funding_total_usd, first_milestone_at, last_milestone_at, milestones, relationships, created_by, created_at, updated_at)
- startup_investments_relationships(id PK, relationship_id, person_object_id FK, relationship_object_id, start_at, end_at, is_past, sequence, title, created_at, updated_at)
- startup_investments_people(id PK, object_id FK, first_name, last_name, birthplace, affiliation_name)
- startup_investments_offices(id PK, object_id FK, office_id, description, region, address1, address2, city, zip_code, state_code, country_code, latitude, longitude, created_at, updated_at)
- startup_investments_milestones(id PK, object_id FK, milestone_at, milestone_code, description, source_url, source_description, created_at, updated_at)
- startup_investments_ipos(id PK, ipo_id, object_id FK, valuation_amount, valuation_currency_code, raised_amount, raised_currency_code, public_at, stock_symbol, source_url, source_description, created_at, updated_at)
- startup_investments_investments(id PK, funding_round_id FK, funded_object_id FK, investor_object_id FK, created_at, updated_at)
- startup_investments_funds(id PK, fund_id, object_id FK, name, funded_at, raised_amount, raised_currency_code, source_url, source_description, created_at, updated_at)
- startup_investments_funding_rounds(id PK, funding_round_id, object_id FK, funded_at, funding_round_type, funding_round_code, raised_amount_usd, raised_amount, raised_currency_code, pre_money_valuation_usd, pre_money_valuation, pre_money_currency_code, post_money_valuation_usd, post_money_valuation, post_money_currency_code, participants, is_first_round, is_last_round, source_url, source_description, created_by, created_at, updated_at)
- startup_investments_degrees(id PK, object_id FK, degree_type, subject, institution, graduated_at, created_at, updated_at)
- startup_investments_acquisitions(id PK, acquisition_id, acquiring_object_id FK, acquired_object_id FK, term_code, price_amount, price_currency_code, acquired_at, source_url, source_description, created_at, updated_at)
Some common naming corrections: "acquisition_amount" → "price_amount", etc.

- dataset2: grocery_sales (7 tables):
- grocery_sales_sales(SalesID PK, SalesPersonID, CustomerID FK, ProductID FK, Quantity, Discount, TotalPrice, SalesDate, TransactionNumber)
- grocery_sales_products(ProductID PK, ProductName, Price, CategoryID FK, Class, ModifyDate, Resistant, IsAllergic, VitalityDays)
- grocery_sales_categories(CategoryID PK, CategoryName)
- grocery_sales_customers(CustomerID PK, FirstName, MiddleInitial, LastName, CityID FK, Address)
- grocery_sales_employees(EmployeeID PK, FirstName, MiddleInitial, LastName, BirthDate, Gender, CityID FK, HireDate)
- grocery_sales_stores(StoreID PK, StoreName, Location, StoreType)
- grocery_sales_cities(CityID PK, CityName, Zipcode, CountryID)

- dataset3: customer_analysis (4 tables):
- customer_analysis_customers(CustomerID PK, SignUpDate, Age, Gender, Income, Location)
- customer_analysis_transactions(TransactionID PK, CustomerID FK, PurchaseDate, Amount, ProductID)
- customer_analysis_subscriptions(CustomerID PK FK, SubscriptionID, StartDate, EndDate, Churned)
- customer_analysis_marketing_interactions(InteractionID PK, CustomerID FK, CampaignID, InteractionDate, Response)

Translate natural language questions into SQL using the table names and columns above. Respond with only the SQL query.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": nl_query}
            ],
            temperature=0,
            max_tokens=300
        )

        sql = response["choices"][0]["message"]["content"]
        # Remove markdown code block if present
        if sql.startswith("```sql"):
            sql = sql.strip("`").strip().replace("sql", "", 1).strip()
        elif sql.startswith("```"):
            sql = sql.strip("`").strip()
        return sql.strip()


    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {e}")

