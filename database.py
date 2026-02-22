import os
import streamlit as st

def get_db_connection():
    """
    Creates or connects to the database.
    Using @st.cache_resource ensures we don't reconnect on every click.
    """
    # Create a 'data' directory if it doesn't exist for your vector store
    if not os.path.exists("./data"):
        os.makedirs("./data")
    
    # Example: If using SQLite or ChromaDB locally
    db_path = "./data/mindgap_vectorstore"
    
    # Return your connection object here
    # return YourDBClient(db_path)
    return db_path

def clear_database():
    """Helper to reset the app state if needed."""
    if os.path.exists("./data"):
        import shutil
        shutil.rmtree("./data")
        st.success("Database cleared!")
