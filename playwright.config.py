def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default="http://127.0.0.1:8080")
