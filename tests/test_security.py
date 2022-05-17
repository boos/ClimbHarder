from routers import security


async def test_authenticate_wrong_username():
    # username: dc724af18fbdd4e59189f5fe768a5f8311527050
    # password: 763ab79c83dc114cac76e8fafa9ca0fc0f0fc6cf
    response = await security.verify_username('dc724af18fbdd4e59189f5fe768a5f8311527050+wrong-username')
    assert response is False


async def test_authenticate_right_username():
    response = await security.verify_username('dc724af18fbdd4e59189f5fe768a5f8311527050')
    assert response['username'] == 'dc724af18fbdd4e59189f5fe768a5f8311527050'


async def test_authenticate_wrong_username_wrong_password():
    response = await security.authenticate_user('dc724af18fbdd4e59189f5fe768a5f8311527050+wrong-username',
                                                'wrong-password')
    assert response is None


async def test_authenticate_right_username_wrong_password():
    response = await security.authenticate_user('dc724af18fbdd4e59189f5fe768a5f8311527050',
                                                'wrong-password')
    assert response is None


async def test_authenticate_right_username_right_password():
    response = await security.authenticate_user('dc724af18fbdd4e59189f5fe768a5f8311527050',
                                                '763ab79c83dc114cac76e8fafa9ca0fc0f0fc6cf')
    assert response['username'] == 'dc724af18fbdd4e59189f5fe768a5f8311527050'
    assert response['password'] == '$2b$12$o0e/E4yLuc98.8Ym5FE.SurnuVoaFKbl.4v0oGKmJN7jAt3Wf598K'
