/**
 * script.js - Two-person real-time chat with sentiment analysis
 * Handles WebSocket communication, message display, and user interactions
 */

let socket;
let currentUsername = '';
const ROOM_NAME = 'LOCAL';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    showUsernameModal();
    setupInfoModal();
});

/**
 * Show username entry modal on startup
 */
function showUsernameModal() {
    const modal = document.getElementById('username-modal');
    const input = document.getElementById('username-input');
    const joinBtn = document.getElementById('join-chat-btn');
    
    modal.style.display = 'flex';
    modal.classList.remove('hidden');
    
    // Focus on input
    setTimeout(() => input.focus(), 100);
    
    // Handle join button click
    joinBtn.addEventListener('click', () => {
        const username = input.value.trim();
        if (username) {
            currentUsername = username;
            modal.style.display = 'none';
            modal.classList.add('hidden');
            initializeChat();
        } else {
            alert('⚠️ Please enter your name to join the chat');
            input.focus();
        }
    });
    
    // Handle Enter key
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            joinBtn.click();
        }
    });
}

/**
 * Setup info modal handlers
 */
function setupInfoModal() {
    const infoBtn = document.getElementById('info-btn');
    const infoModal = document.getElementById('info-modal');
    const closeInfo = document.getElementById('close-info');
    
    if (infoBtn) {
        infoBtn.addEventListener('click', () => {
            infoModal.classList.remove('hidden');
            infoModal.style.display = 'flex';
        });
    }
    
    if (closeInfo) {
        closeInfo.addEventListener('click', () => {
            infoModal.classList.add('hidden');
            infoModal.style.display = 'none';
        });
    }
    
    // Close on outside click
    infoModal.addEventListener('click', (e) => {
        if (e.target === infoModal) {
            infoModal.classList.add('hidden');
            infoModal.style.display = 'none';
        }
    });
}

/**
 * Initialize WebSocket connection and chat interface
 */
function initializeChat() {
    // Show chat panel
    const chatPanel = document.getElementById('chat-panel');
    chatPanel.classList.remove('hidden');
    
    // Update UI with current user
    document.getElementById('current-user').textContent = `You: ${currentUsername}`;
    
    // Connect to WebSocket server
    const serverUrl = window.location.origin;
    socket = io(serverUrl);
    
    console.log(`Connecting to ${serverUrl}...`);
    
    // WebSocket event listeners
    socket.on('connect', () => {
        console.log('Connected to server');
        showSystemMessage('✅ Connected to LOCAL chat');
        
        // Join the chat room
        socket.emit('join_chat', { username: currentUsername });
    });
    
    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        showSystemMessage('⚠️ Disconnected from server');
    });
    
    socket.on('connect_error', (error) => {
        console.error('Connection error:', error);
        showSystemMessage('❌ Connection error. Please refresh.');
    });
    
    // Listen for chat history
    socket.on('chat_history', (data) => {
        console.log('Received chat history:', data.messages.length, 'messages');
        data.messages.forEach(msg => displayMessage(msg));
    });
    
    // Listen for new messages
    socket.on('new_message', (data) => {
        console.log('New message from', data.sender);
        displayMessage(data);
    });
    
    // Listen for user join events
    socket.on('user_joined', (data) => {
        console.log(data.username, 'joined');
        showSystemMessage(`${data.username} joined the chat 👋`);
    });
    
    // Listen for user leave events
    socket.on('user_left', (data) => {
        console.log(data.username, 'left');
        showSystemMessage(`${data.username} left the chat 👋`);
    });
    
    // Listen for errors
    socket.on('error', (data) => {
        console.error('Socket error:', data.message);
        showSystemMessage(`❌ Error: ${data.message}`);
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
        sendMessage();
    });
    
    // Auto-resize textarea
    input.addEventListener('input', () => {
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 120) + 'px';
    });
    
    // Send on Enter, new line on Shift+Enter
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

/**
 * Send a message to the server
 */
function sendMessage() {
    const input = document.getElementById('message-input');
    const text = input.value.trim();
    
    if (!text) return;
    
    if (!socket || !socket.connected) {
        showSystemMessage('❌ Not connected to server. Please refresh.');
        return;
    }
    
    // Emit message to server
    socket.emit('send_message', { text });
    
    // Clear input
    input.value = '';
    input.style.height = 'auto';
    input.focus();
}

/**
 * Display a chat message in the UI
 * Messages from current user appear on right, others on left (WhatsApp style)
 */
function displayMessage(data) {
    const messagesContainer = document.getElementById('messages-inner');
    const messageDiv = document.createElement('div');
    
    // Determine if message is from current user
    const isOwnMessage = data.sender === currentUsername;
    messageDiv.className = `message ${isOwnMessage ? 'message-right' : 'message-left'}`;
    
    // Add sentiment color border
    if (data.sentiment && data.sentiment.color) {
        if (isOwnMessage) {
            messageDiv.style.borderRight = `4px solid ${data.sentiment.color}`;
        } else {
            messageDiv.style.borderLeft = `4px solid ${data.sentiment.color}`;
        }
    }
    
    // Build message HTML
    const senderName = isOwnMessage ? 'You' : data.sender;
    const timestamp = formatTime(data.timestamp);
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <span class="message-sender">${escapeHtml(senderName)}</span>
            <span class="message-time">${timestamp}</span>
        </div>
        <div class="message-text">${escapeHtml(data.text)}</div>
        ${data.sentiment ? `
            <div class="message-sentiment">
                <span class="sentiment-emoji">${data.sentiment.emoji}</span>
                <span class="sentiment-category">${data.sentiment.category}</span>
            </div>
        ` : ''}
    `;
    
    // Add to container
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom with smooth animation
    setTimeout(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 50);
}

/**
 * Display a system message (join/leave notifications, errors, etc.)
 */
function showSystemMessage(text) {
    const messagesContainer = document.getElementById('messages-inner');
    const systemDiv = document.createElement('div');
    systemDiv.className = 'system-message';
    systemDiv.textContent = text;
    
    messagesContainer.appendChild(systemDiv);
    
    // Scroll to bottom
    setTimeout(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 50);
}

/**
 * Format timestamp to readable time
 */
function formatTime(timestamp) {
    if (!timestamp) return '';
    
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
 * Escape HTML to prevent XSS attacks
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Handle page visibility changes (optional: pause/resume connection)
 */
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        console.log('Page hidden');
    } else {
        console.log('Page visible');
        // Optionally reconnect if disconnected
        if (socket && !socket.connected) {
            socket.connect();
        }
    }
});