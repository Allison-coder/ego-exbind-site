"""Local browser smoke tests. Requires Playwright and a Chromium executable."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "verification"
OUT.mkdir(exist_ok=True)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/chromium-browser",
                                    headless=False, args=["--headless=new", "--no-sandbox", "--disable-dev-shm-usage"])
        report = []
        for width, height in [(1440, 1000), (390, 844), (320, 740)]:
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto((ROOT / "index.html").as_uri())
            # Load lazy images before recording layout and asset integrity.
            page.evaluate("document.querySelectorAll('img').forEach(i => i.loading = 'eager')")
            page.wait_for_function("Array.from(document.querySelectorAll('img[src]')).every(i => i.complete && i.naturalWidth > 0)")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Horizontal page overflow"
            assert page.locator(".actions a").first.get_attribute("href") == "https://github.com/Allison-coder/ego-exbind"
            page.screenshot(path=str(OUT / (str(width) + "-home.png")))
            page.screenshot(path=str(OUT / (str(width) + "-full.png")), full_page=True)
            page.locator("#tab-pmi").click()
            assert page.locator("#panel-pmi").is_visible()
            assert not page.locator("#panel-retrieval").is_visible()
            page.locator('[data-figure="pmi"]').click()
            assert page.locator("#figure-dialog").is_visible()
            page.keyboard.press("Escape")
            assert not page.locator("#figure-dialog").is_visible()
            page.locator("#tab-retrieval").click()
            page.locator("#tab-splits").click()
            assert page.locator("#panel-splits").is_visible()
            assert "24.51" in page.locator("#panel-splits").inner_text()
            page.locator("#tab-splits").press("ArrowRight")
            assert page.locator("#panel-margins").is_visible()
            assert "0.065" in page.locator("#panel-margins").inner_text()
            page.locator("#tab-overall").click()
            assert "33.70" in page.locator("#panel-overall").inner_text()
            page.locator("#results").scroll_into_view_if_needed()
            page.screenshot(path=str(OUT / (str(width) + "-results.png")))
            assert not errors, errors
            report.append({"viewport": [width, height], "assets": "loaded", "tabs": "passed",
                           "dialog": "passed", "overflow": False, "js_errors": errors})
            page.close()
        browser.close()
    (OUT / "report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
