#!/usr/bin/env python3
"""
Test Colorado Ski data structure without Selenium
Uses the HTML we already saved to test parsing logic
"""

from bs4 import BeautifulSoup
import pandas as pd
import re

print("="*70)
print("TESTING PARSER WITHOUT SELENIUM")
print("="*70)

# Check if we have saved HTML from earlier
try:
    with open('colorado_ski_page.html', 'r') as f:
        html = f.read()
    print("✅ Loaded saved HTML from earlier test\n")
except FileNotFoundError:
    print("❌ No saved HTML found")
    print("\nTo test the scraper, you need either:")
    print("1. Chrome installed (brew install --cask google-chrome)")
    print("2. Or just push to GitHub and test there (Chrome pre-installed)")
    exit(1)

soup = BeautifulSoup(html, 'html.parser')

print("Analyzing page structure...")
print("-"*70)

# Look for resort data in various formats
print(f"\n1. Tables: {len(soup.find_all('table'))}")
print(f"2. Divs with 'resort' class: {len(soup.find_all('div', class_=lambda x: x and 'resort' in x.lower()))}")
print(f"3. Articles: {len(soup.find_all('article'))}")
print(f"4. Script tags: {len(soup.find_all('script'))}")

# Check for JavaScript-embedded JSON data
print("\n" + "="*70)
print("SEARCHING FOR JSON DATA IN SCRIPTS")
print("="*70)

for i, script in enumerate(soup.find_all('script')):
    if script.string and len(script.string) > 100:
        content = script.string.strip()
        
        # Look for patterns that suggest resort data
        if any(keyword in content.lower() for keyword in ['resort', 'snow', 'trail', 'lift']):
            # Check if it looks like structured data
            if '{' in content and ('"name"' in content or '"resort"' in content):
                print(f"\n✅ Found potential resort data in script #{i}")
                print(f"Length: {len(content)} characters")
                
                # Try to extract JSON
                # Common patterns: var data = {...} or window.resortData = {...}
                patterns = [
                    r'var\s+\w+\s*=\s*(\{.*?\});',
                    r'window\.\w+\s*=\s*(\{.*?\});',
                    r'=\s*(\[.*?\]);',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.DOTALL)
                    if matches:
                        print(f"Found JSON pattern!")
                        print("Sample:", matches[0][:200] + "...")
                        break

# Look for resort names in text
print("\n" + "="*70)
print("LOOKING FOR RESORT NAMES IN PAGE TEXT")
print("="*70)

text = soup.get_text()
colorado_resorts = [
    'Arapahoe Basin', 'Aspen', 'Beaver Creek', 'Breckenridge',
    'Copper', 'Crested Butte', 'Echo Mountain', 'Eldora',
    'Keystone', 'Loveland', 'Monarch', 'Snowmass',
    'Steamboat', 'Telluride', 'Vail', 'Winter Park', 'Wolf Creek'
]

found = []
for resort in colorado_resorts:
    if resort in text:
        found.append(resort)
        # Try to find context around the resort name
        idx = text.find(resort)
        context = text[max(0, idx-50):idx+100]
        print(f"\n{resort}: ...{context}...")

print(f"\n\n✅ Found {len(found)} resort names in page")

# Check for common data patterns
print("\n" + "="*70)
print("LOOKING FOR SNOW DATA PATTERNS")
print("="*70)

patterns_to_check = [
    (r'\d+"\s*snow', 'Snow amounts with inches'),
    (r'Trails open:\s*\d+/\d+', 'Trail counts'),
    (r'Lifts open:\s*\d+/\d+', 'Lift counts'),
    (r'Base:\s*\d+"', 'Base depth'),
    (r'Conditions?:\s*\w+', 'Conditions'),
]

for pattern, description in patterns_to_check:
    matches = re.findall(pattern, text, re.IGNORECASE)
    if matches:
        print(f"\n✅ {description}")
        print(f"   Found {len(matches)} matches")
        print(f"   Sample: {matches[:3]}")
    else:
        print(f"\n❌ {description} - not found")

print("\n" + "="*70)
print("DIAGNOSIS")
print("="*70)

if len(found) > 10:
    print("✅ Page has resort data")
    if any(re.findall(r'\d+"\s*snow', text)):
        print("✅ Snow data is present")
        print("\n💡 The page structure is parseable!")
        print("   Scraper should work once we identify exact selectors")
    else:
        print("⚠️  Resort names present but no snow data")
        print("   Data might load via AJAX after page render")
        print("   Selenium with wait time should handle this")
else:
    print("❌ Limited resort data found")
    print("   Page likely uses heavy JavaScript rendering")
    print("   Selenium is definitely needed")

print("\n" + "="*70)
print("NEXT STEPS")
print("="*70)
print("Without Chrome locally, best options:")
print("1. Install Chrome: brew install --cask google-chrome")
print("2. OR deploy to GitHub Actions (Chrome pre-installed)")
print("3. GitHub test is actually easier and matches production!")
print("="*70)

