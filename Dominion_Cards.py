# Dominion Card Resolution

from Dominion_Player import *
from Dominion_AI import *
from __builtin__ import set

# CONSIDER MOVING ALL OF THESE INTO THE PLAYER CLASS - WOULD DO AWAY WITH HAVING TO PASS A DUMMY SELF
class Card_Res(object):
	"""
	This class includes functions for the resolution of all complex Dominion cards in use in this simulation.
	Class structure is used so that getattr can call on the correct function using card name without having to name all 
	of these functions in the body of the program.
	
	Note: there are 2 categories of function: those that include opponent cards in input and those that do not.
	"""
	def __init__(self):
		self.name = "CARD FUNCTIONS"
		
	def Adventurer(self, player, Ref):
		T_counter = 0
		card_counter = 0
		card_total = len(player.deck) + 2*len(player.discard)
		while T_counter < 2: 
			if card_counter > card_total: break # VERIFY THAT THIS IS THE RIGHT NUMBER OF CARDS TO PULL
			# NOTE: in a deck/discard without money, this could loop forever!!! Fix this.
			card = player.pull(1)
			if card == []: return
			else: card = card[0]
			card_counter += 1
			if card in Ref.treasure_cards:
				player.hand.append(card)
			#	print "Adventurer drew and kept a", card
				T_counter += 1
			else:
				player.discard.append(card)
			#	print "Adventurer drew and discarded", card
		return

	def Baron(self, player, Ref):
		if 'Estate' in player.hand:
			player.card_discard('Estate')
			player.treasure += 4
		else:
			player.gain(Ref, 'Estate')
		return

	def Border_Village(self, player, Ref):
		return

	def Bureaucrat(self, player, opponents, Ref):
		player.gain_to_deck(Ref, 'Silver')
		for opponent in opponents:
			if opponent.defender(Ref, 'Margrave'): pass
			elif [x for x in opponent.hand if x in Ref.victory_cards]:
				opponent.hand_to_deck( [x for x in opponent.hand if x in Ref.victory_cards][0] )
			else: pass
				
	def Cellar(self, player, Ref): # ADD A TRY CLAUSE TO CALL ON AI FUNCTION SEPARATELY
		cards = []
		for i in range(len(player.hand)):
			if player.hand[i] in Ref.strict_victory_cards or ( player.turn > 4 and player.hand[i] == 'Copper' and player.wealth() != 8) or player.hand[i] == 'Curse' or player.hand[i] == 'Cellar':
				cards.append(player.hand[i])
		if cards == []: return
		else:
			number = len(cards)
			for i in range(number):
			#	print "Used Cellar to discard", cards[i]
				player.card_discard(cards[i])
			player.draw(number)
		#	print "After cellar draw, hand is", player.hand
		return
				
