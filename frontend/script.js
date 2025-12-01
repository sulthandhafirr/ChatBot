const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

// API endpoint - automatically detect if running on localhost or production
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000'
    : '';  // Use relative URL for production
const API_URL = `${API_BASE}/api/chat`;

// Add message to chat
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = isUser 
        ? `<strong>You:</strong> ${content}`
        : `<strong>Bot:</strong> ${content}`;
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add loading indicator
function addLoadingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = 'loading-indicator';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = '<strong>Bot:</strong> Typing<span class="loading"></span>';
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove loading indicator
function removeLoadingIndicator() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.remove();
    }
}

// Send message to API
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Disable input
    userInput.disabled = true;
    sendButton.disabled = true;
    
    // Add user message
    addMessage(message, true);
    
    // Clear input
    userInput.value = '';
    
    // Show loading
    addLoadingIndicator();
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove loading
        removeLoadingIndicator();
        
        // Add bot response
        addMessage(data.response);
        
    } catch (error) {
        console.error('Error:', error);
        removeLoadingIndicator();
        addMessage('Sorry, an error occurred. Please ensure the server is running and DeepSeek API key is configured.');
    } finally {
        // Enable input
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
    }
}

// Event listeners
sendButton.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Focus input on load
userInput.focus();

// Check server health on load
async function checkHealth() {
    try {
        const healthUrl = `${API_BASE}/api/health`;
        const response = await fetch(healthUrl);
        const data = await response.json();
        console.log('Server health:', data);
        if (data.documents_count === 0) {
            console.warn('Warning: Knowledge base is empty!');
        }
    } catch (error) {
        console.warn('Server not connected:', error);
    }
}

checkHealth();
