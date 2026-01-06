import os
import warnings

import numpy as np
import pytest
from axe_playwright_python.sync_playwright import Axe
from PIL import Image
from skimage.metrics import structural_similarity as ssim

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


def compare_snapshot(actual_path, expected_path):
    actual_image = Image.open(actual_path).convert("L")
    expected_image = Image.open(expected_path).convert("L")

    min_width = min(actual_image.width, expected_image.width)
    min_height = min(actual_image.height, expected_image.height)

    actual_cropped = actual_image.crop((0, 0, min_width, min_height))
    expected_cropped = expected_image.crop((0, 0, min_width, min_height))

    actual_np = np.array(actual_cropped, dtype=np.uint8)
    expected_np = np.array(expected_cropped, dtype=np.uint8)

    if actual_np.shape != expected_np.shape:
        warnings.warn(f"Actual shape: {actual_np.shape}")
        warnings.warn(f"Expected shape: {expected_np.shape}")
        raise ValueError("Image sizes do not match")

    score, _diff = ssim(actual_np, expected_np, full=True)
    return score >= 0.9, score


def assert_matches_snapshot(page, page_name):
    viewports = [
        ("desktop", {"width": 1280, "height": 720}),
        ("mobile", {"width": 375, "height": 667}),
    ]

    for label, viewport in viewports:
        actual_path = f"snapshots/{page_name}_{label}_actual.png"
        expected_path = f"snapshots/{page_name}_{label}_expected.png"

        page.set_viewport_size(viewport)
        page.screenshot(path=actual_path, full_page=True)

        if not os.path.exists(expected_path):
            os.replace(actual_path, expected_path)
            pytest.fail(
                f"Expected {label} snapshot for {page_name} not found - this whas been generated. Re-run to try again"
            )

        page.screenshot(path=actual_path, full_page=True)
        result, score = compare_snapshot(actual_path, expected_path)

        if not result:
            pytest.fail(
                f"\n{page_name} on {label} has changed ({score}). Please check screenshots/{page_name}_{label}_actual.png and update screenshots/{page_name}_{label}_expected.png if happy."
            )
