#!/usr/bin/env python3
"""
Test script to explore RapidAPI Ski Resorts API
Run this first to see what data is available for Colorado resorts
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")

def test_rapidapi_endpoints():
    """
    Test RapidAPI ski resorts endpoints to understand data structure
    """
    
    print("=" * 70)
    print("TESTING RAPIDAPI SKI RESORTS ENDPOINTS")
    print("=" * 70)
    
    # RapidAPI base URL
    base_url = "https://ski-resorts-and-conditions.p.rapidapi.com"
    
    # RapidAPI headers
    headers = {
        "x-rapidapi-host": "ski-resorts-and-conditions.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    
    # Test endpoints - these are common for ski resort APIs
    endpoints_to_test = [
        "/v1/resort",           # List all resorts
        "/v1/resort/colorado",  # Colorado resorts
        "/v1/resort/us",        # US resorts
    ]
    
    print(f"\nAPI Key loaded: {'✅ Yes' if RAPIDAPI_KEY else '❌ No (set RAPIDAPI_KEY in .env)'}")
    print(f"Base URL: {base_url}")
    print("\nTesting endpoints...\n")
    
    for endpoint in endpoints_to_test:
        url = base_url + endpoint
        try:
            print(f"\n{'='*70}")
            print(f"Trying: {url}")
            print(f"{'='*70}")
            
            response = requests.get(url, headers=headers, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS!")
                print(f"Response type: {type(data)}")
                
                # Print structure
                if isinstance(data, list):
                    print(f"Number of items: {len(data)}")
                    if len(data) > 0:
                        print(f"\n📊 First item structure:")
                        print(json.dumps(data[0], indent=2))
                        
                        # If there are Colorado resorts, show a few
                        colorado_resorts = [r for r in data if isinstance(r, dict) and 
                                          ('colorado' in str(r.get('location', '')).lower() or 
                                           'CO' in str(r.get('state', '')) or
                                           'colorado' in str(r.get('region', '')).lower())]
                        
                        if colorado_resorts:
                            print(f"\n🎿 Found {len(colorado_resorts)} Colorado resorts!")
                            print("\nSample Colorado resorts:")
                            for resort in colorado_resorts[:3]:
                                print(f"  - {resort.get('name', 'Unknown')}")
                
                elif isinstance(data, dict):
                    print(f"Keys: {list(data.keys())}")
                    print(f"\n📄 Full response preview:")
                    response_preview = json.dumps(data, indent=2)
                    if len(response_preview) > 1000:
                        print(response_preview[:1000] + "\n... (truncated)")
                    else:
                        print(response_preview)
            
            elif response.status_code == 401:
                print("❌ Unauthorized - Check API key")
            elif response.status_code == 404:
                print("❌ Not Found - Endpoint may not exist")
            elif response.status_code == 403:
                print("❌ Forbidden - Check API subscription/permissions")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            print("❌ Timeout")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
        except json.JSONDecodeError:
            print("❌ Response is not JSON")
            print(f"Response text: {response.text[:200]}")


def test_index_endpoint():
    """
    Test the Index endpoint shown in the RapidAPI interface
    """
    print("\n" + "=" * 70)
    print("TESTING INDEX ENDPOINT")
    print("=" * 70)
    
    base_url = "https://ski-resorts-and-conditions.p.rapidapi.com"
    
    headers = {
        "x-rapidapi-host": "ski-resorts-and-conditions.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    
    # Try the index endpoint
    endpoints = [
        "/",
        "/v1/resort",
    ]
    
    for endpoint in endpoints:
        url = base_url + endpoint
        try:
            print(f"\nTrying: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCCESS!")
                data = response.json()
                print(json.dumps(data, indent=2)[:2000])
            else:
                print(f"Response: {response.text[:300]}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    test_rapidapi_endpoints()
    test_index_endpoint()
    
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Review the successful endpoint responses above")
    print("2. Note the data structure and available fields")
    print("3. Identify which fields map to our needs:")
    print("   - Resort name, lat/lng")
    print("   - Snow depth (base/summit)")
    print("   - New snow (24h/48h/7d)")
    print("   - Lifts/runs open")
    print("   - Conditions status")
    print("4. Update ski_api_fetcher.py with correct endpoints and field mappings")
    print("=" * 70)

