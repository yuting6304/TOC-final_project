from transitions.extensions import GraphMachine

from utils import send_text_message
from utils import send_image_url
from utils import send_button_message
from utils import isDateCorrect
from utils import isHomeTeamCorrect
from utils import isTeamExist


date = ''
team = ''
pitcher = ''
player = ''
selectedTeam = ''
boxdate = ''
boxteam = ''
imglink = ''
officialNet = ''
mlbWebsite = 'https://www.mlb.com/'


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )


#*************************************************************************
# Description Mode
    def is_going_to_Description(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                return text.lower() == 'hi'
        return False

    def on_enter_Description(self, event):
        desstr = ''
        desstr = desstr + 'Welcome to my Baseball Chatbot\n'
        desstr = desstr + '(1) If you want to get the result of the game in a day you choose :\n'
        desstr = desstr + "Please enter 'game'\n"
        desstr = desstr + '(2) If you want to get the players performance which is at the day you choose\n'
        desstr = desstr + "Please enter 'box'\n"
        desstr = desstr + '(3) If you want to go to the official site and get ball team logo\n'
        desstr = desstr + "Please enter 'team'\n"
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, desstr, 0)
        responese = send_text_message(sender_id, "back to user and getting start by enter :\n'game', 'box', 'team'", 0)
        self.go_back()

    def on_exit_Description(self):
        print('Leaving Description')

