#!/usr/bin/env python

import time
import threading
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException

options = Options()
options.add_argument(r"user-data-dir=/home/ivand/.config/chromium")
options.add_argument(r"profile-directory=Profile 2")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(.7)


class JobApplicationBot:

    def __init__(self):
        self.is_applying = False
        self.retry_threshold = 2

    def scroll(self, h):
        driver.execute_script(f"arguments[0].scrollTo(0, {h})",
                              driver.find_element(By.CLASS_NAME, "jobs-search-results-list"))

    def load_all_jobs(self):
        for i in range(0, 3600, 100):
            self.scroll(i)
            time.sleep(.1)

    def click_if_present(self, selector):
        while True:
            try:
                driver.find_element(By.CSS_SELECTOR, selector).click()
            except (StaleElementReferenceException):
                continue
            break

    def click_element(self, selector):
        for i in range(self.retry_threshold):
            try:
                self.click_if_present(selector)
                return True
            except (NoSuchElementException):
                continue
            except (ElementClickInterceptedException):
                continue
        return False

    def is_element_present(self, selector):
        result = False
        for i in range(self.retry_threshold):
            try:
                el = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(el) > 0:
                    result = True
                    break
            except (NoSuchElementException):
                time.sleep(.2)
                continue
        return result

    def choose_resume(self):
        print("choose resume")
        self.click_element(".jobs-resume-picker__resume-btn-container")

    def continue_next(self):
        print("continue next")
        self.click_element("[aria-label='Continue to next step']")

    def review_application(self):
        print("review application")
        self.click_element("[aria-label='Review your application']")

    def submit_application(self):
        print("submit application")
        self.click_element("[aria-label='Submit application']")
        self.is_applying = False

    def no_element_present(self):
        print("nothing...")
        self.is_applying = False

    def error(self):
        print("error...")
        self.is_applying = False

    def list_elements_present(self):
        selector = ".artdeco-inline-feedback--error, .jobs-resume-picker__resume-btn-container, [aria-label='Continue to next step'], [aria-label='Review your application'], [aria-label='Submit application']"
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        print(elements)

    def determine_next_step(self):
        elements = self.list_elements_present()
        print(elements)
        if elements["error"]:
            return self.error
        if elements["resume"]:
            return self.choose_resume
        if elements["continue"]:
            return self.continue_next
        if elements["review"]:
            return self.review_application
        if elements["submit"]:
            return self.submit_application
        return self.no_element_present

    def apply(self):
        if not self.is_element_present(".artdeco-inline-feedback--success"):
            if self.click_element(".jobs-apply-button"):
                self.is_applying = True
        while self.is_applying:
            self.determine_next_step()()
        time.sleep(1)
        if self.is_element_present(".artdeco-modal__dismiss"):
            self.click_element(".artdeco-modal__dismiss")
            time.sleep(1)
            if self.is_element_present("[data-control-name='discard_application_confirm_btn']"):
                self.click_element(
                    "[data-control-name='discard_application_confirm_btn']")
                time.sleep(1)

    def get_jobs(self):
        return driver.find_elements(By.CLASS_NAME, "artdeco-entity-lockup__title")

    def select_job(self, index):
        self.get_jobs()[index].click()

    def select_page(self, index):
        self.click_element(f"[aria-label='Page {index}']")


driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&f_WT=2&geoId=91000000&keywords=java%20software%20engineer&location=European%20Union&refresh=true")


time.sleep(3)
bot = JobApplicationBot()


def apply_on_page(page):
    bot.select_page(page)
    time.sleep(2)
    bot.load_all_jobs()
    for i in range(len(bot.get_jobs()) - 1):
        time.sleep(1)
        bot.select_job(i)
        time.sleep(1)
        # bot.apply()
        bot.click_element(".jobs-apply-button")
        bot.list_elements_present()
        time.sleep(3)


for i in range(1, 100):
    apply_on_page(1)
