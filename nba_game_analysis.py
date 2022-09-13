import csv as csv
import re as re

def upload_param(players, regexp, actions, abr):
    lists = []

    for play in actions:
        present_action = play[7]
        try:
            param_regexp = re.compile(regexp)
            param = param_regexp.search(present_action)[1]
            lists.append(param)
        except:
            pass

    for param in lists:
        try:
            for player in players["home_team"]["players_data"]:
                if player["player_name"] == param:
                    player[abr] += 1
            for player in players["away_team"]["players_data"]:
                if player["player_name"] == param:
                    player[abr] += 1
        except:
            pass

def load_file(filename):
    result = []
    with open (filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')
        fieldes = next(csvreader)

        for row in csvreader:
            result.append(row)
    return result




def format(play_by_play_moves):
    result = {"home_team": {"name": "", "players_data": []}, "away_team": {"name": "", "players_data": []}}

    for play in play_by_play_moves:
        result["away_team"]["name"] = play[3]
        result["home_team"]["name"] = play[4]
        break

    for play in play_by_play_moves:
        home_team = play[4]
        relevant_team = play[2]
        present_action = play[7]

        try:
            player_name_regexp = re.compile(r"^([\S]\. [A-Z]\S{1,}\b|[A-Z]\. [A-Z]\w{1,}\-\w{1,})")
            player_name = player_name_regexp.search(present_action)[1]
            player = {"player_name": player_name, "FG": 0, "FGM": 0, "FGA": 0, "FG%": 0.0, "3P": 0, "3PM": 0, "3PA": 0, "3P%": 0.0, "2P": 0, "2PM": 0, "FT": 0, "FTM": 0, "FTA": 0, "FT%": 0.0, "ORB": 0, "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0, "MCPFT": 0, "MICPFT": 0}

            if(relevant_team == home_team):
                if not player in result["home_team"]["players_data"]:
                    result["home_team"]["players_data"].append(player)
            else:
                if not player in result["away_team"]["players_data"]:
                    result["away_team"]["players_data"].append(player)
        except:
            pass

    return result
def analyse_nba_game():
    play_by_play_moves = load_file("nba_game_warriors_thunder_20181016.txt")
    players_data = format(play_by_play_moves)
    upload_param(players_data, "^([\S]\. [\S]*) makes 3-pt", play_by_play_moves, "3P")
    upload_param(players_data, "^([\S]\. [\S]*) misses 3-pt", play_by_play_moves, "3PM")
    upload_param(players_data, "^([\S]\. [\S]*) makes 2-pt", play_by_play_moves, "2P")
    upload_param(players_data, "^([\S]\. [\S]*) misses 2-pt", play_by_play_moves, "2PM")
    upload_param(players_data, "Offensive rebound by ([A-Z]\. [A-Z]\w{1,}|[A-Z]\. [A-Z]\w{1,}\-\w{1,})", play_by_play_moves, "ORB")
    upload_param(players_data, "Defensive rebound by ([A-Z]\. [A-Z]\w{1,}|[A-Z]\. [A-Z]\w{1,}\-\w{1,})", play_by_play_moves, "DRB")
    upload_param(players_data, "block by ([A-Z]\. [A-Z]\w{1,}|[A-Z]\. [A-Z]\w{1,}\-\w{1,})", play_by_play_moves, "BLK")
    upload_param(players_data, "steal by ([A-Z]\. [A-Z]\w{1,}|[A-Z]\. [A-Z]\w{1,}\-\w{1,})", play_by_play_moves, "STL")
    upload_param(players_data, "Turnover by ([A-Z]\. [A-Z]\w{1,}|[A-Z]\. [A-Z]\w{1,}\-\w{1,})", play_by_play_moves, "TOV")
    upload_param(players_data, "assist by ([A-Z]\. [A-Z]\w{1,}|[A-Z]\. [A-Z]\w{1,}\-\w{1,})", play_by_play_moves, "AST")
    upload_param(players_data, "Personal foul by ([A-Z]\. [A-Z]\w{1,}|[A-Z]\. [A-Z]\w{1,}\-\w{1,})", play_by_play_moves, "PF")
    upload_param(players_data, "([A-Z]\. [A-Z]\w{1,}|[A-Z]\. [A-Z]\w{1,}\-\w{1,}) makes free throw", play_by_play_moves, "FT")
    upload_param(players_data, "([A-Z]\. [A-Z]\w{1,}|[A-Z]\. [A-Z]\w{1,}\-\w{1,}) misses free throw", play_by_play_moves, "FTM")
    upload_param(players_data, "([A-Z]\. [A-Z]\w{1,}|[A-Z]\. [A-Z]\w{1,}\-\w{1,}) makes clear path free throw", play_by_play_moves, "MCPFT")
    upload_param(players_data, "([A-Z]\. [A-Z]\w{1,}|[A-Z]\. [A-Z]\w{1,}\-\w{1,}) misses clear path free throw", play_by_play_moves, "MICPFT")
    for team in players_data.items():
        for player in team[1]["players_data"]:
            player["FG"] = player["3P"] + player["2P"]
            player["FGA"] = player["3P"] + player["2P"] + player["3PM"] + player["2PM"]
            player['3PA'] = player['3P'] + player['3PM']
            player["FT"] = player["FT"] * 1 + player["MCPFT"] + player["MICPFT"]
            player["FTA"] = player["FT"] + player["FTM"]

            player["PTS"] = player["3P"] * 3 + player["2P"] * 2 + player["FT"]

            player["TRB"] = player["DRB"] + player["ORB"]

            try:
                player["FG%"] = round(player["FG"] / player["FGA"], 3)
            except:
               pass

            try:
                player['3P%'] = round(player['3P'] / player['3PA'], 3)
            except:
                pass

            try:
                player["FT%"] = round(player["FT"] / player["FTA"], 3)
            except:
                pass

    for team in players_data.items():
        for player in team[1]["players_data"]:
            del player["FTM"]
            del player["2P"]
            del player["2PM"]
            del player["3PM"]
            del player["MCPFT"]
            del player["MICPFT"]

    return players_data
def print_table():
    players_data = analyse_nba_game()
    for team in players_data.items():
        fg, fga, fgp, p3, p3a, p3p, ft, fta, ftp, orb, drb, trb, ast, stl, blk, tov, pf, pts = 0, 0, 0.0, 0, 0, 0.0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        print(f'{"Players name":<20} | {"FG":<5} | {"FGA":<5} | {"FG%":<6} | {"3P":<5} | {"3PA":<5} | {"3P%":<6} | {"FT":<5} | {"FTA":<5} | {"FT%":<6} | {"ORB":<5} | {"DRB":<5} | {"TRB":<5} | {"AST":<5} | {"STL":<5} | {"BLK":<5} | {"TOV":<5} | {"PF":<5} | {"PTS":<5} ')
        for player in team[1]["players_data"]:
            print(f'{player["player_name"]:<20} | {player["FG"]:<5} | {player["FGA"]:<5} | {player["FG%"]:<6} | {player["3P"]:<5} | {player["3PA"]:<5} | {player["3P%"]:<6} | {player["FT"]:<5} | {player["FTA"]:<5} | {player["FT%"]:<6} | {player["ORB"]:<5} | {player["DRB"]:<5} | {player["TRB"]:<5} | {player["AST"]:<5} | {player["STL"]:<5} | {player["BLK"]:<5} | {player["TOV"]:<5} | {player["PF"]:<5} | {player["PTS"]:<5} ')
            fg += player["FG"]
            fga += player["FGA"]
            p3 += player["3P"]
            p3a += player["3PA"]
            ft += player["FT"]
            fta += player["FTA"]
            orb += player["ORB"]
            drb += player["DRB"]
            ast += player["AST"]
            stl += player["STL"]
            blk += player["BLK"]
            tov += player["TOV"]
            pf += player["PF"]
            pts += player["PTS"]

        fgp = round(fg / fga, 3) if fga > 0 else 0
        p3p = round(p3 / p3a, 3) if fga > 0 else 0
        ftp = round(ft / fta, 3) if fga > 0 else 0
        trb = orb + drb

        print(f'{"Team Totals":<20} | {fg:<5} | {fga:<5} | {fgp:<6} | {p3:<5} | {p3a:<5} | {p3p:<6} | {ft:<5} | {fta:<5} | {ftp:<6} | {orb:<5} | {drb:<5} | {trb:<5} | {ast:<5} | {stl:<5} | {blk:<5} | {tov:<5} | {pf:<5} | {pts:<5} ')
        print("\n")


print_table()