#*************************************************************************
#  Game Score Mode
    def is_going_to_Game(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                return text.lower() == 'game'
        return False

    def on_enter_Game(self, event):
  
        sender_id = event['sender']['id']
        # responese = send_text_message(sender_id, "welcome to use my MLB GANE chatbot", 0)
        responese = send_text_message(sender_id, "Game Score mode :\nPlease enter the day and follow the following rules to get the ball games result at your enter day :\nyears from 2005~2018\nmonth from 3~11\n(format : xxxx xx xx)", 0)

 #*************************************************************************   
 # enter a date to see all game result in that day
    def is_going_to_allScore(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                # print(text)
                global date
                date = ''
                date = text
                if(isDateCorrect(date) == 0):
                    sender_id = event['sender']['id']
                    send_text_message(sender_id, "your chosen day had no game\nplease enter another day again!", 0)
                    return False
                return True  #text.lower() == 'score'

        return False

    def on_enter_allScore(self, event):

        sender_id = event['sender']['id']

        send_text_message(sender_id, "Game Score mode :\nthis is the ball game result at your chosen day :", 0)
        send_text_message(sender_id, date, 1)
        send_text_message(sender_id, "Please enter the name of home team(the rear team show as above result) to get the game scoreboard :", 0)
    
 #*************************************************************************  
 # enter a home team's name to get the scoreboard 
    def is_going_to_scoreBoard(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                global team
                team = ''
                team = team + date
                team = team + ' '
                team = team + text
                if(isHomeTeamCorrect(date, text) == 0):
                    sender_id = event['sender']['id']
                    send_text_message(sender_id, "your entered home team name is false\nplease reenter again!", 0)
                    return False
                return True  #text.lower() == 'go to state3'
        return False

    def on_enter_scoreBoard(self, event):

        sender_id = event['sender']['id']

        send_text_message(sender_id, "Game Score mode :\nthis is the scoreboard of a team you choose :", 0)
        send_text_message(sender_id, team, 2)
        send_text_message(sender_id, "if you want to view win/lose pitcher :\nplease enter 'pitcher'\nAnd if you want to view the home team player list :\nplease enter 'player'", 0)


#************************************************************************* 
# enter 'pitcher' to get win/lose pitcher  
    def is_going_to_Pitcher(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                global pitcher
                pitcher = ''
                pitcher = team
                return text.lower() == 'pitcher'
        return False

    def on_enter_Pitcher(self, event):

        sender_id = event['sender']['id']
        
        send_text_message(sender_id, "Game Score mode :\nThis is the game's win/lose pitcher :", 0)
        send_text_message(sender_id, pitcher, 3)
        send_text_message(sender_id, "Thanks for using", 0)

        self.go_back()

    def on_exit_Pitcher(self):

        print('Leaving Pitcher')


#************************************************************************* 
#enter 'player' to get the whole player in home team in that day 
    def is_going_to_Player(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                global player
                player = ''
                player = team
                return text.lower() == 'player'
        return False
    
    def on_enter_Player(self, event):

        sender_id = event['sender']['id']

        send_text_message(sender_id, "Game Score mode :\nThis is the home team's player list :", 0)
        send_text_message(sender_id, player, 4)
        send_text_message(sender_id, "Thanks for using", 0)

        self.go_back()

    def on_exit_Player(self):

        print('Leaving Player')

#*************************************************************************   
# enter 'team' to see your selected team
    def is_going_to_Team(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                return text.lower() == 'team'
        return False

    def on_enter_Team(self, event):
  
        sender_id = event['sender']['id']
        # send_text_message(sender_id, "Thanks for using", 0)
        # responese = send_image_url(sender_id, "https://i.imgur.com/8pRFCT1.jpg")
        buttons = [{
            'type' : 'postback',
            'title' : 'AL',
            'payload' : 'AL'
            },
            {
            'type' : 'postback',
            'title' : 'NL',
            'payload' : 'NL'  
            }]
        responese = send_button_message(sender_id, "choose AL or NL to see the league of team", buttons)

#*************************************************************************   
# use button to select the region AL/NL
    def is_going_to_AL(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'AL'
        return False

    def on_enter_AL(self, event):
  
        sender_id = event['sender']['id']

        buttons = [{
            'type' : 'postback',
            'title' : 'WEST',
            'payload' : 'AL_WEST'
            },
            {
            'type' : 'postback',
            'title' : 'CENTRAL',
            'payload' : 'AL_CENTRAL'
            },
            {
            'type' : 'postback',
            'title' : 'EAST',
            'payload' : 'AL_EAST'  
            }]
        responese = send_button_message(sender_id, "choose the region of your team in AL", buttons)
        # send_text_message(sender_id, "Enter AL", 0)
        
    def is_going_to_NL(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'NL'
        return False

    def on_enter_NL(self, event):
  
        sender_id = event['sender']['id']
        buttons = [{
            'type' : 'postback',
            'title' : 'WEST',
            'payload' : 'NL_WEST'
            },
            {
            'type' : 'postback',
            'title' : 'CENTRAL',
            'payload' : 'NL_CENTRAL'
            },
            {
            'type' : 'postback',
            'title' : 'EAST',
            'payload' : 'NL_EAST'  
            }]
        responese = send_button_message(sender_id, "choose the region of your team in NL", buttons)
        # send_text_message(sender_id, "Enter NL", 0)

#************************************************************************* 
# use button to choose AL region (WEST/CENTRAL/EAST)  
    def is_going_to_AL_W(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'AL_WEST'
        return False

    def on_enter_AL_W(self, event):
  
        sender_id = event['sender']['id']
     
        send_text_message(sender_id, "Enter the team you want to see :\nAngels\nAstros\nRangers\nMariners\nAthletics", 0)

    def is_going_to_AL_C(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'AL_CENTRAL'
        return False

    def on_enter_AL_C(self, event):
  
        sender_id = event['sender']['id']

        send_text_message(sender_id, "Enter the team you want to see :\nIndians\nRoyals\nTigers\nTwins\nWhite Sox", 0)


    def is_going_to_AL_E(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'AL_EAST'
        return False

    def on_enter_AL_E(self, event):
  
        sender_id = event['sender']['id']

        send_text_message(sender_id, "Enter the team you want to see :\nYankees\nRed Sox\nOrioles\nBlue Jays\nBay Rays", 0)

#************************************************************************* 
# use button to choose NL region (WEST/CENTRAL/EAST)  
    def is_going_to_NL_W(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'NL_WEST'
        return False

    def on_enter_NL_W(self, event):
 
        sender_id = event['sender']['id']

        
        send_text_message(sender_id, "Enter the team you want to see :\nDiamondbacks\nDodgers\nGiants\nPadres\nRockies", 0)

    def is_going_to_NL_C(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'NL_CENTRAL'
        return False

    def on_enter_NL_C(self, event):
  
        sender_id = event['sender']['id']

        
        send_text_message(sender_id, "Enter the team you want to see :\nBrewers\nCardinals\nCubs\nPirates\nReds", 0)


    def is_going_to_NL_E(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'NL_EAST'
        return False

    def on_enter_NL_E(self, event):
  
        sender_id = event['sender']['id']

        
        send_text_message(sender_id, "Enter the team you want to see :\nBraves\nMarlins\nMets\nNationals\nPhillies", 0)


#************************************************************************* 
# use button to choose AL region (WEST/CENTRAL/EAST)'s team 
    def is_going_to_AL_T(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                global selectedTeam
                selectedTeam = ''
                selectedTeam = text
                if(isTeamExist(text) == 0):
                    sender_id = event['sender']['id']
                    send_text_message(sender_id, "your input had some mistakes\nplease enter again!", 0)
                    return False
                return True
        return False

    def on_enter_AL_T(self, event):
        global imglink
        global officialNet
        global mlbWebsite
        imglink = ''
        officialNet = ''
#**************************** AL West *************************************
        if(selectedTeam == 'Angels'):
            imglink = "https://i.imgur.com/8ezoHvZ.png"
            officialNet = 'https://www.mlb.com/angels'
        elif(selectedTeam == 'Astros'):
            imglink = "https://i.imgur.com/eEuUUHR.png"
            officialNet = 'https://www.mlb.com/astros'
        elif(selectedTeam == 'Rangers'):
            imglink = "https://i.imgur.com/yARtaev.png"
            officialNet = 'https://www.mlb.com/rangers'
        elif(selectedTeam == 'Mariners'):
            imglink = "https://i.imgur.com/Mw9E4KP.png"
            officialNet = 'https://www.mlb.com/mariners'
        elif(selectedTeam == 'Athletics'):
            imglink = "https://i.imgur.com/nY2STzB.png"
            officialNet = 'https://www.mlb.com/athletics'
#**************************** AL Central *************************************
        elif(selectedTeam == 'Indians'):
            imglink = "https://i.imgur.com/QD45eLq.jpg"
            officialNet = 'https://www.mlb.com/indians'
        elif(selectedTeam == 'Royals'):
            imglink = "https://i.imgur.com/gZFYyPC.jpg"
            officialNet = 'https://www.mlb.com/royals'
        elif(selectedTeam == 'Tigers'):
            imglink = "https://i.imgur.com/sccNQHo.jpg"
            officialNet = 'https://www.mlb.com/tigers'
        elif(selectedTeam == 'Twins'):
            imglink = "https://i.imgur.com/wj4UcT0.jpg"
            officialNet = 'https://www.mlb.com/twins'
        elif(selectedTeam == 'White Sox'):
            imglink = "https://i.imgur.com/vLxtAqO.jpg"
            officialNet = 'https://www.mlb.com/whitesox'
#**************************** AL East *************************************
        elif(selectedTeam == 'Yankees'):
            imglink = "https://i.imgur.com/8pRFCT1.jpg"
            officialNet = 'https://www.mlb.com/yankees'
        elif(selectedTeam == 'Red Sox'):
            imglink = "https://i.imgur.com/8JTE5Av.jpg"
            officialNet = 'https://www.mlb.com/redsox'
        elif(selectedTeam == 'Orioles'):
            imglink = "https://i.imgur.com/Rcsz55R.jpg"
            officialNet = 'https://www.mlb.com/orioles'
        elif(selectedTeam == 'Blue Jays'):
            imglink = "https://i.imgur.com/d0VnJ0u.jpg"
            officialNet = 'https://www.mlb.com/bluejays'
        elif(selectedTeam == 'Bay Rays'):
            imglink = "https://i.imgur.com/VHUqjkP.jpg"
            officialNet = 'https://www.mlb.com/rays'

        sender_id = event['sender']['id']
        
        buttons = [{
            'type' : 'web_url',
            'title' : "go to Official Site",
            'url' : officialNet,
            'webview_height_ratio' : 'full'
            },
            {
            'type' : 'web_url',
            'title' : "MLB Official Site",
            'url' : mlbWebsite,
            'webview_height_ratio' : 'full'
            },
            {
            'type' : 'postback',
            'title' : 'get Logo and back',
            'payload' : 'logo'  
            }]
        responese = send_button_message(sender_id, "choose the one to get next(Official Site or Logo)", buttons)

        
#************************************************************************* 
# use button to choose NL region (WEST/CENTRAL/EAST)'s team 
    def is_going_to_NL_T(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                global selectedTeam
                selectedTeam = ''
                selectedTeam = text
                if(isTeamExist(text) == 0):
                    sender_id = event['sender']['id']
                    send_text_message(sender_id, "your input had some mistakes\nplease enter again!", 0)
                    return False
                return True
        return False

    def on_enter_NL_T(self, event):
        global imglink
        global officialNet
        global mlbWebsite
        imglink = ''
        officialNet = ''
#**************************** NL West *************************************
        if(selectedTeam == 'Diamondbacks'):
            imglink = "https://i.imgur.com/q6dzsF9.png"
            officialNet = 'https://www.mlb.com/dbacks'
        elif(selectedTeam == 'Dodgers'):
            imglink = "https://i.imgur.com/PE4ktg1.png"
            officialNet = 'https://www.mlb.com/dodgers'
        elif(selectedTeam == 'Giants'):
            imglink = "https://i.imgur.com/OP8hVwg.png"
            officialNet = 'https://www.mlb.com/giants'
        elif(selectedTeam == 'Padres'):
            imglink = "https://i.imgur.com/u7FiEJU.jpg"
            officialNet = 'https://www.mlb.com/padres'
        elif(selectedTeam == 'Rockies'):
            imglink = "https://i.imgur.com/smxjtrQ.jpg"
            officialNet = 'https://www.mlb.com/rockies'
#**************************** NL Central *************************************
        elif(selectedTeam == 'Brewers'):
            imglink = "https://i.imgur.com/aDjz5S1.png"
            officialNet = 'https://www.mlb.com/brewers'
        elif(selectedTeam == 'Cardinals'):
            imglink = "https://i.imgur.com/hCIVfzZ.png"
            officialNet = 'https://www.mlb.com/cardinals'
        elif(selectedTeam == 'Cubs'):
            imglink = "https://i.imgur.com/EvuKNm9.png"
            officialNet = 'https://www.mlb.com/cubs'
        elif(selectedTeam == 'Pirates'):
            imglink = "https://i.imgur.com/7uVdDzk.jpg"
            officialNet = 'https://www.mlb.com/pirates'
        elif(selectedTeam == 'Reds'):
            imglink = "https://i.imgur.com/HHBwL42.png"
            officialNet = 'https://www.mlb.com/reds'
#**************************** NL East *************************************
        elif(selectedTeam == 'Braves'):
            imglink = "https://i.imgur.com/X2HE8zR.jpg"
            officialNet = 'https://www.mlb.com/braves'
        elif(selectedTeam == 'Marlins'):
            imglink = "https://i.imgur.com/sVWO5WL.jpg"
            officialNet = 'https://www.mlb.com/marlins'
        elif(selectedTeam == 'Mets'):
            imglink = "https://i.imgur.com/RMoXOhJ.png"
            officialNet = 'https://www.mlb.com/mets'
        elif(selectedTeam == 'Nationals'):
            imglink = "https://i.imgur.com/VpDOTY7.png"
            officialNet = 'https://www.mlb.com/nationals'
        elif(selectedTeam == 'Phillies'):
            imglink = "https://i.imgur.com/dYnzPgE.png"
            officialNet = 'https://www.mlb.com/phillies'
  
        sender_id = event['sender']['id']
        
        buttons = [{
            'type' : 'web_url',
            'title' : "go to Official Site",
            'url' : officialNet,
            'webview_height_ratio' : 'full'
            },
            {
            'type' : 'web_url',
            'title' : "MLB Official Site",
            'url' : mlbWebsite,
            'webview_height_ratio' : 'full'
            },
            {
            'type' : 'postback',
            'title' : 'get Logo and back',
            'payload' : 'logo'  
            }]
        responese = send_button_message(sender_id, "choose the one to get next(Official Site or Logo)", buttons)

# official net work state
    def is_going_to_Logo(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'logo'
        return False

    def on_enter_Logo(self, event):
        global imglink
        sender_id = event['sender']['id']
        responese = send_image_url(sender_id, imglink)
        send_text_message(sender_id, "Thanks for using", 0)
        self.go_back()

    def on_exit_Logo(self):

        print('Leaving Logo')


#*************************************************************************
#  Game Box Mode

    def is_going_to_Gamebox(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                return text.lower() == 'box'
        return False

    def on_enter_Gamebox(self, event):
  
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "welcome to use my MLB GANE chatbot", 0)
        responese = send_text_message(sender_id, "Game Box mode :\nPlease enter the day and follow the following rules to get the ball games result at your enter day :\nyears from 2005~2018\nmonth from 3~11\n(format : xxxx xx xx)", 0)
#*************************************************************************
#  enter a date the same as the above

    def is_going_to_allScorebox(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                # print(text)
                global boxdate
                boxdate = ''
                boxdate = text
                if(isDateCorrect(boxdate) == 0):
                    sender_id = event['sender']['id']
                    send_text_message(sender_id, "your chosen day had no game\nplease enter another day again!", 0)
                    return False
                return True  #text.lower() == 'score'

        return False

    def on_enter_allScorebox(self, event):

        sender_id = event['sender']['id']

        send_text_message(sender_id, "Game Box mode :\nthis is the ball game result at your chosen day :", 0)
        send_text_message(sender_id, boxdate, 1)
        send_text_message(sender_id, "Please enter the name of home team(the rear team show as above result) to get the game scoreboard :", 0)

#*************************************************************************
#  enter a team name

    def is_going_to_scoreBoardbox(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                global boxteam
                boxteam = ''
                boxteam = boxteam + boxdate
                boxteam = boxteam + ' '
                boxteam = boxteam + text
                if(isHomeTeamCorrect(boxdate, text) == 0):
                    sender_id = event['sender']['id']
                    send_text_message(sender_id, "your entered home team name is false\nplease reenter again!", 0)
                    return False
                return True  #text.lower() == 'go to state3'
        return False

    def on_enter_scoreBoardbox(self, event):

        sender_id = event['sender']['id']

        buttons = [{
            'type' : 'postback',
            'title' : 'Home Team',
            'payload' : 'home'
            },
            {
            'type' : 'postback',
            'title' : 'Away Team',
            'payload' : 'away'
            }]
        responese = send_button_message(sender_id, "Choose Home team or Away team to view players box:", buttons)

#*************************************************************************
#  use button to choose to see home or away game box
    def is_going_to_homeTeam(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'home'
        return False

    def on_enter_homeTeam(self, event):

        sender_id = event['sender']['id']

        buttons = [{
            'type' : 'postback',
            'title' : 'Home Team Pitcher',
            'payload' : 'pitcher'
            },
            {
            'type' : 'postback',
            'title' : 'Home Team Hitter',
            'payload' : 'hitter'
            }]
        responese = send_button_message(sender_id, "Select to view the HOME TEAM Pitcher box or Hitter box", buttons)


    def is_going_to_awayTeam(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'away'
        return False

    def on_enter_awayTeam(self, event):

        sender_id = event['sender']['id']

        buttons = [{
            'type' : 'postback',
            'title' : 'Away Team Pitcher',
            'payload' : 'pitcher'
            },
            {
            'type' : 'postback',
            'title' : 'Away Team Hitter',
            'payload' : 'hitter'
            }]
        responese = send_button_message(sender_id, "Select to view the AWAY TEAM Pitcher or Hitter box", buttons)

#*************************************************************************
#  use button to choose to see HOME pitcher box or hitter box
#  home pitcher

    def is_going_to_homePitcher(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'pitcher'
        return False

    def on_enter_homePitcher(self, event):
        global boxteam
        sender_id = event['sender']['id']

        send_text_message(sender_id, boxteam, 5)
        send_text_message(sender_id, 'thanks for using', 0)
        self.go_back()

    def on_exit_homePitcher(self):

        print('Leaving homePitcher')

#  home hitter

    def is_going_to_homeHitter(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'hitter'
        return False

    def on_enter_homeHitter(self, event):
        global boxteam
        sender_id = event['sender']['id']

        send_text_message(sender_id, boxteam, 6)
        send_text_message(sender_id, 'thanks for using', 0)

        self.go_back()

    def on_exit_homeHitter(self):

        print('Leaving homeHitter')

#*************************************************************************
#  use button to choose to see AWAY pitcher box or hitter box
#  away pitcher

    def is_going_to_awayPitcher(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'pitcher'
        return False

    def on_enter_awayPitcher(self, event):
        global boxteam
        sender_id = event['sender']['id']

        send_text_message(sender_id, boxteam, 7)
        send_text_message(sender_id, 'thanks for using', 0)

        self.go_back()

    def on_exit_awayPitcher(self):

        print('Leaving awayPitcher')

#  away hitter

    def is_going_to_awayHitter(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                payload = event['postback']['payload']
                return payload == 'hitter'
        return False

    def on_enter_awayHitter(self, event):
        global boxteam
        sender_id = event['sender']['id']

        send_text_message(sender_id, boxteam, 8)
        send_text_message(sender_id, 'thanks for using', 0)

        self.go_back()

    def on_exit_awayHitter(self):

        print('Leaving awayHitter')
