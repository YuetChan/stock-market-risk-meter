import json
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Get browser compatibility for a CSS property')
parser.add_argument('-p', '--property', required=True, help='CSS property name')
parser.add_argument('-b', '--browsers', nargs='+', default=['chrome', 'firefox', 'safari', 'edge'], help='List of browsers to check')
args = parser.parse_args()

# Load caniuse data
with open('data.json', 'r') as f:
    caniuse_data = json.load(f)

# Check if property is valid
if args.property not in caniuse_data['data']:
    print(f"Error: '{args.property}' is not a valid CSS property name")
    exit(1)

# Get compatibility data for each browser
property_data = caniuse_data['data'][args.property]['stats']
print(property_data)
for browser in args.browsers:
    if browser not in property_data:
        print(f"Error: '{browser}' is not a valid browser name")
        continue
    version_data = property_data[browser]

    # print(version_data)
    # print("\n")

    # print(f"{browser}:")
    # for version, support in version_data.items():
    #     print(f"\t{version}: {support}")
