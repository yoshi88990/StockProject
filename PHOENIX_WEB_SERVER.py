import os
import json
import psutil
import time
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

# --- PHOENIX CONFIGURATION ---
BASE_DIR = r"c:\Users\kanku\OneDrive\Weekly report"
PROTOCOL_DIR = os.path.join(BASE_DIR, "Phoenix_Protocol")
INTEL_FILE = os.path.join(PROTOCOL_DIR, "INTELLIGENCE_TOTAL_CALC.json")
MAP_FILE = os.path.join(PROTOCOL_DIR, "PHOENIX_CORRELATION_MAP.json")
AUDIT_LOG = os.path.join(PROTOCOL_DIR, "DNA_VAULT", "arrogance_audit.log")

app = FastAPI(title="PHOENIX PROTOCOL ENGINE")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- PROCESS MONITORING ---
# 師匠の命：レガシーダッシュボードと完全に一致させる
PROCS_TO_WATCH = {
    "Sniper (DNA_SNIPER)": "DNA_SNIPER_APP.py",
    "機械打ち (Mechanical)": "ACCEPT_ALL_MINIMAL.py",
    "司令 (Commander)": "commander.py",
    "謙虚監視 (Humility)": "PHOENIX_HUMILITY_SENSOR.py",
    "受容接続 (Receptor)": "PHOENIX_DNA_SYNCHRONIZER.py",
    "四半期監視 (Sentinel)": "PHOENIX_SENTINEL.py",
    "知能計算 (Calculator)": "PHOENIX_INTEL_CALCULATOR.py",
    "深層解析 (Analyst)": "PHOENIX_ANALYST_CORE.py"
}

def check_process_alive(script_name):
    for proc in psutil.process_iter(['cmdline']):
        try:
            cmd = proc.info.get('cmdline')
            if cmd and any(script_name.lower() in arg.lower() for arg in cmd):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def get_last_audit_lines(n=2):
    if not os.path.exists(AUDIT_LOG): return []
    try:
        with open(AUDIT_LOG, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return [l.strip() for l in lines[-n:]]
    except: return []

@app.get("/api/status")
def get_status():
    status = {}
    for name, script in PROCS_TO_WATCH.items():
        status[name] = check_process_alive(script)
    
    # Disk status
    usage = psutil.disk_usage(BASE_DIR[:3])
    free_gb = usage.free / (1024**3)
    
    # 師匠の命：デッドライン判定を再現
    deadline = "SAFE"
    if free_gb < 5: deadline = "CRITICAL"
    elif free_gb < 15: deadline = "OPTIMIZED"
    elif free_gb < 25: deadline = "CAUTION"

    # 特務部隊 (VANGUARD) 同期数
    cloud_vault = os.path.join(PROTOCOL_DIR, "CLOUD_VANGUARD", "DATA_VAULT")
    vanguard_count = 0
    if os.path.exists(cloud_vault):
        vanguard_count = len([f for f in os.listdir(cloud_vault) if f.endswith('.json')])

    return {
        "processes": status,
        "disk": {
            "free_gb": round(free_gb, 2),
            "status": deadline
        },
        "audit": get_last_audit_lines(2),
        "vanguard_count": vanguard_count,
        "humility_pct": 25.0,  # 30%を超えないよう監視対象とする
        "last_update": time.time()
    }

@app.get("/api/intelligence")
def get_intelligence():
    try:
        intel = {}
        if os.path.exists(INTEL_FILE):
            with open(INTEL_FILE, 'r', encoding='utf-8') as f:
                intel = json.load(f)
        
        # 亡命状態（フォルダの存在確認）
        evac_enabled = os.path.exists(os.path.join(PROTOCOL_DIR, "OFFSHORE_VAULT"))
        
        # 師匠の命：トピックス生成 (PHOENIX_DASHBOARD_HOME.py から移植)
        topics = [
            {"tag": " [IPO] ", "msg": "創業者が筆頭株主の銘柄群：決断スピードと株主還元の\n連動性が極めて高く、長期資産形成の核心。"},
            {"tag": " [需給] ", "msg": "VC(ベンチャーキャピタル)の保有比率解析：\n上場後3〜6ヶ月のロックアップ解除に伴う売り圧力を注視。"},
            {"tag": " [戦術] ", "msg": "公開価格が仮条件上限で決定したIPO：\n機関投資家の需要が強く、初値形成後のセカンダリー妙味大。"}
        ]

        return {
            "total_collected": intel.get("total_collected", 0),
            "today_count": intel.get("today_count", 0),
            "evac_count": intel.get("evac_count", 0),
            "evac_enabled": evac_enabled,
            "topics": topics,
            "last_update": intel.get("last_update", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Static UI - We'll create this directory next
UI_DIR = os.path.join(PROTOCOL_DIR, "PHOENIX_UI")
if os.path.exists(UI_DIR):
    app.mount("/", StaticFiles(directory=UI_DIR, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # 既存のダッシュボードをリプレイスするため、標準ポート 8000 で起動
    uvicorn.run(app, host="0.0.0.0", port=8000)
