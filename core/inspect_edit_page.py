import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:59259')
    page = browser.contexts[0].pages[0]
    
    text = page.evaluate("() => document.body.innerText")
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for i, l in enumerate(lines[:60]):
        print(f"[{i}] {l}")
        
    print("\n--- Interactive elements on the right ---")
    for el in page.locator("button, ytcp-button, [role='button'], [role='combobox']").all():
        t = el.inner_text().strip().replace("\n", " ")
        aria = el.get_attribute("aria-label") or ""
        id_attr = el.get_attribute("id") or ""
        if any(k in (t + aria + id_attr).lower() for k in ["lên lịch", "chế độ", "hiển thị", "visibility", "schedule", "riêng tư", "private"]):
            print(f"Tag: {el.evaluate('e => e.tagName')} | ID: {id_attr} | Aria: {aria} | Text: {t}")
