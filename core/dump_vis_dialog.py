import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:59259')
    page = browser.contexts[0].pages[0]
    
    # Click visibility edit button
    vis_btn = page.locator("[aria-label*='Chỉnh sửa trạng thái hiển thị']").first
    if vis_btn.is_visible():
        vis_btn.click()
        time.sleep(2)
        
    page.screenshot(path='outputs/visibility_dialog.png')
    print("Screenshot saved to outputs/visibility_dialog.png")
    
    # List all radio buttons or clickable options
    for el in page.locator("[role='radio'], tp-yt-paper-radio-button, ytcp-radio-button").all():
        tag = el.evaluate("e => e.tagName")
        name = el.get_attribute("name") or ""
        txt = el.inner_text().strip().replace("\n", " ")
        print(f"Tag: {tag} | Name: {name} | Text: {txt}")
