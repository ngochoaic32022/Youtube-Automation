import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:56805')
    ctx = browser.contexts[0]
    page = [pg for pg in ctx.pages if 'HqFLVnOu9PY' in pg.url][0]
    page.bring_to_front()
    
    # Save a full page screenshot
    page.screenshot(path='outputs/full_studio_page.png')
    print("Screenshot saved to outputs/full_studio_page.png")
    
    # Check dialogs
    for d in page.locator('ytcp-dialog').all():
        print("ytcp-dialog visible:", d.is_visible())
        if d.is_visible():
            print("ytcp-dialog text:\n", d.inner_text()[:400])
            
    # Check what relates to "Video có liên quan" on the main page
    print("\n--- Locating Related Video elements ---")
    for el in page.locator('#related-video, [aria-label*="liên quan"], [aria-label*="Related"]').all():
        print("Tag:", el.evaluate("e => e.tagName"), "ID:", el.evaluate("e => e.id"), "Visible:", el.is_visible(), "Text:", el.inner_text()[:100])
