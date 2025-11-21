# Build Instructions

## Windows Executable (via GitHub Actions)

Since this project is developed on Linux but targets Windows users, we use **GitHub Actions** to automatically build the Windows executable (`.exe`).

### How it works
1.  Push your changes to GitHub.
2.  Go to the **Actions** tab in your repository.
3.  Click on the **Build Windows Executable** workflow.
4.  Once the build finishes (green checkmark), click on it.
5.  Scroll down to the **Artifacts** section and download `MyntraTk-Windows`.
6.  Extract the zip file to get your `MyntraTk.exe`.

### Manual Build (Windows Only)
If you are on a Windows machine, you can build it manually:

1.  Install Python 3.11+.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    pip install pyinstaller
    ```
3.  Run the build command:
    ```bash
    pyinstaller MyntraTk.spec
    ```
4.  The executable will be in the `dist` folder.

## Linux Build
To build a Linux executable (for testing):
```bash
pyinstaller MyntraTk.spec
```
Note: The Linux executable will NOT work on Windows.
