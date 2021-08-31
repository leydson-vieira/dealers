from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestApiV1Cashback:
    @pytest.fixture
    def cashback_response(self):
        return {
            'statusCode': 200,
            'body': {
                'credit': 1700
            }
        }

    def test_should_get_accumulated_cashback(self, logged_client, cashback_response):
        mocked_response = mock.Mock()
        mocked_response.status_code = 200
        mocked_response.json = mock.Mock(return_value=cashback_response)

        with mock.patch('cashback.services.requests.get') as mock_get:
            mock_get.return_value = mocked_response
            response = logged_client.get(reverse('accumulated-cashback'))

        mock_get.assert_called()
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['credit'] == 1700

    def test_should_not_get_accumulated_cashback(self, logged_client, cashback_response):
        mocked_response = mock.Mock()
        mocked_response.status_code = 400
        mocked_response.json = mock.Mock(return_value=cashback_response)

        with mock.patch('cashback.services.requests.get') as mock_get:
            mock_get.return_value = mocked_response
            response = logged_client.get(reverse('accumulated-cashback'))

        mock_get.assert_called()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
