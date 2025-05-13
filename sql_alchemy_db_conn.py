import sqlalchemy
import pandas as pd
import urllib # Used for quoting connection string parameters if needed

# --- Database Connection Parameters ---
# IMPORTANT: Replace these placeholders with your actual SQL Server details.
# Avoid hardcoding credentials in production code. Use environment variables,
# configuration files, or secrets management tools instead.
db_server = "10.10.21.3"  # e.g., 'localhost', 'server.database.windows.net', in address
db_database = "BFS-FinalcialAdvisory" # Enter your database name
db_username = False # Optional: Use None/False for Windows Authentication
db_password = False # Optional: Use None/False for Windows Authentication
# The ODBC driver name might vary based on your installation.
# Check your installed ODBC drivers. Common examples:
# 'ODBC Driver 17 for SQL Server'
# 'SQL Server Native Client 11.0'
# 'SQL Server'
db_driver = "ODBC Driver 17 for SQL Server" # CHANGE AS NEEDED

# --- SQL Query ---
# Replace with the actual query you want to run.
sql_query = "select * from investment_types;" # Example query

# --- Connection String ---
# Using pyodbc
# For SQL Server Authentication:
if db_username and db_password:
    # Quote password in case it contains special characters
    quoted_password = urllib.parse.quote_plus(db_password)
    conn_str = (
        f"mssql+pyodbc://{db_username}:{quoted_password}@{db_server}/{db_database}?"
        f"driver={urllib.parse.quote_plus(db_driver)}"
        # Add other parameters like encrypt/trust server certificate if needed
        # f"&Encrypt=yes&TrustServerCertificate=yes"
    )
# For Windows Authentication (Trusted Connection):
else:
    conn_str = (
        f"mssql+pyodbc://@{db_server}/{db_database}?"
        f"driver={urllib.parse.quote_plus(db_driver)}&trusted_connection=yes"
        # Add other parameters like encrypt/trust server certificate if needed
        # f"&Encrypt=yes&TrustServerCertificate=yes"
    )

# --- Create SQLAlchemy Engine ---
try:
    print(f"Attempting to connect to: {db_server}/{db_database}")
    # The engine object manages connections to the database.
    engine = sqlalchemy.create_engine(conn_str)

    # Optional: Test connection (recommended)
    with engine.connect() as connection:
        print("Connection successful!")

    # --- Execute Query and Load into Pandas DataFrame ---
    print(f"\nExecuting query: {sql_query}")
    # pd.read_sql takes the SQL query and the SQLAlchemy engine (or connection)
    df = pd.read_sql(sql_query, engine)

    # --- Print the DataFrame ---
    print("\nQuery Results:")
    print(df)

except sqlalchemy.exc.SQLAlchemyError as e:
    print(f"Database connection or query error: {e}")
except ImportError as e:
    print(f"Error: A required library is missing. {e}")
    print("Please install required libraries: pip install sqlalchemy pandas pyodbc")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Dispose of the engine connection pool if it was created
    if 'engine' in locals() and engine:
        engine.dispose()
        print("\nDatabase engine disposed.")
