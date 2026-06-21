const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const DATA_DIR = path.join(__dirname, '..', 'data');
const CONV_DIR = path.join(DATA_DIR, 'conversations');
const CAT_DIR = path.join(DATA_DIR, 'categories');
const OUTPUT_DIR = path.join(__dirname, '..', 'output');
const CONFIG_FILE = path.join(__dirname, '..', 'config.json');

function readJSON(filePath) {
  try {
    if (!fs.existsSync(filePath)) return null;
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch { return null; }
}

app.get('/api/status', (req, res) => {
  const config = readJSON(CONFIG_FILE);
  const convFiles = fs.existsSync(CONV_DIR) ? fs.readdirSync(CONV_DIR) : [];
  const outputFiles = fs.existsSync(OUTPUT_DIR) ? fs.readdirSync(OUTPUT_DIR) : [];

  const catCounts = {};
  if (fs.existsSync(CAT_DIR)) {
    for (const f of fs.readdirSync(CAT_DIR)) {
      const cat = path.basename(f, '.jsonl');
      const data = fs.readFileSync(path.join(CAT_DIR, f), 'utf-8').trim();
      catCounts[cat] = data ? data.split('\n').length : 0;
    }
  }

  res.json({
    agent: config?.AGENT_NAME || null,
    provider: config?.PROVIDER || null,
    mainModel: config?.MAIN_MODEL || null,
    partnerModel: config?.PARTNER_MODEL || null,
    totalConversations: convFiles.length,
    categories: catCounts,
    outputFiles: outputFiles
  });
});

app.get('/api/turns', (req, res) => {
  const turns = [];
  if (!fs.existsSync(CONV_DIR)) return res.json([]);
  const files = fs.readdirSync(CONV_DIR).sort();
  for (const f of files) {
    const data = readJSON(path.join(CONV_DIR, f));
    if (data) turns.push(data);
  }
  res.json(turns.slice(0, 200));
});

app.get('/api/category/:name', (req, res) => {
  const catPath = path.join(CAT_DIR, `${req.params.name}.jsonl`);
  if (!fs.existsSync(catPath)) return res.json([]);
  const lines = fs.readFileSync(catPath, 'utf-8').trim().split('\n').filter(Boolean);
  res.json(lines.map(l => JSON.parse(l)));
});

app.get('/api/output/:file', (req, res) => {
  const filePath = path.join(OUTPUT_DIR, req.params.file);
  if (!fs.existsSync(filePath)) return res.status(404).json({ error: 'File not found' });
  res.sendFile(filePath);
});

app.listen(PORT, () => {
  console.log(`[Corent Web] Dashboard running at http://localhost:${PORT}`);
});
