import json
import os

class AssetManager:
    def __init__(self, db_path="assets_db.json"):
        self.db_path = db_path
        self.data = self._load_db()

    def _load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"Database saved to {self.db_path}")

    def get_summary(self):
        total = sum(asset["balance"] for asset in self.data["assets"])
        print(f"--- Asset Summary ---")
        print(f"Total Assets: {total:,} JPY")
        for asset in self.data["assets"]:
            perc = (asset["balance"] / total * 100) if total > 0 else 0
            print(f"- {asset['name']}: {asset['balance']:,} JPY ({perc:.1f}% / Target: {asset['target_ratio']}%)")

def main():
    manager = AssetManager()
    manager.get_summary()

if __name__ == "__main__":
    main()
