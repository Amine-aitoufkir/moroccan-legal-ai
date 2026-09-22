"""Tests du premier point de controle de l'API."""

import unittest

from fastapi.testclient import TestClient

from main import app


class HealthTest(unittest.TestCase):
    def test_health_returns_ok(self) -> None:
        with TestClient(app) as client:
            response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

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
