from pydantic import BaseModel, Field
from typing import List, Dict, Callable, Any
from openai import OpenAI
import time
import sqlite3
import json
from packages.environment import load_keys, pdf_reader, read_text_file_to_string
from sql_agent.db_functions import get_db_schema, query_database

# AVAILABLE_TOOLS: Dict[str, Callable] = {
#     # Maps the string name (used in TOOLS_SCHEMA) to the imported function object
#     "get_db_schema": get_db_schema
# }

# class ColumnSchema(BaseModel):
#     """
#     Defines the structural details for a single column.
#     """
#     column_name: str = Field(..., description="The name of the column.")
#     data_type: str = Field(..., description="The SQL data type (e.g., INT, VARCHAR, DATE).")
#     is_primary_key: bool = Field(False, description="True if this column is the primary key for the table.")
#     is_nullable: bool = Field(True, description="True if this column allows NULL values.")

# # 2. Table Schema Model
# # Represents a single table and holds a list of its columns.
# class TableSchema(BaseModel):
#     """
#     Defines the structure of a single database table, including its columns.
#     """
#     table_name: str = Field(..., description="The name of the database table.")
#     columns: List[ColumnSchema] = Field(..., description="A list of all columns belonging to this table.")

# # 3. Database Schema Model (Top Level)
# # The final model to be returned by your get_db_schema function.
# class DatabaseSchema(BaseModel):
#     """
#     The top-level schema defining the structure of the entire database.
#     This model contains a list of all tables.
#     """
#     tables: List[TableSchema] = Field(..., description="A list of all tables in the database schema.")

def db_structure_retrieve_agent(client, user_prompt: str) -> str:

    # The tool function is defined locally here (as in your original script)
    def get_db_schema(db_file: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Connects to a SQLite database and extracts the schema (table and column info).

        Args:
            db_file: The path to the SQLite database file.

        Returns:
            A dictionary where keys are table names and values are a list of
            dictionaries, each describing a column.
        """
        schema_info = {}
        conn = None

        try:
            # 1. Establish the connection
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            # 2. Get a list of all non-system tables
            # The 'sqlite_master' table holds metadata for all objects.
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = [row[0] for row in cursor.fetchall()]

            # 3. Iterate through each table to get column information
            for table_name in tables:
                # PRAGMA table_info is a special SQLite command to get column details
                cursor.execute(f"PRAGMA table_info({table_name});")
                
                # Columns: (cid, name, type, notnull, dflt_value, pk)
                columns = []
                for col in cursor.fetchall():
                    columns.append({
                        "name": col[1],
                        "type": col[2],
                        "notnull": bool(col[3]),
                        "primary_key": bool(col[5])
                    })
                
                schema_info[table_name] = columns

        except sqlite3.Error as e:
            # Handle connection or query errors
            print(f"Database Connection Error: {e}")
            return {"error": f"Database Connection Error: {e}"}

        finally:
            if conn:
                conn.close()

        # In a real tool context, it's often best to return the result as a string
        # so the LLM can easily parse it.
        return json.dumps(schema_info, indent=2)
        
    tools = [
    {
        "type": "function",
        "function": {
            "name": "get_db_schema",
            "description": get_db_schema.__doc__.strip(),
            "parameters": {
                "type": "object",
                "properties": {
                    "db_file": {
                        "type": "string",
                        "description": "The path to the SQLite database file to inspect (e.g., 'example_database.db')."
                    }
                },
                "required": ["db_file"] 
            }
        }
    }]

    system_prompt = """You are a helpful assistant. Your task is to use the get_db_schema function tool to gather information about the database schema. 
    The database name will be provided in the user prompt. You will use the database name as the parameter 'db_file' in the get_db_schema function tool. 
    Return the output with no extra commentary or analysis."""
    
    # Message history for the first API call
    input_list = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # 1. First API call: The model decides to call the tool
    response = client.chat.completions.create( # Using chat.completions.create
        model="openai/gpt-5",
        messages=input_list, # Correct key is 'messages'
        tools = tools,
        tool_choice = "auto",
    ) 

    # --- START OF FIX: Correctly process the tool call ---
    
    # 2. Get the list of tool calls from the response
    tool_calls = response.choices[0].message.tool_calls
  
    if tool_calls:
        for tool_call in tool_calls:
            if tool_call.function.name == "get_db_schema":
                
                # The arguments are a JSON string, must be parsed
                arguments = json.loads(tool_call.function.arguments)
                db_file_arg = arguments.get('db_file')
  
                # 3. Execute the function
                schema = get_db_schema(db_file_arg)

                return schema
                
    #             # 4. Append the function result to the message history
    #             input_list.append({
    #                 "role": "tool", # Use 'tool' role
    #                 "tool_call_id": tool_call.id, # Use the specific call ID
    #                 "content": schema # The JSON string output from the function
    #             })

    # # --- END OF FIX ---
    
    # # 5. Second API call: The model generates the final answer
    # # Note: Use the updated input_list (now containing the function output)
    # response2 = client.chat.completions.create(
    #     model="openai/gpt-5",
    #     # NOTE: 'instructions' is non-standard. The 'messages' parameter is used instead.
    #     # The model will rely on the initial system prompt to summarize.
    #     messages=input_list, 
    #     tools = tools,
    #     tool_choice = "none", # Instructs the model to provide a text response
    # )

    # # 6. Return the final content
    # # This access path remains correct for the final text output
    # return response2.choices[0].message.content


def main():
    key_test, api_key = load_keys()
    if key_test:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    
    user_prompt = "What is the structure of the test_db.db database?"
    
    # NOTE: You must ensure 'test_db.db' exists in the script's execution directory 
    # for the get_db_schema function to succeed.
    structure = db_structure_retrieve_agent(client, user_prompt)
    print(structure)


if __name__ == "__main__":
    main()