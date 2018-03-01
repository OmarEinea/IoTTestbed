### Setup and Deployment

1. To install all packages required for this application, use the following command:
    ```bash
    pip install -r requirements.txt
    ```

2. After applying changes to the application layout, run the following command:
    ```bash
    pyuic5 iottestbed.ui -o layout.py
    ```

3. To convert the application into an "exe" executable, use the following command (find .exe in dist/ folder): 
    ```bash
    pyinstaller --clean --onefile -w main.py
    ```
