from flask import Flask, render_template, request, flash, session, url_for, redirect
from wtforms import StringField, SubmitField, PasswordField, SelectField, validators, RadioField
import flask_wtf #import FlaskFormimport
from wtforms.fields.html5 import DateField
from cardset import CardSet
from pokerhand import PokerHand
import random 
class LoginForm(flask_wtf.FlaskForm):
    username = StringField('User name')
    password = PasswordField('Password')
    login_button = SubmitField('Login In')
    cardnumber = RadioField('Number of Cards', choices=[('20','20 cards'),('52','52 cards')],  default='52')
    #register = SubmitField('Create New Account')
    #entrydate =DateField()

class BookingForm(flask_wtf.FlaskForm):

    showplayercard = SubmitField('Show Player Cards')
    showopponentcard = SubmitField('Show Opponent Cards')
    cardnumber = RadioField('Number of Cards', choices=[('20','20 cards'),('52','52 cards')])
    new_index = StringField('New Index')#),validators=[validators.DataRequired()])
    delete=  SubmitField('Delete selected Index')
    add_document = SubmitField('Add a new document')
    delete_document = SubmitField('Delete a document')
    new_document = StringField('New Document')#),validators=[validators.DataRequired()])


    entrydate =DateField('Date')#,validators=[validators.DataRequired()])
    timeslot = SelectField('Time Slot',choices=['9:30am','10:30am','11:30am','13:30pm','14:30pm','15:30pm'])
    
    update=  SubmitField('Update selected Appointment')
    appointments =SelectField('Appointments',choices=[])
    newgame=  SubmitField('New Game')

class UpdateForm(flask_wtf.FlaskForm):
    firstname = StringField('First Name',validators=[validators.DataRequired()])
    lastname = StringField('Last Name',validators=[validators.DataRequired()])
    email = StringField('email',validators=[validators.Email(granular_message=True)])
    telephone = StringField('Telephone',validators=[validators.DataRequired()])
    gender = SelectField('Gender',choices=['M','F'])
    age = StringField('Age',validators=[validators.DataRequired()])
    update = SubmitField('Update your Account')
    delete = SubmitField('Delete your Account')
    booking = SubmitField('Create an Appointment')

def convert_tuple_to_cards(new_hand):
    #this function convert card in tuple to string
    cards = ''
    valDict ={1: 'ace', 10:'ten', 11:'jack', 12:'queen', 13:'king'}
    suitDict ={1:'spades',2:'hearts',3:'diamonds',4:'clubs'}
    card_files=[]
    for val, suit in new_hand:
        card = ''
        file_string =''
        if val in [1, 10, 11, 12, 13]:
            card = card + valDict[val][0].upper()
            file_string = valDict[val]
        else:
            card = card + str(val)
            file_string =str(val)
        card = card + suitDict[suit][0].upper() + ' '
    
        file_string = file_string + '_of_'+suitDict[suit] +'.png'
        card_files.append(file_string)
        cards = cards  + card
    return cards[0:-1], card_files



app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username = form.username.data
    password = form.password.data
    if not(username is None or password is None) and form.login_button.data: 
        session['isshow'] = [False, False]
        session['cardnumber'] = form.cardnumber.data
        session['username'] = username
        opponents= ['John', 'Tom', 'Mary', 'Amy']
        session['opponent'] = opponents[random.randint(0, len(opponents)-1)]
        return  redirect(url_for('mainpage',password=password, username=username))

    return render_template('login.html', form = form, message = '' )
        
