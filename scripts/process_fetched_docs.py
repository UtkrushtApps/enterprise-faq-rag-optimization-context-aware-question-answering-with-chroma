import json
from pathlib import Path

def main():
    src = Path('data/documents/faq_corpus.json')
    with open(src, encoding='utf-8') as f:
        faqs = json.load(f)
    for i, faq in enumerate(faqs.get('faqs', [])):
        text = faq['question'] + '\n' + faq['answer']
        category = faq.get('category', 'General')
        out_path = Path('data/documents') / f"faq_{i+1}.txt"
        out_path.write_text(f"[{category}]\nQ: {faq['question']}\nA: {faq['answer']}", encoding='utf-8')
if __name__ == "__main__":
    main()
