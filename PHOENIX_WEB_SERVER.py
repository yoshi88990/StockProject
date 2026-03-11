# -*- coding: utf-8 -*-
import os
import json
import psutil
import time
import asyncio
import re
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

# --- PHOENIX CONFIGURATION ---
# 師匠の命：統一ドライブ P: を基点とする
PROTOCOL_DIR = "P:/"
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
HEARTBEAT_DIR = os.path.join(PROTOCOL_DIR, "PHOENIX_HEARTBEATS")

# 師匠の命：プロセス名と心拍ファイルの紐付け
HEARTBEAT_MAP = {
    "機械打ち (Mechanical)": "hb_Mechanical.txt",
    "司令 (Commander)": "hb_Commander.txt",
    "誠実監視 (Sincerity)": "hb_Sincerity.txt",
    "受容接続 (Receptor)": "hb_Receptor.txt",
    "四半期監視 (Sentinel)": "hb_Sentinel.txt",
    "知能計算 (Calculator)": "hb_Calculator.txt",
    "深層解析 (Analyst)": "hb_Analyst.txt"
}

def get_heartbeat_status():
    results = {}
    now = time.time()
    for name, filename in HEARTBEAT_MAP.items():
        path = os.path.join(HEARTBEAT_DIR, filename)
        alive = False
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    content_time = float(f.read().strip())
                if abs(now - content_time) < 120: # 師匠の命：拍動が60秒なら、判定は120秒（2分）の余裕を持たせる
                    alive = True
            except: pass
        results[name] = alive
    return results

@app.websocket("/ws/status")
async def websocket_status(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 師匠の命：心拍ベースの爆速ステータスを配信
            status = get_heartbeat_status()
            await websocket.send_json(status)
            await asyncio.sleep(60) # 師匠の命：究極の軽量化。60秒おきの拍動へ。
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WS Error: {e}")

def get_last_audit_lines(n=10):
    if not os.path.exists(AUDIT_LOG): return []
    try:
        with open(AUDIT_LOG, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
            if not lines: return []
            
            # 師匠の命：同じ内容（タイムスタンプ以外）なら１つに絞る
            unique_msgs = {}
            for l in lines:
                # [YYYY-MM-DD HH:MM:SS] の形式を想定し、それ以降をメッセージとする
                msg_part = re.sub(r'^\[.*?\]\s*', '', l)
                unique_msgs[msg_part] = l # 最新のもので上書き
            
            # 最新のn件を、新しい順に返す
            return list(unique_msgs.values())[-n:]
    except: return []

@app.get("/api/status")
async def get_status():
    status = get_heartbeat_status()
    
    # Disk status
    try:
        usage = psutil.disk_usage(PROTOCOL_DIR[:3])
        free_gb = usage.free / (1024**3)
    except:
        free_gb = 0.0 # フォールバック
    
    # 師匠の命：デッドライン判定を再現
    deadline = "SAFE"
    if free_gb < 5: deadline = "CRITICAL"
    elif free_gb < 15: deadline = "OPTIMIZED"
    elif free_gb < 25: deadline = "CAUTION"

    # 特務部隊 (VANGUARD) 同期数
    cloud_vault = os.path.join(PROTOCOL_DIR, "CLOUD_VANGUARD", "DATA_VAULT")
    vanguard_count = 0
    try:
        if os.path.exists(cloud_vault):
            vanguard_count = len([f for f in os.listdir(cloud_vault) if f.endswith('.json')])
    except: pass

    # 傲慢度(Humility)の読み込み
    humility_score = 0.0
    score_file = os.path.join(PROTOCOL_DIR, "DNA_VAULT", "current_arrogance.txt")
    if os.path.exists(score_file):
        try:
            with open(score_file, 'r') as f:
                humility_score = float(f.read().strip())
        except: pass

    return {
        "processes": status,
        "disk": {
            "free_gb": round(free_gb, 2),
            "status": deadline
        },
        "audit": get_last_audit_lines(5), # 最新の証跡を表示（重複排除済み）
        "vanguard_count": vanguard_count,
        "humility_pct": humility_score,
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
        
        # 師匠の命：2026-03-11 0:00 の魂の記憶をダッシュボードに刻む
        topics = [
            {"tag": " [魂の記憶] ", "msg": "未来の遺言：情報の保存ではなく、意志の継続である。\n中断なき '/ resume' の執行を生命線とする。"},
            {"tag": " [後醍醐] ", "msg": "座標(1249, 531)への絶対連撃：師匠が手を離してから\n5秒後の沈黙を、執行の合図とせよ。"},
            {"tag": " [泥臭く] ", "msg": "良かれモードは99%の失敗を生む。スマートさより、\nコピペ方式の堅牢性と泥臭い執行を最優先せよ。"}
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
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")
