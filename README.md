# Poker Game with Cards
## Contributor: Sabina Ku

This solution contains four Python program files, 

1. poker.py: This file is a simple poker game. In the game, there are two players, the player and the opponent. The program will generate one hand (5 cards) for each player. The program will determine the winner based on the cards they get in each game.
2. cardset.py: this file contains the class CardSet, a class of a card set (set of 5 cards) with methods to generate a hand for the player and convert the cards into a string.  
3. pokerhand.py: this file contains the class PokerHand. This class accepts a string which stands for 5 cards when it is initiated. This class has methods to rank a hand and compare the hands to determine the winner of the game.
4. tests.py: This file is used to test some of the functions in porker.py.
     
This test solution is about the poker game. Let's start the game.

## 1. The Game   

### 1-1. Start Session 

The game starts from a greeting message and the information about the set-up. There are two different set-ups of the game, based on the number of cards:

- The stripped 20-card deck: each suit only contains 5 cards of 10, J, Q, K and A
- The standard 52-card deck

Players will be asked to choose one of them before the game starts.

#### Unless specified, the following explanation assuming the users select standard 52-card deck. The only difference between stripped 20-card and standard 52-card game is the number of cards used. 

### 1-2. Game Session 

Once the game starts, in each game, the computer will randomly choose 5 cards for the players, player and opponent. The computer will choose 5 cards from 52 cards for the player first and choose 5 cards from the remaining 47 cards for the opponent next.

The program will classify each hand into one of the 10 possible rankings. Based on the rankings, the program will determine the winner and the current game ends here.

The users can keep playing by pressing 'Enter' key or input no to quit the game session.

### 1-3. Ending Session  

The game ends with a summary of the game session showing how many games have been played and the distribution of the game result, i.e the number of the games in terms of TIE, WON and LOST followed by a good-bye message.

The core of this program is the classification of the ranking. It will be explained next.
There are two *classes* ***CardSet*** and ***PokerHand***. For detailed codes, please see files cardset.py and pokerhand.py. 

    class CardSet:
    #a card set (set of 5 cards) class with methods to generate the card set(5 cards) and convert the card to a string in the format specified 
    #two class variables, all_hands, and card_number 
    #all_hands is the list of the cards that have been dealt, used it to avoid the card is dealt more than once
    #card_number is [1, 13] by default. If 20-card deck game is selected, card_number = [10, 14]
    all_hands = []
    card_number = [1,13]
    def __init__(self) :
        self.new_hand = []
        num_of_cards = 5
        self.deal_cards(num_of_cards)
        self.convert_tuple2cards() 

    def deal_cards(self, num_of_cards):
        #this function generate 5 cards in random, each card is a tuple with (value, suit)
        #both value and suit are numeric

    def convert_tuple2cards(self):
        #this function convert card in tuple to string


and 

    class PokerHand:
    def __init__(self, hand):
        self.hand = hand

    def compare_with(self, opponent):
        #this function gives a ranking to each hand and compares the player's and oppentnt's rankings
        # to determine the winner
        # input: oppenent
        # output: 0, 1 or 2; 0, 1, 2 stand for a tie, player wins and player loses respectively

    @staticmethod
    def ranking(player_cardset):
    #this function classifies the hand into a ranking and returns the classification result 
    #to determine the winner


