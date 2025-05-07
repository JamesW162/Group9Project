# fix.py documentation
## Colored Output Functionality

The script includes a utility function to print colored status messages for better readability:

```python
def check_color_print(message, status, color):
    """Print colored status messages"""
    colors = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'end': '\033[0m'
    }
    
    # Check if we're in a terminal that supports colors
    if sys.stdout.isatty():
        print(f"{message}: {colors[color]}{status}{colors['end']}")
    else:
        print(f"{message}: {status}")
```

This function uses ANSI color codes to highlight success (green), warnings (yellow), and failures (red) in the terminal output, making issues immediately visible.

## Dependency Checking

The script verifies if all required Python packages are installed:

```python
def check_dependency(package_name):
    """Check if a Python package is installed"""
    # Special case for opencv-python which is imported as cv2
    if package_name == 'opencv-python':
        package_to_import = 'cv2'
    elif package_name == 'pickle':
        # Pickle is part of the standard library
        return True
    else:
        package_to_import = package_name
    
    try:
        spec = importlib.util.find_spec(package_to_import)
        if spec is not None:
            check_color_print(f"✓ {package_name} installed", "OK", "green")
            return True
        else:
            check_color_print(f"✗ {package_name} NOT installed", "MISSING", "red")
            return False
    except ImportError:
        check_color_print(f"✗ {package_name} NOT installed", "MISSING", "red")
        return False
```

This function handles special cases like OpenCV (which is imported as `cv2`) and standard library modules like `pickle`.

## File Existence Verification

The script checks if critical files required by the BSL interpreter exist:

```python
def check_file_exists(filepath, description=""):
    """Check if a file exists"""
    if os.path.exists(filepath):
        check_color_print(f"✓ Found {description} at {filepath}", "OK", "green")
        return True
    else:
        check_color_print(f"✗ {description} missing at {filepath}", "NOT FOUND", "red")
        return False
```

## System Information Collection

The script gathers basic system information to help with debugging:

```python
def get_python_version():
    """Get the installed Python version"""
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    check_color_print(f"Python version", version, "yellow")
    return version
```

## Stream ID Configuration

If the required `active_stream.txt` file is missing, the script offers to create one:

```python
def create_stream_id_file():
    """Create a temporary active_stream.txt file for testing"""
    stream_id = input("Enter a stream ID for testing (or press Enter to skip): ").strip()
    if stream_id:
        with open('active_stream.txt', 'w') as f:
            f.write(stream_id)
        check_color_print("Created active_stream.txt with ID", stream_id, "green")
        return True
    return False
```

This helps users quickly set up the stream ID needed by the BSL interpreter without having to manually create the file.

## Network Port Verification

The script checks if required network ports are available:

```python
def verify_port_available(port=3000):
    """Check if the specified port is available"""
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
        s.close()
        check_color_print(f"Port {port}", "AVAILABLE", "green")
        return True
    except socket.error:
        check_color_print(f"Port {port}", "IN USE", "red")
        return False
```

This is important because the BSL interpreter may run a web server on port 3000 for displaying translations.

## Automatic Dependency Installation

For convenience, the script offers to automatically install missing dependencies:

```python
def install_missing_dependencies(missing_deps):
    """Ask user if they want to install missing dependencies"""
    if not missing_deps:
        return
    
    print("\nMissing dependencies detected:")
    for dep in missing_deps:
        print(f"  - {dep}")
    
    choice = input("\nAttempt to install missing dependencies? (y/n): ").strip().lower()
    if choice == 'y':
        try:
            for dep in missing_deps:
                print(f"Installing {dep}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            check_color_print("Dependencies installation", "COMPLETED", "green")
        except Exception as e:
            check_color_print("Dependencies installation", f"FAILED: {str(e)}", "red")
```

This function prompts the user before attempting installation and uses the current Python executable to ensure dependencies are installed in the correct environment.

## Main Diagnostic Function

The `run_diagnostic_test` function orchestrates all the checks:

```python
def run_diagnostic_test(interpreter_path='paste.txt'):
    """Run diagnostic tests to identify issues"""
    print("\n===== BSL Interpreter Diagnostic Tool =====\n")
    print("Running system checks...\n")

    # Check operating system
    check_color_print("Operating System", platform.system() + " " + platform.release(), "yellow")
    
    # Check Python version
    get_python_version()
    
    # Check dependencies
    dependencies = ['mediapipe', 'opencv-python', 'numpy', 'pickle', 'nltk', 
                    'firebase_admin', 'requests']
    
    missing_deps = []
    for dep in dependencies:
        if not check_dependency(dep):
            missing_deps.append(dep)
    
    # Check files
    print("\nChecking required files:")
    check_file_exists('model.p', "BSL model file")
    check_file_exists('bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json', "Firebase credentials")
    check_file_exists('active_stream.txt', "Active stream ID file")
    check_file_exists('translation_data.json', "Translation data file")
```

This function checks:
1. The operating system and Python version
2. Required Python packages
3. Critical files needed by the BSL interpreter

## Diagnostic Summary and Recommendations

The script concludes with a summary of issues found and suggested fixes:

```python
# Summarize findings
print("\n===== Diagnostic Summary =====")
if missing_deps:
    check_color_print("Missing Dependencies", ", ".join(missing_deps), "red")
    print("  → Fix: Install the missing packages using pip install [package_name]")

if not os.path.exists('model.p'):
    check_color_print("Missing model file", "model.p not found", "red")
    print("  → Fix: Ensure 'model.p' is in the current directory or a parent directory")

# Additional checks...

print("\n===== Next Steps =====")
print("1. Fix the issues noted above")
print("2. Try running the interpreter with detailed debugging:")
print(f"   python {interpreter_path} [stream_id] 2>&1 | tee debug_log.txt")
print("3. Review 'debug_log.txt' for detailed error messages\n")
```

This provides clear next steps for the user to resolve any detected issues.

## Error Handling

The script includes error handling to ensure the diagnostic tool itself doesn't crash:

```python
if __name__ == "__main__":
    try:
        run_diagnostic_test()
    except Exception as e:
        print("\nDiagnostic tool encountered an error:")
        traceback.print_exc()
```