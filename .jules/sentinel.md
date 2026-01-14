## 2025-05-15 - Python Path Injection via os.getcwd()
**Vulnerability:** `sys.path.append(os.getcwd())` in `main.py` and `server.py` allowed arbitrary code execution by running the script from a directory containing a malicious `src` package or standard library shadow.
**Learning:** Utility scripts that modify `sys.path` to allow relative imports must be careful not to blindly trust `os.getcwd()`, as it's user-controlled.
**Prevention:** Use `os.path.dirname(__file__)` to resolve the project root relative to the script location, ensuring only the intended code is loaded.
