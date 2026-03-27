"""
Hospital Queue Chatbot Module
Lightweight intent-based chatbot for hospital queue management system.
Uses keyword matching and pattern recognition for intent classification.
Can be easily upgraded to use OpenAI API or transformer models.
"""

import json
import os
import re
import sqlite3
from typing import Dict, List, Tuple, Optional
from contextlib import contextmanager

# Global model data (loaded once at startup)
INTENTS_DATA = None
DB_FILE = None


@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def load_intents(intents_file: str = "intents.json") -> Dict:
    """Load intents data from JSON file"""
    global INTENTS_DATA
    script_dir = os.path.dirname(os.path.abspath(__file__))
    intents_path = os.path.join(script_dir, intents_file)
    
    try:
        with open(intents_path, 'r', encoding='utf-8') as f:
            INTENTS_DATA = json.load(f)
        return INTENTS_DATA
    except FileNotFoundError:
        print(f"Warning: {intents_path} not found. Using default intents.")
        return get_default_intents()
    except json.JSONDecodeError as e:
        print(f"Error parsing {intents_path}: {e}")
        return get_default_intents()


def get_default_intents() -> Dict:
    """Return default intents if file not found"""
    return {
        "intents": [
            {
                "tag": "greeting",
                "patterns": ["hello", "hi", "hey", "good morning", "good afternoon", "greetings"],
                "responses": ["Hello! How can I help you with the hospital queue today?", 
                             "Hi there! I'm here to help with queue information.",
                             "Hello! Ask me about the patient queue or hospital information."]
            },
            {
                "tag": "queue_status",
                "patterns": ["how many patients", "queue length", "patients in queue", 
                           "how many in queue", "queue count", "number of patients"],
                "responses": ["There are {queue_count} patients currently in the queue."]
            },
            {
                "tag": "next_patient",
                "patterns": ["who is next", "next patient", "who's next", "next in line",
                           "who will be served", "next to serve"],
                "responses": ["The next patient to be served is {next_patient_info}."]
            },
            {
                "tag": "queue_empty",
                "patterns": ["is queue empty", "anyone waiting", "patients waiting"],
                "responses": ["{queue_status_message}"]
            },
            {
                "tag": "patient_info",
                "patterns": ["patient details", "tell me about patient", "patient information",
                           "who is patient", "patient name"],
                "responses": ["{patient_info_response}"]
            },
            {
                "tag": "priority_info",
                "patterns": ["what is priority", "priority levels", "how does priority work",
                           "priority system", "priority meaning"],
                "responses": ["Priority levels: 1 = High/Critical (served first), "
                             "2 = Medium/Urgent, 3 = Low/Regular. "
                             "Within same priority, older patients are served first."]
            },
            {
                "tag": "hospital_hours",
                "patterns": ["hospital hours", "opening hours", "when is hospital open",
                           "hospital schedule", "visiting hours"],
                "responses": ["The hospital is open 24/7 for emergency services. "
                             "Regular appointments are available Monday-Friday 8 AM - 6 PM."]
            },
            {
                "tag": "goodbye",
                "patterns": ["bye", "goodbye", "see you", "thanks", "thank you", "exit"],
                "responses": ["You're welcome! Feel free to ask if you need more information.",
                             "Goodbye! Take care.",
                             "Thank you for using the hospital queue system!"]
            },
            {
                "tag": "help",
                "patterns": ["help", "what can you do", "what do you know", "capabilities"],
                "responses": ["I can help you with:\n"
                             "- Queue status and patient count\n"
                             "- Next patient information\n"
                             "- Patient details\n"
                             "- Priority system explanation\n"
                             "- Hospital information\n"
                             "Just ask me anything about the queue!"]
            }
        ]
    }


def initialize_chatbot(db_file_path: str, intents_file: str = "intents.json") -> bool:
    """Initialize chatbot with database path and load intents"""
    global DB_FILE, INTENTS_DATA
    DB_FILE = db_file_path
    INTENTS_DATA = load_intents(intents_file)
    return INTENTS_DATA is not None


def preprocess_text(text: str) -> str:
    """Preprocess user input: lowercase, remove punctuation, normalize"""
    text = text.lower().strip()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text


