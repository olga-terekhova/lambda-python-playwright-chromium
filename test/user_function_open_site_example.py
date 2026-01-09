import traceback
import boto3

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

def OpenSite(ID, URL, bucket, output_dir):
    
    from playwright.sync_api import sync_playwright

    key_dir = output_dir + "/" + ID + "/"
    screenshot_key = key_dir +"screenshot.png"
    page_key = key_dir + "page.html"
    s3 = boto3.client("s3")

    s = """
    if (navigator.webdriver === false) {
    // Post Chrome 89.0.4339.0 and already good
    } else if (navigator.webdriver === undefined) {
    // Pre Chrome 89.0.4339.0 and already good
    } else {
    // Pre Chrome 88.0.4291.0 and needs patching
    delete Object.getPrototypeOf(navigator).webdriver
    }

    """
 
    
    try:
        with sync_playwright() as p:
            
            browser = p.chromium.launch(headless=True, 
                                        args= get_chromium_on_aws_lambda_flags() )  # Launch Chromium browser. Arguments are important for running within AWS Lambda. 
            
            # Desktop Chrome device settings
            desktop_chrome = p.devices["Desktop Chrome"]
            extra_headers = {
                "Sec-CH-UA": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
                "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,fr-FR;q=0.7,fr;q=0.6",
                "Sec-Fetch-Site": "cross-site"
            }

            # Create browser context with Desktop Chrome emulation
            context = browser.new_context(
                **desktop_chrome,
                extra_http_headers=extra_headers 
            )
            
            # Create page and pass initialization script
            page = context.new_page()      
            page.add_init_script(s)

            # Navigate to the URL
            page.goto(URL, wait_until="load") 

            # Take screenshot into memory (bytes)
            screenshot_bytes = page.screenshot(full_page=True)

            # Upload to S3
            s3.put_object(
                Bucket=bucket,
                Key=screenshot_key,
                Body=screenshot_bytes,
                ContentType="image/png"
            )

            # Get full DOM as serialized HTML
            dom_html = page.content()

            # Upload to S3
            s3.put_object(
                Bucket=bucket,
                Key=page_key,
                Body=dom_html.encode("utf-8"),
                ContentType="text/html; charset=utf-8"
            )

            str = f"Success: The screenshot and the DOM-tree for {page.title()} were put in {key_dir}"               # Print the page title
            browser.close()                 # Close the browser
    
    except Exception as e:
        tb = traceback.print_exc()
        str = f"Error: {str(e)} {tb}"
               


    return str
