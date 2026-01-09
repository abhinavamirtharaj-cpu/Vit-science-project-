/**
 * script.js - Two-person real-time chat with sentiment analysis
 * Handles WebSocket communication, message display, and UI interactions
 */

let socket;
let currentUsername = '';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    showUsernameModal();
});

/**
 * Show username entry modal
 */
function showUsernameModal() {
    const modal = document.getElementById('username-modal');
    const input = document.getElementById('username-input');
    const joinBtn = document.getElementById('join-chat-btn');
    
    modal.style.display = 'flex';
    
    // Join button handler
    joinBtn.addEventListener('click', () => {
        const username = input.value.trim();
        if (username) {
            currentUsername = username;
            modal.style.display = 'none';
            initializeChat();
        } else {
            alert('Please enter your name');
        }
    });
    
    // Enter key handler
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            joinBtn.click();
        }
    });
    
    // Focus input
    input.focus();
}

/**
 * Initialize chat with WebSocket connection
 */
function initializeChat() {
    // Update UI with current user
    document.getElementById('current-user').textContent = `You: ${currentUsername}`;
    
    // Connect to WebSocket server
    socket = io(window.location.origin);
    
    // Connection established
    socket.on('connect', () => {
        console.log('[WebSocket] Connected');
        // Join the chat room
        socket.emit('join_chat', { username: currentUsername });
    });
    
    // Listen for chat history
    socket.on('chat_history', (data) => {
        console.log('[WebSocket] Received chat history:', data.messages.length, 'messages');
        // Clear existing messages
        const messagesContainer = document.getElementById('messages-inner');
        messagesContainer.innerHTML = '';
        
        // Display all history messages
        data.messages.forEach(msg => displayMessage(msg, false));
        scrollToBottom();
    });
    
    // Listen for new messages
    socket.on('new_message', (data) => {
        console.log('[WebSocket] New message from:', data.sender);
        displayMessage(data, true);
        scrollToBottom();
    });
    
    // Listen for user join notifications
    socket.on('user_joined', (data) => {
        showSystemMessage(`${data.username} joined the chat`);
    });
    
    // Listen for user leave notifications
    socket.on('user_left', (data) => {
        showSystemMessage(`${data.username} left the chat`);
    });
    
    // Listen for errors
    socket.on('error', (data) => {
        console.error('[WebSocket] Error:', data.message);
        showSystemMessage(`Error: ${data.message}`, 'error');
    });
    
    // Disconnection
    socket.on('disconnect', () => {
        console.log('[WebSocket] Disconnected');
        showSystemMessage('Disconnected from server', 'error');
    });
    
    // Setup message form
    setupMessageForm();
}

/**
 * Setup message sending form
 */
function setupMessageForm() {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('message-input');
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = input.value.trim();
        
        if (text) {
            // Send message via WebSocket
            socket.emit('send_message', { text });
            
            // Clear input
            input.value = '';
            input.style.height = 'auto';
        }
    });
    
    // Auto-resize textarea
    input.addEventListener('input', () => {
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 150) + 'px';
    });
    
    // Send on Enter, new line on Shift+Enter
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            form.dispatchEvent(new Event('submit'));
        }
    });
}

/**
 * Display a message in the chat
 */
function displayMessage(data, animate = true) {
    const messagesContainer = document.getElementById('messages-inner');
    const messageDiv = document.createElement('div');
    
    // Determine if message is from current user
    const isOwnMessage = data.sender === currentUsername;
    messageDiv.className = `message ${isOwnMessage ? 'message-right' : 'message-left'}`;
    
    if (animate) {
        messageDiv.classList.add('message-animate');
    }
    
    // Add sentiment color border
    if (data.sentiment && data.sentiment.color) {
        messageDiv.style.borderLeft = isOwnMessage ? 'none' : `4px solid ${data.sentiment.color}`;
        messageDiv.style.borderRight = isOwnMessage ? `4px solid ${data.sentiment.color}` : 'none';
    }
    
    // Build message HTML
    messageDiv.innerHTML = `
        <div class="message-header">
            <span class="message-sender">${escapeHtml(data.sender)}</span>
            <span class="message-time">${formatTime(data.timestamp)}</span>
        </div>
        <div class="message-text">${escapeHtml(data.text)}</div>
        ${data.sentiment ? `
            <div class="message-sentiment">
                <span class="sentiment-emoji">${data.sentiment.emoji}</span>
                <span class="sentiment-category">${data.sentiment.category}</span>
            </div>
        ` : ''}
    `;
    
    messagesContainer.appendChild(messageDiv);
}

/**
 * Show system message (join/leave notifications, errors)
 */
function showSystemMessage(text, type = 'info') {
    const messagesContainer = document.getElementById('messages-inner');
    const systemDiv = document.createElement('div');
    systemDiv.className = `system-message system-message-${type}`;
    systemDiv.textContent = text;
    messagesContainer.appendChild(systemDiv);
    scrollToBottom();
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    const messagesContainer = document.getElementById('messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/**
 * Format timestamp to readable time
 */
function formatTime(timestamp) {
    try {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
        });
    } catch (e) {
        return '';
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}