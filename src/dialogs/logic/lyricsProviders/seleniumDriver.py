from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver.firefox.options import Options

#opt = Options()
#opt.headless = True

dc = dict(DesiredCapabilities.PHANTOMJS)
dc["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"

#Best practices with Selenium say to create a new driver for each get and then quit()
def getHtmlWithDriver(url):
    #driver = webdriver.Firefox(options=opt)
    driver = webdriver.PhantomJS(desired_capabilities=dc)
    driver.set_window_size(1024, 768)
    driver.get(url)
    return_html = driver.page_source.encode("utf-8")
    driver.quit()
    return return_html


#But heck with best practices we want this thing to be fast dangit!
class GeckoDriver: pass