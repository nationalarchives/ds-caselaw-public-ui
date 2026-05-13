import pytest
from playwright.sync_api import Page

from .utils.assertions import assert_is_accessible, assert_matches_snapshot

courts_and_tribunals = [
    "ewhc/pat",
    "ewhc/tcc",
    "ewhc/mercantile",
    "ewhc/comm",
    "ewhc/ch",
    "ewhc/scco",
    "ewhc/fam",
    "ewhc/ipec",
    "ewhc/admin",
    "ewhc/admlty",
    "ewhc/kb",
    "ukpc",
    "ewca",
    "eat",
    "ewcc",
    "ewca/crim",
    "ewca/civ",
    "paac",
    "ukftt/grc",
    "ukftt/tc",
    "ukftt/estate",
    "ukftt/hesc",
    "ukftt/credit",
    "ftt/pc",
    "ftt/phl",
    "ftt/transport",
    "ftt/claims",
    "ukut/aac",
    "ukut/iac",
    "ukut/tcc",
    "ukut/lc",
    "ukist",
    "uksc",
    "ukiptrib",
    "ewfc",
    "ewcop",
    "ukftt",
    "ewcr",
    "siac",
    "poac",
    "ewhc",
]


@pytest.mark.parametrize("court", courts_and_tribunals)
def test_court_page(page: Page, court):
    page.goto(f"/courts-and-tribunals/{court}")

    assert_matches_snapshot(page, f"court_{court}_page")
    assert_is_accessible(page)
