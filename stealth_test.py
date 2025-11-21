#!/usr/bin/env python3
"""
Simple standalone script to test rebrowser-playwright stealthiness.
- Opens https://bot-detector.rebrowser.net/
- Saves full-page screenshot and JSON/text results to diagnostics/
- Headless can be toggled via CLI flag
"""
import argparse
import asyncio
import os
import time
import json
import random
from rebrowser_playwright.async_api import async_playwright


TEST_URL = "https://bot-detector.rebrowser.net/"


async def apply_stealth(context):
    try:
        await context.add_init_script(
            """
            // Define on Navigator.prototype so navigator has no own-properties
            const navProto = Object.getPrototypeOf(navigator);
            try { delete navigator.webdriver; } catch(e) {}
            Object.defineProperty(navProto, 'webdriver', { get: () => false, configurable: true });
            // languages
            try { delete navigator.languages; } catch(e) {}
            Object.defineProperty(navProto, 'languages', { get: () => ['en-IN','en'], configurable: true });
            // plugins
            try { delete navigator.plugins; } catch(e) {}
            Object.defineProperty(navProto, 'plugins', { get: () => [1,2,3], configurable: true });
            // chrome object
            window.chrome = window.chrome || { runtime: {} };
            // hardwareConcurrency
            try { delete navigator.hardwareConcurrency; } catch(e) {}
            Object.defineProperty(navProto, 'hardwareConcurrency', { get: () => 8, configurable: true });
            // minimal permissions.query spoof
            const originalQuery = window.navigator.permissions && window.navigator.permissions.query;
            if (originalQuery) {
              window.navigator.permissions.query = (parameters) => (
                parameters && parameters.name === 'notifications' ?
                  Promise.resolve({ state: Notification.permission }) :
                  originalQuery(parameters)
              );
            }
            // Hide Playwright init scripts footprint
            try {
              const removePwInit = () => {
                try {
                  if (window.__pwInitScripts && typeof window.__pwInitScripts === 'object') {
                    for (const k of Object.keys(window.__pwInitScripts)) delete window.__pwInitScripts[k];
                  }
                  try { delete window.__pwInitScripts; } catch(e) {}
                  Object.defineProperty(window, '__pwInitScripts', { get: () => undefined, set: () => {}, configurable: true });
                } catch (e) {}
              };
              removePwInit();
              setTimeout(removePwInit, 0);
            } catch (e) {}

            // Provide navigator.userAgentData with Google Chrome brand
            try {
              const brands = [
                { brand: 'Chromium', version: '120' },
                { brand: 'Google Chrome', version: '120' },
                { brand: 'Not=A?Brand', version: '24' }
              ];
              const fullVersionList = [
                { brand: 'Chromium', version: '120.0.0.0' },
                { brand: 'Google Chrome', version: '120.0.0.0' }
              ];
              const uadata = {
                brands,
                mobile: true,
                platform: 'Android',
                getHighEntropyValues: async (hints) => ({
                  brands,
                  fullVersionList,
                  platform: 'Android',
                  platformVersion: '13.0.0',
                  architecture: 'arm',
                  model: 'Pixel 7',
                  bitness: '64'
                })
              };
              try { delete navigator.userAgentData; } catch(e) {}
              Object.defineProperty(navProto, 'userAgentData', { get: () => uadata, configurable: true });
            } catch (e) {}

            // Ensure Object.getOwnPropertyNames(navigator) and Reflect.ownKeys(navigator) return []
            try {
              const _gopn = Object.getOwnPropertyNames;
              Object.getOwnPropertyNames = function(obj) {
                try { if (obj === navigator) return []; } catch(e) {}
                return _gopn.call(Object, obj);
              };
              const _ownKeys = Reflect.ownKeys;
              Reflect.ownKeys = function(obj) {
                try { if (obj === navigator) return []; } catch(e) {}
                return _ownKeys.call(Reflect, obj);
              };
            } catch (e) {}
            """
        )
    except Exception:
        pass


async def run_test(headless: bool, mobile: bool, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    ts = int(time.time())
    headless_tag = "headless" if headless else "headed"
    png_path = os.path.join(out_dir, f"stealth_{ts}_{headless_tag}.png")
    json_path = os.path.join(out_dir, f"stealth_{ts}_{headless_tag}.json")

    async with async_playwright() as p:
        # Try to use Chrome stable channel if available; fallback to default
        try:
            browser = await p.chromium.launch(
                headless=headless,
                slow_mo=random.randint(20, 80),
                channel="chrome",
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                ],
            )
        except Exception:
            browser = await p.chromium.launch(
                headless=headless,
                slow_mo=random.randint(20, 80),
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                ],
            )
        try:
            context_kwargs = {
                "locale": "en-IN",
                "timezone_id": "Asia/Kolkata",
            }
            if mobile:
                # Pixel-like profile
                base_sizes = [(360, 800), (390, 844), (412, 915)]
                bw, bh = random.choice(base_sizes)
                context_kwargs.update(
                    viewport={"width": bw, "height": bh},
                    user_agent=(
                        "Mozilla/5.0 (Linux; Android 13; Pixel 7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Mobile Safari/537.36"
                    ),
                    device_scale_factor=3,
                    is_mobile=True,
                    has_touch=True,
                )
            # UA-CH headers (brand list including Google Chrome)
            context_kwargs.update(
                extra_http_headers={
                    'sec-ch-ua': '"Chromium";v="120", "Google Chrome";v="120", "Not=A?Brand";v="24"',
                    'sec-ch-ua-mobile': '?1',
                    'sec-ch-ua-platform': '"Android"'
                }
            )
            context = await browser.new_context(**context_kwargs)
            await apply_stealth(context)
            page = await context.new_page()

            await page.goto(TEST_URL, wait_until="domcontentloaded")
            await asyncio.sleep(random.uniform(0.25, 0.6))
            try:
                await page.mouse.move(50, 80)
                await page.mouse.move(120, 130)
            except Exception:
                pass

            # Extract JSON-like results
            result_text = None
            try:
                pre = page.locator("pre").first
                await pre.wait_for(state="visible", timeout=4000)
                result_text = await pre.inner_text()
            except Exception:
                try:
                    result_text = await page.evaluate("() => document.body.innerText")
                except Exception:
                    result_text = ""

            # Save screenshot (full page if possible)
            try:
                await page.screenshot(path=png_path, full_page=True)
            except Exception:
                try:
                    await page.screenshot(path=png_path, full_page=False)
                except Exception:
                    pass

            # Save JSON (or raw text)
            try:
                parsed = None
                try:
                    parsed = json.loads(result_text)
                except Exception:
                    parsed = {"raw": (result_text or "").strip()[:5000]}
                with open(json_path, "w") as f:
                    json.dump(parsed, f, indent=2)
            except Exception:
                pass
        finally:
            try:
                await context.close()
            except Exception:
                pass
            try:
                await browser.close()
            except Exception:
                pass

    print("Saved screenshot:", png_path)
    print("Saved results:", json_path)


def main():
    parser = argparse.ArgumentParser(description="Rebrowser Playwright stealth test")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--no-mobile", action="store_true", help="Disable mobile emulation")
    parser.add_argument("--out", default="diagnostics", help="Output directory for artifacts")
    args = parser.parse_args()

    asyncio.run(run_test(headless=args.headless, mobile=not args.no_mobile, out_dir=args.out))


if __name__ == "__main__":
    main()
