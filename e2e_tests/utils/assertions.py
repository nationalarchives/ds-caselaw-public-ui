import warnings

import pytest
from axe_playwright_python.sync_playwright import Axe

axe = Axe()


class AccessibilityWarning(UserWarning):
    pass


def generate_accessibility_report(violations):
    return "\n".join(format_violation(v) for v in violations)


def assert_critical_violations(violations, page_url):
    critical_or_serious_violations = []

    for violation in violations:
        if violation["impact"] in ["critical", "serious"]:
            critical_or_serious_violations.append(violation)

    if critical_or_serious_violations:
        report = generate_accessibility_report(critical_or_serious_violations)
        pytest.fail(f"\nCritical/Serious Accessibility Violations Detected ({page_url}):\n{report}")


def check_other_violations(violations, page_url):
    other_violations = []

    for violation in violations:
        if violation["impact"] not in ["critical", "serious"]:
            other_violations.append(violation)

    if other_violations:
        report = generate_accessibility_report(other_violations)
        warnings.warn(f"\nAccessibility Violations (Minor/Moderate) ({page_url}):\n{report}", AccessibilityWarning)


def assert_is_accessible(page):
    results = axe.run(page)
    violations = results.response.get("violations", [])

    if not violations:
        return

    assert_critical_violations(violations, page.url)
    check_other_violations(violations, page.url)


def format_violation(violation):
    violation_str = f"Violation: {violation['description']}\n"
    violation_str += f"Impact: {violation['impact'].capitalize()}\n"
    violation_str += f"Help: {violation['help']}\n"
    violation_str += f"URL: {violation['helpUrl']}\n"

    for node in violation["nodes"]:
        violation_str += f"HTML Element: {node['html']}\n"
        violation_str += f"Target: {', '.join(node['target'])}\n"
        violation_str += "Issues:\n"
        for issue in node["any"]:
            violation_str += f"  - {issue['message']}\n"
        violation_str += "\n"

    return violation_str
