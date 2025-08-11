import requests
import json
from pathlib import Path
import time
FAQ_URL = "https://raw.githubusercontent.com/Utkrusht-AI/assessment-datasets/main/faq/faq_corpus.json"
def main():
    dest_dir = Path('data/documents')
    dest_dir.mkdir(parents=True, exist_ok=True)
    download_path = dest_dir / "faq_corpus.json"
    success = False
    tries = 0
    while not success and tries < 3:
        try:
            resp = requests.get(FAQ_URL, timeout=30)
            if resp.status_code == 200 and resp.text and len(resp.text) > 3000:
                download_path.write_text(resp.text, encoding='utf-8')
                success = True
            else:
                time.sleep(2)
                tries += 1
        except Exception:
            time.sleep(2)
            tries += 1
    if not success:
        raise RuntimeError('Failed to download FAQ corpus after 3 attempts')
if __name__ == "__main__":
    main()
