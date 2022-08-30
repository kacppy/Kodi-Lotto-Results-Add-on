import xbmcgui
from datetime import timezone
from datetime import datetime
from datetime import date
from urllib.request import Request, urlopen
import json

def gather_data(funny_url):
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Wyniki Lotto', 'Ładowanie wyników...')

    req = Request(
        url=funny_url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    pDialog.update(25)

    webpage = urlopen(req).read()
    pDialog.update(50)

    page_content = json.loads(webpage)
    pDialog.close()

    return page_content


while True:
    dialog = xbmcgui.Dialog()
    url='https://www.lotto.pl/api/lotteries/draw-results/last-results'

    data = gather_data(url)

    list_games = []
    for i in data:
        list_games.append(str(i['gameType']))

    ret = dialog.select('Wybierz grę', list_games)
    if ret == -1:
        break

    game_data = data[ret]['results']
    inside_game_res = []
    for i in game_data:
        inside_game_res.append(str(i['gameType']))

    ret2 = dialog.select('Wybierz grę', inside_game_res)
    if ret2 == -1:
        break

    nazwa = str(game_data[ret2]['gameType'])
    data_losowania = datetime.fromisoformat(game_data[ret2]['drawDate'][:-1]).strftime('%d/%m/%y %H:%M')
    nr_losowania = str(game_data[ret2]['drawSystemId'])
    wyniki = str(game_data[ret2]['resultsJson'])
    bonus = str(game_data[ret2]['specialResults'])

    title = nazwa+' - '+str(data_losowania)
    msg = 'Numer losowania '+nr_losowania+'\n'+'Wyniki '+wyniki+'\n'+'Bonus '+bonus

    dialog.ok(title, msg)
    ret3 = dialog.yesno('Wyniki Lotto', 'Chcesz zobaczyć wyniki z poprzednich dni?')
    if ret3 == True:
        today = date.today()
        url = "https://www.lotto.pl/api/lotteries/draw-results/by-date-per-game?gameType="+nazwa+"&drawDate="+str(today)+"&index=1&size=6&sort=DrawSystemId&order=DESC"

        y = gather_data(url)
        msg2 = '\n'

        for i in y['items']:
            nazwa = str(i['results'][0]['gameType'])
            data_losowania = datetime.fromisoformat(i['results'][0]['drawDate'][:-1]).strftime('%d/%m/%y %H:%M')
            nr_losowania = str(i['results'][0]['drawSystemId'])
            wyniki = str(i['results'][0]['resultsJson'])
            bonus = str(i['results'][0]['specialResults'])
            msg2 = msg2+'Data '+str(data_losowania)+'\n'+'Numer losowania '+nr_losowania+'\n'+'Wyniki '+wyniki+'\n'+'Bonus '+bonus+'\n\n'
        
        title2 = 'Poprzednie wyniki '+nazwa
        dialog.textviewer(title2, msg2)
    break