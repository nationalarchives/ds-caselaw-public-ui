import warnings

import pytest
from axe_playwright_python.sync_playwright import Axe

axe = Axe()


class AccessibilityWarning(UserWarning):
    pass


def assert_accessible(page):
    results = axe.run(page)
    violations = results.response.get("violations", [])

    if not violations:
        return

    critical_or_serious_violations = []
    other_violations = []

    for violation in violations:
        if violation["impact"] in ["critical", "serious"]:
            critical_or_serious_violations.append(violation)
        else:
            other_violations.append(violation)

    if critical_or_serious_violations:
        critical_report = "\n".join(format_violation(v) for v in critical_or_serious_violations)
        pytest.fail(f"\nCritical/Serious Accessibility Violations Detected:\n{critical_report}")

    if other_violations:
        other_report = "\n".join(format_violation(v) for v in other_violations)
        warnings.warn(f"\nAccessibility Violations (Minor/Moderate):\n{other_report}", AccessibilityWarning)


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