def calculate_similarity(pattern: str, user_input: str) -> float:
    """Calculate similarity score between pattern and user input"""
    pattern_words = set(pattern.lower().split())
    input_words = set(user_input.lower().split())
    
    if not pattern_words or not input_words:
        return 0.0
    
    # Jaccard similarity
    intersection = len(pattern_words & input_words)
    union = len(pattern_words | input_words)
    
    if union == 0:
        return 0.0
    
    similarity = intersection / union
    
    # Bonus for exact substring match
    if pattern.lower() in user_input.lower() or user_input.lower() in pattern.lower():
        similarity += 0.3
    
    return min(similarity, 1.0)


def classify_intent(user_input: str) -> Tuple[str, float]:
    """Classify user intent based on input text"""
    if not INTENTS_DATA or "intents" not in INTENTS_DATA:
        return "unknown", 0.0
    
    user_input = preprocess_text(user_input)
    best_intent = "unknown"
    best_score = 0.0
    
    for intent in INTENTS_DATA["intents"]:
        for pattern in intent.get("patterns", []):
            score = calculate_similarity(pattern, user_input)
            if score > best_score:
                best_score = score
                best_intent = intent["tag"]
    
    # Threshold for intent recognition
    if best_score < 0.2:
        return "unknown", best_score
    
    return best_intent, best_score


def get_queue_count() -> int:
    """Get current queue count from database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM patients WHERE status = 'queued'")
            count = cursor.fetchone()[0]
            return count
    except Exception as e:
        print(f"Error getting queue count: {e}")
        return 0


def get_next_patient() -> Optional[Dict]:
    """Get next patient to be served (highest priority)"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, age, priority FROM patients WHERE status = 'queued' "
                "ORDER BY priority ASC, age DESC, id ASC LIMIT 1"
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "age": row[2],
                    "priority": row[3]
                }
            return None
    except Exception as e:
        print(f"Error getting next patient: {e}")
        return None


