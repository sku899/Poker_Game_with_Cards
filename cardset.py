#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

class CardSet:
    #a a card set(set of 5 cards) class with metods to generate the card set(5 cards) and convert the card to a string in the format specified
    #two class variables, all_hands, and card_number 
    #all_hands is the list of the cards that have been dealt, used it to avoid the crad is dealt more than once
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
        for i in range(num_of_cards):
            is_repeated = True
            while is_repeated:
                # next_card is a tuple with (value, suit)
                val = random.randint(CardSet.card_number[0], CardSet.card_number[1])
                if val ==14:
                    val = 1
                next_card = (val, random.randint(1, 4))
                is_repeated = next_card in CardSet.all_hands
            self.new_hand.append(next_card)
            CardSet.all_hands.append(next_card)            
        #print(self.new_hand)
        #print(CardSet.all_hands)


    def convert_tuple2cards(self):
        #this function convert card in tuple to string
        self.cards = ''
        valDict ={1: 'ace', 10:'ten', 11:'jack', 12:'queen', 13:'king'}
        suitDict ={1:'spades',2:'hearts',3:'diamonds',4:'clubs'}
        card_files=[]
        for val, suit in self.new_hand:
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
            self.cards = self.cards  + card
        self.cards = self.cards[0:-1]
        print(card_files)
        self.card_files = card_files

        # @staticmethod
        # def convert_tuple_to_cards(new_hand):
        #     #this function convert card in tuple to string
        #     cards = ''
        #     valDict ={1: 'ace', 10:'ten', 11:'jack', 12:'queen', 13:'king'}
        #     suitDict ={1:'spades',2:'hearts',3:'diamonds',4:'clubs'}
        #     card_files=[]
        #     for val, suit in new_hand:
        #         card = ''
        #         file_string =''
        #         if val in [1, 10, 11, 12, 13]:
        #             card = card + valDict[val][0].upper()
        #             file_string = valDict[val]
        #         else:
        #             card = card + str(val)
        #             file_string =str(val)
        #         card = card + suitDict[suit][0].upper() + ' '
            
        #         file_string = file_string + '_of_'+suitDict[suit] +'.png'
        #         card_files.append(file_string)
        #         self.cards = self.cards  + card
        #     return cards[0:-1], card_files