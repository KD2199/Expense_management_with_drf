from django.contrib.auth import get_user_model
from django.test import Client
import pytest

User = get_user_model()
client = Client()


class TestClass:

    @pytest.mark.parametrize("credential", [{'username': 'karan', 'password': 'karan@123'}])
    def test_correct(self, credential):
        response = self.client.post('/login/', credential)
        print(response)
        assert(response.status_code == 302)
