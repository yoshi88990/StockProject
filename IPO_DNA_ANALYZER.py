import re
import json
import os
import sys

# 文字化け対策
try:
    if sys.stdout.encoding != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
except: pass

class IPODnaAnalyzer:
    def __init__(self):
        # VC・ファンド等の警戒キーワード
        self.vc_keywords = [
            "投資事業", "ベンチャー", "ファンド", "キャピタル", "パートナーズ", 
            "インベストメント", "ホールディングス(VC的挙動)", "投資口", "組合", 
            "L.P.", "Fund"
        ]

    def clean_name(self, name):
        """余計な空白や役職を取り除き、純粋な名前にする"""
        name = re.sub(r'[\s\u3000]', '', name) # 空白除去
        name = re.sub(r'(社長|代表取締役|会長|取締役)', '', name)
        return name

    def analyze_ipo_dna(self, president_name, shareholders_list):
        """
        社長名と大株主リスト(name: percentage)から、🐶/👔/🏦 を判定する。
        """
        dna_type = "👔 雇われ社長(新興)"  # 初期値は雇われ
        vc_ratio = 0.0
        owner_ratio = 0.0
        
        cleaned_president = self.clean_name(president_name)

        # 1. 大株主と社長の照合、およびVC比率の計算
        for holder in shareholders_list:
            holder_name = holder.get("name", "")
            cleaned_holder = self.clean_name(holder_name)
            ratio = float(holder.get("ratio", 0.0))

            # 🐶 オーナー判定 (社長が株主欄にいるか、あるいは同姓の親族がいるか)
            if cleaned_president in cleaned_holder or cleaned_holder in cleaned_president:
                owner_ratio += ratio
            
            # 🏦 VC判定 (カタカナのファンド名義や組合)
            is_vc = any(kw in holder_name for kw in self.vc_keywords)
            if is_vc:
                vc_ratio += ratio

        # 2. 最終判定ロジック (厳しい基準)
        if owner_ratio >= 15.0: # 社長(または一族)が15%以上持っていればワンマンの系譜
            dna_type = "🐶 理想のワンマンIPO"
        
        # ただし、VC比率がオーナー比率を上回る、あるいは30%以上ある場合は「VC主導の売り抜け警戒」が勝る
        if vc_ratio >= 30.0 or (vc_ratio > owner_ratio and vc_ratio > 10.0):
            dna_type = "🏦 VC主導型IPO (イグジット警戒)"

        return {
            "社長名": president_name,
            "判定DNA": dna_type,
            "社長保有率": f"{owner_ratio:.1f}%",
            "VC等警戒比率": f"{vc_ratio:.1f}%"
        }

if __name__ == "__main__":
    print("=== 👑 IPO DNA ANALYZER (ワンマン/雇われ/VC判定器) ===")
    analyzer = IPODnaAnalyzer()

    # --- テスト用の泥臭い取得データ (四季報や目論見書からコピペしたと仮定) ---
    test_cases = [
        {
            "stock_name": "QPS研究所 [5595]",
            "president": "大西 俊輔",
            "shareholders": [
                {"name": "九州みらい創生投資事業有限責任組合", "ratio": 12.5},
                {"name": "大西 俊輔", "ratio": 10.2},
                {"name": "INCJ", "ratio": 8.5},
                {"name": "スパークス・新・国際優良日本株ファンド", "ratio": 6.0}
            ]
        },
        {
            "stock_name": "某・雇われ新興IT [XXXX]",
            "president": "佐藤 健太",
            "shareholders": [
                {"name": "親会社ホールディングス", "ratio": 45.0},
                {"name": "日本カストディ銀行", "ratio": 8.1},
                {"name": "佐藤 健太", "ratio": 1.2} # ほとんど持っていない
            ]
        },
        {
            "stock_name": "真のオーナースーパー株 [YYYY]",
            "president": "山田 太郎",
            "shareholders": [
                {"name": "山田 太郎", "ratio": 42.5},
                {"name": "山田 資産管理(株)", "ratio": 15.0},
                {"name": "日本マスタートラスト", "ratio": 5.0}
            ]
        }
    ]

    for data in test_cases:
        print(f"\n[ 対象銘柄 ] : {data['stock_name']}")
        result = analyzer.analyze_ipo_dna(data["president"], data["shareholders"])
        print(f"  -> {result['判定DNA']}")
        print(f"     社長保有率: {result['社長保有率']} | VC等警戒比率: {result['VC等警戒比率']}")

    print("\n---------------------------------------------------------")
    print("実運用では、ここに『師匠がコピーした四季報のテキスト』を")
    print("自動でパース（解析）して、ダッシュボードに送信する仕組みを繋ぎます。")
