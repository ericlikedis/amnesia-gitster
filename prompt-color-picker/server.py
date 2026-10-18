#!/usr/bin/env python3
"""Tiny local server: serves a color picker page and saves the chosen color."""
import http.server, json, os, re, secrets, shutil, subprocess, threading

COLOR_FILE = os.path.expanduser("~/.config/amnesia-color")
TOKEN = secrets.token_urlsafe(16)

def current_color():
    try:
        c = open(COLOR_FILE).read().strip()
        if re.fullmatch(r"#[0-9a-fA-F]{6}", c):
            return c
    except OSError:
        pass
    return "#00ff00"

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Prompt Color Picker</title>
<style>
  body { font-family: -apple-system, sans-serif; background:#1e1e1e; color:#ddd;
         display:flex; flex-direction:column; align-items:center; margin-top:10vh; gap:20px; }
  .prompt { font-family: Menlo, monospace; font-size:28px; background:#000; padding:20px 30px; border-radius:8px; }
  .row { display:flex; gap:12px; align-items:center; }
  input[type=color] { width:90px; height:60px; border:none; background:none; cursor:pointer; }
  input[type=text] { font-family:Menlo,monospace; font-size:18px; width:110px; padding:6px; }
  button { font-size:16px; padding:10px 24px; cursor:pointer; }
  #msg { height:1em; color:#6c6; }
</style></head><body>
<h2>Choose your prompt color</h2>
<div class="prompt"><span id="p" style="font-weight:bold">amnesia</span> <span style="color:#0f0;font-weight:bold">&lambda;</span> ~</div>
<div class="row">
  <input type="color" id="c" value="__COLOR__">
  <input type="text" id="h" value="__COLOR__" maxlength="7">
  <button id="save">Save</button>
</div>
<div id="msg"></div>
<script>
const c = document.getElementById('c'), h = document.getElementById('h'), p = document.getElementById('p');
function set(v){ p.style.color = v; }
set(c.value);
c.oninput = () => { h.value = c.value; set(c.value); };
h.oninput = () => { if (/^#[0-9a-fA-F]{6}$/.test(h.value)) { c.value = h.value; set(h.value); } };
document.getElementById('save').onclick = async () => {
  const r = await fetch('/save', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({color: c.value, token: '__TOKEN__'})});
  document.getElementById('msg').textContent = r.ok ? 'Saved! Your next prompt will use it. You can close this tab.' : 'Save failed';
};
</script></body></html>"""

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path != "/":
            self.send_error(404); return
        body = PAGE.replace("__COLOR__", current_color()).replace("__TOKEN__", TOKEN).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_POST(self):
        if self.path != "/save":
            self.send_error(404); return
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            ok = data.get("token") == TOKEN and re.fullmatch(r"#[0-9a-fA-F]{6}", data.get("color", ""))
        except Exception:
            ok = False
        if not ok:
            self.send_error(400); return
        with open(COLOR_FILE, "w") as f:
            f.write(data["color"] + "\n")
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
        print("Saved", data["color"])

srv = http.server.HTTPServer(("127.0.0.1", 0), H)
url = f"http://127.0.0.1:{srv.server_address[1]}/"
print(f"Color picker at {url}  (Ctrl-C to quit)")
opener = shutil.which("open") or shutil.which("xdg-open")
if opener:
    subprocess.Popen([opener, url])
try:
    srv.serve_forever()
except KeyboardInterrupt:
    pass
