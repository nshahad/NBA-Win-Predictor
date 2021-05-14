import pandas as pd
import Teams

data_games = pd.read_csv('games.csv')
data_players = pd.read_csv('players.csv')
data_games_details = pd.read_csv('games_details.csv')
data_teams = pd.read_csv('teams.csv')
data_ranking = pd.read_csv('ranking.csv')




def head_to_head(p1, p2):
    player1 = p1
    player2 = p2


    # Outputs a list of the Team ID's of a given player. (index 0 is 2019)

    player1_teams = data_players[data_players.PLAYER_NAME == player1]
    player2_teams = data_players[data_players.PLAYER_NAME == player2]

    teams1 = []
    teams2 = []


    range1 = player1_teams.iloc[0]["SEASON"] - player1_teams.iloc[len(player1_teams) - 1]["SEASON"] + 1
    for x in range(range1):
        season = 2019 - x
        if len(player1_teams[player1_teams.SEASON == season]) > 0:
            teams1.append(player1_teams[player1_teams.SEASON == season].iloc[0]["TEAM_ID"])
        else:
            teams1.append(1610612745) 
        
        
    range2 = player2_teams.iloc[0]["SEASON"] - player2_teams.iloc[len(player2_teams) - 1]["SEASON"] + 1
    for x in range(range2):
        season = 2019 - x
        if len(player2_teams[player2_teams.SEASON == season]) > 0:
            teams2.append(player2_teams[player2_teams.SEASON == season].iloc[0]["TEAM_ID"])
        else:
            teams2.append(1610612745) 

    # Outputs a list of the games of a given player. 

    player1_games = data_games_details[data_games_details.PLAYER_NAME == player1]
    player1_games = player1_games[player1_games.MIN.notnull()]
    player2_games = data_games_details[data_games_details.PLAYER_NAME == player2]
    player2_games = player2_games[player2_games.MIN.notnull()]


    # Combine home/away mismatch into one loop

    # Big Work for Big Data (but fast..)

    years = min(len(teams1), len(teams2))
    player1_wins = 0
    player2_wins = 0
    for x in range(years): 
        year = 2019 - x
        Home_team_id = teams1[x]
        Away_team_id = teams2[x]
        home_team = data_games[data_games.HOME_TEAM_ID == Home_team_id]
        games = home_team[home_team.VISITOR_TEAM_ID == Away_team_id]
        refined_games = games[games.SEASON == year]
        
        for y in range(len(refined_games)):
            players_game_id = refined_games.iloc[y]["GAME_ID"]
            player1_played = False
            player2_played = False
            
            player1_games_refined = player1_games[player1_games.GAME_ID == players_game_id]
            if len(player1_games_refined) == 1:
                player1_played = True
            
            player2_games_refined = player2_games[player2_games.GAME_ID == players_game_id]
            if len(player2_games_refined) == 1:
                player2_played = True

            if player1_played and player2_played:
                if refined_games.iloc[y]["HOME_TEAM_WINS"] == 1:
                    player1_wins += 1
                else:
                    player2_wins += 1
     

        home_team = data_games[data_games.HOME_TEAM_ID == Away_team_id]
        games = home_team[home_team.VISITOR_TEAM_ID == Home_team_id]
        refined_games = games[games.SEASON == year]
        for y in range(len(refined_games)):
            players_game_id = refined_games.iloc[y]["GAME_ID"]
            player1_played = False
            player2_played = False
            
            player1_games_refined = player1_games[player1_games.GAME_ID == players_game_id]
            if len(player1_games_refined) == 1:
                player1_played = True
            
            player2_games_refined = player2_games[player2_games.GAME_ID == players_game_id]
            if len(player2_games_refined) == 1:
                player2_played = True

            if player1_played and player2_played:
                if refined_games.iloc[y]["HOME_TEAM_WINS"] == 1:
                    player2_wins += 1
                else:
                    player1_wins += 1
    
    return [player1_wins, player2_wins]


##team1name = "Los Angeles Lakers"
##team2name = "Los Angeles Clippers"
team1name = input("First Team: ")
team2name = input("Second Team: ")
new_team1 = Teams.Teams[team1name]
new_team2 = Teams.Teams[team2name]

team1_wins = 0
team1_losses = 0
team1_ratio = 0
for x in range(len(new_team1)):
    first_team_player = new_team1[x]
    player1_wins = 0
    player1_losses = 0
    for y in range(len(new_team2)):
        print(new_team1[x])
        print(new_team2[y])
        second_team_player = new_team2[y]
        score = head_to_head(first_team_player, second_team_player)
        
        print(score[0])
        print(score[1])

        player1_wins += score[0]
        player1_losses += score[1]
        
        team1_ratio += score[0] / (score[0] + score[1])
    team1_wins += player1_wins
    team1_losses += player1_losses

team1_ratio = (team1_ratio / 25) * 100
print(team1name + " Wins: " + str(team1_wins))
print(team2name + " Wins: " + str(team1_losses))
team1_win_ratio = (team1_wins / (team1_wins + team1_losses)) * 100
print("Prediction 1: " + team1name + " Win Chance: " + str(team1_win_ratio))
print("Prediction 2: " + team1name + " Win Chance: " + str(team1_ratio))

