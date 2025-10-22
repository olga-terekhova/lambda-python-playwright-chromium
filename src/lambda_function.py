from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
   browser = playwright.chromium.launch()
   page = browser.new_page()
   page.goto("https://example.com")
   str_res = page.title()
   browser.close()
   return str_res

def handler(event, context):
   with sync_playwright() as playwright:
      res = run(playwright)
    
   return 'Title is: ' + res