def get_patient_by_name(name: str) -> Optional[Dict]:
    """Get patient information by name (for demo purposes)"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, age, priority, status FROM patients WHERE name LIKE ? LIMIT 5",
                (f"%{name}%",)
            )
            rows = cursor.fetchall()
            if rows:
                patients = [{
                    "id": row[0],
                    "name": row[1],
                    "age": row[2],
                    "priority": row[3],
                    "status": row[4]
                } for row in rows]
                return patients
            return None
    except Exception as e:
        print(f"Error getting patient by name: {e}")
        return None


def format_patient_info(patient: Dict) -> str:
    """Format patient information for response"""
    priority_names = {1: "High", 2: "Medium", 3: "Low"}
    priority_name = priority_names.get(patient["priority"], "Unknown")
    return f"Patient ID {patient['id']}: {patient['name']}, Age {patient['age']}, Priority {priority_name} ({patient['priority']})"


def generate_response(intent: str, user_input: str) -> str:
    """Generate response based on intent and context"""
    if not INTENTS_DATA or "intents" not in INTENTS_DATA:
        return "I'm sorry, I'm having trouble understanding. Could you rephrase your question?"
    
    # Find intent data
    intent_data = None
    for i in INTENTS_DATA["intents"]:
        if i["tag"] == intent:
            intent_data = i
            break
    
    if not intent_data:
        return "I'm not sure how to help with that. Try asking about the queue status or next patient."
    
    responses = intent_data.get("responses", ["I understand, but I need more information."])
    base_response = responses[0] if responses else "I'm here to help!"
    
    # Fill in dynamic information based on intent
    if intent == "queue_status":
        count = get_queue_count()
        return base_response.format(queue_count=count)
    
    elif intent == "next_patient":
        next_patient = get_next_patient()
        if next_patient:
            patient_info = format_patient_info(next_patient)
            return base_response.format(next_patient_info=patient_info)
        else:
            return "There are no patients currently in the queue."
    
    elif intent == "queue_empty":
        count = get_queue_count()
        if count == 0:
            return "Yes, the queue is currently empty. No patients are waiting."
        else:
            return f"No, there are {count} patient(s) currently in the queue."
    
    elif intent == "patient_info":
        # Try to extract patient name from input
        user_input_lower = user_input.lower()
        # Look for "patient" followed by a name or just a name
        words = user_input_lower.split()
        name_candidates = []
        for i, word in enumerate(words):
            if word in ["patient", "about", "tell", "who", "is"] and i + 1 < len(words):
                # Next word might be the name
                potential_name = words[i + 1]
                if len(potential_name) > 2:  # Likely a name
                    name_candidates.append(potential_name)
        
        # Also check for capitalized words (likely names)
        original_words = user_input.split()
        for word in original_words:
            if word[0].isupper() and len(word) > 2:
                name_candidates.append(word)
        
        if name_candidates:
            for name in name_candidates:
                patients = get_patient_by_name(name)
                if patients:
                    if len(patients) == 1:
                        return f"Here's the information: {format_patient_info(patients[0])}, Status: {patients[0]['status']}"
                    else:
                        result = f"Found {len(patients)} patient(s) matching '{name}':\n"
                        for p in patients:
                            result += f"- {format_patient_info(p)}, Status: {p['status']}\n"
                        return result
        
        # Generic patient info response
        count = get_queue_count()
        if count > 0:
            next_patient = get_next_patient()
            if next_patient:
                return f"There are {count} patients in the queue. The next patient is {next_patient['name']} (ID: {next_patient['id']})."
        return "I can help you find patient information. Please provide the patient's name, or ask about the next patient in queue."
    
    # For other intents, return base response
    return base_response


def get_response(user_input: str) -> str:
    """
    Main function to get chatbot response for user input.
    
    Args:
        user_input: User's message/question
    
    Returns:
        Chatbot's response string
    """
    if not user_input or not user_input.strip():
        return "Please ask me a question about the hospital queue or patient information."
    
    # Classify intent
    intent, confidence = classify_intent(user_input)
    
    # Generate response
    response = generate_response(intent, user_input)
    
    return response


def train_model(intents_file: str = "intents.json") -> bool:
    """
    Train/validate the chatbot model.
    In this lightweight version, this just validates the intents file.
    For ML models, this would train the actual model.
    
    Args:
        intents_file: Path to intents JSON file
    
    Returns:
        True if training/validation successful
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        intents_path = os.path.join(script_dir, intents_file)
        
        with open(intents_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate structure
        if "intents" not in data:
            print("Error: 'intents' key not found in JSON file")
            return False
        
        required_keys = ["tag", "patterns", "responses"]
        for i, intent in enumerate(data["intents"]):
            for key in required_keys:
                if key not in intent:
                    print(f"Error: Intent {i} missing required key: {key}")
                    return False
            if not intent["patterns"]:
                print(f"Warning: Intent '{intent['tag']}' has no patterns")
            if not intent["responses"]:
                print(f"Warning: Intent '{intent['tag']}' has no responses")
        
        print(f"✓ Successfully validated {len(data['intents'])} intents from {intents_file}")
        return True
    
    except FileNotFoundError:
        print(f"Error: {intents_file} not found")
        return False
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return False
    except Exception as e:
        print(f"Error during training: {e}")
        return False


# For OpenAI API integration (optional upgrade)
def get_response_openai(user_input: str, api_key: str = None) -> str:
    """
    Optional: Get response using OpenAI API.
    Uncomment and configure if you want to use GPT models.
    
    Requires: pip install openai
    """
    # Uncomment to use OpenAI:
    # try:
    #     import openai
    #     if not api_key:
    #         api_key = os.getenv("OPENAI_API_KEY")
    #     if not api_key:
    #         return get_response(user_input)  # Fallback to local model
    #     
    #     openai.api_key = api_key
    #     
    #     # Get context from database
    #     queue_count = get_queue_count()
    #     next_patient = get_next_patient()
    #     
    #     context = f"""You are a helpful hospital queue assistant. 
    #     Current queue status: {queue_count} patients waiting.
    #     Next patient: {next_patient['name'] if next_patient else 'None'}.
    #     Answer questions about the queue, patients, and hospital information."""
    #     
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": context},
    #             {"role": "user", "content": user_input}
    #         ],
    #         max_tokens=150,
    #         temperature=0.7
    #     )
    #     
    #     return response.choices[0].message.content
    # except ImportError:
    #     return get_response(user_input)  # Fallback
    # except Exception as e:
    #     print(f"OpenAI API error: {e}")
    #     return get_response(user_input)  # Fallback
    
    return get_response(user_input)  # Default to local model


if __name__ == "__main__":
    # Test the chatbot
    print("Testing Hospital Queue Chatbot...")
    print("=" * 50)
    
    # Initialize with test database path
    test_db = os.path.join(os.path.dirname(__file__), "hospital_queue.db")
    initialize_chatbot(test_db, "intents.json")
    
    # Test queries
    test_queries = [
        "Hello",
        "How many patients are in the queue?",
        "Who is next?",
        "What is priority?",
        "Tell me about patient John",
        "Is the queue empty?",
        "Help",
        "Thank you"
    ]
    
    for query in test_queries:
        print(f"\nUser: {query}")
        response = get_response(query)
        print(f"Bot: {response}")
        print("-" * 50)

