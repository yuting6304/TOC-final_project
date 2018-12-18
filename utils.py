from __future__ import print_function
import requests

import mlbgame.events
import mlbgame.game
import mlbgame.info
import mlbgame.stats
import mlbgame.version

import calendar
from datetime import date, datetime

VERSION = mlbgame.version.__version__

import json

import lxml.etree as etree

import mlbgame.data
import mlbgame.object


GRAPH_URL = "https://graph.facebook.com/v2.6"

# txt = ''
judgeVar = 0
teamVar = 0
t_existVar = 0
sepstr = ''
HTeam = ''
ATeam = ''
splout = []

teams = ['Angels', 'Astros', 'Rangers', 'Mariners', 'Athletics',
        'Indians', 'Royals', 'Tigers', 'Twins', 'White Sox',
        'Yankees', 'Red Sox', 'Orioles', 'Blue Jays', 'Bay Rays',
        'Diamondbacks', 'Dodgers', 'Giants', 'Padres', 'Rockies',
        'Brewers', 'Cardinals', 'Cubs', 'Pirates', 'Reds',
        'Braves', 'Marlins', 'Mets', 'Nationals', 'Phillies']

def __player_stats_info(data, name):
    home = []
    away = []
    for y in data:
        # loops through pitchers and batters
        for x in y.findall(name):
            stats = {}
            # loop through and save stats
            for i in x.attrib:
                stats[i] = x.attrib[i]
            # apply to correct list
            if y.attrib['team_flag'] == 'home':
                home.append(stats)
            else:
                away.append(stats)
    return (home, away)


def __raw_player_stats_info(data):
    home_pitchers = []
    away_pitchers = []
    home_batters = []
    away_batters = []

    for team in data.findall('team'):
        home_flag = team.attrib['team_flag'] == 'home'
        pitching = team.find('pitching')
        for pitcher in pitching.findall('pitcher'):
            stats = {}
            for i in pitcher.attrib:
                stats[i] = pitcher.attrib[i]
            if home_flag:
                home_pitchers.append(stats)
            else:
                away_pitchers.append(stats)

        batting = team.find('batting')
        for batter in batting.findall('batter'):
            stats = {}
            for i in batter.attrib:
                stats[i] = batter.attrib[i]
            if home_flag:
                home_batters.append(stats)
            else:
                away_batters.append(stats)
    home = {'pitchers': home_pitchers, 'batters': home_batters}
    away = {'pitchers': away_pitchers, 'batters': away_batters}
    return (home, away)


def player_stats(game_id):
    """Return dictionary of individual stats of a game with matching id.

       The additional pitching/batting is mostly the same stats, except it
       contains some useful stats such as groundouts/flyouts per pitcher
       (go/ao). MLB decided to have two box score files, thus we return the
       data from both.
    """
    # get data from data module
    box_score = mlbgame.data.get_box_score(game_id)
    raw_box_score = mlbgame.data.get_raw_box_score(game_id)
    # parse XML
    box_score_tree = etree.parse(box_score).getroot()
    raw_box_score_tree = etree.parse(raw_box_score).getroot()
    # get pitching and batting info
    pitching = box_score_tree.findall('pitching')
    batting = box_score_tree.findall('batting')
    # get parsed stats
    pitching_info = __player_stats_info(pitching, 'pitcher')
    batting_info = __player_stats_info(batting, 'batter')
    # get parsed additional stats
    additional_stats = __raw_player_stats_info(raw_box_score_tree)
    addl_home_pitching = additional_stats[0]['pitchers']
    addl_home_batting = additional_stats[0]['batters']
    addl_away_pitching = additional_stats[1]['pitchers']
    addl_away_batting = additional_stats[1]['batters']

    output = {
        'home_pitching': pitching_info[0],
        'away_pitching': pitching_info[1],
        'home_batting': batting_info[0],
        'away_batting': batting_info[1],
        'home_additional_pitching': addl_home_pitching,
        'away_additional_pitching': addl_away_pitching,
        'home_additional_batting': addl_home_batting,
        'away_additional_batting': addl_away_batting
    }
    return output

