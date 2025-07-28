import strawberry

@strawberry.input
class UserInput:
    username: str
    email: str
    password: str
    role: str = "Viewer"

@strawberry.input
class LoginInput:
    email: str
    password: str
