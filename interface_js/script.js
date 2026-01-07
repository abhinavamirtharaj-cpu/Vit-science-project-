// Chat panel with contacts, sentiment analysis, and server save
document.addEventListener('DOMContentLoaded', () => {
  console.log('Script loaded successfully');
  const btn = document.getElementById('get-started');
  const btnSm = document.getElementById('get-started-sm');
  const chatPanel = document.getElementById('chat-panel');
  const closeBtn = document.getElementById('close-chat');
  const messagesContainer = document.getElementById('messages-inner');
  const chatForm = document.getElementById('chat-form');
  const input = document.getElementById('message-input');
  const contactsListEl = document.getElementById('contacts-list');
  const chatWithEl = document.getElementById('chat-with');
  
  // Sentiment analysis state
  let isAnalyzing = false;

  // Sample contacts (now include avatar images)
  const contacts = [
    {id: 'support', name: 'Support', status: 'Online', avatar: 'assets/avatar_support.svg'},
    {id: 'alice', name: 'Alice', status: 'Online', avatar: 'assets/avatar_alice.svg'},
    {id: 'bob', name: 'Bob', status: 'Away', avatar: 'assets/avatar_bob.svg'}
  ];

  let currentContact = contacts[0];

  // Storage helpers (per-contact)
  function storageKeyFor(contactId){ return `chat_history_v1_${contactId}` }

  // Time formatting (clean inline format)
  function nowTime(){
    const d = new Date();
    const date = d.toLocaleDateString();
    const time = d.toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
    return {time, date, iso: d.toISOString()};
  }

  function saveHistory(history, contactId){
    try{ localStorage.setItem(storageKeyFor(contactId), JSON.stringify(history)); }catch(e){console.warn('Could not save chat history', e)}
  }

  function loadHistory(contactId){
    messagesContainer && (messagesContainer.innerHTML = '');
    try{
      const raw = localStorage.getItem(storageKeyFor(contactId));
      const history = raw ? JSON.parse(raw) : [];
      if(Array.isArray(history) && history.length>0){
        history.forEach(renderMessage);
      } else {
        // seed with a welcome message if no history
        const seed = {text: `Welcome to ${contactId} conversation!`, time: nowTime().time, date: nowTime().date, dir: 'received'};
        renderMessage(seed);
      }
      scrollBottom();
      return history;
    }catch(err){
      console.warn('Could not load history', err);
      return [];
    }
  }

  function renderMessage(msg){
    if(!messagesContainer) return;
    // message row contains avatar + bubble to allow left/right alignment
    const row = document.createElement('div');
    row.className = 'message-row ' + (msg.dir === 'sent' ? 'sent' : 'received');

    const avatarImg = document.createElement('img');
    avatarImg.className = 'avatar-img';
    // choose avatar: received => current contact avatar, sent => user avatar
    avatarImg.src = msg.dir === 'sent' ? 'assets/avatar_me.svg' : (currentContact.avatar || 'assets/avatar_support.svg');
    avatarImg.alt = '';

    const bubble = document.createElement('div');
    // Add sentiment-based styling if available
    bubble.className = 'msg ' + (msg.dir === 'sent' ? 'sent' : 'received');
    if(msg.sentiment && msg.sentiment.color) {
      bubble.setAttribute('data-sentiment-color', msg.sentiment.color);
      bubble.setAttribute('data-sentiment-category', msg.sentiment.category);
      bubble.setAttribute('data-sentiment-description', msg.sentiment.description);
      bubble.setAttribute('data-sentiment-emoji', msg.sentiment.emoji);
    }
    
    const timeHtml = `<span class="time">${escapeHtml(msg.time)}</span>`;
    const meta = msg.date ? `<span class="meta">${escapeHtml(msg.date)}</span>` : '';
    
    let sentimentBadge = '';
    if(msg.sentiment) {
      sentimentBadge = `<span class="sentiment-badge" title="${escapeHtml(msg.sentiment.description)}">${msg.sentiment.emoji} ${escapeHtml(msg.sentiment.category)}</span>`;
    }
    
    bubble.innerHTML = `<div class="text">${escapeHtml(msg.text)}</div>${sentimentBadge}${timeHtml}${meta}`;

    // assemble row: avatar + bubble
    if(msg.dir === 'sent'){
      row.appendChild(bubble);
      row.appendChild(avatarImg);
    } else {
      row.appendChild(avatarImg);
      row.appendChild(bubble);
    }

    messagesContainer.appendChild(row);
  }

  function getLastSentiment(contactId) {
    try {
      const raw = localStorage.getItem(storageKeyFor(contactId));
      const history = raw ? JSON.parse(raw) : [];
      // Look for the last 'sent' message that has sentiment data
      for (let i = history.length - 1; i >= 0; i--) {
        if (history[i].dir === 'sent' && history[i].sentiment) {
          return history[i].sentiment.category;
        }
      }
    } catch (e) { console.warn('Could not read last sentiment', e); }
    return null;
  }

  function escapeHtml(str){
    return String(str).replace(/[&<>\\\"']/g, (s) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'\''}[s]));
  }

  function scrollBottom(){
    const scrollEl = document.getElementById('messages');
    if(scrollEl) scrollEl.scrollTop = scrollEl.scrollHeight;
  }

  function addToHistory(text, dir='sent', contactId){
    contactId = contactId || currentContact.id;
    let history = [];
    try{ const raw = localStorage.getItem(storageKeyFor(contactId)); history = raw ? JSON.parse(raw) : [] }catch(e){ history = [] }
    const ts = nowTime();
    const msg = {text, time: ts.time, date: ts.date, iso: ts.iso, dir};
    history.push(msg);
    saveHistory(history, contactId);
    renderMessage(msg);
    scrollBottom();

    // If message was sent by user, trigger an automated reply for that contact
    if(dir === 'sent'){
      scheduleAutoReply(contactId, text);
    }

    return msg;
  }

  // Sentiment Analysis Integration
  async function analyzeSentimentAndSend(text) {
    if(!text.trim() || isAnalyzing) return false;
    
    isAnalyzing = true;
    const submitBtn = chatForm.querySelector('button[type="submit"]');
    if(submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Analyzing...';
    }
    
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          text: text,
          contact_id: currentContact.id,
          contact_name: currentContact.name
        })
      });
      
      if(!response.ok) {
        console.error('Sentiment analysis failed:', response.status);
        // Fallback: add without sentiment if API fails
        addToHistory(text, 'sent', currentContact.id);
        return true;
      }
      
      const result = await response.json();
      
      if(result.success) {
        // Add message with sentiment data
        let history = [];
        try{ const raw = localStorage.getItem(storageKeyFor(currentContact.id)); history = raw ? JSON.parse(raw) : [] }catch(e){ history = [] }
        
        const ts = nowTime();
        const msg = {
          text: text,
          time: ts.time,
          date: ts.date,
          iso: ts.iso,
          dir: 'sent',
          sentiment: {
            emoji: result.sentiment.emoji,
            category: result.sentiment.category,
            description: result.sentiment.description,
            color: result.sentiment.color,
            polarity: result.sentiment.polarity
          }
        };
        
        history.push(msg);
        saveHistory(history, currentContact.id);
        renderMessage(msg);
        scrollBottom();
        
        // Schedule auto reply
        scheduleAutoReply(currentContact.id, text);
        
        return true;
      } else {
        console.error('API error:', result.error);
        addToHistory(text, 'sent', currentContact.id);
        return true;
      }
    } catch(err) {
      console.error('Fetch error:', err);
      // Fallback: add without sentiment
      addToHistory(text, 'sent', currentContact.id);
      return true;
    } finally {
      isAnalyzing = false;
      if(submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send';
      }
    }
  }

  // Contacts rendering and selection

  // Automated replies: map of contactId -> last scheduled timeout to avoid duplicate replies
  const _autoReplyTimers = {};

  function cannedReplyFor(msgText){
    const replies = [
      "Got it! I'll check and get back to you.",
      "Thanks for the update — noted.",
      "Interesting, tell me more.",
      "On it. I'll follow up shortly.",
      "Thanks — message received!"
    ];
    // Simple heuristic: if user asks a question, reply acknowledging
    if(/[?]$/.test(msgText.trim())) return "Good question — let me look into that.";
    return replies[Math.floor(Math.random()*replies.length)];
  }

  function scheduleAutoReply(contactId, userMsg){
    // avoid scheduling multiple replies rapidly for same contact
    if(_autoReplyTimers[contactId]){
      clearTimeout(_autoReplyTimers[contactId]);
    }
    _autoReplyTimers[contactId] = setTimeout(()=>{
      const replyText = cannedReplyFor(userMsg);
      // add to history as 'received'
      const ts = nowTime();
      const reply = {text: replyText, time: ts.time, date: ts.date, iso: ts.iso, dir: 'received'};
      // load, append, save
      let history = [];
      try{ const raw = localStorage.getItem(storageKeyFor(contactId)); history = raw ? JSON.parse(raw) : [] }catch(e){ history = [] }
      history.push(reply);
      saveHistory(history, contactId);
      // if the reply is for the current visible contact, render it now
      if(currentContact && currentContact.id === contactId){
        renderMessage(reply);
        scrollBottom();
      }
      delete _autoReplyTimers[contactId];
    }, 900 + Math.floor(Math.random()*900)); // 900-1800ms delay
  }

  function renderContacts(){
    contactsListEl.innerHTML = '';
    contacts.forEach(c=>{
      const li = document.createElement('li');
      li.className = 'contact-item' + (c.id === currentContact.id ? ' active' : '');
      const avatar = `<img class="c-avatar" src="${escapeHtml(c.avatar||'assets/avatar_support.svg')}" alt="${escapeHtml(c.name)}" />`;
      li.innerHTML = `${avatar}<div class="c-name">${escapeHtml(c.name)}</div><div class="c-status">${escapeHtml(c.status)}</div>`;
      li.addEventListener('click', ()=> selectContact(c.id));
      contactsListEl.appendChild(li);
    });
  }

  function selectContact(contactId){
    const c = contacts.find(x=>x.id === contactId);
    if(!c) return;
    currentContact = c;
    chatWithEl.textContent = c.name;
    // set header avatar
    const headerAvatar = document.querySelector('.chat-title .avatar');
    if(headerAvatar) headerAvatar.src = c.avatar || 'assets/avatar_support.svg';
    // mark active
    Array.from(contactsListEl.children).forEach(li=> li.classList.toggle('active', li.querySelector('.c-name').textContent === c.name));
    loadHistory(contactId);
  }

  // Live-chat and server-facing code removed. Use `storage.py` for CSV persistence.

  // Open / close chat
  function openChat(){
    if(!chatPanel) return;
    chatPanel.classList.remove('hidden');
    chatPanel.setAttribute('aria-hidden', 'false');
    renderContacts();
    selectContact(currentContact.id);
    setTimeout(()=> input && input.focus(), 150);
  }
  function closeChat(){ if(!chatPanel) return; chatPanel.classList.add('hidden'); chatPanel.setAttribute('aria-hidden','true'); }

  if(btn) btn.addEventListener('click', (e)=>{e.preventDefault(); openChat();});
  if(btnSm) btnSm.addEventListener('click', (e)=>{e.preventDefault(); openChat();});
  if(closeBtn) closeBtn.addEventListener('click', closeChat);

  document.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') closeChat(); });
  chatPanel && chatPanel.addEventListener('click', (e)=>{ if(e.target === chatPanel) closeChat(); });

  // Handle send: analyze sentiment and store
  chatForm && chatForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    const txt = input.value.trim();
    if(!txt) return;
    input.value = '';
    analyzeSentimentAndSend(txt);
  });

  // Enter to send
  input && input.addEventListener('keydown', (e)=>{ if(e.key === 'Enter' && !e.shiftKey){ e.preventDefault(); chatForm.dispatchEvent(new Event('submit', {cancelable:true})); } });

  // Typing animation for chat bar
  const typingTextEl = document.getElementById('text');
  if(typingTextEl){
    const message = "We Welcome You";
    const speed = 120;
    let index = 0;

    function typeText() {
      if (index < message.length) {
        typingTextEl.textContent += message.charAt(index);
        index++;
        setTimeout(typeText, speed);
      }
    }
    typeText();
  }

  // initial render
  renderContacts();
});