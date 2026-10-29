import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:59259')
    ctx = browser.contexts[0]
    page = ctx.new_page()
    page.goto('https://studio.youtube.com/video/ENs4lnEr5Lg/edit', wait_until='networkidle')
    time.sleep(3)
    
    # Click on the element that shows "Đã lên lịch"
    print("Clicking 'Đã lên lịch'...")
    target = page.locator("text='Đã lên lịch'").first
    target.click()
    time.sleep(2)
    
    page.screenshot(path='outputs/test_click_scheduled.png')
    
    for d in page.locator("tp-yt-paper-dialog, ytcp-dialog").all():
        if d.is_visible():
            print("Visible dialog text:\n", d.inner_text()[:400])
            
    page.close()
