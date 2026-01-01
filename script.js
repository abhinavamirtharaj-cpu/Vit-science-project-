// Chat panel with contacts, exports, and server save
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('get-started');
  const btnSm = document.getElementById('get-started-sm');
  const chatPanel = document.getElementById('chat-panel');
  const closeBtn = document.getElementById('close-chat');
  const messagesContainer = document.getElementById('messages-inner');
  const chatForm = document.getElementById('chat-form');
  const input = document.getElementById('message-input');
  const contactsListEl = document.getElementById('contacts-list');
  const chatWithEl = document.getElementById('chat-with');

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
    bubble.className = 'msg ' + (msg.dir === 'sent' ? 'sent' : 'received');
    const timeHtml = `<span class="time">${escapeHtml(msg.time)}</span>`;
    const meta = msg.date ? `<span class="meta">${escapeHtml(msg.date)}</span>` : '';
    bubble.innerHTML = `<div class="text">${escapeHtml(msg.text)}</div>${timeHtml}${meta}`;

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

  // Handle send: store locally
  chatForm && chatForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    const txt = input.value.trim();
    if(!txt) return;
    addToHistory(txt, 'sent', currentContact.id);
    input.value = '';
  });

  // Enter to send
  input && input.addEventListener('keydown', (e)=>{ if(e.key === 'Enter' && !e.shiftKey){ e.preventDefault(); chatForm.dispatchEvent(new Event('submit', {cancelable:true})); } });

  // initial render
  renderContacts();
});