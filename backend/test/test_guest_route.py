from unittest.mock import MagicMock
import bson
from fastapi.testclient import TestClient
import pytest
from app.core.app import app


class TestGuestRoute:
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        # This runs before each test method in this class
        mock_producer = MagicMock()

        # Patch the get_producer function to return the mock KafkaProducer
        mocker.patch(
            "app.core.kafka.KafkaProducerWrapper.get_producer",
            return_value=mock_producer,
        )

        self.client = TestClient(app)

        # You can add other setup steps here if necessary

    def test_get_all_guests_returns_list(self):
        with self.client as client:
            res = client.get("/api/guests")
            guests = res.json()
            assert res.status_code == 200
            assert type(guests) is list

    def test_get_guest_by_invalid_id_returns_400(self):
        with self.client as client:
            res = client.get("/api/guests/not_a_real_id")
            error = res.json()
            assert res.status_code == 400
            assert type(error) is dict
            assert "detail" in error

    def test_create_guest(self):
        with self.client as client:
            guest_to_insert = {
                "name": "Liel",
                "age": 20,
                "isVip": False,
            }

            res = client.post(
                "/api/guests",
                json=guest_to_insert,
            )

            guest = res.json()

            # Needs to be 201
            assert res.status_code == 200

            assert "_id" in guest
            assert guest["name"] == guest_to_insert["name"]
            assert guest["age"] == guest_to_insert["age"]
            assert guest["isVip"] == guest_to_insert["isVip"]

    def test_create_guest_with_missing_fields_returns_400(self):
        with self.client as client:
            guest_to_insert = {
                "name": "Liel",
            }

            res = client.post(
                "/api/guests",
                json=guest_to_insert,
            )

            error = res.json()

            # Needs to be 400
            assert res.status_code == 400

            assert "detail" in error

    def test_create_guest_with_underage_returns_400(self):
        with self.client as client:
            guest_to_insert = {
                "name": "Liel",
                "age": 12,
                "isVip": False,
            }

            res = client.post(
                "/api/guests",
                json=guest_to_insert,
            )

            error = res.json()

            # Needs to be 400
            assert res.status_code == 400

            assert "detail" in error

    def test_create_vip_guest(self):
        with self.client as client:
            guest_to_insert = {
                "name": "Liel",
                "age": 20,
                "isVip": True,
            }

            res = client.post(
                "/api/guests",
                json=guest_to_insert,
            )

            guest = res.json()

            # Needs to be 201
            assert res.status_code == 200

            assert "_id" in guest
            assert guest["name"] == guest_to_insert["name"]
            assert guest["age"] == guest_to_insert["age"]
            assert guest["isVip"] == guest_to_insert["isVip"]

    def test_create_non_vip_guest_with_custom_requests_returns_400(self):
        with self.client as client:
            guest_to_insert = {
                "name": "Liel",
                "age": 20,
                "isVip": False,
                "customRequests": [
                    {
                        "description": "I want a pony",
                    }
                ],
            }

            res = client.post(
                "/api/guests",
                json=guest_to_insert,
            )

            error = res.json()

            # Needs to be 400
            assert res.status_code == 400

            assert "detail" in error

    def test_create_vip_guest_with_custom_requests(self):
        with self.client as client:
            guest_to_insert = {
                "name": "Liel",
                "age": 20,
                "isVip": True,
                "customRequests": [
                    {
                        "description": "I want a pony",
                    }
                ],
            }

            res = client.post(
                "/api/guests",
                json=guest_to_insert,
            )

            guest = res.json()

            # Needs to be 201
            assert res.status_code == 200

            assert "_id" in guest
            assert guest["name"] == guest_to_insert["name"]
            assert guest["age"] == guest_to_insert["age"]
            assert guest["isVip"] == guest_to_insert["isVip"]
            # THe server adds properties to the customRequests array
            assert type(guest["customRequests"]) is list

    def test_get_guest_by_nonexistent_id_returns_404(self):
        with self.client as client:
            not_found_id = bson.ObjectId()
            res = client.get(f"/api/guests/{not_found_id}")
            error = res.json()
            assert res.status_code == 404
            assert type(error) is dict
            assert "detail" in error
