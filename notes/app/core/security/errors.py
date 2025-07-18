from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
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


class NoteAlreadyExistsError(HTTPException):
    def __init__(self, name: str):
        detail = f"Note with name '{name}' already exists" 
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, 
            detail=detail
        )


class NoteNotFound(HTTPException):
    def __init__(self, note_id: str):
        detail = f"Note with ID '{note_id}' not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class UnauthorizedNoteAccessError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this note"
        )


class InvalidAuthorizationTokenError(CredentialsException):
    def __init__(self):
        super().__init__(
            detail="Invalid authorization token"
        )


class IncorrectUserDataException(CredentialsException):
    def __init__(self):
        super().__init__(
            detail="Incorrect user data"
        )






