async function fetchJSON(url) {
  const res = await fetch(url);
  return res.json();
}

function renderStatus(status) {
  const badge = document.getElementById('statusBadge');
  if (status.agent) {
    badge.textContent = '● Active';
    badge.classList.add('active');
  } else {
    badge.textContent = '● Idle — jalankan main.py dulu';
    badge.classList.remove('active');
  }

  document.getElementById('agentName').textContent = status.agent || '—';
  document.getElementById('providerName').textContent = status.provider || '—';
  document.getElementById('mainModel').textContent = status.mainModel || '—';
  document.getElementById('partnerModel').textContent = status.partnerModel || '—';

  document.getElementById('totalTurns').textContent = status.totalConversations || 0;

  const activeCats = Object.values(status.categories || {}).filter(c => c > 0).length;
  document.getElementById('totalCategories').textContent = activeCats;
  document.getElementById('outputFiles').textContent = (status.outputFiles || []).length;

  const catGrid = document.getElementById('catGrid');
  catGrid.innerHTML = '';
  for (const [cat, count] of Object.entries(status.categories || {})) {
    if (count > 0) {
      const div = document.createElement('div');
      div.className = 'cat-item';
      div.innerHTML = `<div class="name">${cat}</div><div class="count">${count}</div>`;
      catGrid.appendChild(div);
    }
  }
}

function renderConversations(turns) {
  const list = document.getElementById('convList');
  list.innerHTML = '';
  turns.slice(-30).reverse().forEach(t => {
    const div = document.createElement('div');
    div.className = 'conv-card';
    const roleClass = t.role === 'main' ? 'main' : 'partner';
    div.innerHTML = `
      <div class="meta">
        <span class="role ${roleClass}">${t.role === 'main' ? t.agent_name : 'Partner'}</span>
        <span>${t.model}</span>
        <span>Turn #${t.turn}</span>
        <span>🏷 ${t.category}</span>
      </div>
      <div class="content">${escapeHTML(t.content)}</div>
    `;
    list.appendChild(div);
  });
}

function escapeHTML(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

async function refresh() {
  const [status, turns] = await Promise.all([
    fetchJSON('/api/status'),
    fetchJSON('/api/turns')
  ]);
  renderStatus(status);
  renderConversations(turns);
}

refresh();
setInterval(refresh, 5000);
