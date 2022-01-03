import re
import os
import sys
import time
import json
import random
import subprocess
from itertools import groupby, count

class DouDiZhu:
    def __init__(self):
        self.cards_dict = {
            "pass": 0,
            "3":    1,
            "4":    2,
            "5":    3,
            "6":    4,
            "7":    5,
            "8":    6,
            "9":    7,
            "10":   8,
            "J":    9,
            "Q":    10,
            "K":    11,
            "A":    12,
            "2":    13,
            "BW-Joker": 14,
            "CL-Joker": 15
        }

        self.leftovers = []
        self.user_deck = []
        self.cpu_one_deck = []
        self.cpu_two_deck = []

        self.round = 1

        self.dizhu = -1 # player who is dizhu (1=user, 2=cpuOne, 3=cpuTwo)
        self.play_order = [0, 0, 0]

        self.double = False
        self.chain = False

        self.chain_len = 0

        # 0->any
        # 1->single
        # 2->double
        # 3->chaining
        self.type = 0

    
    def play_game(self):
        os.system("cls")
        self.round = 0

        print("A new game has started!")
        self.generate_cards()
        print(f"\nYour deck of cards: {self.deck_to_string()}")

        # select Di Zhu
        dizhu_select = self.prompt_user_input(card=False)
        if dizhu_select == '00':
            self.set_dizhu(player=1)
        elif dizhu_select == '01':
            self.set_dizhu(player=random.randint(2, 3))

        self.print_decks()
        self.generate_play_order()
        # time.sleep(3)

        self.start_round()

        
        
    def start_round(self):

        largest_card_val = 0
        pass_count = 0

        while self.win_check() == False:
            print(f'\nRound {self.round} ==============================================================================')
            print(f"Your deck of cards: \t{self.deck_to_string()}")
            print(f"CPU One Deck: \t\t{self.deck_to_string(player=2)}")
            print(f"CPU One Deck: \t\t{self.deck_to_string(player=3)}\n")

            for player in self.play_order:
                
                card = self.play_cards(player_num=player, base_value=largest_card_val)

                if card != 'pass':
                    pass_count = 0

                if card == 'pass':
                    pass_count += 1

                    if pass_count == 2: # next player can play any cards (largest + type gets reset)
                        largest_card_val = self.cards_dict[card]
                        pass_count = 0
                        self.type = 0 # reset type to any

                    continue
                
                largest_card_val = self.cards_dict[card]
            
            self.round += 1


    def play_cards(self, player_num=0, base_value=0):
        
        # if player_num == 1:
        #     return self.prompt_user_input(card=True, base_value=base_value)



        # CPU play cards ////////////////////////////////////////////////////
        if player_num == 1:

            if self.type == 0 or self.type == 1:
                for card in self.user_deck:
                    if self.cards_dict[card] > base_value:

                        self.type = 1
                        print(f'CPU Zero: {card}')
                        self.user_deck.remove(card)
                        return card
                
                print(f'CPU Zero: pass')
                return 'pass'
            else:
                print(f'CPU Zero: pass')
                return 'pass'


        if player_num == 2:

            if self.type == 0:
                chain_out = self.CPU_search_chain(cpu=2, base_value=base_value)
                if chain_out != None:
                    self.type = 3
                    print(f'CPU One: {chain_out}')
                    return chain_out[0]
                else:
                    card_out = self.CPU_search_double(cpu=2, base_value=base_value)
                    if card_out != None:
                        self.type = 2
                        print(f'CPU One: {card_out} {card_out}')
                        return card_out
                    else:
                        for card in self.cpu_one_deck:
                            if self.cards_dict[card] > base_value:

                                print(f'CPU One: {card}')
                                self.cpu_one_deck.remove(card)

                                self.type = 1 # set to type single
                                return card

                        print(f'CPU One: pass')
                        return 'pass'


            if self.type == 1:
                for card in self.cpu_one_deck:
                    if self.cards_dict[card] > base_value:

                        print(f'CPU One: {card}')
                        self.cpu_one_deck.remove(card)

                        self.type = 1 # set to type single
                        return card
                
                print(f'CPU One: pass')
                return 'pass'

            elif self.type == 2:
                card_out = self.CPU_search_double(cpu=2, base_value=base_value)

                if card_out == None:
                    print(f'CPU One: pass')
                    return 'pass'
                else:
                    self.type = 2
                    print(f'CPU One: {card_out} {card_out}')
                    return card_out

            elif self.type == 3:
                chain_out = self.CPU_search_chain(cpu=2, base_value=base_value)

                if chain_out == None:
                    print(f'CPU One: pass')
                    return 'pass'
                else:
                    self.type = 3
                    print(f'CPU One: {chain_out}')
                    return chain_out[0]

            else:
                print(f'CPU One: pass')
                return 'pass'


        if player_num == 3:

            if self.type == 0:
                chain_out = self.CPU_search_chain(cpu=3, base_value=base_value)
                if chain_out != None:
                    self.type = 3
                    print(f'CPU Two: {chain_out}')
                    return chain_out[0]
                else:
                    card_out = self.CPU_search_double(cpu=3, base_value=base_value)
                    if card_out != None:
                        self.type = 2
                        print(f'CPU Two: {card_out} {card_out}')
                        return card_out
                    else:
                        for card in self.cpu_two_deck:
                            if self.cards_dict[card] > base_value:

                                print(f'CPU Two: {card}')
                                self.cpu_two_deck.remove(card)

                                self.type = 1 # set to type single
                                return card

                        print(f'CPU Two: pass')
                        return 'pass'


            if self.type == 1:
                for card in self.cpu_two_deck:
                    if self.cards_dict[card] > base_value:

                        print(f'CPU Two: {card}')
                        self.cpu_two_deck.remove(card)

                        self.type = 1 # set to type single
                        return card
                
                print(f'CPU Two: pass')
                return 'pass'

            elif self.type == 2  or self.type == 0:
                card_out = self.CPU_search_double(cpu=3, base_value=base_value)

                if card_out == None:
                    print(f'CPU Two: pass')
                    return 'pass'
                else:
                    self.type = 2
                    print(f'CPU Two: {card_out} {card_out}')
                    return card_out

            elif self.type == 3:
                chain_out = self.CPU_search_chain(cpu=3, base_value=base_value)

                if chain_out == None:
                    print(f'CPU Two: pass')
                    return 'pass'
                else:
                    self.type = 3
                    print(f'CPU Two: {chain_out}')
                    return chain_out[0]
            else:
                print(f'CPU Two: pass')
                return 'pass'


    def CPU_search_chain(self, cpu=0, base_value=0):
        if cpu == 0 or cpu == 1:
            print('Error: cpu number incorrect.')
            sys.exit(0)

        elif cpu == 2:
            self.sort_deck(player=2)
            comb = self.process_combination(self.cpu_one_deck)

            # min len == 3 and first element must be > base value
            new_comb = [chain for chain in comb if len(chain) >= 3 and self.cards_dict[chain[0]] > base_value]

            print(new_comb)

            if len(new_comb) == 0:
                return None

            max_length = 2
            ret_chain = []
            if self.chain_len == 0:
                for chain in new_comb:
                    if len(chain) > max_length:
                        max_length = len(chain)
                        ret_chain = chain
                
                self.chain_len = max_length
                for card in ret_chain: self.cpu_one_deck.remove(card)
                return ret_chain

            for chain in comb:
                if len(chain) == self.chain_len:
                    if len(ret_chain) == 0:
                        ret_chain = chain
                    else:
                        if self.cards_dict[ret_chain[0]] > self.cards_dict[chain[0]]:
                            ret_chain = chain
            
            if len(ret_chain) == 0:
                return None
            else:
                for card in ret_chain: self.cpu_one_deck.remove(card)
                return ret_chain

        elif cpu == 3:
            self.sort_deck(player=3)
            comb = self.process_combination(self.cpu_two_deck)

            # min len == 3 and first element must be > base value
            new_comb = [chain for chain in comb if len(chain) >= 3 and self.cards_dict[chain[0]] > base_value]

            print(new_comb)

            if len(new_comb) == 0:
                return None

            max_length = 2
            ret_chain = []
            if self.chain_len == 0:
                for chain in new_comb:
                    if len(chain) > max_length:
                        max_length = len(new_comb)
                        ret_chain = chain
                
                self.chain_len = max_length
                for card in ret_chain: self.cpu_two_deck.remove(card)
                return ret_chain

            for chain in comb:
                if len(chain) == self.chain_len:
                    if len(ret_chain) == 0:
                        ret_chain = chain
                    else:
                        if self.cards_dict[ret_chain[0]] > self.cards_dict[chain[0]]:
                            ret_chain = chain
            
            if len(ret_chain) == 0:
                return None
            else:
                for card in ret_chain: self.cpu_two_deck.remove(card)
                return ret_chain
        
    def process_combination(self, sequence):
        result = []
        for s in sequence:
            if not result or self.cards_dict[s] != self.cards_dict[result[-1][-1]] + 1:
                result.append([])
            result[-1].append(s)
        return result

    def CPU_search_double(self, cpu=0, base_value=0):
        if cpu == 0 or cpu == 1:
            print('Error: cpu number incorrect.')
            sys.exit(0)

        double_list = []

        if cpu == 2:
            prev = ''
            for card in self.cpu_one_deck:
                if card == prev: double_list.append(prev)
                else: prev = card

            double_set = list(set(double_list))
            double_list = self.sort_cards(double_set)

            # print(f'double set: {double_list}')

            for card in double_list:
                if self.cards_dict[card] > base_value:
                    self.cpu_one_deck.remove(card)
                    self.cpu_one_deck.remove(card)
                    return card
            return None
        
        elif cpu == 3:
            prev = ''
            for card in self.cpu_two_deck:
                if card == prev: double_list.append(prev)
                else: prev = card

            double_set = list(set(double_list))
            double_list = self.sort_cards(double_set)

            for card in double_list:
                if self.cards_dict[card] > base_value:
                    self.cpu_two_deck.remove(card)
                    self.cpu_two_deck.remove(card)
                    return card
            return None 



    def generate_cards(self):
        deck_of_cards = []
        for card in self.cards_dict.keys():
            for count in range(4):
                if card != "BW-Joker" and card != "CL-Joker" and card != 'pass':
                    deck_of_cards.append(card)
        deck_of_cards.append("BW-Joker")
        deck_of_cards.append("CL-Joker")

        deck_of_cards = self.shuffle_cards(deck_of_cards)

        self.leftovers = deck_of_cards[len(deck_of_cards) - 3:]
        deck_of_cards = deck_of_cards[:len(deck_of_cards) - 3]

        self.user_deck = deck_of_cards[:16]
        deck_of_cards = deck_of_cards[17:]

        self.cpu_one_deck = deck_of_cards[:16]
        deck_of_cards = deck_of_cards[17:]

        self.cpu_two_deck = deck_of_cards[:16]
        deck_of_cards = deck_of_cards[17:]
        
        self.verify_cards()
        self.sort_deck()
        
    def shuffle_cards(self, deck_of_cards: list):
        shuffle_count = len(deck_of_cards) * 10000

        for i in range(shuffle_count):
            rand_idx_one = random.randint(0, len(deck_of_cards) - 1)
            rand_idx_two = random.randint(0, len(deck_of_cards) - 1)

            if rand_idx_one == rand_idx_two:
                rand_idx_two -= 1

            card_temp = deck_of_cards[rand_idx_one]
            deck_of_cards[rand_idx_one] = deck_of_cards[rand_idx_two]
            deck_of_cards[rand_idx_two] = card_temp

        return deck_of_cards

    def verify_cards(self):
        assert len(self.leftovers) == 3
        assert len(self.user_deck) == 16
        assert len(self.cpu_one_deck) == 16
        assert len(self.cpu_two_deck) == 16


    def sort_deck(self, player=0):
        # player=0 -> all players
        # player=1 -> user
        # player=2 -> cpu one
        # player=3 -> cpu two

        if player % 1 == 0:
            for i in range(1, len(self.user_deck)):
                key_card = self.user_deck[i]
                key_val = self.cards_dict[self.user_deck[i]]
                j = i - 1

                while j >= 0 and key_val < self.cards_dict[self.user_deck[j]]:
                    self.user_deck[j + 1] = self.user_deck[j]
                    j -= 1
                self.user_deck[j + 1] = key_card


        if player % 2 == 0:
            for i in range(1, len(self.cpu_one_deck)):
                key_card = self.cpu_one_deck[i]
                key_val = self.cards_dict[self.cpu_one_deck[i]]
                j = i - 1

                while j >= 0 and key_val < self.cards_dict[self.cpu_one_deck[j]]:
                    self.cpu_one_deck[j + 1] = self.cpu_one_deck[j]
                    j -= 1
                self.cpu_one_deck[j + 1] = key_card

        if player % 3 == 0:
            for i in range(1, len(self.cpu_two_deck)):
                key_card = self.cpu_two_deck[i]
                key_val = self.cards_dict[self.cpu_two_deck[i]]
                j = i - 1

                while j >= 0 and key_val < self.cards_dict[self.cpu_two_deck[j]]:
                    self.cpu_two_deck[j + 1] = self.cpu_two_deck[j]
                    j -= 1
                self.cpu_two_deck[j + 1] = key_card

    def sort_cards(self, cards: list) -> list:


        for i in range(0, len(cards)):
            if cards[i].upper() == 'BJ':
                cards[i] = 'BW-Joker'
            elif cards[i].upper() == 'CJ':
                cards[i] = 'CL-Joker'
            else:
                cards[i] = cards[i].upper()

        for i in range(1, len(cards)):
            key_card = cards[i]
            key_val = self.cards_dict[cards[i]]
            j = i - 1

            while j >= 0 and key_val < self.cards_dict[cards[j]]:
                cards[j + 1] = cards[j]
                j -= 1
            cards[j + 1] = key_card
        return cards

    def prompt_user_input(self, card=True, base_value=0):
        # 00 -> True
        # 01 -> False
        # 10 -> Error

        if card == False: # dizhu select
            # dizhu_select = input('Would you like to become the Di Zhu? [y/n]')

            # if dizhu_select.lower() == 'y' or dizhu_select.lower() == 'yes':
            #     return '00'
            # elif dizhu_select.lower() == 'n' or dizhu_select.lower() == 'no':
            #     return '01'
            # else:
            #     print("Your input is not recognized. Please enter 'y' for yes or 'n' for no.")
            #     return self.prompt_user_input(card=False)
            return '01'

        if card == True:
            card_selected = input("Your turn: ")
            card_selected = card_selected.lower()

            if card_selected == 'pass':
                return "pass"

            # TODO: needs to parse the input to find the type (single, chaining, double)
            ret_double = re.search("^[a-zA-Z0-9]+ [a-zA-Z0-9]+$", card_selected)
            ret_chain = len(card_selected.split(' ')) >= 3

            is_double = ret_double != None
            is_chain = ret_chain
            curr_type = -1


            # get type
            if self.type != 0:
                if is_double == False and is_chain == False:
                    curr_type = 1
                elif is_double == True and is_chain == False:
                    curr_type = 2
                elif is_double == False and is_chain == True:
                    curr_type = 3

            if curr_type != self.type and self.type != 0:
                if self.type == 1:
                    print("Your input must match the previous card's type. You must enter a single card!")
                elif self.type == 2:
                    print("Your input must match the previous card's type. You must enter a double (2-cards of the same value)!")
                elif self.type == 3:
                    print(f"Your input must match the previous card's type. You must enter chain of length {self.chain_len}!")
                return self.prompt_user_input(card=True, base_value=base_value)

            # set type
            if self.type == 0:
                self.double = is_double
                self.chain = is_chain
                self.chain_len = 0

                if self.double == False and self.chain == False:
                    self.type = 1
                elif self.double == True and self.chain == False:
                    self.type = 2
                elif self.double == False and self.chain == True:
                    self.type = 3
                    self.chain_len = len(card_selected.split(' '))

                curr_type = self.type
                print(f'The type has been reset to {self.type}')


            # single card ==============================================================================
            if curr_type == 1:
                card_out = self.select_single_card_from_deck(card_selected)
                
                if card_out == None: # card doesn't exist in deck
                    print("You do not have this card. Please re-enter a card.")
                    return self.prompt_user_input(card=True, base_value=base_value)

                if self.cards_dict[card_out] <= base_value:
                    self.user_deck.append(card_out) # put the card removed back
                    self.sort_deck(player=1)

                    print("Your card must be larger than the previous card! Please re-enter a card.")
                    return self.prompt_user_input(card=True, base_value=base_value)

                if card_out != None: # card correct selected
                    # print("Card out successful!")
                    # print(f"Your deck of cards: {self.deck_to_string()}")
                    return card_out
            
            # double cards ==============================================================================
            if curr_type == 2:
                [card_one, card_two] = re.search("^[a-zA-Z0-9]+ [a-zA-Z0-9]+$", card_selected).group(0).split(' ')
                card_one = card_one.upper()
                card_two = card_two.upper()

                if card_one != card_two: # incorrect double: two cards do not match
                    print("The two cards you entered do not match! Please re-enter your card.")
                    print(f"Your deck of cards: {self.deck_to_string()}")
                    return self.prompt_user_input(card=True, base_value=base_value) 

                if self.cards_dict[card_one] < base_value:
                    print("Your card must be larger than the previous entry! Please re-enter your input.")
                    print(f"Your deck of cards: {self.deck_to_string()}")
                    return self.prompt_user_input(card=True, base_value=base_value)

                card_out = self.select_double_cards_from_deck(card_one)
                
                if card_out == None:
                    print("You do not possess one or more of these cards. Please re-enter your input.")
                    print(f"Your deck of cards: {self.deck_to_string()}")
                    return self.prompt_user_input(card=True, base_value=base_value)

                else:
                    # print("Card out double successful!")
                    # print(f"Your deck of cards: {self.deck_to_string()}")
                    return card_out

            # chaining ==================================================================================
            if curr_type == 3:
                # print("chaining detected")
                
                chain = card_selected.split(' ')

                #print(f'Input chain: {chain}')
                for card in chain:
                    if card == '':
                        print("You entry is not recognized (do not include extra spaces). Please en-enter your input.")
                        return self.prompt_user_input(card=True, base_value=base_value)

                chain = self.sort_cards(chain)

                prev_card = 'pass'
                for card in chain:

                    if self.cards_dict[card] == self.cards_dict[prev_card]:
                        print("Your input's order is incorrect (two of the same cards detected). Please en-enter your input.")
                        return self.prompt_user_input(card=True, base_value=base_value)
                    
                    # print(f"card: {card}-{self.cards_dict[card]}, prev: {prev_card}-{self.cards_dict[prev_card]}")

                    if self.cards_dict[card] - 1 != self.cards_dict[prev_card]:
                        if prev_card == 'pass':
                            prev_card = card
                            continue
                        print("Your input's order is incorrect (only increments of 1 between cards is allowed). Please en-enter your input.")
                        return self.prompt_user_input(card=True, base_value=base_value)

                    prev_card = card

                card_out = self.select_chaining_cards_from_deck(chain)
                
                if card_out == None:
                    print("You do not possess one or more of these cards. Please re-enter your input.")
                    print(f"Your deck of cards: {self.deck_to_string()}")
                    return self.prompt_user_input(card=True, base_value=base_value)

                else:
                    # print("Card out chain successful!")
                    # print(f"Your deck of cards: {self.deck_to_string()}")
                    return card_out

            else:
                print("Error: double and chaining both true.")
                sys.exit(0)


    def select_chaining_cards_from_deck(self, chain_input):
        '''
        Searches for the a chain that the user selected in the user deck. 
        If found, remove from deck and return card. 
        If not, return None.

        :rytpe: str
        :ret: chain in string if found card is found in deck, None otherwise
        '''

        for card_in_chain in chain_input:
            if card_in_chain.upper() not in self.user_deck:
                return None

        for card_in_chain in chain_input:
            self.user_deck.remove(card_in_chain.upper())


        return chain_input[0] # return first element in chain

    def select_double_cards_from_deck(self, card_input):
        '''
        Searches for the a double that the user selected in the user deck. 
        If found, remove from deck and return card. 
        If not, return None.

        :rytpe: str
        :ret: double cards in string if found card is found in deck, None otherwise
        '''
        card_count = 0
        card_out = ''

        for card in self.user_deck:
            if card == card_input:
                
                card_out = card
                card_count += 1

        # print(f"card count: {card_count}")

        if card_count >= 2:
            self.user_deck.remove(card_out)
            self.user_deck.remove(card_out)
            return card_out

        return None

    def select_single_card_from_deck(self, card_input):
        '''
        Searches for the card that the user selected in the user deck. 
        If found, remove from deck and return card. 
        If not, return None.

        :rytpe: str
        :ret: card in string if found card is found in deck, None otherwise
        '''
        for card in self.user_deck:
            if card.lower() == card_input:

                self.user_deck.remove(card)
                return card

        if "CL-Joker" in self.user_deck and card_input == 'cj':
            self.user_deck.remove("CL-Joker")
            return "CL-Joker"
        if "BW-Joker" in self.user_deck and card_input == 'bj':
            self.user_deck.remove("BW-Joker")
            return "BW-Joker"

        return None


    def set_dizhu(self, player=1):
        # player=1 -> user
        # player=2 -> cpu one
        # player=3 -> cpu two

        print('\n')

        if player == 1:
            self.dizhu = 1

            self.user_deck += self.leftovers
            self.sort_deck(player=1)
            
            print("You have became the Di Zhu!")
            print(f"Your newly added cards: {self.deck_to_string(player=0)}")
            print(f"Your new deck of cards: {self.deck_to_string(player=1)}")

        if player == 2:
            self.dizhu = 2

            self.cpu_one_deck += self.leftovers
            self.sort_deck(player=2)
            
            print("CPU One has became the Di Zhu!")
            print(f"CPU One has gained cards: {self.deck_to_string(player=0)}")

        if player == 3:
            self.dizhu = 3

            self.cpu_two_deck += self.leftovers
            self.sort_deck(player=3)
            
            print("CPU Two has became the Di Zhu!")
            print(f"CPU Two has gained cards: {self.deck_to_string(player=0)}")

    def print_decks(self):
        print(self.user_deck)
        print(self.cpu_one_deck)
        print(self.cpu_two_deck)
        print(self.leftovers)
    
    def deck_to_string(self, player=1):
        # player=0 -> leftover cards
        # player=1 -> user
        # player=2 -> cpu one
        # player=3 -> cpu two

        str_deck = ''
        
        if player == 1:
            for i in range(len(self.user_deck)):
                if i != len(self.user_deck) - 1:
                    str_deck += self.user_deck[i] + ", "
                else:
                    str_deck += self.user_deck[i]
        if player == 2:
            for i in range(len(self.cpu_one_deck)):
                if i != len(self.cpu_one_deck) - 1:
                    str_deck += self.cpu_one_deck[i] + ", "
                else:
                    str_deck += self.cpu_one_deck[i] 
        if player == 3:
            for i in range(len(self.cpu_two_deck)):
                if i != len(self.cpu_two_deck) - 1:
                    str_deck += self.cpu_two_deck[i] + ", "
                else:
                    str_deck += self.cpu_two_deck[i] 
        if player == 0:
            for i in range(len(self.leftovers)):
                if i != len(self.leftovers) - 1:
                    str_deck += self.leftovers[i] + ", "
                else:
                    str_deck += self.leftovers[i] 
        
        return str_deck

    def generate_play_order(self):
        if self.dizhu == 1:
            self.play_order = [1, 2, 3]
        elif self.dizhu == 2:
            self.play_order = [2, 3, 1]
        elif self.dizhu == 3:
            self.play_order = [3, 1, 2]

    def win_check(self):
        if len(self.user_deck) == 0:
            print("The user has won!!! Congrats!")
            self.log_win(1)
            return True
        elif len(self.cpu_one_deck) == 0:
            print("Oh no! CPU One has won the game!")
            self.log_win(2)
            return True
        elif len(self.cpu_two_deck) == 0:
            print("Oh no! CPU Two has won the game!")
            self.log_win(3)
            return True
        return False


    def log_win(self, player):
        data = dict()

        with open('log.json', "r") as f:
            data = json.load(f)

            if player == 1:
                data['log'][0]['player1'] += 1
            elif player == 2:
                data['log'][1]['player2'] += 1
            elif player == 3:
                data['log'][2]['player3'] += 1

        with open('log.json', "w") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    game = DouDiZhu()

    # game.cpu_one_deck = ['3', '4', '5', '6', '7', '8', '8', '9', '9', '10', 'J', 'Q', 'Q', 'Q', 'K', 'K', 'K', '2', 'BW-Joker']
    # print(game.CPU_search_chain(cpu=2, base_value=0))
    count = 0

    while True:
        game.play_game()

