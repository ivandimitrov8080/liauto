#!/usr/bin/env python

import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException

options = Options()
options.add_argument(r"user-data-dir=/home/ivand/.config/chromium")
options.add_argument(r"profile-directory=Profile 2")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(1)


class JobApplicationBot:

    def __init__(self):
        self.is_applying = False
        self.has_filled = False
        self.retry_threshold = 2
        self.html_attributes = {
            "applied": "artdeco-inline-feedback--success",
            "apply": "jobs-apply-button",
            "error": "artdeco-inline-feedback--error",
            "text_input": "artdeco-text-input--input",
            "select": "data-test-text-entity-list-form-select",
            "checkbox": "fb-form-element__checkbox",
            "resume": "jobs-resume-picker__resume-btn-container",
            "continue": 'aria-label="Continue to next step"',
            "review": 'aria-label="Review your application"',
            "submit": 'aria-label="Submit application"',
            "dismiss": "artdeco-modal__dismiss",
            "discard": 'data-control-name="discard_application_confirm_btn"'
        }
        self.selectors = {
            "applied": ".artdeco-inline-feedback--success",
            "apply": ".jobs-apply-button",
            "error":  ".artdeco-inline-feedback--error",
            "text_input": ".jobs-easy-apply-modal .artdeco-text-input--input",
            "select": ".jobs-easy-apply-modal [data-test-text-entity-list-form-select]",
            "checkbox": ".jobs-easy-apply-modal .fb-form-element__checkbox",
            "resume": ".jobs-resume-picker__resume-btn-container",
            "continue": "[aria-label='Continue to next step']",
            "review": "[aria-label='Review your application']",
            "submit": "[aria-label='Submit application']",
            "dismiss": ".artdeco-modal__dismiss",
            "discard": "[data-control-name='discard_application_confirm_btn']"
        }

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

    def click_all_if_present(self, selector):
        while True:
            try:
                elements = driver.find_elements(
                    By.CSS_SELECTOR, selector)
                for el in elements:
                    el.click()
            except (StaleElementReferenceException):
                continue
            break

    def click_elements(self, selector):
        for i in range(self.retry_threshold):
            try:
                self.click_all_if_present(selector)
                return True
            except (NoSuchElementException):
                continue
            except (ElementClickInterceptedException):
                continue
        return False

    def ignore(self):
        print("already applied")
        self.is_applying = False

    def click_apply(self):
        print("applying...")
        self.click_element(self.selectors["apply"])

    def choose_resume(self):
        print("choose resume")
        self.click_element(self.selectors["resume"])

    def fill_empty_text_inputs(self):
        print("filling text inputs")
        fields = driver.find_elements(
            By.CSS_SELECTOR, self.selectors["text_input"])
        for f in filter(lambda f: f.get_attribute("value") == "", fields):
            f.send_keys("6")

    def fill_empty_select(self):
        print("filling select fields")
        fields = driver.find_elements(
            By.CSS_SELECTOR, self.selectors["select"])
        for f in fields:
            select = Select(f)
            if select.options[0] == select.first_selected_option:
                select.select_by_index(len(select.options) - 1)

    def fill_checkboxes(self):
        print("filling checkboxes")
        self.click_elements(self.selectors["checkbox"])

    def fill_empty_inputs(self):
        self.fill_empty_select()
        self.fill_empty_text_inputs()
        self.fill_checkboxes()
        self.has_filled = True

    def continue_next(self):
        print("continue next")
        self.click_element(self.selectors["continue"])
        self.has_filled = False

    def review_application(self):
        print("review application")
        self.click_element(self.selectors["review"])

    def submit_application(self):
        print("submit application")
        self.click_element(self.selectors["submit"])
        self.dismiss_modal()
        self.is_applying = False

    def dismiss_modal(self):
        self.click_element(self.selectors["dismiss"])
        self.is_applying = False

    def discard_application(self):
        self.click_element(self.selectors["discard"])
        self.is_applying = False

    def no_element_present(self):
        print("nothing...")
        self.is_applying = False

    def error(self):
        print("error...")
        self.dismiss_modal()
        self.discard_application()

    def list_elements_present(self):
        result = {
            "applied": False,
            "apply": False,
            "error": False,
            "text_input": False,
            "select": False,
            "checkbox": False,
            "resume": False,
            "continue": False,
            "review": False,
            "submit": False,
            "dismiss": False,
            "discard": False
        }
        selector = ",".join(self.selectors.values())
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        for el in filter(lambda el: el.is_displayed(), elements):
            html = str(el.get_attribute("outerHTML"))
            if self.html_attributes["applied"] in html:
                result["applied"] = True
            if self.html_attributes["apply"] in html:
                result["apply"] = True
            if self.html_attributes["error"] in html:
                result["error"] = True
            if self.html_attributes["text_input"] in html:
                result["text_input"] = True
            if self.html_attributes["select"] in html:
                result["select"] = True
            if self.html_attributes["checkbox"] in html:
                result["checkbox"] = True
            if self.html_attributes["resume"] in html:
                result["resume"] = True
            if self.html_attributes["continue"] in html:
                result["continue"] = True
            if self.html_attributes["review"] in html:
                result["review"] = True
            if self.html_attributes["submit"] in html:
                result["submit"] = True
            if self.html_attributes["dismiss"] in html:
                result["dismiss"] = True
            if self.html_attributes["discard"] in html:
                result["discard"] = True
        return result

    def determine_next_step(self):
        while True:
            try:
                elements = self.list_elements_present()
                if elements["error"]:
                    return self.error
                if (elements["text_input"] or elements["select"] or elements["checkbox"]) and not self.has_filled:
                    return self.fill_empty_inputs
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
                if elements["dismiss"]:
                    return self.dismiss_modal
                if elements["discard"]:
                    return self.discard_application
                if elements["applied"]:
                    return self.ignore
                if elements["apply"]:
                    return self.click_apply
            except StaleElementReferenceException:
                pass
            break
        return self.no_element_present

    def apply(self):
        self.is_applying = True
        while self.is_applying:
            self.determine_next_step()()
        time.sleep(1)

    def get_jobs(self):
        return driver.find_elements(By.CLASS_NAME, "artdeco-entity-lockup__title")

    def select_job(self, index):
        while True:
            try:
                self.get_jobs()[index].click()
                self.has_filled = False
            except ElementClickInterceptedException:
                self.error()
            break

    def select_page(self, index):
        self.click_element(f"[aria-label='Page {index}']")


java_jobs_url = "https://www.linkedin.com/jobs/search/?f_AL=true&f_WT=2&geoId=91000000&keywords=java%20software%20engineer&location=European%20Union&refresh=true"
all_jobs_url = "https://www.linkedin.com/jobs/search/?f_AL=true&f_WT=2&geoId=91000000&keywords=software%20engineer&location=European%20Union&refresh=true"

driver.get(all_jobs_url)


time.sleep(3)
bot = JobApplicationBot()


def apply_on_page(page):
    bot.select_page(page)
    time.sleep(2)
    bot.load_all_jobs()
    for i in range(len(bot.get_jobs()) - 1):
        bot.select_job(i)
        time.sleep(1)
        bot.apply()


for i in range(1, 1000):
    apply_on_page(i)
