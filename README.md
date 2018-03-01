### Setup

1. Install all packages required for this application using this command:
    ```bash
    pip install -r requirements.txt
    ```

2. After applying changes to the application layout (using QT Designer), run this command:
    ```bash
    pyuic5 iottestbed.ui -o layout.py
    ```

### Deployment
- To run the application directly through Python, simply use this command:
    ```bash
    python main.py
    ```

- To convert the application into an "exe" executable, use this command (find .exe in dist/ folder): 
    ```bash
    pyinstaller --clean --onefile -w main.py -n iottestbed
    ```