def send_text_message(id, text, mode):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    # global txt
    txt = ''
    listore = []
    if(mode == 0):
        payload = {
            "recipient": {"id": id},
            "message": {"text": text}
        }
    elif(mode == 1):
        txt, listore = gameResult(text)
        payload = {
            "recipient": {"id": id},
            "message": {"text": txt}
        }
    elif(mode == 2):
        txt = scoreBoard(text)
        payload = {
            "recipient": {"id": id},
            "message": {"text": txt}
        }
    elif(mode == 3):
        txt = pitcherWL(text)
        payload = {
            "recipient": {"id": id},
            "message": {"text": txt}
        }
    elif(mode == 4):
        txt = homePlayer(text)
        payload = {
            "recipient": {"id": id},
            "message": {"text": txt}
        }
    elif(mode == 5):
        txt = PitcherBOX(text, 1)
        payload = {
            "recipient": {"id": id},
            "message": {"text": txt}
        }
    elif(mode == 6):
        txt = HitterBOX(text, 1)
        payload = {
            "recipient": {"id": id},
            "message": {"text": txt}
        }
    elif(mode == 7):
        txt = PitcherBOX(text, 2)
        payload = {
            "recipient": {"id": id},
            "message": {"text": txt}
        }
    elif(mode == 8):
        txt = HitterBOX(text, 2)
        payload = {
            "recipient": {"id": id},
            "message": {"text": txt}
        }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

def isDateCorrect(instr):
    value = 0
    lioutput = []
    result, lioutput = gameResult(instr)
    
    global judgeVar

    if(len(result) == 0):
        judgeVar = 0
    else:
        judgeVar = 1

    return judgeVar

def isHomeTeamCorrect(instr, homeTeam):
    value = 0
    lioutput = []
    result, lioutput = gameResult(instr)
    
    global teamVar
    global HTeam
    global ATeam

    HTeam = ''
    ATeam = ''

    teamVar = 0
    
    lensplout = len(lioutput)

    i = 1
    while i < lensplout:
        if(homeTeam == str(lioutput[i][4:len(lioutput[i])-3])):
            HTeam = str(lioutput[i][4:len(lioutput[i])-3])
            ATeam = str(lioutput[i-1][0:len(lioutput[i-1])-3])
            teamVar = 1
            break
        i = i + 2

    return teamVar

def isTeamExist(instr):
    global teams
    global texistVar

    t_existVar = 0
    
    i = 0
    while(i < 30):
        if(instr == str(teams[i])):
            t_existVar = 1
            break
        i = i + 1
    return t_existVar

def gameResult(instr):
    global sepstr
    global splout
    sepstr = ''
    output = ''
    lioutput = []
    strli = []
    strli = instr.split(' ')

    lioutput = []

    if(len(strli) < 3):
        return output, lioutput
    
    if(strli[0].isdigit() == False or strli[1].isdigit() == False or strli[2].isdigit() == False):
        return output, lioutput        

    daysinmonth = calendar.monthrange(int(strli[0]), int(strli[1]))[1]
    data = mlbgame.game.scoreboard(int(strli[0]), int(strli[1]), int(strli[2]), home=None, away=None)

    for p in data:
        sepstr = sepstr + str(mlbgame.game.GameScoreboard(data[p]))

        output = output + str(mlbgame.game.GameScoreboard(data[p]))
        output = output + '\n'

    splout = sepstr.split(')')
    splout.remove('')

    return output, splout

