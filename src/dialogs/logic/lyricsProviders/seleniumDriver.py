from selenium import webdriver
from selenium.webdriver.firefox.options import Options

opt = Options()
opt.headless = True

#Best practices with Selenium say to create a new driver for each get and then quit()
def getHtmlWithDriver(url):
    driver = webdriver.Firefox(options=opt)
    driver.get(url)
    return_html = driver.page_source.encode("utf-8")
    driver.quit()
    return return_html