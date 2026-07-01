from playwright.sync_api import sync_playwright

URL = "https://www.shl.com/solutions/products/product-catalog/"


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")

    page.wait_for_timeout(5000)

    print("TITLE:")
    print(page.title())

    print("\nCURRENT URL:")
    print(page.url)

    print("\nFIRST 3000 CHARACTERS OF HTML:\n")
    print(page.content()[:3000])

    input("\nPress Enter to close browser...")

    browser.close()