def scoreBoard(instr):
    output = ''
    strli = []
    strli = instr.split(' ', 3)

    game = mlbgame.day(int(strli[0]), int(strli[1]), int(strli[2]), home=strli[3])[0]
    data = mlbgame.game.box_score(game.game_id)
    print(data)

    length = len(data)
    print(length)
    output = ''
    home = []
    homeTotal = 0
    away = []
    awayTotal = 0
    i = 1
    while i < length:
        if(data[i]['home'] == 'x'):
            home.append(0)
            homeTotal = homeTotal + 0
        else:
            home.append(data[i]['home'])
            homeTotal = homeTotal + int(data[i]['home'])
        away.append(data[i]['away'])
        awayTotal = awayTotal + int(data[i]['away'])
        i = i+1

    home.append(homeTotal)
    away.append(awayTotal)

    # print('home : ', home)
    # print('away : ', away)

    j = 0

    while j < length+1:
        if(j == 0):
            output = output + 'Inning'
            output = output + '\t'
        elif(j == length):
            output = output + 'F'
        else:
            output = output + str(j)
            output = output + '\t'
        j = j + 1
    output = output + '\n'
    output = output + 'Away'
    k = 0

    while k < length:
        output = output + '\t'
        output = output + str(away[k])
        k = k + 1
    output = output + '\n'
    output = output + 'Home'
    n = 0
    while n < length:
        output = output + '\t'
        output = output + str(home[n])
        n = n + 1

    return output

def pitcherWL(instr):
    output = ''
    pit = ''
    strli = []
    strli = instr.split(' ', 3)

    day = mlbgame.day(int(strli[0]), int(strli[1]), int(strli[2]), home=strli[3], away=strli[3])
    game = day[0]
    pit = 'Winning pitcher: %s (%s) - \nLosing Pitcher: %s (%s)'
    output = pit % (game.w_pitcher, game.w_team, game.l_pitcher, game.l_team)

    return output

def homePlayer(instr):
    output = ''
    global HTeam
    global ATeam
    strli = []
    strli = instr.split(' ', 3)

    game = mlbgame.day(int(strli[0]), int(strli[1]), int(strli[2]), home=strli[3])[0]
    stats = mlbgame.player_stats(game.game_id)
    for player in stats.home_batting:
        output = output + str(player)
        output = output + '\n'


    return output

