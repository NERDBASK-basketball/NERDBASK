import pandas as pd
import requests
import pickle
import sys
import os


def retorna_header():
  headers: dict = {'Accept': '*/*',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                  'Connection': 'keep-alive',
                  'Host': 'stats.nba.com',
                  'Origin': 'https://www.nba.com',
                  'Referer': 'https://www.nba.com/',
                  'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                  'sec-ch-ua-mobile': '?0',
                  'Sec-Fetch-Dest': 'empty',
                  'Sec-Fetch-Mode': 'cors',
                  'Sec-Fetch-Site': 'same-site',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

  return headers

def jogo_todos_q(GameID):

	status_code = 200
	df_players_all = pd.DataFrame()
	Q = 1
	nome_pasta_jogo, gameId = '', ''
	rangeType = '1'
	startRange = '0'
	endRange = '31800'

	headers = retorna_header()  
	url_base = f'https://stats.nba.com/stats/boxscoretraditionalv3?GameID={GameID}&LeagueID=00&'

	while status_code != None:

		startPeriod, endPeriod = Q, Q
		
		url_stats = f'{url_base}endPeriod={endPeriod}&endRange={endRange}&rangeType={rangeType}&startPeriod={startPeriod}&startRange={startRange}'

		with requests.Session() as sessao:
				resposta: requests.models.Response = sessao.get(url_stats, headers=headers)

		y = resposta.json()
		
		status_code = y['boxScoreTraditional']['homeTeam']['teamName']

		if status_code != None:

			name_homeTeam = y['boxScoreTraditional']['homeTeam']['teamName']
			name_awayTeam = y['boxScoreTraditional']['awayTeam']['teamName']
			gameId = y['boxScoreTraditional']['gameId']
			
			nome_pasta_jogo = f'{gameId}_{name_homeTeam}_{name_awayTeam}'

			df_players_homeTeam = pd.json_normalize(y['boxScoreTraditional']['homeTeam']['players'])
			df_players_homeTeam['teamName'] = name_homeTeam
			df_players_awayTeam = pd.json_normalize(y['boxScoreTraditional']['awayTeam']['players'])
			df_players_awayTeam['teamName'] = name_awayTeam
			df_players = df_players_awayTeam.append(df_players_homeTeam)

			df_players['Q'] = Q
			df_players_all = df_players_all.append(df_players)

		Q += 1

	try:
		os.mkdir(f'dados/{nome_pasta_jogo}')
	except OSError:
		pass

	df_players_all.to_csv(f'dados/{nome_pasta_jogo}/{gameId}_players_statistics.csv', index=False)

def temporada_todos_q(temporada, season='002'):

	rangeType = '1'
	startRange = '0'
	endRange = '31800'

	headers = retorna_header() 
	df_players_all = pd.DataFrame()
	
	ID = 1
	GameID = season + temporada + f'{ID:05d}'
	url_base = f'https://stats.nba.com/stats/boxscoretraditionalv3?GameID={GameID}&LeagueID=00&'
	url_stats = f'{url_base}endPeriod=1&endRange={endRange}&rangeType={rangeType}&startPeriod=1&startRange={startRange}'
	status_code_site=requests.get(url_stats, headers=retorna_header()).status_code

	while status_code_site == 200:
		print(GameID)
		status_code = 200
		Q = 1		

		while status_code != None:

			startPeriod, endPeriod = Q, Q
			
			url_stats = f'{url_base}endPeriod={endPeriod}&endRange={endRange}&rangeType={rangeType}&startPeriod={startPeriod}&startRange={startRange}'

			y = requests.get(url_stats, headers=headers).json()
			
			status_code = y['boxScoreTraditional']['homeTeam']['teamName']

			if status_code != None:

				name_homeTeam = y['boxScoreTraditional']['homeTeam']['teamName']
				name_awayTeam = y['boxScoreTraditional']['awayTeam']['teamName']
				gameId = y['boxScoreTraditional']['gameId']

				df_players_homeTeam = pd.json_normalize(y['boxScoreTraditional']['homeTeam']['players'])
				df_players_homeTeam['teamName'] = name_homeTeam
				df_players_awayTeam = pd.json_normalize(y['boxScoreTraditional']['awayTeam']['players'])
				df_players_awayTeam['teamName'] = name_awayTeam
				df_players = df_players_awayTeam.append(df_players_homeTeam)
				
				df_players['gameId'] = gameId
				df_players['Q'] = Q
				
				df_players_all = df_players_all.append(df_players)

			Q += 1
		ID += 1
		GameID = season + temporada + f'{ID:05d}'
		url_base = f'https://stats.nba.com/stats/boxscoretraditionalv3?GameID={GameID}&LeagueID=00&'
		url_stats = f'{url_base}endPeriod=1&endRange={endRange}&rangeType={rangeType}&startPeriod=1&startRange={startRange}'
		status_code_site=requests.get(url_stats, headers=retorna_header()).status_code

	df_players_all.to_csv(f'dados/{season}_{temporada}_all_Q.csv', index=False)

def baixar_temporada_todos_q(temporada, season='002'):

	rangeType = '1'
	startRange = '0'
	endRange = '31800'

	headers = retorna_header()
	
	ID = 1
	GameID = season + temporada + f'{ID:05d}'
	url_base = f'https://stats.nba.com/stats/boxscoretraditionalv3?GameID={GameID}&LeagueID=00&'
	url_stats = f'{url_base}endPeriod=1&endRange={endRange}&rangeType={rangeType}&startPeriod=1&startRange={startRange}'
	status_code_site=requests.get(url_stats, headers=retorna_header()).status_code

	while status_code_site == 200:
		print(GameID)
		status_code = 200
		Q = 1		

		while status_code != None:

			startPeriod, endPeriod = Q, Q
			
			url_stats = f'{url_base}endPeriod={endPeriod}&endRange={endRange}&rangeType={rangeType}&startPeriod={startPeriod}&startRange={startRange}'

			y = requests.get(url_stats, headers=headers).json()
			
			status_code = y['boxScoreTraditional']['homeTeam']['teamName']

			if status_code != None:
				gameId = y['boxScoreTraditional']['gameId']
				a_file = open(f"dados/dict/{gameId}_{Q}.pkl", "wb")
				pickle.dump(y, a_file)
				a_file.close()

			Q += 1
		ID += 1
		GameID = season + temporada + f'{ID:05d}'
		url_base = f'https://stats.nba.com/stats/boxscoretraditionalv3?GameID={GameID}&LeagueID=00&'
		url_stats = f'{url_base}endPeriod=1&endRange={endRange}&rangeType={rangeType}&startPeriod=1&startRange={startRange}'
		status_code_site=requests.get(url_stats, headers=retorna_header()).status_code

def montar_temporada_todos_q(temporada, num_jogos, season='002'):
	
	df_players_all = pd.DataFrame()	
	
	for ID in range(1, num_jogos+1):
		GameID = season + temporada + f'{ID:05d}'	
		print(GameID)

		Q = 1		
		y = True		

		while y != None:
			
			try:
				a_file = open(f"dados/dict/{GameID}_{Q}.pkl", "rb")
			except:
				y = None
			else:				
				y = pickle.load(a_file)

			if y != None:				

				name_homeTeam = y['boxScoreTraditional']['homeTeam']['teamName']
				name_awayTeam = y['boxScoreTraditional']['awayTeam']['teamName']
				gameId = y['boxScoreTraditional']['gameId']

				df_players_homeTeam = pd.json_normalize(y['boxScoreTraditional']['homeTeam']['players'])
				df_players_homeTeam['teamName'] = name_homeTeam
				df_players_awayTeam = pd.json_normalize(y['boxScoreTraditional']['awayTeam']['players'])
				df_players_awayTeam['teamName'] = name_awayTeam
				df_players = df_players_awayTeam.append(df_players_homeTeam)
				
				df_players['gameId'] = gameId
				df_players['Q'] = Q
				
				print(gameId, Q, sep=' ', end='\n')

				df_players_all = df_players_all.append(df_players)
			Q += 1
		ID += 1
	
	df_players_all.to_csv(f'dados/{season}_{temporada}_all_Q.csv', index=False)
	print(df_players_all.shape)

# baixar_temporada_todos_q('20')
montar_temporada_todos_q('20', 1080)
# _, GameID = sys.argv
###
# df_id_date = pd.read_csv('dados/nets_id_game_season_20_21.csv')
# for id_game, _ in df_id_date.values:
# 	jogo_todos_q('00' + str(id_game))
###
# jogo_todos_q('0042000' + GameID)

#0042000217 NetsXBucks
#0042000402 SunsXBucks
#004 20 00406 BucksXSuns


##002 = regular season
##20 = temporada 20/21
##00000 = num jogo