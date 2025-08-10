import re
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Go to the admin login page
    page.goto("http://127.0.0.1:8000/admin/login/")

    # Fill in the credentials
    page.get_by_label("Имя пользователя").fill("admin")
    page.get_by_label("Пароль").fill("admin123")

    # Click the login button
    page.get_by_role("button", name="Войти").click()

    # Take a screenshot of the dashboard page
    page.screenshot(path="jules-scratch/verification/dashboard.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
