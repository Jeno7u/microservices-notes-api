from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


class DataBaseConnectionError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error"
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
            status_code=status.HTTP_404_NOTE_FOUND,
            detail=detail
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