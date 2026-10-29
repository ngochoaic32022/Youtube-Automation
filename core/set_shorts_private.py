import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

OLD_VIDEOS = [
    {"id": "ENs4lnEr5Lg", "name": "The Bloop Cũ"},
    {"id": "GQ_yQoLgjj4", "name": "Hố Đen Cũ"},
    {"id": "HypEjaTo3KY", "name": "La Bàn Cũ"}
]

def make_video_private(page, video_id, name):
    print(f"\n================ Setting {name} ({video_id}) to PRIVATE ================")
    url = f"https://studio.youtube.com/video/{video_id}/edit"
    print(f"[*] Navigating to {url}...")
    page.goto(url)
    
    # Wait for the editor to load
    page.wait_for_selector("#visibility-button, [aria-label*='Chế độ hiển thị'], [aria-label*='Visibility']", timeout=20000)
    time.sleep(2)
    
    # Click visibility dropdown
    vis_btn = page.locator("#visibility-button, [aria-label*='Chế độ hiển thị'], [aria-label*='Visibility']").first
    print("[*] Clicking visibility button...")
    vis_btn.click()
    time.sleep(1.5)
    
    # Select 'Riêng tư' (Private) radio button
    print("[*] Selecting 'Riêng tư' (Private)...")
    private_radio = page.locator("tp-yt-paper-radio-button[name='PRIVATE'], tp-yt-paper-radio-button:has-text('Riêng tư'), tp-yt-paper-radio-button:has-text('Private')").first
    if private_radio.is_visible():
        private_radio.click()
        time.sleep(1)
        print("[+] Clicked Riêng tư radio button")
    else:
        print("[!] Could not find Riêng tư radio button directly, searching all radio buttons...")
        for r in page.locator("tp-yt-paper-radio-button").all():
            txt = r.inner_text().strip()
            if "Riêng tư" in txt or "Private" in txt:
                print(f"[+] Clicking radio button: {txt}")
                r.click()
                time.sleep(1)
                break
                
    # Click 'Xong' (Done) button in popup dialog
    done_btn = page.locator("#done-button, button:has-text('Xong'), button:has-text('Done')").first
    if done_btn.is_visible():
        print("[*] Clicking 'Xong' (Done)...")
        done_btn.click()
        time.sleep(1.5)
        
    # Click 'Lưu' (Save) button in top-right
    save_btn = page.locator("#save-button, [aria-label*='Lưu'], [aria-label*='Save'], button:has-text('Lưu')").first
    if save_btn.is_visible():
        is_disabled = save_btn.get_attribute("disabled") is not None or save_btn.get_attribute("aria-disabled") == "true"
        if not is_disabled:
            print("[*] Clicking 'Lưu' (Save)...")
            save_btn.click()
            time.sleep(3)
            print(f"[✓] SUCCESS: {name} ({video_id}) is now set to PRIVATE!")
            return True
        else:
            print(f"[*] Save button already disabled for {video_id}.")
            return True
    else:
        print(f"[!] Save button not found for {video_id}.")
        return False

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:59259')
        ctx = browser.contexts[0]
        page = ctx.pages[0]
        
        for item in OLD_VIDEOS:
            make_video_private(page, item["id"], item["name"])
            time.sleep(2)
            
        # Navigate back to shorts list
        print("\n[*] Navigating back to Shorts list to refresh view...")
        page.goto("https://studio.youtube.com/channel/UCDnEMYzjKRwAGPFWQNU8LYQ/videos/short")
        time.sleep(3)
        page.screenshot(path="outputs/channel_1_shorts_cleaned.png")
        print("[✓] ALL DONE! Screenshot saved to outputs/channel_1_shorts_cleaned.png")
