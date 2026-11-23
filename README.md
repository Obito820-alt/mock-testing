# Mock Testing

A small Python project based on the course material about software testing and `pytest`.

It demonstrates:

- **Unit tests** for individual calculation functions.
- **Integration tests** for `OrderService` working with `ProductRepository`.
- **Mocking** a Groq API client so tests do not need a real API key, internet access, or paid API calls.
- Shared pytest fixtures and the Arrange–Act–Assert (AAA) testing pattern.

## Project structure

```text
mock-testing/
├── app.py
├── groq_chat.py
├── requirements.txt
├── pytest.ini
├── README.md
└── tests/
    ├── conftest.py
    ├── test_unit.py
    ├── test_integration.py
    └── test_groq_chat.py
```

## Setup

Create and activate a virtual environment (recommended), then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run the tests

Run the complete test suite:

```bash
pytest
```

Run only unit tests:

```bash
pytest tests/test_unit.py
```

Run only integration tests:

```bash
pytest tests/test_integration.py
```

Run only mocking tests:

```bash
pytest tests/test_groq_chat.py
```

## Test coverage

Install dependencies from `requirements.txt`, then run:

```bash
pytest --cov=app --cov=groq_chat --cov-report=term-missing
```

Coverage measures which lines of the application code are exercised by tests. The report helps identify code that still needs tests.

## What the examples demonstrate

### 1. Unit tests

The unit tests check `calculate_discount`, `calculate_tax`, and `calculate_total` independently. They include normal inputs, boundary values, decimal values, empty input, and invalid values that should raise an exception.

### 2. Integration tests

The integration tests use a real in-memory `ProductRepository` and an `OrderService`. They check successful orders, stock updates, unknown products, insufficient stock, and successive orders.

The `order_service` fixture in `tests/conftest.py` creates fresh test data for each test, avoiding shared state between tests.

### 3. Mocking

The mocking tests pass a fake client to `ask_groq`. The fake client returns a predictable response, so the tests do not contact the real Groq API.

They verify that:

- The function returns the mocked answer.
- The API method is called exactly once with the expected model, messages, and token limit.
- An API exception is propagated.
- An empty question is rejected before the API method is called.

The tests use the `mocker` fixture provided by the `pytest-mock` package.

## Other testing concepts from the course

- **End-to-end testing:** tools such as Playwright or Selenium can simulate a real user interacting with a complete web application. This small command-line example does not implement an E2E browser flow.
- **Load testing:** measures response time and throughput under a specified workload. Locust is one possible tool.
- **Version testing:** checks compatibility across Python versions. tox can automate running tests in multiple environments.
- **Markers:** pytest markers categorize tests so selected groups can be run separately. This project registers `slow` and `faster` markers in `pytest.ini`.
- **AAA pattern:** Arrange (prepare data), Act (call the code), Assert (check the result). The tests are organized to keep these steps easy to identify.

## Important

The Groq API key is not needed for the mocking tests because they inject a fake client. If you call `ask_groq` without passing a client, the Groq SDK will create a real client and will require a valid `GROQ_API_KEY` environment variable. Never commit API keys to a public repository.
