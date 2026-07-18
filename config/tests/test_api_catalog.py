from django.test import TestCase


class TestApiCatalog(TestCase):
    def test_returns_linkset_json(self):
        response = self.client.get("/.well-known/api-catalog")

        assert response.status_code == 200
        assert response["Content-Type"].startswith("application/linkset+json")

    def test_includes_link_relations(self):
        response = self.client.get("/.well-known/api-catalog")

        body = response.json()
        assert "linkset" in body
        assert isinstance(body["linkset"], list)
        assert len(body["linkset"]) == 1

        entry = body["linkset"][0]

        assert entry["anchor"] == "http://testserver/atom.xml"
        assert entry["self"] == [{"href": "http://testserver/atom.xml", "title": "Atom feed"}]
        assert entry["service-desc"] == [
            {
                "href": "https://raw.githubusercontent.com/nationalarchives/ds-find-caselaw-docs/refs/heads/main/doc/openapi/public_api.yml"
            }
        ]
        assert entry["service-doc"] == [{"href": "https://nationalarchives.github.io/ds-find-caselaw-docs/public"}]
        assert entry["license"] == [{"href": "http://testserver/open-justice-licence/version/2"}]
        assert "status" not in entry
