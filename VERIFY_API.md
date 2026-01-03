# How to Verify API is Working

## Quick Check

### 1. Visual Indicator in UI
When you open the validation UI, look at the **top-right corner**:
- **Green "✓ API Connected"** = API is working
- **Red "✗ API Offline"** = API is not running

### 2. Browser Console
Open browser console (F12) and check for:
- `✓ API is available` = API is working
- `✗ API not available` = API is not running

### 3. Test Script
Run the test script:
```bash
python test_api_connection.py
```

This will test:
- API server connection
- GET validations endpoint
- POST validation endpoint
- Database connectivity

## Common Issues

### Issue: "API Offline" or "using local storage"

**Cause:** API server is not running

**Solution:**
1. Make sure you're running the **combined server**:
   ```bash
   python run_validator_tinydb.py
   ```
   
   NOT just:
   ```bash
   python validation_api_tinydb.py  # This only starts API, not UI
   ```

2. Check if API is running:
   ```bash
   # In another terminal
   curl http://localhost:8001/
   ```
   
   Should return:
   ```json
   {"message":"Sign Segmentation Validator API - TinyDB","status":"running","tinydb":"connected"}
   ```

### Issue: "Connection timeout"

**Cause:** API server is slow or not responding

**Solution:**
1. Check if port 8001 is in use:
   ```bash
   lsof -i :8001
   ```
   
2. Restart the API server

### Issue: "HTTP 503 - MongoDB/TinyDB not initialized"

**Cause:** Database not properly initialized

**Solution:**
1. For TinyDB: Make sure `tinydb` is installed:
   ```bash
   pip install tinydb
   ```

2. Check database file exists:
   ```bash
   ls -la outputs/validation_database_tinydb.json
   ```

## Manual Verification Steps

### Step 1: Check API Server
```bash
# Should show API info
curl http://localhost:8001/
```

### Step 2: Check Validations Endpoint
```bash
# Should return validations (may be empty)
curl http://localhost:8001/api/validations
```

### Step 3: Test Save Validation
```bash
curl -X POST http://localhost:8001/api/validations \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "TEST",
    "validation": {
      "timestamp": "2024-01-01T00:00:00Z",
      "status": "correct",
      "feedback": "Test",
      "validator": "test"
    }
  }'
```

Should return:
```json
{"success":true,"message":"Validation saved successfully","video_id":"TEST","total_validations":1}
```

## Expected Behavior

### When API is Working:
- ✅ Status indicator shows "✓ API Connected" (green)
- ✅ Saving validation shows: "✓ Validation saved to database successfully!"
- ✅ Progress table updates immediately after save
- ✅ Refresh button loads latest data from database

### When API is NOT Working:
- ❌ Status indicator shows "✗ API Offline" (red)
- ❌ Saving validation shows: "✓ Validation saved (using local storage - API unavailable)"
- ❌ Progress table doesn't update (only shows localStorage data)
- ⚠️ Data is saved to browser localStorage only (not persistent)

## Troubleshooting Checklist

- [ ] API server is running (`python run_validator_tinydb.py`)
- [ ] Port 8001 is accessible (`curl http://localhost:8001/`)
- [ ] TinyDB is installed (`pip install tinydb`)
- [ ] Database file is writable (`outputs/validation_database_tinydb.json`)
- [ ] No firewall blocking port 8001
- [ ] Browser console shows no CORS errors
- [ ] API status indicator in UI shows green

## Still Not Working?

1. **Check terminal output** where API server is running
2. **Check browser console** (F12) for detailed error messages
3. **Run test script**: `python test_api_connection.py`
4. **Check database file**: `cat outputs/validation_database_tinydb.json`
