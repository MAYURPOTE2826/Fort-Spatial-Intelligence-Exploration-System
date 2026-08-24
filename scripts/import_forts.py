import os
import csv
import json
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
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

# Constants for Validation
MAHARASHTRA_BBOX = {
    "min_lat": 15.6, "max_lat": 22.0,
    "min_lon": 72.6, "max_lon": 80.9
}
MIN_ELEVATION = 0
MAX_ELEVATION = 2000  # Kalsubai is 1646m, so 2000m is a safe upper bound for forts

def get_db_connection():
    """Establish database connection."""
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
    """Ensure the forts table exists."""
    query = """
    CREATE TABLE IF NOT EXISTS forts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        marathi_name VARCHAR(255),
        latitude DECIMAL(9,6) NOT NULL,
        longitude DECIMAL(9,6) NOT NULL,
        elevation INTEGER,
        district VARCHAR(100),
        difficulty VARCHAR(50),
        best_season VARCHAR(100),
        history TEXT,
        image_url TEXT,
        source VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
        logger.info("Checked/Created 'forts' table successfully.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error creating table: {e}")
        raise

def validate_fort_data(row):
    """Validate fort data constraints."""
    errors = []
    
    # Validate coordinates
    try:
        lat = float(row['latitude'])
        lon = float(row['longitude'])
        if not (MAHARASHTRA_BBOX['min_lat'] <= lat <= MAHARASHTRA_BBOX['max_lat']):
            errors.append(f"Latitude {lat} out of Maharashtra bounds.")
        if not (MAHARASHTRA_BBOX['min_lon'] <= lon <= MAHARASHTRA_BBOX['max_lon']):
            errors.append(f"Longitude {lon} out of Maharashtra bounds.")
    except ValueError:
        errors.append("Invalid latitude or longitude format.")

    # Validate elevation
    try:
        elev = int(row['elevation'])
        if not (MIN_ELEVATION <= elev <= MAX_ELEVATION):
            errors.append(f"Elevation {elev}m seems unreasonable for Maharashtra.")
    except ValueError:
        errors.append("Invalid elevation format.")

    # Check source attribution
    if not row.get('source'):
        errors.append("Source attribution is missing.")

    return errors

def import_forts(csv_filepath):
    """Read CSV, validate, and import into database with rollback on error."""
    if not os.path.exists(csv_filepath):
        logger.error(f"File not found: {csv_filepath}")
        return

    conn = get_db_connection()

    inserted_count = 0
    duplicate_count = 0
    error_count = 0

    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            with conn.cursor() as cur:
                for row in reader:
                    logger.info(f"Processing fort: {row['name']}")
                    
                    # Validation
                    validation_errors = validate_fort_data(row)
                    if validation_errors:
                        logger.warning(f"Validation failed for {row['name']}: {', '.join(validation_errors)}")
                        error_count += 1
                        continue

                    # Check for duplicates
                    cur.execute("SELECT id FROM forts WHERE name = %s", (row['name'],))
                    if cur.fetchone():
                        logger.info(f"Fort {row['name']} already exists. Skipping.")
                        duplicate_count += 1
                        continue

                    # Insert data
                    insert_query = """
                        INSERT INTO forts 
                        (name, marathi_name, geometry, elevation, district, difficulty, best_season, history, image_url, source)
                        VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s, %s, %s, %s, %s, %s)
                    """
                    try:
                        cur.execute(insert_query, (
                            row['name'], row['marathi_name'], float(row['longitude']), float(row['latitude']),
                            int(row['elevation']), row['district'], row['difficulty'], row['best_season'],
                            row['history'], row['image_url'], row['source']
                        ))
                        inserted_count += 1
                    except Exception as e:
                        logger.error(f"Error inserting {row['name']}: {e}")
                        # Don't rollback the whole transaction here if we want to continue, 
                        # but standard requirement is rollback on error. Let's raise to trigger outer rollback.
                        raise
                
                # Commit all successful inserts
                conn.commit()
                logger.info(f"Import complete. Inserted: {inserted_count}, Duplicates skipped: {duplicate_count}, Errors: {error_count}")
    
    except Exception as e:
        logger.error(f"Fatal error during import. Rolling back transaction. Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'data', 'forts_mvp.csv')
    import_forts(csv_path)
