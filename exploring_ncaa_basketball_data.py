# Collaborators: Fill in names and SUNetIDs here

def query_one():
    """Query for Stanford's venue"""
    return """
        SELECT DISTINCT venue_name, venue_capacity
	   	FROM `bigquery-public-data.ncaa_basketball.mbb_games_sr` 
	   	WHERE VENUE_CITY LIKE 'Stanford' 
    """

def query_two():
    """Query for games in Stanford's venue"""
    return """
    	SELECT COUNT(*) AS games_at_stanford_season_2013
		FROM (SELECT DISTINCT venue_city, scheduled_date 
		      FROM `bigquery-public-data.ncaa_basketball.mbb_pbp_sr`
			  WHERE venue_city = 'Stanford' and season = 2013)      
    """

def query_three():
    """Query for maximum-red-intensity teams"""
    return """
       SELECT MARKET, COLOR
	   FROM `bigquery-public-data.ncaa_basketball.team_colors` 
	   WHERE COLOR LIKE '#FF%' OR COLOR LIKE '#ff%'
	   ORDER BY MARKET
    """

def query_four():
    """Query for Stanford's wins at home"""
    return """
    	SELECT COUNT(game_id) AS total_games_won_by_stanford_at_home, ROUND(AVG(points_game), 2) AS stanford_avg_points, ROUND(AVG(opp_points_game), 2)  AS opponents_avg_points
		FROM `bigquery-public-data.ncaa_basketball.mbb_teams_games_sr`
		WHERE venue_city = 'Stanford' and win = true and season BETWEEN 2013 AND 2017 and home_team = true
    """

def query_five():
    """Query for players for birth city"""
    return """
    	SELECT COUNT(*) 
		FROM (SELECT DISTINCT mbbPlayersGames.player_id,  mbbPlayersGames.birthplace_city, mbbTeams.venue_city
      		  FROM `bigquery-public-data.ncaa_basketball.mbb_players_games_sr` as mbbPlayersGames, `bigquery-public-data.ncaa_basketball.mbb_teams` as mbbTeams
      	      WHERE mbbPlayersGames.birthplace_city = mbbTeams.venue_city AND mbbPlayersGames. team_id = mbbTeams. id
                    and mbbPlayersGames. birthplace_state = mbbTeams. venue_state)

    """

def query_six():
    """Query for biggest blowout"""
    return """
        SELECT win_name, win_pts, lose_name, lose_pts, win_pts - lose_pts AS win_margin
		FROM `bigquery-public-data.ncaa_basketball.mbb_historical_tournament_games` 
		WHERE (win_pts - lose_pts) = 
		(SELECT MAX(win_pts - lose_pts) 
		 FROM `bigquery-public-data.ncaa_basketball.mbb_historical_tournament_games` 
		)
    """

def query_seven():
    """Query for historical upset percentage"""
    return """
		SELECT ROUND(COUNT(season) * 100.0 / (SELECT COUNT(*) FROM `bigquery-public-data.ncaa_basketball.mbb_historical_tournament_games`), 2) AS historical_tournament_games_upsets_percentage
		FROM `bigquery-public-data.ncaa_basketball.mbb_historical_tournament_games` 
		WHERE win_seed > lose_seed
    """

def query_eight():
    """Query for teams with same states and colors"""
    return """
    	SELECT first_team_name, second_team_name, venue_state
		FROM (SELECT mbb_teams_a. id as first_team_id, 
	             mbb_teams_b. id as second_team_id,
	             mbb_teams_a. name as first_team_name,
	             mbb_teams_b. name as second_team_name,
	             mbb_teams_a. venue_state
		      FROM `bigquery-public-data.ncaa_basketball.mbb_teams` mbb_teams_a, 
		           `bigquery-public-data.ncaa_basketball.mbb_teams` mbb_teams_b
		      WHERE (mbb_teams_a. venue_state = mbb_teams_b. venue_state) and 
		            (mbb_teams_a. id < mbb_teams_b. id)
		      ORDER BY mbb_teams_a. name, mbb_teams_b. name
	      	), 
		    (SELECT team_colors_a. id as first_team_color_id, 
		            team_colors_b. id as second_team_color_id,
		            team_colors_a. market as first_team_color_name,
		            team_colors_b. market as second_team_color_name
	 	     FROM `bigquery-public-data.ncaa_basketball.team_colors` team_colors_a, 
		          `bigquery-public-data.ncaa_basketball.team_colors` team_colors_b
		     WHERE (team_colors_a. color = team_colors_b. color) and 
		           (team_colors_a. id < team_colors_b. id)
		    )
		WHERE (first_team_id = first_team_color_id) and (second_team_id = second_team_color_id)
		ORDER BY first_team_name, second_team_name
    """

def query_nine():
    """Query for teams with lots of high-scorers"""
    return """
    	SELECT team_market, COUNT(team_market) as total_players_15_goals
		FROM (SELECT DISTINCT team_market, player_id
		      FROM `bigquery-public-data.ncaa_basketball.mbb_pbp_sr` 
		      WHERE (team_market IS NOT NULL) AND
		            (player_full_name IS NOT NULL) AND
		            (period = 1) AND 
		            (points_scored IS NOT NULL)
		      GROUP BY game_id, 
		               team_market, 
		               player_id, 
		               period
		      HAVING SUM(points_scored) >= 15
		     )
		GROUP BY team_market
		ORDER BY total_players_15_goals DESC
    """

def query_ten():
    """Query for top geographical locations"""
    return """
      	SELECT SUM(points) AS total_geographical_points, 
		       birthplace_city, 
		       birthplace_state, 
		       birthplace_country
		FROM `bigquery-public-data.ncaa_basketball.mbb_players_games_sr` 
		WHERE field_goals_made IS NOT NULL AND 
		      team_name = (SELECT name
		                   FROM `bigquery-public-data.ncaa_basketball.mbb_teams` 
		                   WHERE market = 'Stanford') 
		GROUP BY birthplace_city, birthplace_state, birthplace_country
		ORDER BY total_geographical_points DESC
		LIMIT 3
    """

def query_eleven():
    """Query for highest-winner teams"""
    return """
       	SELECT market, COUNT(market) as top_performers_cnt
		FROM (SELECT season, market
		      FROM (SELECT season as grouped_by_season, MAX(wins) as maximum_season_wins
		            FROM `bigquery-public-data.ncaa_basketball.mbb_historical_teams_seasons`
		            WHERE (market IS NOT null) AND (season >= 1900) AND season <= 2000
		            GROUP BY season 
		            ORDER BY season
		            ), 
		            (SELECT season, wins, market
		             FROM `bigquery-public-data.ncaa_basketball.mbb_historical_teams_seasons`
		             WHERE (market IS NOT null) AND (season >= 1900) AND season <= 2000
		            )
		      WHERE (season = grouped_by_season) AND
		            (wins = maximum_season_wins)
		      ORDER BY season)
		GROUP BY market
		ORDER BY top_performers_cnt DESC, market
		LIMIT 5
    """
