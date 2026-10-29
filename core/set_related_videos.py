import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def set_related_video(page, short_id: str, target_video_id: str, target_title: str):
    print(f"\n================ CONFIGURING SHORT: {short_id} ================")
    url = f"https://studio.youtube.com/video/{short_id}/edit"
    if url not in page.url:
        page.goto(url, wait_until='networkidle')
    page.bring_to_front()
    time.sleep(3)

    # 1. Tìm khu vực "Video có liên quan" hoặc "Related video"
    print("[*] Finding Related Video section...")
    # In YouTube Studio, the row has a button or click handler
    related_row = page.locator('text="Video có liên quan"').first
    if not related_row.is_visible():
        related_row = page.locator('text="Related video"').first

    if not related_row.is_visible():
        print("[!] Could not find Related Video button!")
        page.screenshot(path=f"outputs/debug_no_btn_{short_id}.png")
        return False

    print("[+] Clicking Related Video button...")
    related_row.click()
    time.sleep(2)

    # Take screenshot of dialog
    page.screenshot(path=f"outputs/dialog_open_{short_id}.png")

    # 2. Tìm kiếm hoặc chọn video đích
    print(f"[*] Looking for target video: {target_video_id} ({target_title})...")
    # In the dialog, there is usually a search input or a list of channel videos
    # Check if target video is already visible in the list
    target_item = page.locator(f'text="{target_title}"').first
    if not target_item.is_visible():
        # Search input
        search_input = page.locator('input[placeholder*="Tìm"], input[placeholder*="Search"]').first
        if search_input.is_visible():
            print("[*] Typing into search input...")
            search_input.fill(target_video_id)
            time.sleep(2)
            target_item = page.locator(f'text="{target_title}"').first

    if target_item.is_visible():
        print(f"[+] Found target video: {target_title}. Clicking...")
        target_item.click()
        time.sleep(2)
    else:
        # Try finding by link or ID
        print(f"[!] Target title not immediately found, checking dialog items...")
        dialog_items = page.locator('ytcp-entity-card, ytcp-video-row, [role="row"]').all()
        print(f"Dialog has {len(dialog_items)} items.")
        clicked = False
        for it in dialog_items:
            txt = it.inner_text()
            if target_video_id in txt or target_title.lower() in txt.lower():
                print(f"[+] Clicking matching item: {txt[:50]}...")
                it.click()
                clicked = True
                break
        if not clicked:
            print("[!] Could not select target item. Screenshot saved.")
            page.screenshot(path=f"outputs/debug_selection_fail_{short_id}.png")
            return False

    # 3. Bấm nút Lưu (Save)
    time.sleep(1)
    print("[*] Looking for Save button...")
    save_btn = page.locator('#save-button, [aria-label*="Lưu"], [aria-label*="Save"], button:has-text("Lưu"), button:has-text("Save")').first
    if save_btn.is_visible():
        # Check if disabled
        is_disabled = save_btn.get_attribute('disabled') is not None or save_btn.get_attribute('aria-disabled') == 'true'
        if not is_disabled:
            print("[+] Clicking Save button...")
            save_btn.click()
            time.sleep(3)
            print(f"[✓] SUCCESS! Related video set for Short {short_id} -> {target_video_id}")
            page.screenshot(path=f"outputs/success_{short_id}.png")
            return True
        else:
            print("[*] Save button is disabled (maybe already saved).")
            return True
    else:
        print("[!] Save button not found!")
        return False

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:56805')
        ctx = browser.contexts[0]
        
        # Short 1: HqFLVnOu9PY -> Target: 1-6gOvgoQHw ("Vintage Christmas Songs Playlist")
        pg1 = None
        for pg in ctx.pages:
            if 'HqFLVnOu9PY' in pg.url:
                pg1 = pg
                break
        if not pg1:
            pg1 = ctx.new_page()
            pg1.goto('https://studio.youtube.com/video/HqFLVnOu9PY/edit', wait_until='networkidle')

        res1 = set_related_video(pg1, 'HqFLVnOu9PY', '1-6gOvgoQHw', 'Vintage Christmas Songs Playlist')

        # Short 2: UPEAtJWOfOo -> Target: FVjOfcIBzp0 ("Traditional Christmas Carols")
        pg2 = None
        for pg in ctx.pages:
            if 'UPEAtJWOfOo' in pg.url:
                pg2 = pg
                break
        if not pg2:
            pg2 = ctx.new_page()
            pg2.goto('https://studio.youtube.com/video/UPEAtJWOfOo/edit', wait_until='networkidle')

        res2 = set_related_video(pg2, 'UPEAtJWOfOo', 'FVjOfcIBzp0', 'Traditional Christmas Carols')

        print("\n================ SUMMARY ================")
        print(f"Short 1 related video set: {res1}")
        print(f"Short 2 related video set: {res2}")
