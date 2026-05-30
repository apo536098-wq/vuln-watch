import requests
from rich.console import Console
from rich.table import Table
import time
import json
import os

console = Console()
SEEN_DB_FILE = "seen_items.json"

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def load_seen_items():
    if os.path.exists(SEEN_DB_FILE):
        with open(SEEN_DB_FILE, "r") as f:
            return json.load(f)
    return {"cves": [], "repos": []}

def save_seen_items(seen_data):
    with open(SEEN_DB_FILE, "w") as f:
        json.dump(seen_data, f, indent=4)

def send_telegram_message(token, chat_id, message):
    if not token or not chat_id or "BURAYA" in token:
        return 
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        console.print(f"[bold red]Telegram hatası: {e}[/bold red]")

def check_github(keyword, seen_repos, config):
    url = f"https://api.github.com/search/repositories?q={keyword}+created:>2026-01-01&sort=updated&order=desc"
    headers = {"Accept": "application/vnd.github.v3+json"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            items = response.json().get("items", [])[:3]
            new_items = []
            for item in items:
                repo_id = str(item["id"])
                if repo_id not in seen_repos:
                    seen_repos.append(repo_id)
                    new_items.append(item)
                    msg = f"🔔 *YENİ GITHUB PoC!*\n\n📂 *Repo:* {item['full_name']}\n📝 *Açıklama:* {item['description']}\n🔗 {item['html_url']}"
                    send_telegram_message(config["telegram_token"], config["telegram_chat_id"], msg)
            return new_items, seen_repos
    except Exception as e:
        console.print(f"[bold red]GitHub Hatası ({keyword}): {e}[/bold red]")
    return [], seen_repos

def check_nvd_cve(keyword, seen_cves, config):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}&resultsPerPage=3"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            vulnerabilities = response.json().get("vulnerabilities", [])
            new_cves = []
            for vuln in vulnerabilities:
                cve_data = vuln.get("cve", {})
                cve_id = cve_data.get("id")
                if cve_id and cve_id not in seen_cves:
                    seen_cves.append(cve_id)
                    descriptions = cve_data.get("descriptions", [])
                    desc_text = descriptions[0].get("value", "Açıklama yok.") if descriptions else "Açıklama yok."
                    new_cves.append({"id": cve_id, "desc": desc_text[:100]})
                    msg = f"⚠️ *YENİ CVE YAYINLANDI!*\n\n🆔 *ID:* {cve_id}\n🔍 *Kelime:* {keyword}\n📝 *Özet:* {desc_text[:150]}...\n🔗 https://nvd.nist.gov/vuln/detail/{cve_id}"
                    send_telegram_message(config["telegram_token"], config["telegram_chat_id"], msg)
            return new_cves, seen_cves
    except Exception as e:
        console.print(f"[bold red]NVD Hatası ({keyword}): {e}[/bold red]")
    return [], seen_cves

def main():
    console.print("[bold magenta]🚀 Vuln-Watch Başlatıldı...[/bold magenta]\n")
    while True:
        try:
            config = load_config()
            seen_data = load_seen_items()
            
            table = Table(title="📊 Siber İstihbarat Taraması", title_style="bold green")
            table.add_column("Anahtar Kelime", style="cyan")
            table.add_column("Yeni GitHub PoC", style="bold yellow", justify="center")
            table.add_column("Yeni NVD CVE", style="bold red", justify="center")
            
            for keyword in config["keywords"]:
                new_repos, seen_data["repos"] = check_github(keyword, seen_data["repos"], config)
                new_cves, seen_data["cves"] = check_nvd_cve(keyword, seen_data["cves"], config)
                table.add_row(keyword, str(len(new_repos)), str(len(new_cves)))
                time.sleep(1)
            
            console.print(table)
            save_seen_items(seen_data)
            
            console.print(f"\n[dim]💤 {config['check_interval_minutes']} dakika bekleniyor...[/dim]\n")
            time.sleep(config["check_interval_minutes"] * 60)
        except KeyboardInterrupt:
            console.print("\n[bold red]Program kapatıldı.[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]Hata: {e}[/bold red]")
            time.sleep(10)

if __name__ == "__main__":
    main()
