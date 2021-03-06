import pytest
import os
import rootpath
import shutil

def pytest_html_report_title(report):
    report.title = "BookStore API Test Report"

def pytest_sessionstart(session):
    path = os.path.join(rootpath.detect(), "reports")
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def pytest_sessionfinish(session, exitstatus):
    pass

# @pytest.fixture
# def json_loader():
#     """Loads data from JSON file"""
#     def _loader(filename):
#         with open(filename, 'r') as f:
#             data = json.load(f)
#         return data
#     return _loader

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """This hook will create a HTML report"""
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # driver = item.funcargs['request'].getfixturevalue('driver')
            # timestamp = datetime.now().strftime('%H-%M-%S.%f')[:-3]
            # path = os.path.join(rootpath.detect(), "reports", "screenshot_" + timestamp + ".png")
            # driver.save_screenshot(path)
            # extra.append(pytest_html.extras.image(path))
            pass
        report.extra = extra
    pass




