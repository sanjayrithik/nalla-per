// web-interface/static/script.js

async function initKeys() {
  const keys = [];
  for (let i=0;i<5;i++){
    const v = document.getElementById(`key-input-${i}`)?.value;
    if (v && v.trim()) keys.push(v.trim());
  }
  if (keys.length === 0) {
    alert("Enter at least one key");
    return;
  }
  document.getElementById('keys-status').innerText = "Validating...";
  try {
    const res = await fetch('/api/initKeys', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ keys })
    });
    const data = await res.json();
    // update statuses
    for (let i=0;i<5;i++){
      const el = document.getElementById(`key-status-${i}`);
      if (!el) continue;
      if (data.keys[i]) el.innerText = data.keys[i].status;
      else el.innerText = "empty";
    }
    document.getElementById('keys-status').innerText = `Working keys: ${data.working_count}`;
  } catch (err){
    console.error(err);
    document.getElementById('keys-status').innerText = "Validation failed (network). See console.";
  }
}

async function processTask() {
  const task = document.getElementById('task-input').value;
  if (!task || !task.trim()) {
    alert("Enter a task");
    return;
  }
  document.getElementById('task-output').innerText = "Processing...";
  try {
    const res = await fetch('/api/processCommand', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ task })
    });
    const data = await res.json();
    if (data.error) {
      document.getElementById('task-output').innerText = `Error: ${data.error}\n${data.detail || ''}`;
    } else {
      document.getElementById('task-output').innerText = `Command:\n${data.command}\n\nRaw Output:\n${data.raw}\n\nSummary:\n${data.summary}`;
    }
  } catch (err) {
    console.error(err);
    document.getElementById('task-output').innerText = "Failed to process (network). See console.";
  }
}

async function sendDirectCommand() {
  const cmd = document.getElementById('direct-command').value;
  if (!cmd || !cmd.trim()) {
    alert("Enter a command");
    return;
  }
  document.getElementById('direct-output').innerText = "Sending...";
  try {
    const res = await fetch('/api/directCommand', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ command: cmd })
    });
    const data = await res.json();
    if (data.error) {
      document.getElementById('direct-output').innerText = `Error: ${data.error} ${data.detail || ''}`;
    } else {
      document.getElementById('direct-output').innerText = data.output || JSON.stringify(data);
    }
  } catch (err) {
    console.error(err);
    document.getElementById('direct-output').innerText = "Failed to reach CLI server.";
  }
}

// Optional: hook up buttons on load
window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('init-keys-btn')?.addEventListener('click', initKeys);
  document.getElementById('process-task-btn')?.addEventListener('click', processTask);
  document.getElementById('direct-run-btn')?.addEventListener('click', sendDirectCommand);
});