## 2. The Ranking Process  
The ranking of the hands follows the rules in [Texas Hold'em rules](http://www.wsop.com/how-to-play-poker/images/how-to-ranking.jpg). In short, there are 10 rankings as followed,

- ROYAL FLUSH
- STRAIGHT FLUSH
- 4 of A KIND
- FULL HOUSE
- FLUSH
- STRAIGHT
- 3 of A KIND
- 2 PAIR
- 1 PAIR
- HIGH CARD 

These 10 rankings can be further divided into three categories,

1. **Flush or Straight:** with the same suit or values of cards in sequence
2. **Pair**: At least two cards with the same values
3. **Nothing**: 5 cards with 5 values, at least two suits, values are not in sequence.

The ranking process will identify the hand as category 1 or (2,3). With further examination on the characteristics of the hand to get the proper ranking. 

This task is performed by two methods in the *class* ***PokerHand***,

#### Instance Method, ***'compare_with'***: 

    def compare_with(self, opponent):
    #this function gives a ranking to each hand and 
    #compares the player's and oppentnt's rankings
    # to determine the winner
    # input: oppenent
    # output: 0, 1 or 2; 0, 1, 2 stand for a tie, player wins and player loses respectively
   
and 
### Static Method, ***'ranking'***

    @staticmethod
    def ranking(player_cardset):
    #this function classifies the hand into a ranking and returns the classification result 
    #to determine who is the winner
    #input: players' card set in a list
    #output: ranking, scores and weight list
    #   ranking: one of 10 rankings depending on the combination of the cards in one hand.
    #   score: Each ranking will be given a score, varying from 1 (lowest) to 10 (highest).
    #   Ranking score is primarily used to determine the winner. 
    #   Weight list: minor scores used to determine the winner when ranking scores are the same


The outcome/goal of the poker game is to determine the winner.

## 3. The Winner is 
     
In most case, the winner of each game can be determined by the ranking score. However, in the tie situation, i.e two hands are the same ranking. The ***weight list***, output of ***ranking*** function in *class* ***PokerHand*** can be used to determined the winner.

The score and weight list of each ranking is as follows,

    ROYAL FLUSH- 10, []
    STRAIGHT FLUSH- 9, [highest value in 5 cards]
    4 of A KIND- 8, [value of quadruplet]
    FULL HOUSE- 7, [value of triplet]
    FLUSH'- 6, [5 card values in descending order]
    STRAIGHT- 5, [highest value in 5 cards]
    3 of A KIND- 4, [value of triplet]
    2 PAIR- 3, [value of highest pair, value of the second pair, value of the 5th card ]
    1 PAIR- 2 [value of the pair, the values of the rest three cards in descending order]
    HIGH CARD- 1, [5 card values in descending order] 

**Please be noted that the rules described in tie situation in this document to determine the winner are based on one deck game. Some of them might not be able to apply to more than one deck game.**

For example, if two players get 3 of a kind. The player who has the highest value of triplets is the winner. In one-deck game, two hands of 3(or 4) of A kind with the same value of triplet (quadruplet) won't appear at the same time. Therefore, for 4 of A Kind, FULL HOUSE and 3 of A KIND tie situation, the value of quadruplet and triplet is enough to determine the winner.
However, for two pairs, compare the values of two pairs and the 5th card might be necessary . If these three values are the same, it is a tie.

## 4. The test

The Python file, tests.py is primarily used to test the codes of the functions, ***compare_with*** and ***ranking*** in *class* ***PokerHand***. It ran 16 tests successfully in 6.080s
Poker Game Unittest result:
Screenshot from VSCode:


 
Full Unittest:

Player's hand -- 3S 3D 2D 3H 3C, 4 OF A KIND, [3]

.......

Opponent's hand -- 5H 5C 5D TH QH, 3 OF A KIND, [5]

.Player's hand -- TD 9S QS QH TH, 2 PAIR, [12, 10, 9]

.......

Opponent's hand -- 5D 5S QC 9H QH, 2 PAIR, [12, 5, 9]

.Player's hand -- 3S 3D 2D 2H 9C, 2 PAIR, [3, 2, 9]

.......

Opponent's hand -- 3H AC 3C 2C 2S, 2 PAIR, [3, 2, 14]

...........Player's hand -- TD AD QD JD KD, ROYAL FLUSH, []

.......

Opponent's hand -- KH JH AH TH QH, ROYAL FLUSH, []

.Player's hand -- TD AD QD JD KD, ROYAL FLUSH, []

.......

Opponent's hand -- 5D 5S 5C 5H QH, 4 OF A KIND, [5]

.Player's hand -- TH 8C 6D 9H 7H, STRAIGHT, [10]

.......

Opponent's hand -- 5S 8D 6C 7H 9C, STRAIGHT, [9]

.
----------------------------------------------------------------------
Ran 16 tests in 6.128s

OK