def PitcherBOX(instr, mode):
    output = ''
    strli = []
    strli = instr.split(' ', 3)

    if(len(strli) < 3):
        return output
    
    if(strli[0].isdigit() == False or strli[1].isdigit() == False or strli[2].isdigit() == False):
        return output      

    game = mlbgame.day(int(strli[0]), int(strli[1]), int(strli[2]), home=strli[3])[0]
    data = player_stats(game.game_id)


    OUT = 0
    H = 0
    R = 0
    ER = 0
    BB = 0
    SO = 0
    HR = 0

    # choose to list away pitcher box
    if(mode == 1):
        output = output + HTeam
        output = output + "'s Pitcher :\n"
        i = 0
        while(i < len(data['home_pitching'])):
            output = output + data['home_pitching'][i]['name_display_first_last']
            output = output + ' :\n'
            output = output + 'IP\tH\tR\tER\tBB\tSO\tHR\tERA\n'

            if(int(data['home_pitching'][i]['out']) % 3 == 1):
                output = output + str(int(int(data['home_pitching'][i]['out'])/3) + 0.1)
            elif(int(data['home_pitching'][i]['out']) % 3 == 2):
                output = output + str(int(int(data['home_pitching'][i]['out'])/3) + 0.2)
            else:
                output = output + str(int(data['home_pitching'][i]['out'])/3)


            output = output + '\t'
            output = output + data['home_pitching'][i]['h']
            output = output + '\t'
            output = output + data['home_pitching'][i]['r']
            output = output + '\t'
            output = output + data['home_pitching'][i]['er']
            output = output + '\t'
            output = output + data['home_pitching'][i]['bb']
            output = output + '\t'
            output = output + data['home_pitching'][i]['so']
            output = output + '\t'
            output = output + data['home_pitching'][i]['hr']
            output = output + '\t'
            output = output + data['home_pitching'][i]['era']
            output = output + '\n'

            OUT = OUT + int(data['home_pitching'][i]['out'])
            H = H + int(data['home_pitching'][i]['h'])
            R = R + int(data['home_pitching'][i]['r'])
            ER = ER + int(data['home_pitching'][i]['er'])
            BB = BB + int(data['home_pitching'][i]['bb'])
            SO = SO + int(data['home_pitching'][i]['so'])
            HR = HR + int(data['home_pitching'][i]['hr'])

            i = i + 1

    elif(mode == 2):
        output = output + ATeam
        output = output + "'s Pitcher :\n"
        i = 0
        while(i < len(data['away_pitching'])):
            output = output + data['away_pitching'][i]['name_display_first_last']
            output = output + '\n'
            output = output + 'IP\tH\tR\tER\tBB\tSO\tHR\tERA\n'

            if(int(data['away_pitching'][i]['out']) % 3 == 1):
                output = output + str(int(int(data['away_pitching'][i]['out'])/3) + 0.1)
            elif(int(data['away_pitching'][i]['out']) % 3 == 2):
                output = output + str(int(int(data['away_pitching'][i]['out'])/3) + 0.2)
            else:
                output = output + str(int(data['away_pitching'][i]['out'])/3)


            output = output + '\t'
            output = output + data['away_pitching'][i]['h']
            output = output + '\t'
            output = output + data['away_pitching'][i]['r']
            output = output + '\t'
            output = output + data['away_pitching'][i]['er']
            output = output + '\t'
            output = output + data['away_pitching'][i]['bb']
            output = output + '\t'
            output = output + data['away_pitching'][i]['so']
            output = output + '\t'
            output = output + data['away_pitching'][i]['hr']
            output = output + '\t'
            output = output + data['away_pitching'][i]['era']
            output = output + '\n'

            OUT = OUT + int(data['away_pitching'][i]['out'])
            H = H + int(data['away_pitching'][i]['h'])
            R = R + int(data['away_pitching'][i]['r'])
            ER = ER + int(data['away_pitching'][i]['er'])
            BB = BB + int(data['away_pitching'][i]['bb'])
            SO = SO + int(data['away_pitching'][i]['so'])
            HR = HR + int(data['away_pitching'][i]['hr'])

            i = i + 1

    output = output + 'total :\n'
    output = output + 'IP\tH\tR\tER\tBB\tSO\tHR\n'
    output = output + str(OUT/3)
    output = output + '\t'
    output = output + str(H)
    output = output + '\t'
    output = output + str(R)
    output = output + '\t'
    output = output + str(ER)
    output = output + '\t'
    output = output + str(BB)
    output = output + '\t'
    output = output + str(SO)
    output = output + '\t'
    output = output + str(HR)
    output = output + '\n'

    # print(output)
    return output

