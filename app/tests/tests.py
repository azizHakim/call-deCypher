# import pytest
# from app import app # Flask instance of the API


# @pytest.mark.get_request
# def test_index_route():
#     response = app.test_client().get('/health')

#     assert response.status_code == 200
#     assert response.data.decode('utf-8') == 'Testing, Flask!'


from tests.conftest import client


def test_should_status_code_ok(client):
	response = client.get('/health')
	assert response.status_code == 200