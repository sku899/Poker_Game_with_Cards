#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

class PokerHand:
    def __init__(self, hand):
        self.hand = hand

    def compare_with(self, opponent):
        #this function gives a ranking to each hand and compares the player's and oppentnt's the rankings
        # to determine the winner
        # input: oppenent
        # output: 0, 1 or 2, 0, 1, 2 stands for a tie, player wins and player loses respectively
        # 
        #  
        #print(self.cards);
        #print(opponent.cards);
        player_cardset = self.hand.split(' ');
        opponent_cardset = opponent.hand.split(' ')
        #print(player_cardset);
        #print(opponent_cardset);
        player_ranking, player_score, player_weight = PokerHand.ranking(player_cardset)
        opponent_ranking, opponent_score, opponent_weight = PokerHand.ranking(opponent_cardset)
        print(f"Player's hand -- {self.hand}, {player_ranking.upper()}, {player_weight}\n")
        print('.......\n')
        time.sleep(1)
        print(f"Opponent's hand -- {opponent.hand}, {opponent_ranking.upper()}, {opponent_weight}\n")

        if player_score > opponent_score:
            return 1 #player wins
        elif player_score < opponent_score:
            return 2 #player loses
        else:
            result = 0
            if player_score ==10:
                return 0 #royal flush
            else:
                for w1, w2 in zip(player_weight, opponent_weight):
                    if w1>w2:
                        result = 1;
                        break
                    elif w1<w2:
                        result =2 ;
                        break
            return result

    @staticmethod
    def ranking(player_cardset):
        #this function classifies the hand into a ranking and returns the classification result 
        #to determine who is the winner
        #input: players' card set in a list
        #output: ranking, scores and weight list
        #   ranking: could be one of the following 10 rankings depending on the combination of the cards in one hand.
        #   score: the score of the ranking. Each ranking will be given a ranking score, varying from 1 (lowest) to 10 (highest).
        #           Ranking score is primarily used to determine the winner. 
        #   weight list: list of numbers. When two hands are the same ranking, the weight list is used to determine the winner.
        #           *** Please be noted that the rule used in tie to determine the winner only apply to one deck.
        #               Some of them might not be able to apply to more than one deck game. 
        #           For example, if two players get 3 of a kind. The player who has the highest value of triplets is the winner. 
        #           In one-deck game, two hands of 3(or 4) of A kind with the same value of triplet (quadruplet) won't appear 
        #           at the same time. Therefore, for 4 of A Kind, FULL HOUSE and 3 of A KIND tie situation, 
        #           the value of quadruplet and triplet is enough to determine the winner.
        #           However, for two pairs, compare the values of two pairs and the the 5th card might be necessary . 
        #           If these three values are the same, it is a tie.
        #The following is the list of 10 rankings(from the highest to lowest), ranking scores and weight lists
        #'ROYAL FLUSH', 10, []
        #'STRAIGHT FLUSH', 9, [highest value in 5 cards]
        #'4 of A KIND', 8, [value of quadruplet]
        #'FULL HOUSE', 7, [value of triplet]
        #'FLUSH', 6, [5 card values in descending order]
        #'STRAIGHT', 5, [highest value in 5 cards]
        #'3 of A Kind', 4, [value of triplet]
        #'2 PAIR', 3, [value of highest pair, value of the second pair, value of the 5th card ]
        #'1 PAIR', 2 [value of the pair, the values of the rest three cards in descending order]
        #'HIGH CARD', 1, [5 card values in descending order] 
        
        player_card_val=[]
        is_flush = True
        first_suit = player_cardset[0][1]
        valDict ={'A':1, 'T':10, 'J':11, 'Q':12, 'K':13}
        for card in player_cardset:
            val = card[0]
            if  val.isdigit():
                val = int(val)
            else:
                val = valDict[val]
            player_card_val.append(val)
            if is_flush:
                is_flush = first_suit== card[1]
        
        is_straight = True
        max_step = len(player_card_val)
        min_val = min(player_card_val)
        if (1 in player_card_val) and (10 in player_card_val):
            min_val = 10
            max_step -=1
        
        for incre in range(1, max_step):
            if not (min_val+incre in player_card_val):
                is_straight = False  
                break
        
        player_card_val.sort(reverse=True)

        if (is_straight or is_flush):
            if min(player_card_val)==1:
                if ((is_straight and (10 in player_card_val)) or \
                    (not is_straight and is_flush)):
                    player_card_val[player_card_val.index(1)]=14
            if is_straight and is_flush:
                if 14 in player_card_val:
                    return ('ROYAL FLUSH', 10, [])
                else:
                    return ('STRAIGHT FLUSH', 9, [max(player_card_val)])
            elif is_flush:
                player_card_val.sort(reverse=True)
                return('FLUSH', 6, player_card_val)
            elif is_straight:
                return('STRAIGHT', 5, [max(player_card_val)]) 
        else: #check pair
            unique_vals = list(set(player_card_val))
            repeated_number =[]
            for unique_val in unique_vals:
                repeated_number.append(player_card_val.count(unique_val))
            if min(unique_vals)==1:
                unique_vals[unique_vals.index(1)] = 14

            if len(repeated_number) ==2:
                if max(repeated_number)==4:
                    weight = [unique_vals[repeated_number.index(4)]]
                    return ('4 of A KIND', 8, weight)
                else:
                    weight = [unique_vals[repeated_number.index(3)]]
                    return ('FULL HOUSE', 7, weight)
            elif len(repeated_number) ==3:
                if max(repeated_number)==3:
                    return ('3 of A KIND', 4, [unique_vals[repeated_number.index(3)]])
                else:
                    last_val = unique_vals[repeated_number.index(1)];
                    unique_vals.remove(last_val)
                    weight =[max(unique_vals), min(unique_vals), last_val]
                    return ('2 PAIR', 3, weight)
            elif len(repeated_number) ==4:
                pair_val = unique_vals[repeated_number.index(2)];
                unique_vals.remove(pair_val)
                unique_vals.sort(reverse=True)
                unique_vals.insert(0,pair_val)
                return ('1 PAIR', 2, unique_vals)
            else:
                unique_vals.sort(reverse=True)
                return ('HIGH CARD', 1, unique_vals )