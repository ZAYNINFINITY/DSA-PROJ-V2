# Chatbot Quick Start Guide

## ✅ What Was Added

1. **Backend:**

   - `chatbot.py` - Chatbot module with intent classification
   - `intents.json` - Training data (patterns and responses)
   - `/api/chat` endpoint in `app_py.py`

2. **Frontend:**
   - Chat widget UI in `index.html`
   - Floating chat button
   - Real-time message display

## 🚀 Quick Test

1. **Start the server:**

   ```bash
   cd backend
   python app_py.py
   ```

2. **Open browser:**

   ```
   http://localhost:5000
   ```

3. **Click the chat button** (💬) in bottom-right

4. **Try these questions:**
   - "Hello"
   - "How many patients are in the queue?"
   - "Who is next?"
   - "What is priority?"
   - "Help"

## 📝 Training (Adding New Responses)

Edit `backend/intents.json`:

```json
{
  "tag": "your_intent",
  "patterns": ["pattern1", "pattern2"],
  "responses": ["Response 1", "Response 2"]
}
```

No retraining needed - just restart the server!

## 🔧 Customization

- **Add intents:** Edit `intents.json`
- **Modify logic:** Edit `chatbot.py` → `generate_response()`
- **Change UI:** Edit `frontend/templates/index.html` → Chat styles

## 📱 Mobile

Works automatically in Capacitor - no changes needed!

## 🐛 Troubleshooting

- **Chat not working?** Check server logs for chatbot initialization
- **Wrong responses?** Add more patterns to `intents.json`
- **Database errors?** Ensure `hospital_queue.db` exists

See `CHATBOT_README.md` for detailed documentation.

