import os
import pytest
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from test_data.urls_data import valid_urls_data
from test_data.login_data import valid_login_data
import operator
import requests
import allure

from pages.page_contact import PageContact

load_dotenv()

@pytest.fixture(scope="session")
def test_config():
    return {
        'test_url': os.getenv('TEST_URL', 'https://www.romlex.hu'),
        'browser': os.getenv('BROWSER', 'chrome'),
        'browser_version': os.getenv('BROWSER_VERSION', 'not-found'),
        'build_number': os.getenv('BUILD_NUMBER', 'not-found'),
        'headless': os.getenv('HEADLESS', 'true'),
        'browser_width': int(os.getenv('BROWSER_WIDTH', '1920')),
        'browser_height': int(os.getenv('BROWSER_HEIGHT', '1080')),
        'implicit_wait': int(os.getenv('IMPLICIT_WAIT', '10')),
        'page_load_timeout': int(os.getenv('PAGE_LOAD_TIMEOUT', '30')),
        'report_dir': os.getenv('REPORT_DIR', 'tests/reports'),
        'screenshot_dir': os.getenv('SCREENSHOT_DIR', 'tests/screenshots'),
    }

def pytest_configure(config):
    """Create report html with timestamp"""
    # Create reports directory if it doesn't exist
    report_dir = os.getenv('REPORT_DIR', 'tests/reports')
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Set report path
    report_name = f"report_{timestamp}.html"
    report_path = os.path.join(report_dir, report_name)
    config.option.htmlpath = report_path


def create_driver(test_config):
    chrome_options = Options()
    chrome_options.add_argument(f"--headless={test_config['headless']}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--window-size={test_config['browser_width']},{test_config['browser_height']}")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument('--ignore-certificate-errors')  # allow no SSL
    # chrome_options.accept_insecure_certs = True               # allow no SSL
    
    try:
        driver_path = ChromeDriverManager().install()
        if 'THIRD_PARTY_NOTICES' in driver_path:
            base_dir = os.path.dirname(driver_path)
            chromedriver_path = os.path.join(base_dir, 'chromedriver')
            if os.path.exists(chromedriver_path):
                driver_path = chromedriver_path
        os.chmod(driver_path, 0o755)
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

    except Exception as e:
        print(f"⚠️  webdriver-manager failed: {e}")
        print("Falling back to system ChromeDriver...")
        driver = webdriver.Chrome(options=chrome_options)
    
    return driver


@pytest.fixture(scope="function")
def function_driver(test_config):
    driver = create_driver(test_config)
    driver.implicitly_wait(int(test_config['implicit_wait']))
    allure.dynamic.label("Browser", test_config['browser'])
    allure.dynamic.label("Browser.Version", test_config['browser_version'])
    yield driver
    
    driver.quit()

@pytest.fixture(scope="class")
def class_driver(test_config):
    driver = create_driver(test_config)
    driver.implicitly_wait(int(test_config['implicit_wait']))
    allure.dynamic.label("Browser", test_config['browser'])
    allure.dynamic.label("Browser.Version", test_config['browser_version'])
    yield driver
    driver.quit()


@pytest.fixture(scope="class")
def session():
    s = requests.Session()
    # print("Session created, id: ", id(s))
    s.verify = False
    yield s
    s.close()


