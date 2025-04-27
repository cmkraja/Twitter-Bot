from playwright.sync_api import sync_playwright
from datetime import datetime
import tweepy

# --- Twitter API keys ---
bearer_token = "AAAAAAAAAAAAAAAAAAAAAKnU0QEAAAAA%2BXDLHNtDYv7zLy9z%2BCBHHOcDM0A%3DXUsbdDHb9CMaaFNmq72JuEeUuRDVUIRzWMLNJ1xYBGTyxxJYDX"
consumer_key = "Ux7ZFOV391n4oPiSM7aFprXBZ"
consumer_secret = "lVHb3J8lqjmzHX7ksi2oGinhHbfrr6PNE1Tp1nFdivEzBm5zGD"
access_token = "1909115498278641664-V25HblmI2Ek85nbPOcIRsc0EqdT0Zk"
access_token_secret = "IcH9e4ADMpAlmFyPr8vWH2sABEvImrvN5iINYm4m1X09x"

# --- Authenticate with Twitter ---
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

BROWSERLESS_WS_ENDPOINT = "wss://chrome.browserless.io?token=SCu5irZ0a6iZKpd039838ed2d59a3a2b169ff5c501"

# Get 22K/24K Gold and Silver price in INR (Scraped from goodreturns.in) ---
def get_metal_value():
    # 24K and 22K gold prices
    g_24k = ''
    g_22k = ''
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(BROWSERLESS_WS_ENDPOINT)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
        )

        page = context.new_page()
        page.goto("https://www.goodreturns.in/gold-rates/chennai.html", wait_until="domcontentloaded")
        page.wait_for_selector("#moneyweb-wrapper #moneyweb-leftPanel .gold-rate-container .gold-each-container", timeout=15000)

        # Query all elements
        elements = page.query_selector_all("#moneyweb-wrapper #moneyweb-leftPanel .gold-rate-container .gold-each-container")

        # store their text content
        for idx, el in enumerate(elements):
            # type = el.query_selector_all('.gold-common-head')[0].inner_text()
            price = el.query_selector_all('.gold-common-head')[1].inner_text()
            # print(f"{type} Gold price is: {price}")
            if idx == 0:
                g_22k = price
            elif idx == 1:
                g_24k = price
            else:
                break

        browser.close()

    # Silver price
    silver_1g = ''
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(BROWSERLESS_WS_ENDPOINT)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
        )

        page = context.new_page()
        page.goto("https://www.goodreturns.in/silver-rates/chennai.html", wait_until="domcontentloaded")
        page.wait_for_selector("#moneyweb-wrapper #moneyweb-leftPanel .gold-rate-container .gold-each-container", timeout=15000)

        # Query all elements
        elements = page.query_selector_all("#moneyweb-wrapper #moneyweb-leftPanel .gold-rate-container .gold-each-container")

        # store their text content
        for idx, el in enumerate(elements):
            # type = el.query_selector_all('.gold-common-head')[0].inner_text()
            price = el.query_selector_all('.gold-common-head')[1].inner_text()
            # print(f"{type} price is: {price}")
            if idx == 0:
                silver_1g = price
            else:
                break

        browser.close()

    return g_24k, g_22k, silver_1g

# --- Get Market Data ---
def get_financial_data():
    # USD/INR value
    usd_inr = ""
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(BROWSERLESS_WS_ENDPOINT)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
        )

        page = context.new_page()
        # page.goto("https://www.goodreturns.in/currency/indian-rupee-inr-to-united-states-dollar-usd-converter.html", wait_until="domcontentloaded")
        page.goto("https://www.goodreturns.in/currency/united-states-dollar-usd-to-indian-rupee-inr-converter.html", wait_until="domcontentloaded")
        page.wait_for_selector("#moneyweb-wrapper #moneyweb-leftPanel .currency-converter-container", timeout=15000)

        # Query all elements
        elements = page.query_selector_all("#moneyweb-wrapper #moneyweb-leftPanel .currency-converter-container .result .gr-green-color")

        # store their text content
        for idx, el in enumerate(elements):
            if idx == 0:
                value = el.inner_text()
                usd_inr = round(float(value), 2)
                # value = 1/float(el.inner_text())
                # print(f"1 USD = ₹{round(value, 2)} INR")
                # usd_inr = round(value, 2)
            else:
                break
        browser.close()
    
    # nifty 50 value
    nifty = ""
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(BROWSERLESS_WS_ENDPOINT)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
        )

        page = context.new_page()
        page.goto("https://www.goodreturns.in/nse/", wait_until="domcontentloaded")
        page.wait_for_selector("#moneyweb-wrapper #moneyweb-leftPanel .moneyweb-tabsContent", timeout=15000)

        # Query all elements
        elements = page.query_selector_all("#moneyweb-wrapper #moneyweb-leftPanel .moneyweb-tabsContent table tbody tr")

        # store their text content
        nifty = elements[4].query_selector_all('td')[1].inner_text()
        # print(f"Nifty 50: {value}")
        browser.close()

    return usd_inr, nifty

# --- Format and Tweet ---
def post_market_update():
    date_str = datetime.now().strftime("%d %b %Y")
    gold_24k, gold_22k, silver = get_metal_value()
    usd_inr, nifty = get_financial_data()
    tweet = f"""{date_str} - Market Captured 📊:

🪙 Gold 24K → {gold_24k} /g
🪙 Gold 22K → {gold_22k} /g
⚪ Silver → {silver} /g
💵 $1 USD → ₹{usd_inr} INR
📈 Nifty 50 → {nifty}

🔔 Follow @GetMarketPulse 🔁 Auto-Updated daily!
#GoldRate #SilverRate #DollarRate #Nifty50
"""

    # tweet = "Hi, Test tweet!"
    response = client.create_tweet(text=tweet)
    print("Tweet ID:", response.data["id"])
    print("✅ Tweet posted successfully!")
    print(tweet)

# --- Run it ---
post_market_update()