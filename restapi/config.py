import os

UNDERPASS_DB=os.getenv("UNDERPASS_API_DB") or "postgresql://localhost/underpass"
ORIGINS = os.getenv("UNDERPASS_API_ORIGINS").split(",") if os.getenv("UNDERPASS_API_ORIGINS") else [
    "*"
]
