import sys
import os
import json

def main():
    if len(sys.argv) != 4:
        print("Usage: python empty-json.py <start> <end> <target_folder>")
        sys.exit(1)

    start = int(sys.argv[1])
    end = int(sys.argv[2])
    target_folder = sys.argv[3]

    # Create target folder if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)

    # Generate files
    for i in range(start, end + 1):
        filename = f"question{i:03d}.json"
        filepath = os.path.join(target_folder, filename)

        with open(filepath, 'w') as f:
            json.dump({}, f)

        print(f"Created {filename}")

    print(f"\nGenerated {end - start + 1} files")

if __name__ == "__main__":
    main()
