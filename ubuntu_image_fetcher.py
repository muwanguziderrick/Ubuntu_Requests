import requests
import os
import hashlib
from urllib.parse import urlparse
from requests.exceptions import RequestException

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename or '.' not in filename:
        filename = "downloaded_image.jpg"
    return filename

def is_duplicate(filepath, content):
    """Check if a file with the same content already exists."""
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'rb') as f:
        existing = f.read()
    return hashlib.md5(existing).digest() == hashlib.md5(content).digest()

def fetch_and_save_image(url, fetched_dir, downloaded_hashes):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Check content type before saving
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped (not an image): {url}")
            return

        filename = get_filename_from_url(url)
        filepath = os.path.join(fetched_dir, filename)
        
        # Prevent duplicate downloads (by hash)
        file_hash = hashlib.md5(response.content).hexdigest()
        if file_hash in downloaded_hashes:
            print(f"✗ Duplicate found, not saved: {filename}")
            return
        downloaded_hashes.add(file_hash)

        # If file exists, avoid overwrite by appending a number
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filepath = os.path.join(fetched_dir, f"{base}_{counter}{ext}")
            counter += 1

        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"✓ Successfully fetched: {os.path.basename(filepath)}")
        print(f"✓ Image saved to {filepath}")
    except RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Multiple URLs support
    urls_input = input("Please enter image URL(s), separated by spaces: ")
    urls = [u.strip() for u in urls_input.split() if u.strip()]
    if not urls:
        print("✗ No URLs provided.")
        return

    fetched_dir = "Fetched_Images"
    os.makedirs(fetched_dir, exist_ok=True)
    downloaded_hashes = set()
    for url in urls:
        fetch_and_save_image(url, fetched_dir, downloaded_hashes)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()