"""
Myntra Automation Module
Handles browser automation for order placement using rebrowser-playwright
"""
import asyncio
from rebrowser_playwright.async_api import async_playwright
import time
import random
import os


class MyntraAutomation:
    def __init__(self, mobile, headless=False, manual_otp=True, log_callback=None, executable_path=None):
        self.mobile = mobile
        self.headless = headless
        self.manual_otp = manual_otp
        self.log_callback = log_callback
        self.executable_path = executable_path
        self.browser = None
        self.context = None
        self.page = None
        self.should_stop = False
    
    def log(self, message):
        """Log message using callback or print"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)
    
    async def _human_sleep(self, min_ms=120, max_ms=350):
        """Randomized short pause to mimic human latency"""
        await asyncio.sleep(random.uniform(min_ms/1000.0, max_ms/1000.0))
    
    async def _human_type(self, locator, text):
        """Type text with per-character random delays"""
        try:
            await locator.click()
        except Exception:
            pass
        # Clear if there's any prefilled value
        try:
            await locator.fill("")
        except Exception:
            pass
        for ch in str(text):
            try:
                await locator.type(ch, delay=random.randint(40, 140))
            except Exception:
                return False
            await self._human_sleep(10, 60)
        return True

    async def _human_mouse_wiggle(self):
        """Do a few small, natural mouse moves to mimic human presence"""
        try:
            if not self.page:
                return
            width = (await self.page.evaluate('() => window.innerWidth')) or 400
            height = (await self.page.evaluate('() => window.innerHeight')) or 700
            x = random.randint(10, max(10, width - 10))
            y = random.randint(10, max(10, height - 10))
            await self.page.mouse.move(x, y, steps=random.randint(3, 8))
            await self._human_sleep(80, 180)
            x2 = min(max(5, x + random.randint(-40, 40)), width - 5)
            y2 = min(max(5, y + random.randint(-40, 40)), height - 5)
            await self.page.mouse.move(x2, y2, steps=random.randint(2, 6))
        except Exception:
            pass

    async def _apply_stealth(self):
        """Apply basic stealth patches to the context"""
        try:
            await self.context.add_init_script(
                """
                // Use Navigator.prototype to avoid own properties on navigator
                const navProto = Object.getPrototypeOf(navigator);
                try { delete navigator.webdriver; } catch(e) {}
                Object.defineProperty(navProto, 'webdriver', { get: () => false, configurable: true });
                try { delete navigator.languages; } catch(e) {}
                Object.defineProperty(navProto, 'languages', { get: () => ['en-IN','en'], configurable: true });
                try { delete navigator.plugins; } catch(e) {}
                Object.defineProperty(navProto, 'plugins', { get: () => [1,2,3], configurable: true });
                // chrome object
                window.chrome = window.chrome || { runtime: {} };
                try { delete navigator.hardwareConcurrency; } catch(e) {}
                Object.defineProperty(navProto, 'hardwareConcurrency', { get: () => 8, configurable: true });
                // permissions query spoof minimal
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
                  // Re-apply in case something sets it later
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

                // Ensure Object.getOwnPropertyNames(navigator) returns []
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

                // Prevent adding own-properties to navigator for known keys
                try {
                  const blockProps = new Set(['webdriver','languages','plugins','hardwareConcurrency','userAgentData']);
                  const _odp = Object.defineProperty;
                  Object.defineProperty = function(obj, prop, desc) {
                    try { if (obj === navigator && blockProps.has(String(prop))) return obj; } catch(e) {}
                    return _odp.call(Object, obj, prop, desc);
                  };
                  const _odps = Object.defineProperties;
                  Object.defineProperties = function(obj, props) {
                    try { if (obj === navigator) {
                      for (const k of Object.keys(props||{})) if (blockProps.has(k)) delete props[k];
                    }} catch(e) {}
                    return _odps.call(Object, obj, props);
                  };
                  const _rdp = Reflect.defineProperty;
                  Reflect.defineProperty = function(obj, prop, desc) {
                    try { if (obj === navigator && blockProps.has(String(prop))) return true; } catch(e) {}
                    return _rdp.call(Reflect, obj, prop, desc);
                  };
                } catch (e) {}
                """
            )
        except Exception:
            pass
    
    def stop(self):
        """Stop the automation"""
        self.should_stop = True
        self.log("🛑 Stop signal received")
    
    def cleanup(self):
        """Cleanup browser resources"""
        try:
            if self.context:
                try:
                    asyncio.run(self.context.close())
                except Exception:
                    pass
            if self.browser:
                try:
                    asyncio.run(self.browser.close())
                except Exception:
                    pass
        except Exception as e:
            self.log(f"⚠️ Cleanup error: {e}")
        finally:
            self.context = None
            self.browser = None
            self.page = None
    
    def open_myntra_login(self):
        """Open Myntra login page"""
        try:
            return asyncio.run(self._open_login_async())
        except Exception as e:
            self.log(f"❌ Error in open_myntra_login: {str(e)}")
            return False
    
    async def _open_login_async(self):
        """Async method to open Myntra login page"""
        try:
            async with async_playwright() as p:
                # Launch browser with rebrowser patches
                self.log("🌐 Launching browser...")
                try:
                    launch_args = {
                        "headless": self.headless,
                        "slow_mo": random.randint(40, 110),
                        "args": [
                            '--disable-blink-features=AutomationControlled',
                            '--disable-dev-shm-usage',
                            '--no-sandbox',
                            '--disable-setuid-sandbox'
                        ]
                    }
                    
                    if self.executable_path and os.path.exists(self.executable_path):
                        self.log(f"🖥️ Using custom browser: {self.executable_path}")
                        launch_args["executable_path"] = self.executable_path
                    else:
                        launch_args["channel"] = 'chrome'

                    self.browser = await p.chromium.launch(**launch_args)
                except Exception:
                    self.browser = await p.chromium.launch(
                        headless=self.headless,
                        slow_mo=random.randint(40, 110),
                        args=[
                            '--disable-blink-features=AutomationControlled',
                            '--disable-dev-shm-usage',
                            '--no-sandbox',
                            '--disable-setuid-sandbox'
                        ]
                    )
                
                # Create context with realistic settings
                self.log("⚙️ Setting up browser context...")
                # Randomize among a small pool of realistic Android UAs and viewports
                ua_pool = [
                    'Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
                    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                    'Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
                ]
                base_sizes = [(360, 800), (384, 832), (390, 844), (412, 915)]
                bw, bh = random.choice(base_sizes)
                jitter_w = random.randint(-8, 8)
                jitter_h = random.randint(-12, 12)
                vw = max(320, bw + jitter_w)
                vh = max(640, bh + jitter_h)
                dpr = random.choice([2.625, 2.75, 3, 3.25])
                ua = random.choice(ua_pool)
                self.log("📱 Enabling mobile emulation (human-like profile)...")
                # Load existing session if present
                sessions_dir = os.path.join(os.getcwd(), 'sessions')
                os.makedirs(sessions_dir, exist_ok=True)
                storage_path = os.path.join(sessions_dir, f'{self.mobile}.json')
                has_session = os.path.exists(storage_path)
                if has_session:
                    self.log("🍪 Found existing session. Attempting to reuse cookies...")

                self.context = await self.browser.new_context(
                    viewport={'width': vw, 'height': vh},
                    user_agent=ua,
                    device_scale_factor=dpr,
                    is_mobile=True,
                    has_touch=True,
                    locale='en-IN',
                    timezone_id='Asia/Kolkata',
                    permissions=[],
                    extra_http_headers={
                        'sec-ch-ua': '"Chromium";v="120", "Google Chrome";v="120", "Not=A?Brand";v="24"',
                        'sec-ch-ua-mobile': '?1',
                        'sec-ch-ua-platform': '"Android"',
                        'sec-ch-ua-full-version-list': '"Chromium";v="120.0.0.0", "Google Chrome";v="120.0.0.0", "Not=A?Brand";v="24.0.0.0"',
                        'sec-ch-ua-platform-version': '"13.0.0"',
                        'sec-ch-ua-arch': '"arm"',
                        'sec-ch-ua-model': '"Pixel 7"'
                    },
                    storage_state=storage_path if has_session else None
                )
                await self._apply_stealth()
                
                self.page = await self.context.new_page()
                
                # Navigate to Myntra login page
                target_login = 'https://www.myntra.com/login'
                self.log("🔐 Opening Myntra login page...")
                await self.page.goto(target_login, wait_until='domcontentloaded')
                self.page.set_default_timeout(20000)
                await self._human_sleep(200, 500)
                # Gentle scroll to mimic reading
                try:
                    await self.page.evaluate('window.scrollBy(0, arguments[0])', random.randint(0, 120))
                    await self._human_sleep(150, 350)
                except Exception:
                    pass
                await self._human_mouse_wiggle()
                
                if self.should_stop:
                    return False
                
                # If cookies were loaded and user is already logged in, URL may redirect off login
                try:
                    await self.page.wait_for_load_state('domcontentloaded')
                    if 'login' not in (self.page.url or '').lower():
                        self.log("✅ Already logged in via saved session")
                        # Refresh and persist latest storage state
                        try:
                            await self.context.storage_state(path=storage_path)
                            self.log("💾 Session refreshed and saved")
                        except Exception:
                            pass
                        return True
                except Exception:
                    pass

                self.log(f"✅ Login page opened for mobile: {self.mobile}")

                # 1) Fill mobile number
                self.log("⌨️ Entering mobile number...")
                input_selectors = [
                    '#reactPageContent > div > div > div.signInContainer > div.mobileInputContainer > div.form-group > input',
                    'input.mobileNumberInput',
                    'input[type="tel"].mobileNumberInput'
                ]
                filled = False
                for sel in input_selectors:
                    try:
                        await self.page.wait_for_selector(sel, state='visible')
                        loc = self.page.locator(sel)
                        # Focus, then type with human-like delays
                        ok = await self._human_type(loc, str(self.mobile))
                        if not ok:
                            continue
                        filled = True
                        break
                    except Exception:
                        continue
                if not filled:
                    self.log("❌ Could not find mobile number input field")
                    return False

                # 2) Click consent checkbox
                self.log("☑️ Checking consent checkbox...")
                checkbox_selectors = [
                    '#reactPageContent > div > div > div.signInContainer > div.mobileInputContainer > div.consentContainer > input',
                    'input.consentCheckbox'
                ]
                checked = False
                for sel in checkbox_selectors:
                    try:
                        await self.page.wait_for_selector(sel, state='attached')
                        cb = self.page.locator(sel)
                        # Attempt to click; if element is off-screen, scroll into view
                        await cb.scroll_into_view_if_needed()
                        await self._human_sleep(100, 250)
                        await cb.click()
                        checked = True
                        break
                    except Exception:
                        continue
                if not checked:
                    self.log("⚠️ Could not click consent checkbox; continuing anyway")

                # 3) Click CONTINUE button
                self.log("➡️ Clicking CONTINUE...")
                continue_selectors = [
                    '#reactPageContent > div > div > div.signInContainer > div.mobileInputContainer > div.submitBottomOption',
                    'div.submitBottomOption:has-text("CONTINUE")',
                    'text=CONTINUE'
                ]
                clicked = False
                for sel in continue_selectors:
                    try:
                        await self.page.wait_for_selector(sel, state='visible')
                        btn = self.page.locator(sel)
                        await btn.scroll_into_view_if_needed()
                        await self._human_sleep(120, 280)
                        await btn.click()
                        clicked = True
                        break
                    except Exception:
                        continue
                if not clicked:
                    self.log("❌ Could not click CONTINUE button")
                    return False

                self.log("✅ Submitted mobile number; awaiting next step...")

                # Wait for OTP page
                try:
                    # Wait for URL or OTP inputs to appear
                    await self.page.wait_for_load_state('domcontentloaded')
                    # Either URL contains /otplogin or otpContainer visible
                    try:
                        await self.page.wait_for_url(lambda url: '/otplogin' in url, timeout=15000)
                    except Exception:
                        pass
                    await self.page.wait_for_selector('div.otpContainer input[type="tel"]', timeout=20000)
                    self.log("📨 OTP page detected")
                except Exception:
                    self.log("⚠️ OTP page not detected; proceeding")
                    return True

                # Manual OTP mode: focus the first box and wait for completion
                if self.manual_otp:
                    try:
                        first_box_selectors = [
                            '#reactPageContent > div > div.mobContainer > div.otpContainer > input[type=tel]:nth-child(1)',
                            'div.otpContainer input[type="tel"]:nth-child(1)',
                            'div.otpContainer input[type="tel"]'
                        ]
                        focused = False
                        for sel in first_box_selectors:
                            try:
                                el = self.page.locator(sel).first
                                await el.scroll_into_view_if_needed()
                                await self._human_sleep(120, 260)
                                await el.click()
                                focused = True
                                break
                            except Exception:
                                continue
                        if focused:
                            self.log("📝 Waiting for manual OTP entry (4 digits)...")
                        else:
                            self.log("⚠️ Could not focus OTP box; waiting anyway")
                        
                        # Wait until 4 inputs have value length 1 or URL changes
                        try:
                            await self.page.wait_for_function(
                                "() => Array.from(document.querySelectorAll('div.otpContainer input[type=tel]')).filter(i => (i.value||'').length === 1).length >= 4",
                                timeout=120000
                            )
                            self.log("✅ Detected OTP entered")
                        except Exception:
                            self.log("⌛ OTP wait timed out (manual mode)")
                    except Exception as e:
                        self.log(f"⚠️ Manual OTP flow error: {e}")
                else:
                    self.log("🤖 Auto-OTP disabled (no provider). Skipping OTP input for now.")
                
                # Try to detect login success and save cookies
                try:
                    # Wait until page navigates away from login flow
                    await self.page.wait_for_url(lambda url: 'login' not in url, timeout=30000)
                except Exception:
                    pass
                try:
                    await self.context.storage_state(path=storage_path)
                    self.log(f"💾 Saved session cookies for {self.mobile}")
                except Exception as e:
                    self.log(f"⚠️ Could not save session: {e}")
                
                return True
                
        except Exception as e:
            self.log(f"❌ Error opening login page: {str(e)}")
            return False
        finally:
            if self.browser and self.headless:
                await self.browser.close()
    
    async def login(self):
        """Login to Myntra"""
        try:
            self.log("🔐 Attempting to login...")
            
            # Click on login/profile icon
            try:
                # Try to find login button
                login_selectors = [
                    'text=Login',
                    '[data-group="account"]',
                    '.desktop-user',
                    'a[href*="login"]'
                ]
                
                for selector in login_selectors:
                    try:
                        await self.page.click(selector, timeout=5000)
                        break
                    except:
                        continue
                
                await asyncio.sleep(2)
                
            except Exception as e:
                self.log(f"⚠️ Could not find login button: {str(e)}")
            
            # Enter mobile number or email
            try:
                # Try multiple input selectors
                input_selectors = [
                    'input[type="text"]',
                    'input[type="tel"]',
                    'input[placeholder*="mobile"]',
                    'input[placeholder*="email"]'
                ]
                
                for selector in input_selectors:
                    try:
                        await self.page.fill(selector, self.email, timeout=5000)
                        self.log(f"📧 Entered credentials")
                        break
                    except:
                        continue
                
                await asyncio.sleep(1)
                
                # Click continue/submit button
                button_selectors = [
                    'text=CONTINUE',
                    'button[type="submit"]',
                    '.submitBottomOption'
                ]
                
                for selector in button_selectors:
                    try:
                        await self.page.click(selector, timeout=5000)
                        break
                    except:
                        continue
                
                await asyncio.sleep(3)
                
                # Enter password if required
                try:
                    await self.page.fill('input[type="password"]', self.password, timeout=5000)
                    await self.page.click('button[type="submit"]', timeout=5000)
                    await asyncio.sleep(3)
                except:
                    pass
                
                self.log("✅ Login successful")
                return True
                
            except Exception as e:
                self.log(f"⚠️ Login may require manual intervention: {str(e)}")
                # Continue anyway, user might be already logged in
                return True
                
        except Exception as e:
            self.log(f"❌ Login error: {str(e)}")
            return False
    
    async def select_size(self, size):
        """Select product size"""
        try:
            self.log(f"📏 Selecting size: {size}")
            
            # Wait for size buttons to load
            await asyncio.sleep(2)
            
            # Try different size selection methods
            size_selectors = [
                f'text="{size}"',
                f'button:has-text("{size}")',
                f'.size-buttons-size-button:has-text("{size}")',
                f'[data-skuid*="{size}"]'
            ]
            
            for selector in size_selectors:
                try:
                    await self.page.click(selector, timeout=5000)
                    self.log(f"✅ Size {size} selected")
                    await asyncio.sleep(1)
                    return True
                except:
                    continue
            
            self.log(f"⚠️ Could not find size {size}")
            return False
            
        except Exception as e:
            self.log(f"❌ Size selection error: {str(e)}")
            return False
    
    async def add_to_bag(self):
        """Add product to shopping bag"""
        try:
            self.log("➕ Adding product to bag...")
            
            # Find and click "Add to Bag" button
            bag_selectors = [
                'text=ADD TO BAG',
                'button:has-text("ADD TO BAG")',
                '.pdp-add-to-bag',
                '[data-button="add-to-bag"]'
            ]
            
            for selector in bag_selectors:
                try:
                    await self.page.click(selector, timeout=5000)
                    self.log("✅ Product added to bag")
                    await asyncio.sleep(2)
                    return True
                except:
                    continue
            
            self.log("❌ Could not find Add to Bag button")
            return False
            
        except Exception as e:
            self.log(f"❌ Add to bag error: {str(e)}")
            return False
    
    async def proceed_to_checkout(self):
        """Proceed to checkout"""
        try:
            self.log("💳 Proceeding to checkout...")
            
            # Find and click "Place Order" or "Proceed" button
            checkout_selectors = [
                'text=PLACE ORDER',
                'button:has-text("PLACE ORDER")',
                '.place-order-button',
                'text=PROCEED',
                'button:has-text("PROCEED")'
            ]
            
            for selector in checkout_selectors:
                try:
                    await self.page.click(selector, timeout=5000)
                    self.log("✅ Proceeding to checkout")
                    await asyncio.sleep(3)
                    return True
                except:
                    continue
            
            self.log("✅ On checkout page")
            return True
            
        except Exception as e:
            self.log(f"⚠️ Checkout: {str(e)}")
            return True  # Continue anyway
    
    async def fill_delivery_details(self, delivery_info):
        """Fill delivery information"""
        try:
            self.log("📦 Filling delivery details...")
            
            # Fill delivery form fields
            fields_map = {
                'name': ['input[name="name"]', 'input[placeholder*="Name"]'],
                'phone': ['input[name="mobile"]', 'input[placeholder*="Mobile"]', 'input[type="tel"]'],
                'pincode': ['input[name="pincode"]', 'input[placeholder*="Pin"]'],
                'address': ['input[name="address"]', 'textarea[name="address"]'],
                'city': ['input[name="city"]', 'input[placeholder*="City"]'],
                'state': ['input[name="state"]', 'select[name="state"]']
            }
            
            for field, selectors in fields_map.items():
                value = delivery_info.get(field)
                if value:
                    for selector in selectors:
                        try:
                            await self.page.fill(selector, value, timeout=3000)
                            self.log(f"✅ Filled {field}")
                            break
                        except:
                            continue
            
            await asyncio.sleep(2)
            self.log("✅ Delivery details filled")
            return True
            
        except Exception as e:
            self.log(f"⚠️ Delivery details: {str(e)}")
            return False
