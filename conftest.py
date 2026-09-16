import os

import pytest
from selenium import webdriver

driver = None
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--test-type")
def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store",default="Chrome", help = "browser selection")

@pytest.fixture(scope='function')
def browserInstance(request):
    global driver
    print("Starting Browser...")
    browser_name = request.config.getoption("browser_name")
    if browser_name == "Chrome":
        driver= webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.implicitly_wait(5)
    elif browser_name == "Firefox":
        driver= webdriver.Firefox()
        driver.implicitly_wait(5)
        driver.maximize_window()
    elif browser_name == "Edge":
        driver= webdriver.Edge()
        driver.implicitly_wait(5)
        driver.maximize_window()
    yield driver
    print("Stopping Browser...")
    driver.close()

@pytest.hookimpl( hookwrapper=True )
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin( 'html' )
    outcome = yield
    report = outcome.get_result()
    extra = getattr( report, 'extra', [] )

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr( report, 'wasxfail' )
        if (report.skipped and xfail) or (report.failed and not xfail):
            reports_dir = os.path.join( os.path.dirname( __file__ ), 'reports' )
            file_name = os.path.join( reports_dir, report.nodeid.replace( "::", "_" ) + ".png" )
            print( "file name is " + file_name )
            _capture_screenshot( file_name )
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append( pytest_html.extras.html( html ) )
        report.extras = extra


def _capture_screenshot(file_name):
    driver.get_screenshot_as_file(file_name)