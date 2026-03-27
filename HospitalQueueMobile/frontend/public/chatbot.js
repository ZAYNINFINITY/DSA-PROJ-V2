/**
 * Hospital Queue Management Chatbot
 * 
 * A simple rule-based chatbot to help users navigate and use the queue management system.
 * This chatbot provides helpful information about queue operations, priority levels, and app features.
 */

class HospitalQueueChatbot {
  constructor() {
    this.responses = {
      greeting: [
        "Hello! 👋 I'm here to help you manage the hospital patient queue. How can I assist you today?",
        "Hi there! 🏥 I can help you with queue management. What would you like to know?",
        "Welcome! I'm your queue assistant. Ask me anything about managing patients!"
      ],
      help: [
        "I can help you with:\n• Adding patients to the queue\n• Understanding priority levels\n• Serving patients\n• Sorting the queue\n• Clearing the queue\n• Exporting data\n• App settings\n\nWhat would you like to know?",
        "Here's what I can help with:\n\n➕ Add Patient - Add new patients with name, age, and priority\n👨‍⚕️ Serve Patient - Mark the next patient as served\n🔄 Sort Queue - Sort patients by priority level\n🗑️ Clear Queue - Remove all patients from queue\n📤 Export Data - Download queue data as JSON\n⚙️ Settings - Configure backend server URL\n\nAsk me about any of these features!",
        "I can explain:\n• How to add patients\n• Priority levels (High/Medium/Low)\n• How the queue works\n• App settings and configuration\n\nWhat do you need help with?"
      ],
      priority: [
        "Priority levels help organize patients:\n\n🔴 Priority 1 (High/Critical) - Urgent cases requiring immediate attention\n🟠 Priority 2 (Medium/Urgent) - Important but not critical\n🟢 Priority 3 (Low/Regular) - Standard cases\n\nThe queue automatically sorts by priority, with Priority 1 patients served first.",
        "There are 3 priority levels:\n\n1️⃣ High Priority (Critical) - Red border, served first\n2️⃣ Medium Priority (Urgent) - Orange border, served second\n3️⃣ Low Priority (Regular) - Green border, served last\n\nPatients are automatically sorted by priority in the queue.",
        "Priority system:\n• 🔴 High (1) - Critical cases, highest priority\n• 🟠 Medium (2) - Urgent cases, medium priority\n• 🟢 Low (3) - Regular cases, lowest priority\n\nThe app sorts patients automatically, so critical cases are always at the top!"
      ],
      addPatient: [
        "To add a patient:\n1. Enter the patient's name\n2. Enter their age (1-150)\n3. Select priority level (High/Medium/Low)\n4. Click '➕ Add Patient'\n\nThe patient will appear in the queue immediately!",
        "Adding patients is easy:\n• Fill in the patient name\n• Enter age\n• Choose priority (🔴 High, 🟠 Medium, or 🟢 Low)\n• Click the Add Patient button\n\nThat's it! The patient joins the queue.",
        "Steps to add:\n1. Patient Name field - enter full name\n2. Age field - enter number between 1-150\n3. Priority dropdown - select High, Medium, or Low\n4. Click '➕ Add Patient' button\n\nThe queue updates automatically!"
      ],
      servePatient: [
        "To serve a patient:\n1. Click '👨‍⚕️ Serve Next Patient' button\n2. The patient at the top of the queue (highest priority) will be marked as served\n3. They'll move to the 'Served Patients' section\n4. The queue automatically updates",
        "Serving patients:\n• Click the 'Serve Next Patient' button\n• The highest priority patient is served first\n• Served patients appear in the bottom section\n• You can remove served patients later if needed",
        "How to serve:\n• The '👨‍⚕️ Serve Next Patient' button serves the top patient\n• Patients are served in priority order (High → Medium → Low)\n• Served patients can be removed from the served list"
      ],
      sortQueue: [
        "The queue automatically sorts by priority:\n• Priority 1 (High) patients appear first\n• Priority 2 (Medium) patients appear second\n• Priority 3 (Low) patients appear last\n\nClick '🔄 Sort by Priority' to manually re-sort if needed.",
        "Sorting:\n• The queue is always sorted by priority automatically\n• High priority patients are at the top\n• Use 'Sort by Priority' button to manually refresh the sort\n• The sort happens on the backend for accuracy",
        "Queue sorting:\n• Automatic: Queue sorts by priority when patients are added\n• Manual: Click '🔄 Sort by Priority' to re-sort\n• Order: High → Medium → Low priority"
      ],
      clearQueue: [
        "⚠️ Clearing the queue:\n• Click '🗑️ Clear Queue' button\n• Confirm the action\n• This removes ALL patients from the queue\n• Served patients are NOT affected\n\nUse this carefully - the action cannot be undone!",
        "To clear:\n• Click 'Clear Queue'\n• Confirm when prompted\n• All queued patients will be removed\n• Served patients remain in their section",
        "Clear queue:\n• Removes all patients from the active queue\n• Does NOT affect served patients\n• Requires confirmation\n• Cannot be undone - be careful!"
      ],
      settings: [
        "Settings help:\n• Click '⚙️ Settings' button\n• Enter your backend server URL (e.g., http://192.168.1.50:5000)\n• Click '💾 Save' to save\n• Use '🔌 Test Connection' to verify connectivity\n• The app reloads after saving",
        "Configure settings:\n• Open Settings from the main screen\n• Enter Flask server IP address\n• Format: http://YOUR_IP:5000\n• Test connection before saving\n• Settings persist across app restarts",
        "Settings configuration:\n• Backend URL: Your Flask server address\n• Format: http://192.168.x.y:5000\n• Test button checks connectivity\n• Save button stores the URL\n• App reloads with new settings"
      ],
      export: [
        "Exporting data:\n• Click '📤 Export Data' button\n• Queue data downloads as JSON file\n• Includes all queued and served patients\n• File name includes timestamp\n• Use this to backup or analyze queue data",
        "To export:\n• Click 'Export Data'\n• JSON file downloads automatically\n• Contains complete queue information\n• Includes patient details and priorities\n• Useful for backups and reporting",
        "Export feature:\n• Downloads queue data as JSON\n• Includes all patients (queued + served)\n• File named with timestamp\n• Can be opened in any text editor\n• Perfect for data backup!"
      ],
      search: [
        "Searching the queue:\n• Use the 'Search Queue' input field\n• Type patient name to filter\n• Results update as you type\n• Shows matching patients only\n• Search is case-insensitive",
        "Search feature:\n• Enter name in search box\n• Queue filters automatically\n• Shows only matching patients\n• Works in real-time\n• Clear search to see all patients",
        "How to search:\n• Type in the search box\n• Filter by patient name\n• Results appear instantly\n• Case-insensitive matching\n• Empty search shows all patients"
      ],
      default: [
        "I'm not sure I understand. Could you ask about:\n• Adding patients\n• Priority levels\n• Serving patients\n• Queue sorting\n• Settings\n• Exporting data\n\nOr type 'help' for more options!",
        "Hmm, I didn't catch that. Try asking about:\n• How to add patients\n• What priority levels mean\n• How to serve patients\n• Queue management\n• App settings\n\nType 'help' to see all topics!",
        "I'm here to help with queue management! Try asking:\n• 'How do I add a patient?'\n• 'What are priority levels?'\n• 'How do I serve a patient?'\n• 'Help with settings'\n\nOr type 'help' for a full list!"
      ]
    };

    this.patterns = {
      greeting: /\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b/i,
      help: /\b(help|what can you do|how can you help|what do you know|commands|features)\b/i,
      priority: /\b(priority|priorities|high|medium|low|critical|urgent|regular|what is priority|priority levels)\b/i,
      addPatient: /\b(add|adding|insert|new patient|how to add|add patient|create patient)\b/i,
      servePatient: /\b(serve|serving|serve patient|next patient|how to serve|mark as served)\b/i,
      sortQueue: /\b(sort|sorting|order|organize|arrange|sort queue|priority sort)\b/i,
      clearQueue: /\b(clear|delete|remove all|empty|clear queue|delete all|remove queue)\b/i,
      settings: /\b(settings|config|configuration|server|backend|url|ip address|connection|connect)\b/i,
      export: /\b(export|download|save|backup|download data|export data|get data)\b/i,
      search: /\b(search|find|filter|look for|search queue|find patient)\b/i
    };
  }

  /**
   * Get a response based on user input
   * @param {string} input - User's message
   * @returns {string} Bot response
   */
  getResponse(input) {
    if (!input || input.trim() === '') {
      return this.getRandomResponse('greeting');
    }

    const lowerInput = input.toLowerCase().trim();

    // Check patterns in order of specificity
    for (const [category, pattern] of Object.entries(this.patterns)) {
      if (pattern.test(lowerInput)) {
        return this.getRandomResponse(category);
      }
    }

    return this.getRandomResponse('default');
  }

  /**
   * Get a random response from a category
   * @param {string} category - Response category
   * @returns {string} Random response
   */
  getRandomResponse(category) {
    const responses = this.responses[category] || this.responses.default;
    return responses[Math.floor(Math.random() * responses.length)];
  }

  /**
   * Get quick action suggestions
   * @returns {string[]} Array of suggested questions
   */
  getSuggestions() {
    return [
      "How do I add a patient?",
      "What are priority levels?",
      "How do I serve a patient?",
      "How do I sort the queue?",
      "Help with settings"
    ];
  }
}

// Export for use in other scripts
if (typeof window !== "undefined") {
  window.HospitalQueueChatbot = HospitalQueueChatbot;
}



