import pytest
import redis

@pytest.fixture(autouse=True)
def mock_redis(mocker):
    """
    Подменяем Redis на подставной (fakeredis) для всех тестов -
    чтобы тесты не зависели от реального сервера Redis.

    Fakeredis создаёт имитацию прямо в памяти, поэтому тесты 
    будут работать на любом компьютере пользователя даже без установленного Redis.  
    """
    fake_redis = redis.Redis(decode_responses=True)
    mocker.patch("app.infra.redis.get_redis", return_value=fake_redis)
    return fake_redis