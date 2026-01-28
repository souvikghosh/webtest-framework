# WebTest Framework

A web application testing framework built with Playwright and pytest.

## Features

- **Page Object Model**: Organized, maintainable test code
- **API Testing**: Built-in HTTP client with assertions
- **Configuration**: YAML and environment variable support
- **Rich Assertions**: Playwright's built-in expect + custom assertions
- **HTML Reports**: Automatic test report generation
- **Screenshots**: Automatic capture on test failure

## Installation

1. Clone the repository:
```bash
git clone https://github.com/souvikghosh/webtest-framework.git
cd webtest-framework
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

4. Install Playwright browsers:
```bash
playwright install chromium
```

## Usage

### Creating Page Objects

```python
from webtest_framework import BasePage

class LoginPage(BasePage):
    # Selectors
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error"

    def login(self, username: str, password: str):
        return (
            self.fill(self.USERNAME_INPUT, username)
            .fill(self.PASSWORD_INPUT, password)
            .click(self.LOGIN_BUTTON)
        )

    def expect_error(self, message: str):
        self.expect_visible(self.ERROR_MESSAGE)
        self.expect_text(self.ERROR_MESSAGE, message)
        return self
```

### Writing Tests

```python
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage

@pytest.mark.smoke
def test_successful_login(page: Page):
    login_page = LoginPage(page, "https://example.com")
    login_page.navigate("/login")
    login_page.login("user@example.com", "password123")
    login_page.wait_for_url("**/dashboard")

@pytest.mark.regression
def test_invalid_credentials(page: Page):
    login_page = LoginPage(page, "https://example.com")
    login_page.navigate("/login")
    login_page.login("invalid", "wrong")
    login_page.expect_error("Invalid credentials")
```

### API Testing

```python
from webtest_framework.api import APIClient, assert_status, assert_json_contains

def test_create_user():
    client = APIClient("https://api.example.com")
    client.set_auth_token("your-token")

    response = client.post("/users", json={
        "name": "John Doe",
        "email": "john@example.com"
    })

    assert_status(response, 201)
    assert_json_contains(response, "id")
    assert_json_contains(response, "name", "John Doe")
```

### Configuration

Create `config.yaml`:
```yaml
base_url: https://staging.example.com
browser:
  headless: true
  slow_mo: 0
  viewport_width: 1920
  viewport_height: 1080
  timeout: 30000
screenshot_on_failure: true
screenshot_dir: screenshots
```

Or use environment variables:
```bash
export TEST_BASE_URL=https://staging.example.com
export TEST_HEADLESS=false
export TEST_TIMEOUT=60000
```

## Running Tests

```bash
# Run all tests
pytest

# Run smoke tests only
pytest -m smoke

# Run with visible browser
pytest --headed

# Run specific browser
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit

# Generate HTML report
pytest --html=report.html
```

## Project Structure

```
webtest-framework/
├── src/
│   └── webtest_framework/
│       ├── __init__.py
│       ├── page.py         # BasePage class
│       ├── config.py       # Configuration
│       ├── assertions.py   # Custom assertions
│       ├── api.py          # API client
│       └── fixtures.py     # pytest fixtures
├── tests/
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_api.py
│   └── test_page.py
├── examples/
│   └── (example tests)
├── pyproject.toml
├── README.md
└── LICENSE
```

## BasePage Methods

### Navigation
- `navigate(path)` - Go to URL
- `reload()` - Refresh page
- `wait_for_load()` - Wait for network idle

### Interactions
- `click(selector)` - Click element
- `fill(selector, value)` - Fill input
- `type(selector, value)` - Type character by character
- `select(selector, value)` - Select dropdown option
- `check(selector)` / `uncheck(selector)` - Checkbox control

### Locators
- `locator(selector)` - Get Playwright locator
- `get_by_text(text)` - Find by text content
- `get_by_role(role)` - Find by ARIA role
- `get_by_label(label)` - Find by label
- `get_by_placeholder(placeholder)` - Find by placeholder
- `get_by_test_id(id)` - Find by data-testid

### Assertions
- `expect_visible(selector)` - Assert visible
- `expect_hidden(selector)` - Assert hidden
- `expect_text(selector, text)` - Assert text content
- `expect_value(selector, value)` - Assert input value

### Information
- `url` - Current URL
- `title` - Page title
- `is_visible(selector)` - Check visibility
- `is_enabled(selector)` - Check if enabled
- `text_content(selector)` - Get text
- `get_attribute(selector, attr)` - Get attribute
- `count(selector)` - Count matching elements

## Technologies

- **Playwright** - Browser automation
- **pytest** - Test framework
- **pytest-playwright** - Playwright integration
- **pytest-html** - HTML reporting
- **Pydantic** - Configuration validation
- **Requests** - API testing

## License

MIT
