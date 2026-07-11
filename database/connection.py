import psycopg2
import os

def get_connection():
  return psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"), 
    database="incident_management",
    user="postgres"
  )
