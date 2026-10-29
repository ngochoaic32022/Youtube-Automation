import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:56805')
    ctx = browser.contexts[0]
    page = [pg for pg in ctx.pages if 'HqFLVnOu9PY' in pg.url][0]
    
    # Get all text from the right column / sidebar
    # Let's inspect the entire DOM text
    full_text = page.evaluate("() => document.body.innerText")
    lines = [line.strip() for line in full_text.split("\n") if line.strip()]
    print(f"Total lines of text on page: {len(lines)}")
    
    # Find lines containing keywords
    keywords = ["liên quan", "Related", "Danh sách phát", "Hiển thị", "Visibility", "Shorts", "Không có", "None"]
    for idx, l in enumerate(lines):
        for kw in keywords:
            if kw.lower() in l.lower():
                print(f"[{idx}] {l}")
                break
