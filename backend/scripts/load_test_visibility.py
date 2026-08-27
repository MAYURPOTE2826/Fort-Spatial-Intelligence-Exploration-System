import asyncio
import aiohttp
import time

API_URL = "http://localhost:8000/api/v1/visibility/from-location"

async def fetch_visibility(session, params):
    start = time.time()
    async with session.get(API_URL, params=params) as response:
        status = response.status
        try:
            data = await response.json()
            calc_time = data.get("calculation_time_ms", 0)
        except:
            calc_time = 0
        return status, time.time() - start, calc_time

async def main():
    params = {
        "lat": 18.67,
        "lon": 73.33,
        "radius_km": 50,
        "heading": 245,
        "fov": 60
    }
    
    print("Sending first request (should be slow, cache miss)...")
    async with aiohttp.ClientSession() as session:
        status, req_time, calc_time = await fetch_visibility(session, params)
        print(f"Status: {status} | Request Time: {req_time:.3f}s | Server Calc Time: {calc_time}ms")
        
        print("\nSending 50 concurrent requests (should be fast, cache hits)...")
        tasks = []
        for _ in range(50):
            tasks.append(fetch_visibility(session, params))
            
        start_concurrent = time.time()
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_concurrent
        
        print(f"\nCompleted 50 requests in {total_time:.3f}s")
        
        avg_calc = sum(r[2] for r in results) / len(results)
        print(f"Average Server Calc Time: {avg_calc:.2f}ms")
        
        failures = sum(1 for r in results if r[0] != 200)
        print(f"Failed requests: {failures} / 50")

if __name__ == "__main__":
    asyncio.run(main())
