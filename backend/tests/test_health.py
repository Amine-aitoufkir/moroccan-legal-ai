"""Tests du premier point de controle de l'API."""

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


class HealthTest(unittest.TestCase):
    def test_health_returns_ok(self) -> None:
        with TestClient(app) as client:
            response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    @patch("main.check_supabase_connection")
    def test_supabase_health_returns_ok(self, check_connection: object) -> None:
        with TestClient(app) as client:
            response = client.get("/health/supabase")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertTrue(check_connection.called)  # type: ignore[attr-defined]

    @patch("main.check_supabase_connection", side_effect=Exception("network error"))
    def test_supabase_health_hides_connection_details(
        self, check_connection: object
    ) -> None:
        with TestClient(app) as client:
            response = client.get("/health/supabase")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(), {"detail": "La connexion Supabase est indisponible."},
        )
        self.assertTrue(check_connection.called)  # type: ignore[attr-defined]

    def test_chat_accepts_a_valid_question(self) -> None:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/chat",
                json={"question": "Quels sont mes droits ?"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sources"], [])
        self.assertIn("RAG", response.json()["answer"])

    def test_chat_rejects_a_question_that_is_too_short(self) -> None:
        with TestClient(app) as client:
            response = client.post("/api/v1/chat", json={"question": "?"})

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
