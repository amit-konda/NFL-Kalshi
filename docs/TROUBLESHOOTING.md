# Troubleshooting

## Import Warnings in IDE

### Problem
You see warnings like:
```
Import "pandas" could not be resolved
Import "numpy" could not be resolved
Import "matplotlib.pyplot" could not be resolved
Import "scipy" could not be resolved
```

### Solution

**These are IDE warnings, NOT actual errors.** The scripts work fine when run from terminal.

The issue is that your IDE (VSCode/Cursor) is using a different Python interpreter than your terminal.

### Fix Options:

#### Option 1: Select Correct Interpreter (Recommended)
1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Python: Select Interpreter"
3. Choose the interpreter that matches your terminal (usually shows Python 3.8)
4. Reload window: `Cmd+Shift+P` → "Developer: Reload Window"

#### Option 2: Install Packages in IDE's Python
1. Check which Python your IDE is using: Look at bottom-right of VSCode
2. Install packages for that specific Python:
   ```bash
   /path/to/ide/python -m pip install -r requirements.txt
   ```

#### Option 3: Verify Packages Work (ignore warnings)
Run this to confirm everything works:
```bash
python3 -c "import pandas; import numpy; import matplotlib; import scipy; print('✅ All imports work!')"
```

If this succeeds, the warnings are harmless and you can ignore them.

## Other Common Issues

### "Module not found" when running scripts
```bash
pip3 install -r requirements.txt
```

### SSL Certificate Errors
```bash
python3 -m pip install --upgrade certifi
```

### Scripts taking too long
The data download (especially `generate_unified_data.py`) can take 5-10 minutes because it downloads 5 years of play-by-play data. This is normal.

### Data not updating
If you modify `generate_unified_data.py`, you need to run it again:
```bash
python3 generate_unified_data.py
```

## IDE Interpreter Setup (Cursor/VSCode)

If import warnings persist or the IDE points to the wrong Python:

- Use interpreter at: `/Library/Frameworks/Python.framework/Versions/3.8/bin/python3` (Python 3.8.10)

### Select Interpreter
1. Cmd+Shift+P → "Python: Select Interpreter"
2. Choose Python 3.8.10 with the path above
3. Cmd+Shift+P → "Developer: Reload Window"

### Manually Enter Path
1. Cmd+Shift+P → "Python: Select Interpreter"
2. "+ Enter interpreter path..."
3. Paste `/Library/Frameworks/Python.framework/Versions/3.8/bin/python3`

### Verify Packages Work
```bash
python3 -c "import pandas, numpy, matplotlib, scipy; print('✅ All packages working!')"
```

If the command succeeds, warnings are IDE-only and can be ignored.

