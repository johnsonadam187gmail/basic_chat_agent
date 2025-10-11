import sqlite3
import json
from pydantic import BaseModel, Field
from typing import List

__all__ = ["get_db_schema", "query_database"]


def get_db_schema(db_file: str) -> str:
    """
    Connects to the specified SQLite database file and returns a JSON string 
    of all tables and columns.
    """
    # The universal SQLite schema query
    schema_query = """
    SELECT 
        tbl_name AS table_name,
        name AS column_name,
        type AS data_type
    FROM 
        sqlite_master AS m, 
        pragma_table_info(m.tbl_name) AS p
    WHERE 
        m.type = 'table'
    ORDER BY 
        table_name, 
        cid;
    """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cursor.execute(schema_query)
        
        # Get column names for the result set
        columns = [description[0] for description in cursor.description]
        
        # Fetch results and format them into a list of dictionaries
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        
        return json.dumps(results, indent=2)

    except sqlite3.Error as e:
        return f"Database Connection Error: {e}"


def query_database(sql_query: str) -> str:
    """
    Executes a read-only SQL query against the 'test_db.db' database
    and returns the results as a string.

    The database has a single table named 'products' with columns:
    id, name, category, and price.
    
    Args:
        sql_query: The complete and valid SQL query to execute. 
                   MUST be a SELECT query. E.g., 'SELECT * FROM products WHERE category = "Electronics"'

    Returns:
        A string representation of the query results or an error message.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect("test_db.db")
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(sql_query)
        
        # Fetch the column names (headers)
        columns = [description[0] for description in cursor.description]
        
        # Fetch all results
        results = cursor.fetchall()
        
        # Close the connection
        conn.close()
        
        # Format the results into a readable string
        formatted_results = f"Columns: {', '.join(columns)}\n"
        for row in results:
            formatted_results += f"{row}\n"
            
        return formatted_results

    except Exception as e:
        return f"Database Error: {e}"
    
if __name__ == "__main__":
    # Example usage
    query = 'SELECT SUM("price") FROM products WHERE category = "Electronics"'
    print(query_database(query))