def HitterBOX(instr, mode):
    output = ''
    global HTeam
    global ATeam
    strli = []
    strli = instr.split(' ', 3)

    if(len(strli) < 3):
        return output
    
    if(strli[0].isdigit() == False or strli[1].isdigit() == False or strli[2].isdigit() == False):
        return output      


    game = mlbgame.day(int(strli[0]), int(strli[1]), int(strli[2]), home=strli[3])[0]

    data = player_stats(game.game_id)

    AB = 0
    R = 0
    H = 0
    RBI = 0
    BB = 0
    SO = 0
    LOB = 0

    # choose to list home hitter box
    if(mode == 1):
        output = output + HTeam
        output = output + "'s Hitter :\n"
        i = 0
        while(i < len(data['home_batting'])):
            output = output + data['home_batting'][i]['name_display_first_last']
            output = output + ' :\n'
            output = output + 'AB\tR\tH\tRBI\tBB\tSO\tLOB\tAVG\tOPS\n'

            output = output + data['home_batting'][i]['ab']
            output = output + '\t'
            output = output + data['home_batting'][i]['r']
            output = output + '\t'
            output = output + data['home_batting'][i]['h']
            output = output + '\t'
            output = output + data['home_batting'][i]['rbi']
            output = output + '\t'
            output = output + data['home_batting'][i]['bb']
            output = output + '\t'
            output = output + data['home_batting'][i]['so']
            output = output + '\t'
            output = output + data['home_batting'][i]['lob']
            output = output + '\t'
            output = output + data['home_batting'][i]['avg']
            output = output + '\t'
            output = output + data['home_batting'][i]['ops']
            output = output + '\n'

            AB = AB + int(data['home_batting'][i]['ab'])
            R = R + int(data['home_batting'][i]['r'])
            H = H + int(data['home_batting'][i]['h'])
            RBI = RBI + int(data['home_batting'][i]['rbi'])
            BB = BB + int(data['home_batting'][i]['bb'])
            SO = SO + int(data['home_batting'][i]['so'])
            LOB = LOB + int(data['home_batting'][i]['lob'])

            i = i + 1
    
    # choose to list away hitter box

    elif(mode == 2):
        output = output + ATeam
        output = output + "'s Hitter :\n"
        i = 0
        while(i < len(data['away_batting'])):
            output = output + data['away_batting'][i]['name_display_first_last']
            output = output + ' :\n'
            output = output + 'AB\tR\tH\tRBI\tBB\tSO\tLOB\tAVG\tOPS\n'

            output = output + data['away_batting'][i]['ab']
            output = output + '\t'
            output = output + data['away_batting'][i]['r']
            output = output + '\t'
            output = output + data['away_batting'][i]['h']
            output = output + '\t'
            output = output + data['away_batting'][i]['rbi']
            output = output + '\t'
            output = output + data['away_batting'][i]['bb']
            output = output + '\t'
            output = output + data['away_batting'][i]['so']
            output = output + '\t'
            output = output + data['away_batting'][i]['lob']
            output = output + '\t'
            output = output + data['away_batting'][i]['avg']
            output = output + '\t'
            output = output + data['away_batting'][i]['ops']
            output = output + '\n'

            AB = AB + int(data['away_batting'][i]['ab'])
            R = R + int(data['away_batting'][i]['r'])
            H = H + int(data['away_batting'][i]['h'])
            RBI = RBI + int(data['away_batting'][i]['rbi'])
            BB = BB + int(data['away_batting'][i]['bb'])
            SO = SO + int(data['away_batting'][i]['so'])
            LOB = LOB + int(data['away_batting'][i]['lob'])

            i = i + 1
    
    output = output + 'total :\n'
    output = output + 'AB\tR\tH\tRBI\tBB\tSO\tLOB\tAVG\tOPS\n'
    output = output + str(AB)
    output = output + '\t'
    output = output + str(R)
    output = output + '\t'
    output = output + str(H)
    output = output + '\t'
    output = output + str(RBI)
    output = output + '\t'
    output = output + str(BB)
    output = output + '\t'
    output = output + str(SO)
    output = output + '\t'
    output = output + str(LOB)
    output = output + '\n'

    return output

def send_image_url(id, img_url):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)

    # encode nested json to avoid errors during multipart encoding process
    msg = {
        "attachment":{
            "type":"image", 
            "payload":{
                "url":img_url, 
                "is_reusable":True
            }
        }
    }
    # 'filedata': (os.path.basename('yankees.png'), open('yankees.png', 'rb'), 'image/png')
    response_msg = json.dumps({"recipient": {"id": id}, "message": msg})
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=response_msg)
    if response.status_code != 200:
        print("Unable to send img message")
    return response



def send_button_message(id, text, buttons):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient" : {"id" : id},
        "message" : {
            "attachment" : {
                "type" : "template",
                "payload" : {
                    "template_type" : "button",
                    "text" : text,
                    "buttons" : buttons
                }
            }
        }
    }
    response = requests.post(url, json=payload)
    if(response.status_code != 200):
        print("button Unable to send img message")
    return response