@pytest.fixture(scope="class")
def valid_token(session, test_config):
    login_url = next((u["url"] for u in valid_urls_data if u["page"] == "login"), None)
    assert login_url, "login_url not found"
    full_url = test_config['test_url'] + login_url
    response = session.post(full_url, data=valid_login_data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    return response.json()['token']

@pytest.fixture(scope="class")
def auth_headers(valid_token):
    return {'Authorization': f'Token {valid_token}'}

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result for screenshot on failure"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

def pytest_html_results_table_header(cells):
    cells.insert(2, '<th class="col-marker">Marks</th>')

def pytest_html_results_table_row(report, cells):
    markers = getattr(report, "markers", "-")
    cells.insert(2, f'<td class="col-marker">{markers}</td>')

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        # Собираем все маркеры теста
        markers = [mark.name for mark in item.iter_markers()]
        report.markers = ", ".join(markers) if markers else "-"

@pytest.fixture(scope="session")
def make_full_url(test_config):
    def _make(urls_data, page, params=None):
        base = next((u["url"] for u in urls_data if u["page"] == page), None)
        assert base is not None, f"base url not found for page {page}"
        url = test_config["test_url"] + base
        if params:
            url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
        return url
    return _make

orders_map = {
    'first': 0,
    'second': 1,
    'third': 2,
    'fourth': 3,
    'fifth': 4,
    'sixth': 5,
    'seventh': 6,
    'eighth': 7,
    'last': -1,
    'second_to_last': -2,
    'third_to_last': -3,
    'fourth_to_last': -4,
    'fifth_to_last': -5,
    'sixth_to_last': -6,
    'seventh_to_last': -7,
    'eighth_to_last': -8,
}


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items):
    """Reorder test by run marker. Ex: @pytest.mark.run(order=0)"""
    grouped_items = {}
    for item in items:
        for mark_name, order in orders_map.items():
            mark = item.get_closest_marker(mark_name)
            if mark:
                item.add_marker(pytest.mark.run(order=order))
                break
        mark = item.get_closest_marker('run')
        if mark:
            order = mark.kwargs.get('order')
        else:
            order = None
        grouped_items.setdefault(order, []).append(item)
    sorted_items = []
    unordered_items = [grouped_items.pop(None, [])]

    start_list = sorted((i for i in grouped_items.items() if i[0] >= 0),
                        key=operator.itemgetter(0))
    end_list = sorted((i for i in grouped_items.items() if i[0] < 0),
                      key=operator.itemgetter(0))

    sorted_items.extend([i[1] for i in start_list])
    sorted_items.extend(unordered_items)
    sorted_items.extend([i[1] for i in end_list])
    items[:] = [item for sublist in sorted_items for item in sublist]


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session):
    """Create environment.properties for Allure after tests finish"""
    allure_dir = os.getenv('ALLURE_RESULTS_DIR', 'allure-results')
    os.makedirs(allure_dir, exist_ok=True)
    
    env_file = os.path.join(allure_dir, 'environment.properties')
    with open(env_file, 'w') as f:
        f.write(f"Browser={os.getenv('BROWSER', 'chrome')}\n")
        f.write(f"Browser.Version={os.getenv('BROWSER_VERSION', 'unknown')}\n")
        f.write(f"Build.Number={os.getenv('BUILD_NUMBER', 'local')}\n")
        f.write(f"Headless={os.getenv('HEADLESS', 'true')}\n")

# #######################
# PageObjects
# #######################

@pytest.fixture(scope="function")
def contact_page(class_driver, make_full_url):
    page = PageContact(class_driver)
    full_url = make_full_url(urls_data=valid_urls_data, page="contact")
    page.load_page(full_url)
    return page


# #######################
# Security
# #######################

SENSITIVE_PATTERNS = [os.getenv(val) for val in ['JWT_USERNAME', 'JWT_PASSWORD'] if os.getenv(val)]

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Mask sensitive data"""
    outcome = yield
    report = outcome.get_result()
    
    if report.failed and hasattr(call, 'excinfo'):
        exc = call.excinfo.value
        
        if hasattr(exc, '__cause__') and exc.__cause__:
            cause_msg = str(exc.__cause__)
            for pattern in SENSITIVE_PATTERNS:
                if pattern:
                    cause_msg = cause_msg.replace(pattern, '******')
            exc.__cause__ = type(exc.__cause__)(cause_msg)
        
        exc_msg = str(exc)
        for pattern in SENSITIVE_PATTERNS:
            if pattern:
                exc_msg = exc_msg.replace(pattern, '******')
        
        report.longrepr = exc_msg