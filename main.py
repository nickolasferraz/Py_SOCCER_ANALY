from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/torschuetzenliste/wettbewerb/BRA1/saison_id/2023/altersklasse/alle/detailpos//plus/1'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')


# Encontrar a tabela específica com a classe correspondente
table = soup.find('table', class_='items')

players = []
clubs = []
goals = []
matches=[]
minutes_in_fild=[]

for row in table.find_all('tr',{'class':['odd','even']}):
  # jogadores
  player = row.find('td', class_='hauptlink').text.strip()
  #Clubes
  club_cell= row.find_all('td',class_='zentriert')[-6]
  club = club_cell.find('a').get('title')
  # partidas
  games = row.find_all('td',class_='zentriert')[-5].text.strip()
  #gols 
  goal = row.find_all('td', class_='zentriert')[-1].text.strip()
  #minutos em campo
  minutes_in_field=row.find('td',class_='rechts').text.strip().replace("'", "")

  players.append(player)
  clubs.append(club)
  goals.append(goal)
  matches.append(games)
  minutes_in_fild.append(minutes_in_field)


  


df=pd.DataFrame({
    'Player': players,
    'Club': clubs,
    'Goals': goals,
    'Matches': matches,
    'Minutes In Field':minutes_in_fild
})

df['Goals'] = pd.to_numeric(df['Goals'])
df['Matches'] = pd.to_numeric(df['Matches'])
df['Minutes In Field'] = pd.to_numeric(df['Minutes In Field'])
df['Minutes per Goal'] = df['Minutes In Field'] / df['Goals']

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


df.to_csv('brasileirao.csv', index=False)

plt.figure(figsize=(10, 6))
df.set_index('Player')['Goals'].sort_values().plot(kind='barh')
plt.title('Goals per Player')
plt.xlabel('Goals')
plt.show()

# Scatter plot of Minutes per Goal
plt.figure(figsize=(10, 6))
plt.scatter(df['Minutes per Goal'], df['Goals'])
plt.title('Minutes per Goal vs Goals')
plt.xlabel('Minutes per Goal')
plt.ylabel('Goals')
plt.show()