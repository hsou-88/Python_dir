import os


def is_url(value: str, web_only: bool = False) -> bool:
    if not value or any(char.isspace() or ord(char) < 32 for char in value):
        return False
    scheme, separator, remainder = value.partition("://")
    if not separator or not remainder or not scheme:
        return False
    if not scheme[0].isascii() or not scheme[0].isalpha():
        return False
    if not all(
        char.isascii() and (char.isalnum() or char in "+-.")
        for char in scheme
    ):
        return False
    if web_only and scheme.lower() not in ("http", "https"):
        return False
    if web_only or scheme.lower() in ("http", "https"):
        authority = remainder.split("/")[0].split("?")[0].split("#")[0]
        if not authority or authority.startswith(":"):
            return False
    return True


def main() -> None:
    print("ORACLE STATUS: Consulting the configuration...")
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("Missing python-dotenv. Install with:")
        print("python3 -m pip install -r ex1/requirements.txt")
        return

    directory = os.path.dirname(os.path.abspath(__file__))
    try:
        load_dotenv(os.path.join(directory, ".env"), override=False)
    except (OSError, UnicodeError):
        print("WARNING: Cannot read .env; using environment variables.")

    mode = os.getenv("MATRIX_MODE", "development").strip().lower()
    if mode not in ("development", "production"):
        print("WARNING: Invalid MATRIX_MODE; using development.")
        mode = "development"
    default_level = "DEBUG" if mode == "development" else "INFO"
    log_level = os.getenv("LOG_LEVEL", default_level).strip().upper()
    if log_level not in (
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "NOTSET",
    ):
        print("WARNING: Invalid LOG_LEVEL; using the mode default.")
        log_level = default_level
    database = os.getenv("DATABASE_URL", "").strip()
    api_key = os.getenv("API_KEY", "")
    endpoint = os.getenv("ZION_ENDPOINT", "").strip()
    database_ok = is_url(database)
    endpoint_ok = is_url(endpoint, web_only=True)
    if database and not database_ok:
        print("WARNING: DATABASE_URL must have a scheme://value structure.")
    if endpoint and not endpoint_ok:
        print("WARNING: ZION_ENDPOINT must be an HTTP(S) URL with a host.")

    print("Configuration loaded:")
    print(f"Mode: {mode}")
    if mode == "development":
        print("Development diagnostics: enabled")
    else:
        print("Production diagnostics: restricted")
    print("Database: " + ("Configured" if database_ok else "Not configured"))
    print("API Access: " + ("Key configured (hidden)" if api_key.strip()
                            else "Not configured"))
    print(f"Log Level: {log_level}")
    print("Remote Network: " + ("Configured" if endpoint_ok
                                else "Not configured"))

    for key in ("MATRIX_MODE", "DATABASE_URL", "API_KEY",
                "LOG_LEVEL", "ZION_ENDPOINT"):
        if not os.getenv(key, "").strip():
            print(f"WARNING: {key} is missing or empty.")

    print("Configuration security check:")
    print("[OK] Sensitive values are not displayed")
    try:
        with open(os.path.join(directory, ".gitignore"),
                  encoding="utf-8") as stream:
            patterns = [line.strip() for line in stream]
        if ".env" in patterns:
            print("[OK] .env is listed in .gitignore")
        else:
            print("WARNING: Add .env to ex1/.gitignore")
    except (OSError, UnicodeError):
        print("WARNING: Cannot check ex1/.gitignore")
    print("[OK] Environment variables take priority over .env")
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
