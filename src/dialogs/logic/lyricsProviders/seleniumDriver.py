from selenium import webdriver
#from selenium.webdriver.firefox.options import Options

#opt = Options()
#opt.headless = True

#Best practices with Selenium say to create a new driver for each get and then quit()
def getHtmlWithDriver(url):
    #driver = webdriver.Firefox(options=opt)
    driver = webdriver.PhantomJS()
    driver.get(url)
    return_html = driver.page_source.encode("utf-8")
    driver.quit()
    return return_html


#But heck with best practices we want this thing to be fast dangit!
class GeckoDriver: pass