@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    form = BookingForm()
    is_show = session['isshow']
    decker_files = ['decker2.png','decker2.png','decker2.png','decker2.png','decker2.png']
    
 

    if not is_show[0] and not is_show[1]:
        cardnumber = session.get('cardnumber')
        username = session.get('username')
        opponentname = session.get('opponent')
        form.cardnumber.data = cardnumber
        if cardnumber =='20':
            CardSet.card_number =[10,14]
        else:
            CardSet.card_number =[1,13]

        player1 = CardSet()
        player2 = CardSet()
        session['hands'] = (player1.new_hand,player2.new_hand) 
        session['cardnumber'] = cardnumber

        player1_cardset = player1.cards.split(' ');
        opponent_cardset = player2.cards.split(' ')
        
        p_ranking, p_score, p_weight = PokerHand.ranking(player1_cardset)
        op_ranking, op_score, op_weight = PokerHand.ranking(opponent_cardset)

        
        print(player1.cards)
        winstr = ''
        win_string = ''
        if p_score > op_score:
            win_string = 'Player ' + username + ' wins'
        elif p_score < op_score:
            win_string = 'Opponent '+ opponentname + ' wins'
        else:
            win_string = 'It is a tie'
            for p, op in zip(p_weight,op_weight):
                if not p==op:
                    if p>op:
                        win_string = 'Player ' + username + ' wins'
                    else:
                        win_string = 'Opponent '+ opponentname + ' wins'
                    break
        p1 = player1.cards +', ' + p_ranking
        p2 = player2.cards +', ' + op_ranking
        player_card_files = decker_files
        opponent_card_files = decker_files
        playerstr = 'Players: ' + username +' (player) and ' + opponentname + ' (opponent) '
        cardgamestr = 'Current game is a '+ cardnumber + ' cards poker game'
        
        session['username'] = username
        session['opponent'] = opponentname
        session['winstring'] = win_string


    if form.showplayercard.data or form.showopponentcard.data:
        cardnumber = session.get('cardnumber')
        username = session.get('username')
        opponentname = session.get('opponent')
        player_hand, opponent_hand = session.get('hands')
        win_string = session.get('winstring')
        is_show = session.get('isshow')

        form.cardnumber.data = cardnumber
        player_cards, player_card_files = convert_tuple_to_cards(player_hand)
        opponent_cards, opponent_card_files = convert_tuple_to_cards(opponent_hand)
        player_cardset = player_cards.split(' ');
        opponent_cardset = opponent_cards.split(' ')
        p_ranking, p_score, p_weight = PokerHand.ranking(player_cardset)
        op_ranking, op_score, op_weight = PokerHand.ranking(opponent_cardset)
        pres = player_cards +', ' + p_ranking
        opres = opponent_cards +', ' + op_ranking
        
        print(is_show )
        if form.showplayercard.data and not is_show[0]:
            session['isshow'] = [True, is_show[1]]
        if form.showopponentcard.data and not is_show[1]:    
            session['isshow'] = [is_show[0], True]
        is_show = session.get('isshow')
        print(is_show )
        winstr=''
        if not is_show[0]:
            player_card_files = decker_files
            pres = ''
        if not is_show[1]:
            opponent_card_files = decker_files
            opres = ''
        if is_show[0] and is_show[1]:
            winstr = win_string

        print(opponent_card_files)
        card_files = opponent_card_files
        session['hands'] = [player_hand, opponent_hand]
        session['winstring'] = win_string
        session['cardnumber'] = form.cardnumber.data
        session['username'] = username
        session['opponent'] = opponentname
        playerstr = 'Players: ' + username +' (player) and ' + opponentname + ' (opponent) '
        cardgamestr = 'Current game is a '+ cardnumber + ' cards poker game'
        
        
        
        return render_template('pokergame.html', form = form, \
            player = playerstr, cardnumber=cardgamestr, \
                playerhand = pres, opponenthand = opres, winstring = winstr, filenames = player_card_files, op_filenames = card_files)


    
    if form.newgame.data:
        session['isshow'] = [False, False]
        CardSet.all_hands = []
        session['cardnumber'] = form.cardnumber.data
        username = session.get('username')
        opponentname = session.get('opponent')
        cardnumber = form.cardnumber.data
        player_card_files = decker_files
        opponent_card_files = decker_files
        playerstr = 'Players: ' + username +' (player) and ' + opponentname + ' (opponent) '
        cardgamestr = 'Current game is a '+ cardnumber + ' cards poker game'
        session['username'] = username
        session['opponent'] = opponentname


    return render_template('pokergame.html', form = form, \
        player = playerstr, cardnumber=cardgamestr, \
            playerhand = '' , opponenthand = '', winstring = '', \
                filenames = player_card_files, \
                    op_filenames = opponent_card_files)



if __name__ == '__main__':
     app.run(host='0.0.0.0') 