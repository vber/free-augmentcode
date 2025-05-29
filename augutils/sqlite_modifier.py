import sqlite3
import shutil
import time
from utils.paths import get_db_path

def _create_backup(file_path: str) -> str:
    """
    Creates a backup of the specified file with timestamp.
    
    Args:
        file_path (str): Path to the file to backup
        
    Returns:
        str: Path to the backup file
        
    Format: <filename>.bak.<timestamp>
    """
    timestamp = int(time.time())
    backup_path = f"{file_path}.bak.{timestamp}"
    shutil.copy2(file_path, backup_path)
    return backup_path

def clean_augment_data() -> dict:
    """
    Cleans augment-related data from the SQLite database.
    Creates a backup before modification.
    
    This function:
    1. Gets the SQLite database path
    2. Creates a backup of the database file
    3. Opens the database connection
    4. Deletes records where key contains 'augment'
    
    Returns:
        dict: A dictionary containing operation results
        {
            'db_backup_path': str,
            'deleted_rows': int
        }
    """
    db_path = get_db_path()
    
    # Create backup before modification
    db_backup_path = _create_backup(db_path)
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Execute the delete query
        cursor.execute("DELETE FROM ItemTable WHERE key LIKE '%augment%'")
        deleted_rows = cursor.rowcount
        
        # Commit the changes
        conn.commit()
        
        return {
            'db_backup_path': db_backup_path,
            'deleted_rows': deleted_rows
        }
    finally:
        # Always close the connection
        cursor.close()
        conn.close() 