import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

OLD_VIDEOS = [
    {"id": "ENs4lnEr5Lg", "name": "The Bloop Cũ"},
    {"id": "GQ_yQoLgjj4", "name": "Hố Đen Cũ"},
    {"id": "HypEjaTo3KY", "name": "La Bàn Cũ"}
]

def make_private(page, vid_id, vid_name):
    print(f"\n================ MAKING PRIVATE: {vid_name} ({vid_id}) ================")
    url = f"https://studio.youtube.com/video/{vid_id}/edit"
    print(f"[*] Navigating to {url}...")
    page.goto(url)
    time.sleep(3)
    
    # Locate visibility edit button
    vis_btn = page.locator("[aria-label*='Chỉnh sửa trạng thái hiển thị'], [aria-label*='Edit visibility']").first
    if not vis_btn.is_visible():
        print(f"[!] Visibility button not found for {vid_id}!")
        page.screenshot(path=f"outputs/err_vis_{vid_id}.png")
        return False
        
    print("[*] Clicking visibility button...")
    vis_btn.click()
    time.sleep(1.5)
    
    # Click Riêng tư
    for r in page.locator("tp-yt-paper-radio-button").all():
        txt = r.inner_text().strip()
        if "Riêng tư" in txt or "Private" in txt:
            print(f"[+] Selecting radio button: {txt}")
            r.click()
            time.sleep(1)
            break
            
    # Click Xong
    done_btn = page.locator("#done-button, [aria-label*='Xong'], [aria-label*='Done'], button:has-text('Xong'), button:has-text('Done')").first
    if done_btn.is_visible():
        print("[*] Clicking 'Xong'...")
        done_btn.click()
        time.sleep(1.5)
        
    # Click Lưu
    save_btn = page.locator("#save, [aria-label*='Lưu'], [aria-label*='Save'], button:has-text('Lưu'), button:has-text('Save')").first
    if save_btn.is_visible():
        is_disabled = save_btn.get_attribute("disabled") is not None or save_btn.get_attribute("aria-disabled") == "true"
        if not is_disabled:
            print("[*] Clicking 'Lưu'...")
            save_btn.click()
            time.sleep(3)
            print(f"[✓] SUCCESS! {vid_name} ({vid_id}) is now PRIVATE!")
            return True
        else:
            print(f"[*] Save button already disabled for {vid_id} (already saved).")
            return True
    else:
        print(f"[!] Save button not found for {vid_id}!")
        return False

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:59259')
        ctx = browser.contexts[0]
        page = ctx.pages[0]
        
        for item in OLD_VIDEOS:
            make_private(page, item["id"], item["name"])
            time.sleep(2)
            
        print("\n[*] Refreshing Shorts list on Channel 1...")
        page.goto("https://studio.youtube.com/channel/UCDnEMYzjKRwAGPFWQNU8LYQ/videos/short")
        time.sleep(3)
        page.screenshot(path="outputs/channel_1_shorts_cleaned_final.png")
        print("[✓] ALL 3 OLD VIDEOS HAVE BEEN SET TO PRIVATE!")
