#!/usr/bin/env python3
# 作品管理画面(admin.html)用のローカルサーバー。
# 「HAL作品管理.command」から起動される。フォルダ選択なしで保存・公開ができる。
# このMacの中だけで動き、外部には公開されない(127.0.0.1のみ)。
import base64
import json
import os
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8765

# 保存を許可する場所(安全のため assets/ 配下と works-data.js だけ)
def safe_path(rel):
    p = os.path.normpath(os.path.join(ROOT, rel))
    if not p.startswith(ROOT + os.sep):
        return None
    ok = p == os.path.join(ROOT, "assets", "works-data.js") or \
         p.startswith(os.path.join(ROOT, "assets") + os.sep)
    return p if ok else None

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, *a):  # ターミナルを静かに保つ
        pass

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/ping":
            return self._json(200, {"ok": True})
        super().do_GET()

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n) or b"{}")

            if self.path == "/api/save":  # works-data.js の保存
                p = safe_path(data["path"])
                if not p:
                    return self._json(400, {"ok": False, "error": "保存できない場所です"})
                with open(p, "w", encoding="utf-8") as f:
                    f.write(data["text"])
                return self._json(200, {"ok": True})

            if self.path == "/api/image":  # 画像(base64)の保存
                p = safe_path(data["path"])
                if not p:
                    return self._json(400, {"ok": False, "error": "保存できない場所です"})
                os.makedirs(os.path.dirname(p), exist_ok=True)
                raw = base64.b64decode(data["dataUrl"].split(",", 1)[1])
                with open(p, "wb") as f:
                    f.write(raw)
                return self._json(200, {"ok": True})

            if self.path == "/api/convert":  # TIFF/HEIC等をJPEGに変換(Mac標準のsipsを使用)
                import tempfile
                raw = base64.b64decode(data["dataUrl"].split(",", 1)[1])
                maxpx = str(int(data.get("max", 1600)))
                with tempfile.TemporaryDirectory() as td:
                    src = os.path.join(td, "in" + os.path.splitext(data.get("name", "x.tif"))[1])
                    dst = os.path.join(td, "out.jpg")
                    with open(src, "wb") as f:
                        f.write(raw)
                    r = subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82",
                                        "--resampleHeightWidthMax", maxpx, src, "--out", dst],
                                       capture_output=True, text=True)
                    if r.returncode != 0 or not os.path.exists(dst):
                        return self._json(422, {"ok": False, "error": "この形式の画像は変換できませんでした"})
                    with open(dst, "rb") as f:
                        jpg = f.read()
                return self._json(200, {"ok": True, "dataUrl": "data:image/jpeg;base64," + base64.b64encode(jpg).decode()})

            if self.path == "/api/publish":  # git add/commit/push で公開
                def run(*cmd):
                    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
                run("git", "add", "-A")
                if run("git", "diff", "--cached", "--quiet").returncode == 0:
                    return self._json(200, {"ok": True, "message": "変更はありません(すでに最新の状態です)"})
                c = run("git", "commit", "-m", "update from admin")
                if c.returncode != 0:
                    return self._json(500, {"ok": False, "error": c.stderr[-400:]})
                p = run("git", "push")
                if p.returncode != 0:
                    return self._json(500, {"ok": False, "error": "プッシュに失敗: ネット接続を確認してください\n" + p.stderr[-400:]})
                return self._json(200, {"ok": True, "message": "公開しました。反映まで1〜2分かかります"})

            self._json(404, {"ok": False, "error": "unknown endpoint"})
        except Exception as e:
            self._json(500, {"ok": False, "error": str(e)})

if __name__ == "__main__":
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        sys.exit(0)  # すでに起動中ならそのまま使う
    srv.serve_forever()