#	def Cartographer(self, player, Ref):	#### NOT FINISHED ###
#		temp = player.pull(4)
#		
#		
#		for i in [3,2,1,0]:
#			if temp[i] in Ref.strict_victory_cards + ['Copper']: 
#				player.discard.append(temp.pop(i))
#
#		num_draws = sum([Ref.add_card[x] for x in player.hand if x in Ref.add_card])
#		if num_draws == 0 or num_draws >= len(temp): player.deck += temp
#		else:
#			
#		currency = player.wealth()
#		num_draws = 0
#		for card in player.hand:
#			if card in Ref.add_card: num_draws += Ref.add_card[card]		
#		if num_draws == 0 or num_draws >= len(temp): player.deck += temp
#		else:		
#		return

	def Chancellor(self, player, Ref):
		# INCLUDE A TRY...EXCEPT
		player.discard += player.deck
		player.deck = []

	def Chapel(self, player, Ref): # FOR ADVANCED STRATEGIES, CHAPEL MIGHT HAVE TO BE ROUTED TO THE AI
		counter = 0
		while counter < 4:  # CONSIDER OTHER WAYS OF DOING THIS
			if 'Curse' in player.hand:
				player.hand.remove('Curse')
				counter += 1
			elif 'Estate' in player.hand:
				player.hand.remove('Estate')
			#	print "Trashing Estate"
				counter += 1
			elif 'Copper' in player.hand:
				if player.total('Copper') > 3:
					player.hand.remove('Copper')
			#		print "Trashing Copper"
					counter += 1
				elif player.total('Silver') > 0 and player.total('Copper') > 1:
					player.hand.remove('Copper')
			#		print "Trashing Copper"
					counter += 1
				elif player.total('Gold') > 0:
					player.hand.remove('Copper')
			#		print "Trashing Copper"
					counter += 1
				else: break
			else: break

	def Conspirator(self, player, Ref):
		if len(player.inplay) >= 3: 
			player.draw(1)
			player.action += 1
		return

	def Council_Room(self, player, opponents, Ref):
		for opponent in opponents:
			opponent.draw(1)
		return
		
	def Crossroads(self, player, Ref):
		if player.inplay.count('Crossroads') == 1: player.action += 3
		counter = 0
		for card in player.hand:
			if card in Ref.victory_cards:
				counter += 1
	#	print "Used Crossroads to draw", counter, "cards"
		player.draw(counter)

	def Cutpurse(self, player, opponents, Ref):
		for opponent in opponents:
			if opponent.defender(Ref, 'Cutpurse'): pass
			else: 
				if 'Copper' in opponent.hand:
					opponent.card_discard('Copper')

	def Embassy(self, player, Ref):
		self.friendly_to_deck(3)

	def Explorer(self, player, Ref):
		if 'Province' in player.hand:
			player.gain_to_hand(Ref, 'Gold')
		else:
			player.gain_to_hand(Ref, 'Silver')

	def Feast(self, player, opponents, Ref):
		store = player.treasure
	#	print "Using Feast, store value is", store
		player.treasure = 5
		card = ai_chooser('buy', player, opponents, Ref)
		player.gain(Ref, card)
		player.treasure = store
		player.inplay.remove('Feast')

	def Haven(self, player, Ref):
		money = player.wealth()
		# INCLUDE A TRY...EXCEPT AS NEEDED
		if player.hand.count('Treasure_Map') == 1: card = 'Treasure_Map'
		elif (money == 5 or money > 9) and 'Silver' in player.hand: card = 'Silver'			
		elif money != 3 and money != 6 and money != 8 and 'Copper' in player.hand: card = 'Copper'
		elif 'Estate' in player.hand: card = 'Estate'  # CLEAN THIS UP - GET SMART AND DO ALL OF THESE IN 1 LINE
		elif 'Duchy' in player.hand: card = 'Duchy' 
		elif 'Province' in player.hand: card = 'Province' 
		else: card = player.hand[0]
		player.hand.remove(card)
		player.haven.append(card)
		
	def Inn(self, player, Ref):
		player.friendly_discard(Ref, 2)
		
