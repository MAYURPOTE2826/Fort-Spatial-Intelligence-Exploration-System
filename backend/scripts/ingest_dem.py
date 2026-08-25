import argparse
import sys
import os
import rasterio
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from geoalchemy2.shape import from_shape
from shapely.geometry import box

# Ensure the app module can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.database import SessionLocal
from app.models.terrain import TerrainTile
from app.core.config import settings

def main():
    parser = argparse.ArgumentParser(description="Ingest DEM file into FortSight AI.")
    parser.add_argument("--source", type=str, required=True, help="DEM source (e.g., copernicus, srtm)")
    parser.add_argument("--file", type=str, help="Path to the local GeoTIFF file. If not provided, instructions will be shown.")
    parser.add_argument("--region", type=str, help="Region name (optional)")
    
    args = parser.parse_args()

    if not args.file:
        print("="*60)
        print("DEM file path not provided. Manual download is required.")
        print("="*60)
        print(f"To ingest DEM for {args.region or 'your region'} from {args.source}:")
        if args.source.lower() == 'copernicus':
            print("1. Go to OpenTopography or Copernicus Data Space.")
            print("2. Select the Copernicus DEM 30m dataset.")
            print("3. Download the GeoTIFF file for your region of interest.")
        else:
            print(f"1. Download the {args.source} DEM GeoTIFF file for your region.")
        
        dem_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), settings.DEM_DATA_DIR)
        print(f"\nExpected storage location: {dem_dir}")
        print(f"\nOnce downloaded, run this script again with the --file argument:")
        print(f"python scripts/ingest_dem.py --source {args.source} --file data/dem/your_file.tif")
        print("="*60)
        sys.exit(0)

    if not os.path.exists(args.file):
        print(f"Error: File not found at {args.file}")
        sys.exit(1)

    print(f"Processing DEM file: {args.file}")
    
    try:
        with rasterio.open(args.file) as dataset:
            bounds = dataset.bounds
            res = dataset.res
            
            # Create a polygon from the bounds
            geom = box(bounds.left, bounds.bottom, bounds.right, bounds.top)
            wkb_element = from_shape(geom, srid=4326)
            
            # Assuming resolution is approximately in degrees for EPSG 4326
            # For 30m DEM, res[0] is roughly 0.0002777777777777778
            # We convert roughly to meters for storing if needed, or just store the source
            # 1 degree is roughly 111km, so 0.000277 * 111000 = ~30m
            resolution_m = res[0] * 111000 
            
            tile_name = os.path.basename(args.file)
            
            # Resolve relative file path to the project root, or store absolute
            # To be safe and portable, if file is inside data/dem, store relative path
            # Otherwise store absolute
            file_path_to_store = args.file
            
            db: Session = SessionLocal()
            try:
                # Check if exists
                existing = db.query(TerrainTile).filter(TerrainTile.tile_name == tile_name).first()
                if existing:
                    print(f"Tile {tile_name} already exists. Updating...")
                    existing.file_path = file_path_to_store
                    existing.geometry = wkb_element
                    existing.resolution_m = resolution_m
                    existing.source = args.source
                else:
                    print(f"Adding new tile: {tile_name}")
                    new_tile = TerrainTile(
                        tile_name=tile_name,
                        zoom_level=12, # placeholder
                        geometry=wkb_element,
                        file_path=file_path_to_store,
                        resolution_m=resolution_m,
                        source=args.source
                    )
                    db.add(new_tile)
                db.commit()
                print("Successfully ingested DEM tile.")
            except IntegrityError as e:
                db.rollback()
                print(f"Database integrity error: {e}")
            finally:
                db.close()
                
    except rasterio.errors.RasterioIOError:
        print(f"Error: {args.file} is not a valid GeoTIFF or raster file.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
