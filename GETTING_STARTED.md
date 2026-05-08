# 🚀 GETTING STARTED - QUICK GUIDE

## What You Need to Do (3 Steps)

### Step 1: Copy Your PDF File
Copy `Egyptian_ERP_System_Comprehensive_Manual.pdf` from the old folder into **this folder** (`CS_Chatbot_Production`)

### Step 2: Start the Server
**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

The server will:
- ✅ Check that Python is installed
- ✅ Check that the PDF file exists
- ✅ Create a virtual environment (if needed)
- ✅ Install all Python packages
- ✅ Load the PDF and create search index
- ✅ Start the API server on http://localhost:5000

### Step 3: Test It Works
In another terminal:
```bash
python test_api.py
```

Or in Python:
```python
import requests

response = requests.post('http://localhost:5000/ask',
    json={"question": "How do I access the system documentation?"})
print(response.json()['answer'])
```

---

## What Changed From Old Folder

✅ **Fixed PDF reference** - Now uses `Egyptian_ERP_System_Comprehensive_Manual.pdf` (the real PDF)  
✅ **Cleaner code** - Single main application file (`main_app.py`)  
✅ **Better scripts** - start.bat and start.sh now properly validate the PDF  
✅ **Fresh config** - Proper configuration with correct defaults  
✅ **No clutter** - Only essential files, no documentation overload  

---

## File Structure

```
CS_Chatbot_Production/
├── main_app.py              ← Run this (Flask API)
├── config.py                ← Configuration module
├── start.bat                ← Windows startup
├── start.sh                 ← Linux/Mac startup
├── test_api.py              ← Test client
├── .env.template            ← Config template
├── requirements.txt         ← Python packages
├── .env                     ← Your config (auto-created)
├── Egyptian_ERP_System_Comprehensive_Manual.pdf  ← COPY YOUR PDF HERE
└── README.md
```

---

## Configuration

Everything is configured correctly by default for `Egyptian_ERP_System_Comprehensive_Manual.pdf`.

If you need to change anything, edit `.env`:
```ini
FILE_PATH=Egyptian_ERP_System_Comprehensive_Manual.pdf
LM_STUDIO_BASE_URL=http://localhost:1234/v1
FLASK_PORT=5000
TEMPERATURE=0.3
```

---

## Common Questions

**Q: Where do I put the PDF?**  
A: In this folder (`CS_Chatbot_Production/`) alongside all the scripts

**Q: What if it can't find the PDF?**  
A: Make sure the PDF filename matches exactly. The startup script will tell you if it's wrong.

**Q: How do I use it?**  
A: API at `http://localhost:5000/ask` (see README.md for examples)

**Q: How do I stop it?**  
A: Press `Ctrl+C` in the terminal

**Q: Can I change the PDF?**  
A: Yes, edit `FILE_PATH` in `.env` to your PDF name

---

## That's It! 🎉

You now have a clean, working Customer Support Chatbot deployment.

**Next steps:**
1. Copy the PDF file here
2. Run `start.bat` (or `start.sh`)
3. Test with `python test_api.py`
4. Start using the API!

See [README.md](README.md) for more details and examples.
