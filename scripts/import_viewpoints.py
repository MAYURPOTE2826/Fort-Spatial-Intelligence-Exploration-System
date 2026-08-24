import os
import csv
import logging
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the root .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            database=os.getenv("POSTGRES_DB", "fortsight")
        )
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

def create_table_if_not_exists(conn):
    query = """
    CREATE TABLE IF NOT EXISTS viewpoints (
        id SERIAL PRIMARY KEY,
        fort_id INTEGER REFERENCES forts(id) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        latitude DECIMAL(9,6) NOT NULL,
        longitude DECIMAL(9,6) NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(fort_id, name)
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
        logger.info("Checked/Created 'viewpoints' table successfully.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error creating table: {e}")
        raise

def import_viewpoints(csv_filepath):
    if not os.path.exists(csv_filepath):
        logger.error(f"File not found: {csv_filepath}")
        return

    conn = get_db_connection()

    inserted_count = 0

    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            with conn.cursor() as cur:
                for row in reader:
                    # Resolve fort_id
                    cur.execute("SELECT id FROM forts WHERE name = %s", (row['fort_name'],))
                    fort = cur.fetchone()
                    if not fort:
                        logger.warning(f"Fort '{row['fort_name']}' not found for viewpoint '{row['name']}'. Skipping.")
                        continue
                    fort_id = fort[0]

                    # Check for duplicates
                    cur.execute("SELECT id FROM fort_viewpoints WHERE fort_id = %s AND name = %s", (fort_id, row['name']))
                    if cur.fetchone():
                        logger.info(f"Viewpoint '{row['name']}' already exists for {row['fort_name']}. Skipping.")
                        continue

                    # Insert data
                    insert_query = """
                        INSERT INTO fort_viewpoints (fort_id, name, geometry, description)
                        VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s)
                    """
                    cur.execute(insert_query, (
                        fort_id, row['name'], float(row['longitude']), float(row['latitude']), row['description']
                    ))
                    inserted_count += 1
                
                conn.commit()
                logger.info(f"Import complete. Inserted: {inserted_count} viewpoints.")
    
    except Exception as e:
        logger.error(f"Fatal error during import. Rolling back transaction. Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'data', 'viewpoints.csv')
    import_viewpoints(csv_path)
