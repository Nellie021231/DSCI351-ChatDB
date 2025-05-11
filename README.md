# ChatDB: Natural Language to SQL Interface for MySQL

**Author:** Yinuo Chen  
**Date:** May 10, 2025
---

## Project Description

ChatDB is a terminal-based application that allows users to interact with a MySQL database using natural language queries. The system uses OpenAI's GPT-3.5 to convert user input into valid SQL queries, then executes them and returns the results in a readable format.

Users can:
- Query across three real-world datasets (Startup Investments, Grocery Sales, Customer Analysis)
- Explore database schema
- Perform both analytical and modification operations
- Dynamically switch datasets and request sample questions

---

## User Guide

### 1. Clone the Repository & Set Up Virtual Environment

```bash
git clone <>
cd ChatDB
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Prerequisites

- **MySQL Server** must be installed and running locally on port 3306.

Create a MySQL database named `project`:

```sql
CREATE DATABASE project;
```

- **Kaggle API Key** (for automatic dataset download via kagglehub):  
Create a `~/.kaggle/kaggle.json` file containing your Kaggle credentials, or set the token through `kagglehub`.

- **OpenAI API Key**:  
In `nl_sql.py`, replace the line:

```python
openai.api_key = "YOUR_API_KEY"
```

with your actual [OpenAI API key](https://platform.openai.com/account/api-keys).  

---

## File Structure

| File                 | Description                                              |
|----------------------|----------------------------------------------------------|
| `main.py`            | Main terminal interface for ChatDB                      |
| `nl_sql.py`          | Converts user questions to SQL using OpenAI GPT-3.5     |
| `db.py`              | Executes SQL queries using SQLAlchemy                   |
| `datasets_import.py` | Loads and imports CSV data into MySQL                   |
| `get_schema.py`      | Extracts schema (PK/FK info) from MySQL for prompt use  |
| `requirements.txt`   | Lists Python dependencies                               |
| `README.md`          | This file                                               |

---

## How It Works

1. **Dataset Selection** – User selects one of the 3 datasets at the beginning.
2. **Query Parsing** – Natural language question is input through terminal.
3. **Prompt Injection** – A schema-specific prompt is sent to GPT-3.5.
4. **SQL Generation** – GPT-3.5 returns a syntactically valid, case-sensitive SQL.
5. **Execution** – SQLAlchemy executes the query in MySQL.
6. **Display** – Output is formatted with Pandas and printed in terminal.

---

## Tips for Using

- Type `switch` to change datasets at any point.
- Type `help` to get example questions based on the selected dataset.
- You can try queries like:

```text
Which companies were acquired in 2020?
List all products sold in category ID 4.
Update the address of customer 99999 to '456 New St'.
```
---

## Testing

```bash
python datasets_import.py   # Load all datasets
python main.py              # Start ChatDB interface
```
