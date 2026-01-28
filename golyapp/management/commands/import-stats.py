import json
import os
import pandas as pd
import requests
from sqlalchemy import create_engine
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Spojí historické dáta z JSONu a aktuálne dáta z API'

    def handle(self, *args, **options):
        # 1. PRIPOJENIE
        engine = create_engine("postgresql://mino:admin@localhost:5432/gba")

        # 2. CESTA K SÚBORU (Skúsime viac možností)
        possible_paths = [
            os.path.join(os.getcwd(), "statistiky.json"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "statistiky.json")
        ]
        
        json_path = next((p for p in possible_paths if os.path.exists(p)), None)

        if not json_path:
            self.stdout.write(self.style.ERROR("Súbor 'statistiky.json' sa nenašiel nikde!"))
            return

        # 3. NAČÍTANIE A ZJEDNOTENIE HISTORICKÝCH DÁT
        self.stdout.write(f"Načítavam: {json_path}")
        with open(json_path, "r", encoding="utf-8") as f:
            df_hist = pd.DataFrame(json.load(f))

        # Premenujeme stĺpce v JSON, ak sú náhodou veľkým (G -> g), aby sedeli s Django modelom
        df_hist.columns = [c.lower() for c in df_hist.columns]

        # 4. ZMAZANIE STAREJ TABUĽKY A ZÁPIS HISTÓRIE
        # Použijeme replace, aby sme mali čistý štart
        df_hist.to_sql("stats", con=engine, if_exists="replace", index=True,index_label="id")
        self.stdout.write(self.style.SUCCESS("Historické dáta nahraté."))

        # 5. SŤAHOVANIE API DÁT
        self.stdout.write("Sťahujem API...")
        try:
            current_season = requests.get("https://api-web.nhle.com/v1/season").json()[-1]
            teams = requests.get("https://api.nhle.com/stats/rest/en/team").json()["data"]
            skratky = [t['triCode'] for t in teams]
            
            all_api_stats = []
            for team in skratky:
                res = requests.get(f"https://api-web.nhle.com/v1/club-stats/{team}/{current_season}/2")
                if res.status_code == 200 and res.text.strip():
                    for i in res.json().get("skaters", []):
                        all_api_stats.append({
                            "sezona": current_season,
                            "klub": team,
                            "id_player": i["playerId"],
                            "hlava": i["headshot"],
                            "meno": f"{i['firstName']['default']} {i['lastName']['default']}",
                            "pozicia": i.get("positionCode", "N/A"),
                            "zapasy": i["gamesPlayed"],
                            "g": i["goals"],
                            "a": i["assists"],
                            "b": i["points"],
                            "plusminus": i.get("plusMinus", 0),
                            "v": i["penaltyMinutes"],
                            "gvp": i.get("powerPlayGoals", 0),
                            "gvo": i.get("shorthandedGoals", 0),
                            "v_g": i.get("gameWinningGoals", 0),
                            "gvot": i.get("overtimeGoals", 0),
                            "strely": i.get("shots", 0),
                            "perc_strel": round(i.get("shootingPctg", 0) * 100, 1),
                            "buly": round(i.get("faceoffWinPctg", 0) * 100, 1)
                        })

            if all_api_stats:
                df_api = pd.DataFrame(all_api_stats)
                # APPEND pridá novú sezónu k histórii
                df_api.to_sql("stats", con=engine, if_exists="append", index=True,index_label="id")
                self.stdout.write(self.style.SUCCESS(f"Pridaných {len(all_api_stats)} záznamov z API."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Chyba pri API: {e}"))
        path1=os.path.join(os.getcwd(),"statistiky2.json")
        self.stdout.write(f"Načítavam: {path1}")
        with open(path1,"r",encoding="utf-8") as json_file1:
            udaje=json.load(json_file1)
        df_rok=pd.DataFrame(udaje)
        df_rok.drop_duplicates(subset="id",keep="last",inplace=True,)
        df_rok.rename(columns={"id":"id_player"},inplace=True)
        df_rok["datum_nar"]=pd.to_datetime(df_rok["datum_nar"])
        df_rok["datum_nar"]=df_rok["datum_nar"].dt.strftime("%d.%m.%Y")
        df_rok.to_sql("rok", con=engine, if_exists="replace", index=True,index_label="id")
        self.stdout.write(self.style.SUCCESS("Údaje o hráčoch nahraté."))
        self.stdout.write("Sťahujem API klubov...")
        team=[]
        url2="https://api.nhle.com/stats/rest/en/team"
        response2=requests.get(url2)
        data2=response2.json()
        for i in data2["data"]:
            club={
                "kod":i['triCode'],
                "cely_nazov_klubu":i["fullName"],
                
                }
            team.append(club) 
        kluby=pd.DataFrame(team)
        kluby=kluby.drop(index=kluby[kluby["kod"].isin(["TBD","NHL"])].index)
        kluby.reset_index(drop=True,inplace=True)
        kluby.to_sql("club", con=engine, if_exists="replace", index=True,index_label="id")
        self.stdout.write(self.style.SUCCESS(f"Pridaných {len(team)} záznamov API o kluboch."))