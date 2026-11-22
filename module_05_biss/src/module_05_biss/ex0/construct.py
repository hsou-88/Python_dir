import os
import site
import sys


def main() -> None:
    inside = sys.prefix != sys.base_prefix or hasattr(sys, "real_prefix")
    if inside:
        print("LABORATORY STATUS: The laboratory is sealed")
    else:
        print("LABORATORY STATUS: You are working in the open")
    print(f"Current Python: {sys.executable}")

    if inside:
        print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
        print(f"Environment Path: {sys.prefix}")
        print("SUCCESS: You are working in an isolated environment!")
        print("Safe to install reagents without affecting")
        print("the global system.")
    else:
        print("Virtual Environment: None detected")
        print("WARNING: You are in the global environment!")
        print("Every reagent you install here leaks into the whole system.")
        print("To seal the laboratory, run:")
        print("python3 -m venv lab_env")
        print("source lab_env/bin/activate # On Unix")
        print(r"lab_env\Scripts\activate # On Windows")
        print("Then run this program again.")

    print("Reagent installation paths (current environment):")
    for path in site.getsitepackages():
        print(path)
    print("Global package locations (base Python):")
    for path in site.getsitepackages([sys.base_prefix]):
        print(path)
    print(f"User package location: {site.getusersitepackages()}")


if __name__ == "__main__":
    main()
