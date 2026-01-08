def get_chromium_on_aws_lambda_flags():
    return [
        "--autoplay-policy=user-gesture-required",
        "--disable-background-networking",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-breakpad",
        "--disable-client-side-phishing-detection",
        "--disable-component-update",
        "--disable-default-apps",
        "--disable-dev-shm-usage",
        "--disable-domain-reliability",
        "--disable-extensions",
        "--disable-features=AudioServiceOutOfProcess",
        "--disable-hang-monitor",
        "--disable-ipc-flooding-protection",
        "--disable-notifications",
        "--disable-offer-store-unmasked-wallet-cards",
        "--disable-popup-blocking",
        "--disable-print-preview",
        "--disable-prompt-on-repost",
        "--disable-renderer-backgrounding",
        "--disable-setuid-sandbox",
        "--disable-speech-api",
        "--disable-sync",
        "--disk-cache-size=33554432",
        "--hide-scrollbars",
        "--ignore-gpu-blacklist",
        "--metrics-recording-only",
        "--mute-audio",
        "--no-default-browser-check",
        "--no-first-run",
        "--no-pings",
        "--no-sandbox",
        "--no-zygote",
        "--password-store=basic",
        "--use-gl=swiftshader",
        "--use-mock-keychain",
    ]

def OpenSite():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        browser = p.chromium.launch(headless=True, 
        #                            user_agent=user_agent,
                                    args= get_chromium_on_aws_lambda_flags() )  # Launch Chromium browser. Arguments are important for running within AWS Lambda. 
        
        # Desktop Chrome device settings
        desktop_chrome = p.devices["Desktop Chrome"]

        # Create browser context with Desktop Chrome emulation
        context = browser.new_context(
            **desktop_chrome
        )
        
        page = context.new_page()       # Create a new page (tab)
        page.goto("https://www.example.com") # Navigate to a URL
        str = page.title()              # Print the page title
        browser.close()                 # Close the browser
    return f"Title is: {str}"
