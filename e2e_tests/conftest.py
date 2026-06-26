import pytest

MUST_PASS_FAILED = False

# arguably we don't need this as 1st is alphabetically before advanced...
# https://stackoverflow.com/questions/17571438/how-to-control-test-case-execution-order-in-pytest


def test_order(item: pytest.Item) -> int:
    """Smaller numbers run earlier"""
    if "test_1st" in item.path.name:
        return -1
    return 0


def pytest_collection_modifyitems(items):
    items.sort(key=test_order)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed and item.get_closest_marker("must_pass"):
        pytest.exit("A critical test failed.")
