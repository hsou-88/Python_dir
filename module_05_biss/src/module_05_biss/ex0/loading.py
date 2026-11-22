import importlib
import os
import sys


def main() -> None:
    print("REAGENT STATUS: Loading reagents...")
    print("Checking dependencies:")
    missing: list[str] = []
    reagents = [
        ("pandas", "Data manipulation ready"),
        ("numpy", "Numerical computation ready"),
    ]
    for name, description in reagents:
        try:
            module = importlib.import_module(name)
            version = str(getattr(module, "__version__", "unknown"))
            print(f"[OK] {name} ({version}) - {description}")
        except Exception as error:
            missing.append(name)
            print(f"[MISSING] {name}: {error}")

    print("pip vs Poetry:")
    print("requirements.txt declares what to install; "
          "pip resolves it at install time.")
    print("pyproject.toml declares the same constraints, "
          "and Poetry pins the resolved")
    print("versions in poetry.lock so every install is identical.")
    if missing:
        directory = os.path.dirname(os.path.abspath(__file__))
        requirements = os.path.join(directory, "requirements.txt")
        print("Install the missing reagents with pip:")
        print(f'"{sys.executable}" -m pip install -r "{requirements}"')
        print("Or install with Poetry:")
        print(f'poetry -C "{directory}" install')
        print(f'poetry -C "{directory}" run python loading.py')
    else:
        print("All reagents present and accounted for.")


if __name__ == "__main__":
    main()
