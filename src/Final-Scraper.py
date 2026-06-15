import pandas as pd
import re
import time
import random
from playwright.sync_api import sync_playwright

# -----------------------------
# 🔍 Extract ALL UPCs
# -----------------------------
def extract_upcs(page):
    upcs = set()

    # Strategy 1: Direct UPC label
    labels = page.locator("text=UPC")
    for i in range(labels.count()):
        try:
            parent = labels.nth(i).locator("xpath=..")
            text = parent.inner_text()

            matches = re.findall(r"\b\d{12}\b", text)
            upcs.update(matches)
        except:
            pass

    # Strategy 2: Table rows
    rows = page.locator("table tr")
    for i in range(rows.count()):
        text = rows.nth(i).inner_text()

        if "upc" in text.lower():
            matches = re.findall(r"\b\d{12}\b", text)
            upcs.update(matches)

    # Strategy 3: Bullet section
    bullets = page.locator("#detailBullets_feature_div li")
    for i in range(bullets.count()):
        text = bullets.nth(i).inner_text()

        if "upc" in text.lower():
            matches = re.findall(r"\b\d{12}\b", text)
            upcs.update(matches)

    # Return list
    return list(upcs) if upcs else ["Not Found"]


# -----------------------------
# 🚀 MAIN
# -----------------------------
def main():
    df = pd.read_excel("data/input.xlsx", engine="openpyxl")
    results = []

    with sync_playwright() as p:
        # ✅ Persistent session (avoid blocking)
        context = p.chromium.launch_persistent_context(
            user_data_dir="user_data",
            headless=False,
            slow_mo=300,
            args=["--start-maximized"]
        )

        page = context.pages[0] if context.pages else context.new_page()

        for index, row in df.iterrows():
            asin = str(row["product_id"])
            url = f"https://www.amazon.com/dp/{asin}"

            print(f"🔍 Processing {index+1}: {asin}")

            try:
                # 🏠 Random homepage visit
                if random.random() < 0.3:
                    page.goto("https://www.amazon.com/")
                    time.sleep(random.uniform(3, 6))

                # 🌐 Open product page
                page.goto(url, timeout=60000)
                time.sleep(random.uniform(4, 7))

                # 🖱 Human behavior
                page.mouse.move(random.randint(100, 500), random.randint(100, 500))
                page.mouse.wheel(0, random.randint(1500, 4000))
                time.sleep(random.uniform(2, 4))

                # Wait for content
                try:
                    page.wait_for_selector("text=Product information", timeout=15000)
                except:
                    pass

                # Expand sections
                try:
                    if page.get_by_role("button", name="Item details").is_visible():
                        page.get_by_role("button", name="Item details").click()
                        time.sleep(1)
                except:
                    pass

                try:
                    if page.get_by_role("button", name="Product details").is_visible():
                        page.get_by_role("button", name="Product details").click()
                        time.sleep(1)
                except:
                    pass

                # 🔍 Extract ALL UPCs
                upcs = extract_upcs(page)

                print(f"✅ {asin} → {upcs}")

                # Create dynamic columns
                row_data = {"product_id": asin}

                for i, code in enumerate(upcs):
                    row_data[f"upc_{i+1}"] = code

                results.append(row_data)

            except Exception:
                print(f"❌ Failed: {asin}")

                results.append({
                    "product_id": asin,
                    "upc_1": "Error"
                })

            # 💾 Save every 5 items
            if (index + 1) % 5 == 0:
                pd.DataFrame(results).to_excel("data/output.xlsx", index=False)
                print("💾 Progress saved...")

            # 🧊 Cooling break every 10 items
            if (index + 1) % 10 == 0:
                print("🧊 Cooling down...")
                time.sleep(random.uniform(15, 30))

        context.close()

    # Final save
    pd.DataFrame(results).to_excel("data/output.xlsx", index=False)

    print("🎉 Done! Output saved to data/output.xlsx")


# -----------------------------
if __name__ == "__main__":
    main()