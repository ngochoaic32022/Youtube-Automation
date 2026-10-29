import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:59259')
    page = browser.contexts[0].pages[0]
    
    # We are on https://studio.youtube.com/video/ENs4lnEr5Lg/edit
    print("Page URL:", page.url)
    
    # Find the button that opens visibility
    # In YouTube Studio, the visibility card has text "Chế độ hiển thị"
    # Let's find the card
    card = page.locator("ytcp-video-metadata-editor-side-panel").first
    print("Card found:", card.is_visible())
    
    # Let's find all buttons inside the side panel
    btns = card.locator("button, ytcp-button, ytcp-icon-button, [role='button']").all()
    print("Buttons in side panel:", len(btns))
    for i, b in enumerate(btns):
        print(f"Btn {i}: aria='{b.get_attribute('aria-label')}' id='{b.get_attribute('id')}' text='{b.inner_text().strip()}'")
