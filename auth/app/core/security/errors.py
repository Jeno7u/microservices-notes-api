from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self, detail="Could not validate credentials"):
        super(CredentialsException, self).__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class InternalServerError(HTTPException):
    def __init__(self, detail="Internal server error"):
        super(InternalServerError, self).__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class UserNotFoundException(HTTPException):
    def __init__(self, detail="User not found"):
        super(UserNotFoundException, self).__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class InvalidAuthorizationTokenError(CredentialsException):
    def __init__(self):
        super(InvalidAuthorizationTokenError, self).__init__(
            detail="Invalid authorization token"
        )


class IncorrectUserDataException(CredentialsException):
    def __init__(self):
        super(IncorrectUserDataException, self).__init__(
            detail="Incorrect email or password"
        )


class AlreadyExistError(CredentialsException):
    def __init__(self):
        super(AlreadyExistError, self).__init__(
            detail="Already exist"
        )
