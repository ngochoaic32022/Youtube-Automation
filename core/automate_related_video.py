import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:56805')
    ctx = browser.contexts[0]
    page = ctx.pages[1]
    
    target_url = "https://studio.youtube.com/video/HqFLVnOu9PY/edit"
    print(f"[*] Navigating to {target_url}...")
    page.goto(target_url)
    
    # Wait for the editor to load
    page.wait_for_selector("ytcp-video-metadata-editor-side-panel, ytcp-video-metadata-editor", timeout=15000)
    time.sleep(3)
    
    print("[+] Page loaded successfully! Title:", page.title())
    page.screenshot(path="outputs/studio_loaded.png")
    
    # Inspect the side panel
    side_panel = page.locator("ytcp-video-metadata-editor-side-panel").first
    if side_panel.is_visible():
        print("[+] Side panel text:\n", side_panel.inner_text())
    else:
        print("[!] Side panel not found or not visible.")
