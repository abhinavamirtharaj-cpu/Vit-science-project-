STEPS FOR STANDALONE EXECUTABLE BUILD (NUITKA)
==============================================

1. Place all required model/data/config files in the models/ directory.
   - Example: models/model.onnx, models/user_insights.json, models/chat_history_global.csv

2. Make sure all code that loads files uses:
   from get_resource_path import get_resource_path
   path = get_resource_path('models/your_file')

3. Open a terminal in the project root directory.

4. Run the build script:
   python build_dist.py

   - This will:
     * Create a clean virtual environment
     * Install only essential dependencies
     * Use Nuitka to bundle everything into a single .exe (or binary)
     * Include all files in the models/ directory inside the executable

5. After the build completes, look for the generated .exe (or binary) in the current directory.

6. You can now run this file on any compatible system—no Python or extra installs needed!

TROUBLESHOOTING:
----------------
- If you add new models or data, re-run the build script.
- If you see missing file errors, make sure the file is in models/ and accessed via get_resource_path().
- For best performance, use ONNX or other optimized model formats.

For more details, see build_dist.py and get_resource_path.py.
