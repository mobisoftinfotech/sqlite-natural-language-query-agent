import sqlite3
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# List of departments
departments = [
    "Engineering",
    "Sales",
    "Marketing",
    "Human Resources",
    "Finance",
    "Operations",
    "Research & Development",
    "Customer Support",
    "Legal",
    "IT"
]

# Connect to SQLite database
conn = sqlite3.connect('employee_database.db')
cursor = conn.cursor()

# Create employees table
cursor.execute('''
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL
)
''')

# Generate and insert 1000 employee records
for i in range(1000):
    name = fake.name()
    department = random.choice(departments)
    # Generate realistic salaries between 35000 and 150000
    salary = round(random.uniform(35000, 150000), 2)
    
    cursor.execute('''
    INSERT INTO employees (name, department, salary)
    VALUES (?, ?, ?)
    ''', (name, department, salary))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created successfully with 1000 employee records!") 
