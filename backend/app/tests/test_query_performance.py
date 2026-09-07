import pytest
import time
from app.models.fort import Fort

def test_query_performance(db_session):
    # Insert 1000 dummy forts
    forts = [
        Fort(id=i, name=f"Fort {i}", latitude=18.0 + (i*0.0001), longitude=73.0 + (i*0.0001))
        for i in range(1000)
    ]
    db_session.add_all(forts)
    db_session.commit()
    
    start_time = time.time()
    results = db_session.query(Fort).all()
    duration = time.time() - start_time
    
    assert len(results) >= 1000
    assert duration < 0.5 # Should be very fast
