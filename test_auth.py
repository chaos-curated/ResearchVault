
from auth import register_user, login_user

success, message = register_user(
    "Test User",
    "test@example.com",
    "Research123!"
)

print("Registration:", message)

user, message = login_user(
    "test@example.com",
    "Research123!"
)

print("Login:", message)

if user:
    print("Welcome,", user["full_name"])