#	def Ironworks(self, player, Ref):
#		store = player.treasure
#	#	print "Using Ironworks, store value is", store
#		player.treasure = 4
#		card = ai_chooser('buy', player, [], Ref)
#		player.gain(Ref, card)
#		player.treasure = store
#	#	print "Player.treasure was restored and has value", player.treasure
#	#	print "You gained", card

	def Jack_of_All_Trades(self, player, Ref):
		player.gain(Ref, 'Silver')
		player.peek_discard(Ref)
		if len(player.hand) < 5:
			player.draw(5 - len(player.hand))
		#	print "New hand is", player.hand
		if 'Estate' in player.hand or 'Curse' in player.hand:
			if 'Curse' in player.hand: player.hand.remove('Curse')
			else: player.hand.remove('Estate')
		#	print "Jack trashed a card"
		return
	
	def Library(self, player, Ref):
		while len(player.hand) < 7:
			new = player.pull(1)[0]
			if new in Ref.action_cards and player.action == 0:	# MAKE THIS SMARTER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
				player.discard.append(new)
			else:
				player.hand.append(new)
	
	def Mandarin(self, player, Ref):
		card = ai_chooser('mandarin', player, [], Ref)
	#	print "The card returned to the top of the deck is", card
		player.hand_to_deck(card) 
		return
	
	def Margrave(self, player, opponents, Ref):
		for opponent in opponents:
			if opponent.defender(Ref, 'Margrave'): pass
			else: 
				opponent.draw(1)
				opponent.friendly_discard(Ref, len(opponent.hand)-3)			
	
	def Militia(self, player, opponents, Ref):
		for opponent in opponents:
			if opponent.defender(Ref, 'Militia'): pass
			else: opponent.friendly_discard(Ref, len(opponent.hand)-3)
	
	def Mine(self, player, Ref): # LATER ADD A TRY STATEMENT TO CHECK IF THE AI HAS OTHER INSTRUCTIONS
		if 'Copper' in player.hand:
			player.hand.remove('Copper')
			player.gain_to_hand(Ref, 'Silver')
			return
		elif 'Silver' in player.hand:
			player.hand.remove('Silver')
			player.gain_to_hand(Ref, 'Gold')
			return
		return		

	def Mining_Village(self, player, opponents, Ref):
		potential_money = player.wealth_action(Ref)
		losing_play = ( Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents ) )
		if (potential_money == 6 or potential_money == 7) and not losing_play:
			player.inplay.remove('Mining_Village')
			player.treasure += 2

	def Minion(self, player, opponents, Ref):
		if player.count_money() >= 6: player.treasure += 2; return    # CONDITION FOR +2 TREASURE NO ATTACK
		else:
			evaluator = 0
			for card in player.hand:
				if card not in Ref.strict_victory_cards: evaluator += Ref.card_cost[card]
			if evaluator >= 10: player.treasure += 2; return
			else:
				player.discard += player.hand
				player.hand = []
				player.draw(4)
				for opponent in opponents:
					if opponent.defender(Ref, 'Minion'): pass
					if len(opponent.hand) >= 5:
						opponent.discard += opponent.hand
						opponent.hand = []
						opponent.draw(4)
			
	def Moneylender(self, player, Ref):	 # NOTE: THIS DOESN"T WORK BECAUSE THE CHANGE TO 'treasure' ISN'T STORED ANYWHERE...RE-INCLUDE TREASURE AS AN ATTRIBUTE OF CLASS OBJECT PLAYER???
		if 'Copper' in player.hand:
			player.hand.remove('Copper')
			player.treasure += 3
		return
	
	def Noble_Brigand(self, player, opponents, Ref):  # ADD THE ACTION TO THE BUY ELEMENT
		for opponent in opponents:
			if opponent.defender(Ref, 'Noble_Brigand'): pass
			else:
				cards = opponent.pull(2)
				if 'Gold' in cards: 
					cards.remove('Gold')
					player.gain(Ref, 'Gold')
				elif 'Silver' in cards:
					cards.remove('Silver')
					player.gain(Ref, 'Silver')	
				elif not [x for x in cards if x in Ref.treasure_cards]:
					opponent.gain(Ref, 'Copper')
				opponent.discard.extend(cards)	
	
	def Nobles(self, player, Ref):
		trigger = 0
		for card in player.hand:
			if card in Ref.action_cards: trigger = 1
		if trigger == 1 and player.action == 0:
			player.action += 2
		#	print "Used Nobles to add 2 actions"
		else:
			player.draw(3)
		#	print "Used Nobles to draw 3 cards"

	def Oasis(self, player, Ref):
		player.friendly_discard(Ref, 1)
		player.draw(1); player.action += 1; player.treasure += 1
	
	def Oracle(self, player, opponents, Ref):
		for opponent in opponents:
			if opponent.defender(Ref, 'Oracle'): pass
			else:
				cards = opponent.pull(2)
	#			print "Oracle shows opponents top cards are", cards
				score = sum( [Ref.treasure_value[x] for x in cards if x in Ref.treasure_value] ) + sum( [Ref.add_card[x] for x in cards if x in Ref.add_card] ) +  sum( [Ref.add_treasure[x] for x in cards if x in Ref.add_treasure] ) + sum( [4 for x in cards if x in Ref.true_attack_cards] ) + sum( [1 for x in cards if x in Ref.action_cards] ) 
				if score > 2: opponent.discard += cards	#; print "Choose for opponent to discard"	# 2 a slightly better threshold than 3
				else: opponent.deck += cards			#; print "Choose for opponent to keep cards"
		cards = player.pull(2)
	#	print "Oracle reveals Oracle's cards are", cards
		if player.wealth() < 5:
			if player.wealth() + player.general_wealth(Ref, cards) + min(1, player.action)*sum([Ref.add_card[x] for x in cards+player.hand if x in Ref.add_card]) + min(1, player.action)*sum([Ref.add_treasure[x] for x in cards+player.hand if x in Ref.add_treasure]) >= 6:
				player.deck += cards					#; print "Chose to keep"
			else: player.discard += cards				#; print "Chose to discard"
		elif player.wealth_action(Ref) < 8:
			if player.wealth() + player.general_wealth(Ref, cards) + min(1, player.action)*sum([Ref.add_card[x] for x in cards+player.hand if x in Ref.add_card]) + min(1, player.action)*sum([Ref.add_treasure[x] for x in cards+player.hand if x in Ref.add_treasure]) >= 8:
				player.deck += cards					#; print "Chose to keep"
			else: player.discard += cards				#; print "Chose to discard"
		elif player.buy + min(1,player.action)*sum([Ref.add_buy[x] for x in cards+player.hand if x in Ref.add_buy]) > 1:
			if player.wealth() + player.general_wealth(Ref, cards) + min(1, player.action)*sum([Ref.add_card[x] for x in cards+player.hand if x in Ref.add_card]) + min(1, player.action)*sum([Ref.add_treasure[x] for x in cards+player.hand if x in Ref.add_treasure]) >= 11:
				player.deck += cards					#; print "Chose to keep"
			else: player.discard += cards				#; print "Chose to discard"
		else: player.deck += cards						#; print "Chose to keep"
		player.draw(2)
	
	def Pawn(self, player, Ref):
		# ADD A TRY...EXCEPT
		if player.action > 2: player.buy += 1
		else: player.action += 1
		player.draw(1)
		
	def Remodel(self, player, opponents, Ref):
		# ADD A TRY...EXCEPT FOR ANY COMPLEX STRATEGY
		if 'Estate' in player.hand or 'Curse' in player.hand: 
			card = player.standard_trash()
		#	print "Remodel selected", card, "for trashing"
			store = player.treasure
			player.treasure = Ref.true_cost(player, card) + 2
			new = ai_chooser('buy', player, opponents, Ref)
		#	print "Remodel opted to gain", new
			player.gain(Ref, new)
			player.treasure = store	
		else: pass 	# For now, only remodel estate, copper, curse
	
		
	def Saboteur(self, player, opponents, Ref):
		for opponent in opponents:
			if opponent.defender(Ref, 'Saboteur'): pass
			else:
				check = 0
				set_aside = []
				while check == 0:
					try: card = opponent.pull(1)[0]
					except: 
					#	print "Opponent has no 3 value cards"
						check = 1
					if Ref.card_cost[card] < 3:
						set_aside.append(card)
					else:
						opponent.treasure = Ref.card_cost[card] - 2
						dummies = opponents[:]
						dummies.append(player)
						new = ai_chooser('buy', opponent, dummies, Ref)
						if new is not False:
							opponent.gain(Ref, new)
						opponent.treasure = 0
						check = 1
				opponent.discard += set_aside
	
	def Salvager(self, player, Ref):	# THIS COULD BE MUCH SMARTER BOTH IN PROVINCE AWARENESS AND TREASURE AWARENESS
		# INCLUDE A TRY...EXCEPT HERE
		if 'Curse' in player.hand:
			player.hand.remove('Curse')
		elif 'Estate' in player.hand:
			player.hand.remove('Estate')
			player.treasure += 2
		elif 'Copper' in player.hand and (player.wealth() !=3 and player.wealth() !=6):
			player.hand.remove('Copper')
	
	def Sea_Hag(self, player, opponents, Ref):	
		for opponent in opponents:
			if opponent.defender(Ref, 'Sea_Hag'): pass
			else:
				opponent.discard.append( opponent.pull(1)[0] )
				opponent.gain_to_deck(Ref, 'Curse')
	
	def Scout(self, player, Ref):
		temp = player.pull(4)
		for i in reversed(range(len(temp))):
			if temp[i] in Ref.victory_cards:
				player.hand.append( temp.pop(i) )
		# NOTE: CURRENTLY DOESN'T ADJUST THE ORDER OF THE CARDS
		player.deck += temp
	
	def Shanty_Town(self, player, Ref):
		for card in player.hand:
			if card in Ref.action_cards: return
		player.draw(2)
		return
	
	def Spice_Merchant(self, player, Ref):	# THIS SHOULD ULTIMATELY INCLUDE OPPONENTS FOR PROV BUYING ANALYSIS
		try: ai_chooser('spice_merchant', player, [], Ref)
		except:
			if not 'Copper' in player.hand: return    # Could include analysis for nuking a silver for a 2 card draw - especially if gold bought and treasure == 7
			else:
				player.hand.remove('Copper')
			#	print "Trashed a Copper with Spice Merchant"
				true_cash = player.wealth() + 1  # this is money adjusted for trashed copper and the +2 from Spice Merchants money option
				if true_cash == 8:
					player.treasure += 2
					player.buy += 1
				else:
					player.action += 1
					player.draw(2)		
	
	def Spy(self, player, opponents, Ref):
		for opponent in opponents:
			if opponent.defender(Ref, 'Spy'): pass
			else:
				card = opponent.pull(1)[0]
				if card in Ref.strict_victory_cards or card == 'Curse' or (card == 'Copper' and opponent.turn > 5): opponent.deck.append(card)
				else: opponent.discard.append(card)
		card = player.pull(1)[0]
		if card in Ref.strict_victory_cards or card == 'Curse' or (card == 'Copper' and opponent.turn > 5): player.discard.append(card)
		else: player.deck.append(card)
				
	def Stables(self, player, Ref):
		if player.money_discard() == True:
			player.action += 1
			player.draw(3)
		#	print "New hand is", player.hand
		return	
		
	def Steward(self, player, Ref):
		try: ai_chooser('steward', player, [], Ref)
		except:
			if player.hand.count('Estate') + player.hand.count('Copper') + player.hand.count('Curse') >= 2 and player.wealth() < 6:
				for i in [1,2]:
					if 'Curse' in player.hand: player.hand.remove('Curse')
					elif 'Estate' in player.hand: player.hand.remove('Estate')
					elif 'Copper' in player.hand: player.hand.remove('Copper')
			elif player.wealth() == 4 or (player.wealth() >= 6 and player.wealth() < 8):
				player.treasure += 2
			else: player.draw(2)
		return
	
	def Thief(self, player, opponents, Ref):		# THIS COULD BE BETTER
		for opponent in opponents:
			if opponent.defender(Ref, 'Thief'): pass
			else:
				cards = opponent.pull(2)
				if cards[0] in Ref.treasure_cards and cards[1] in Ref.treasure_cards:
					cards.sort(key=lambda i: Ref.card_cost[i])
					card = cards.pop()
					if card != 'Copper': player.gain(Ref, card)
				elif cards[0] in Ref.treasure_cards or cards[1] in Ref.treasure_cards:
					if cards[0] in Ref.treasure_cards:
						card = cards.pop(0)
					else: card = cards.pop(1)
					if card != 'Copper': player.gain(Ref, card)
				opponent.discard += cards
	
	def Throne_Room(self, player, opponents, Ref):
		# USE A TRY...EXCEPT FOR COMPLEX STRATEGIES
		if not intersect(player.hand, Ref.action_cards): return
		action_cards = [x for x in player.hand if x in Ref.action_cards]
		action_cards.sort(key=lambda i:Ref.card_cost[i])
		card = action_cards.pop()
	#	print "Used Throne Room on", card
		for i in [0, 1]:
			if card in Ref.add_action: 
				player.action += Ref.add_action[card]
			if card in Ref.add_buy:
				player.buy += Ref.add_buy[card]
			if card in Ref.add_card:
				player.draw(Ref.add_card[card])
			if card in Ref.add_treasure:
				player.treasure += Ref.add_treasure[card]
			if card in Ref.add_victory:
				player.victory += Ref.add_victory[card]		
			if card in Ref.special_cards:
				card_play = getattr(Cards, card)
				card_play(player, Ref)
			if card in Ref.attack_cards:
				card_play = getattr(Cards, card)
				card_play(player, opponents, Ref)

	def Trader(self, player, Ref):
		card = []
		for c in ['Silver', 'Copper', 'Curse', 'Estate']: # BE MORE EFFICIENT
			if c in player.hand:
				card = c		
		if card != []:
			player.hand.remove(card)
		#	print "Using Trader to trash card", card
			for i in range(Ref.card_cost[card]):
				player.gain(Ref, 'Silver')
		#		print "Gain a Silver"
	
	def Trading_Post(self, player, Ref):
		if player.hand.count('Estate') + player.hand.count('Copper') + player.hand.count('Curse') >= 2:
			for i in [1,2]:
				if 'Curse' in player.hand: player.hand.remove('Curse')
				elif 'Estate' in player.hand: player.hand.remove('Estate')
				elif 'Copper' in player.hand: player.hand.remove('Copper')
			player.gain_to_hand(Ref, 'Silver')
		elif (player.hand.count('Estate') + player.hand.count('Copper') + player.hand.count('Curse') ==1) and player.hand.count('Silver') > 0:
			if 'Curse' in player.hand: player.hand.remove('Curse')
			elif 'Estate' in player.hand: player.hand.remove('Estate')
			elif 'Copper' in player.hand: player.hand.remove('Copper')
			# RATHER THAN TRASH THE SILVER AND GAIN A SILVER, JUST DO NOTHING - THE SUPPLY PILE AINT RUNNING OUT
		return
			
	def Treasure_Map(self, player, Ref):
		if 'Treasure_Map' in player.hand:
			player.inplay.remove('Treasure_Map')
			player.hand.remove('Treasure_Map')
			player.deck.extend(['Gold','Gold','Gold','Gold'])				
			
	def Tribute(self, player, opponents, Ref):
		opponent = opponents[0]	
		cards = opponent.pull(2)
		if cards[0] in Ref.victory_cards: player.draw(2)
		if cards[0] in Ref.treasure_cards: player.treasure += 2
		if cards[0] in Ref.action_cards: player.action += 2
		if cards[1] != cards[0]:
			if cards[1] in Ref.victory_cards: player.draw(2)
			if cards[1] in Ref.treasure_cards: player.treasure += 2
			if cards[1] in Ref.action_cards: player.action += 2	
		opponent.discard += cards
	
	def Warehouse(self, player, Ref):
		player.friendly_discard(Ref, 3)
			
	def Witch(self, player, opponents, Ref):
		for opponent in opponents:
			if opponent.defender(Ref, 'Witch'): pass
			else: opponent.gain(Ref, 'Curse')
		
	def Workshop(self, player, Ref):
		store = player.treasure
	#	print "Using workshop, store value is", store
		player.treasure = 4
		card = ai_chooser('buy', player, [], Ref)
		player.gain(Ref, card)
		player.treasure = store
	#	print "Player.treasure was restored and has value", player.treasure
	#	print "You gained", card
		
