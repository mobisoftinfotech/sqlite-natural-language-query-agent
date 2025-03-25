import sqlite3
from typing import List, Dict, Any
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import os
from dotenv import load_dotenv

class SQLiteAgent:
    def __init__(self, db_path: str):
        self.db_path = db_path

        # Load the Environment variables from .env file
        load_dotenv()
        
        # Initialize the LLM with HuggingFace
        self.llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            task="text-generation",
            temperature=0.1,
            max_new_tokens=250,
            do_sample=False,
            model_kwargs={
                "max_length": 512
            },
            huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_TOKEN"),
            client_options={"timeout": 60.0}
        )

        
        # Initialize the database
        self.db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        
        # Create the chain
        self.chain = SQLDatabaseChain.from_llm(
            llm=self.llm,
            db=self.db,
            verbose=True
        )
    
    def query(self, question: str) -> str:
        """Execute a natural language query on the database."""
        try:
            result = self.chain.invoke({"query": question})
            return f"Result: {result['result']}"
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def get_table_info(self) -> List[Dict[str, Any]]:
        """Retrieve information about all the tables in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                table_info = []
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    
                    table_info.append({
                        "table_name": table_name,
                        "columns": [col[1] for col in columns]
                    })
                
                return table_info
        except Exception as e:
            print(f"Error getting table info: {str(e)}")
            return []
if __name__ == "__main__":
    # Initialize the agent with the existing database
    db_path = 'employee_database.db'
    
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found!")
        print("Please make sure the employee_database.db file exists in the current directory.")
        exit(1)
    
    # Initialize the agent
    agent = SQLiteAgent(db_path)
    
    # Display table information
    table_info = agent.get_table_info()
    print("\nAvailable tables in the database:")
    for table in table_info:
        print(f"\nTable: {table['table_name']}")
        print("Columns:", ", ".join(table['columns']))
    
    print("\nSQLite Agent initialized! You can ask questions about the database.")
    print("\nExample questions:")
    print("- What is the average salary in the Engineering department?")
    print("- Who are all the employees in the Marketing department?")
    print("- What is the total number of employees?")
    print("\nType 'exit' to quit.\n")
    
    while True:
        question = input("Your question: ")
        if question.lower() == 'exit':
            break
            
        result = agent.query(question)
        print(result)

