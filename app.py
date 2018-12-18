from bottle import route, run, request, abort, static_file
from fsm import TocMachine


# VERIFY_TOKEN = "Your Webhook Verify Token"
VERIFY_TOKEN = "qweszxc14789632"

machine = TocMachine(
    states=[
        'Description',
        'user',
        'Game',
        'allScore',
        'scoreBoard',
        'Pitcher',
        'Player',
        'Team',
        'AL',
        'AL_W',
        'AL_C',
        'AL_E',
        'AL_T',
        'NL',
        'NL_W',
        'NL_C',
        'NL_E',
        'NL_T',
        'Gamebox',
        'allScorebox',
        'scoreBoardbox',
        'homeTeam',
        'awayTeam',
        'homePitcher',
        'awayPitcher',
        'homeHitter',
        'awayHitter',
        'Logo'

    ],
    transitions=[
#*******************************************************
# sequence 1        
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'Game',
            'conditions': 'is_going_to_Game'
        },
        {
            'trigger': 'advance',
            'source': 'Game',
            'dest': 'allScore',
            'conditions': 'is_going_to_allScore'
        },
        {
            'trigger': 'advance',
            'source': 'allScore',
            'dest': 'scoreBoard',
            'conditions': 'is_going_to_scoreBoard'
        },
        {
            'trigger': 'advance',
            'source': 'scoreBoard',
            'dest': 'Pitcher',
            'conditions': 'is_going_to_Pitcher'
        },
        {
            'trigger': 'advance',
            'source': 'scoreBoard',
            'dest': 'Player',
            'conditions': 'is_going_to_Player'
        },
#*******************************************************
# sequence 2
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'Team',
            'conditions': 'is_going_to_Team'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'Description',
            'conditions': 'is_going_to_Description'
        },
        {
            'trigger': 'advance',
            'source': 'Team',
            'dest': 'AL',
            'conditions': 'is_going_to_AL'
        },
        {
            'trigger': 'advance',
            'source': 'AL',
            'dest': 'AL_W',
            'conditions': 'is_going_to_AL_W'
        },
        {
            'trigger': 'advance',
            'source': 'AL',
            'dest': 'AL_C',
            'conditions': 'is_going_to_AL_C'
        },
        {
            'trigger': 'advance',
            'source': 'AL',
            'dest': 'AL_E',
            'conditions': 'is_going_to_AL_E'
        },
        {
            'trigger': 'advance',
            'source': [
                'AL_W',
                'AL_C',
                'AL_E'
                ],
            'dest': 'AL_T',
            'conditions': 'is_going_to_AL_T'
        },
        {
            'trigger': 'advance',
            'source': 'Team',
            'dest': 'NL',
            'conditions': 'is_going_to_NL'
        },
        {
            'trigger': 'advance',
            'source': 'NL',
            'dest': 'NL_W',
            'conditions': 'is_going_to_NL_W'
        },
        {
            'trigger': 'advance',
            'source': 'NL',
            'dest': 'NL_C',
            'conditions': 'is_going_to_NL_C'
        },
        {
            'trigger': 'advance',
            'source': 'NL',
            'dest': 'NL_E',
            'conditions': 'is_going_to_NL_E'
        },
        {
            'trigger': 'advance',
            'source': [
                'NL_W',
                'NL_C',
                'NL_E'
                ],
            'dest': 'NL_T',
            'conditions': 'is_going_to_NL_T'
        },
        {
            'trigger': 'advance',
            'source': [
                'NL_T',
                'AL_T'
                ],
            'dest': 'Logo',
            'conditions': 'is_going_to_Logo'
        },
#*******************************************************
# sequence 3
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'Gamebox',
            'conditions': 'is_going_to_Gamebox'
        },
        {
            'trigger': 'advance',
            'source': 'Gamebox',
            'dest': 'allScorebox',
            'conditions': 'is_going_to_allScorebox'
        },
        {
            'trigger': 'advance',
            'source': 'allScorebox',
            'dest': 'scoreBoardbox',
            'conditions': 'is_going_to_scoreBoardbox'
        },
        {
            'trigger': 'advance',
            'source': 'scoreBoardbox',
            'dest': 'homeTeam',
            'conditions': 'is_going_to_homeTeam'
        },
        {
            'trigger': 'advance',
            'source': 'scoreBoardbox',
            'dest': 'awayTeam',
            'conditions': 'is_going_to_awayTeam'
        },
        {
            'trigger': 'advance',
            'source': 'homeTeam',
            'dest': 'homePitcher',
            'conditions': 'is_going_to_homePitcher'
        },
        {
            'trigger': 'advance',
            'source': 'homeTeam',
            'dest': 'homeHitter',
            'conditions': 'is_going_to_homeHitter'
        },
        {
            'trigger': 'advance',
            'source': 'awayTeam',
            'dest': 'awayPitcher',
            'conditions': 'is_going_to_awayPitcher'
        },
        {
            'trigger': 'advance',
            'source': 'awayTeam',
            'dest': 'awayHitter',
            'conditions': 'is_going_to_awayHitter'
        },

#*******************************************************
# back
        {
            'trigger': 'go_back',
            'source': [
                'Pitcher',
                'Player',
                # 'AL_T',
                # 'NL_T',
                'Description',
                'awayPitcher',
                'homePitcher',
                'homeHitter',
                'awayHitter',
                'Logo'
            ],
            'dest': 'user'
        }
        
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        machine.advance(event)
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)
