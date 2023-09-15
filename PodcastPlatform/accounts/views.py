

def login(request):
    """
    Authenticates the user using username & password
    and creates the access & refresh token for the user
    and puts user in the whitelist in our cache based database

    args:
        request => request that the user sent

    return:
        HTTPResponse => JSON(API)
    """


def check_auth(request):
    """
    Authenticates the user using access token
    and checks if the user is in the whitelist

    args:
        request => request that the user sent

    return:
        HTTPResponse => JSON(API)
    """


def refresh_token(request):
    """
    generates new access token for the user and set it in the whitelist and header(or body)
    if the refresh token is not expired and the user is in whitelist

    args:
        request => request that the user sent

    return:
        HTTPResponse => JSON(API)
    """


def logout(request):
    """
    Removes the user from whitelist

    args:
        request => request that the user sent

    return:
        HTTPResponse => JSON(API)
    """
