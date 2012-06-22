import random
from __builtin__ import set



def winner(score):
	# HOW DID I DO THIS - NEED TO DETERMINE NUMBER OF PLAYERS AND SORT - USE SORTED AND SORT RANGE(1,len(score) USING score
	combined = zip(score, range(len(score)))
	combined.sort(reverse = True)
	score, ordered = zip(*combined)
	winner = ordered[0]
	if score[0] == score[1]:
		winner = 4
	return winner
	
def intersect(a, b):		# HEY DOG - DO THIS WITH LIST COMPREHENSIONS
	"This function compares 2 lists to see if they have any elements in common. The function ends and returns True as soon as a common"
	"element is found. The shared elements are not stored or returned"
	if len(a) < len(b):
		for element in a:
			if element in b: return True
	else:
		for element in b:
			if element in a: return True	
	return False	
	


class Player(object):
	"""
	This class creates a player in Dominion, where the player is defined by 
	their hand, deck, and discard pile. The deck is initialized to 7 copper 
	and 3 estate. A number of functions exist in this class, mostly for the 
	purpose of moving cards from place to place, evaluating victory points, 
	or counting treasure.
	"""

	def __init__(self, ai, distro):
		self.hand = []
		self.discard = []
		self.inplay = []
		self.duration = []
		self.haven = []
		self.island = []
		self.ai = ai
		self.turn = 0
		if distro == 'random': self.deck = ['Copper']*7 + ['Estate']*3; self.shuffler()
		elif distro == '34': self.deck = ['Copper']*4 + ['Estate']*3 + ['Copper']*3
		elif distro == '43': self.deck = ['Copper']*3 + ['Estate']*3 + ['Copper']*4
		elif distro == '52': self.deck = ['Copper']*2 + ['Estate']*3 + ['Copper']*5
		self.draw(5)
		self.buy = 1
		self.action = 1
		self.treasure = 0
		self.victory = 0
		self.bought = []
		self.gained = []
		self.pirate_tokens = 0		# Used with the pirate ship card
		##### LATER ADD *ARGS TO ALLOW FOR NON-RANDOM STARTS: FORCE 5/2 or 4/3 SPLITS (or 3/4 - think Nomad Camp)

	def shuffler(self):
		"shuffles the deck"
		random.shuffle(self.deck,random.random)
	
	def draw(self, n):
		"Draws n cards with the pull function and puts them in the player's hand"
		self.hand += self.pull(n)
		
	def pull(self, n):
		"Draws n cards, shuffling discard into deck if needed, but doesn't put the cards into the hand"
		if n == 0 or (self.deck == [] and self.discard ==[]):
			return []
		d = min(len(self.deck),n)
		new = self.deck[-d:]
		del self.deck[-d:]
		if d < n:
			self.deck = self.discard[:]
			self.shuffler()
			self.discard = []
			d = min(len(self.deck),n-d)
			new += self.deck[-d:]
			del self.deck[-d:]
		return new
		
	def xbuy(self, opponents, Ref, card):
	#	if card == 'Noble_Brigand':
			
		self.treasure -= Ref.true_cost(self, card) 
		self.buy -= 1	
		self.gain(Ref, card)
		self.bought.append(card)		
		
	def gain(self, Ref, card):
		if Ref.supply[card] == 0: return
		if 'Trader' in self.hand and (card == 'Copper' or card == 'Curse'): 
			self.gain(Ref, 'Silver'); return

		self.discard.append(card) # CARD MUST BE ADDED TO DISCARD PILE PRIOR TO GAIN EFFECT RESOLUTION
		if card in Ref.gain_effect:
			self.gain_resolution(Ref, card)

		Ref.supply[card] -= 1
		self.gained.append(card)
	#	print "Player", self.ai, "gained a", card	

	def gain_to_deck(self, Ref, card):
		if Ref.supply[card] == 0:
			return
		if 'Trader' in self.hand:
			if card == 'Copper' or card == 'Curse': 
				self.gain_to_deck(Ref, 'Silver')
				return
		if card in Ref.gain_effect:
			print "Unresolved gain effect in player.gain_to_deck"
		Ref.supply[card] -= 1
		self.deck.append(card)			
	#	print "Player", self.ai, "gained a", card	

	def gain_to_hand(self, Ref, card):
		if Ref.supply[card] == 0:
			return
		self.hand.append(card)
		#	print "Player", self.ai, "gained a", card

	def gain_resolution(self, Ref, card):
		if card == 'Cache':
			self.gain(Ref, 'Copper')
			self.gain(Ref, 'Copper')	
			
		elif card == 'Mandarin':
			for i in reversed(range(len(self.inplay))):
				if self.inplay[i] in Ref.treasure_cards: 
					self.inplay_to_deck(self.inplay[i])

		elif card == 'Nomad_Camp': self.deck.append( self.discard.pop() )
		
		elif card == 'Inn':  # Right now this just takes all action cards
			additions = []
			for card in self.discard:
				if card in Ref.action_cards:
					self.discard.remove(card)
					additions.append(card)
			if len(additions) > 0:
				self.deck += additions
		#		print "Inn selected the cards", additions, "to shuffle into the deck"
				self.shuffler()	
		else:
			print "NEED TO RESOLVE SPECIAL ACTION UPON CARD GAIN"

	def card_discard(self, card):
		self.hand.remove(card)
		self.discard.append(card)
		return
		
	def friendly_discard(self, Ref, number):
		if number == 1:
			if 'Tunnel' in self.hand: self.card_discard('Tunnel'); return
			else:
				for card in self.hand:
					if card in Ref.strict_victory_cards: self.card_discard(card); return
				# Add a search for 2 dead end action cards here
				if 'Curse' in self.hand: self.card_discard('Curse'); return
				elif self.action == 0 and intersect(self.hand, Ref.action_cards):
					for card in self.hand: 
						if card in Ref.action_cards: self.card_discard(card); return
				elif 'Copper' in self.hand: self.card_discard('Copper'); return
				elif 'Silver' in self.hand: self.card_discard('Silver'); return
				# Sort hand by card cost and go from there
				self.card_discard(self.hand[0]); return  # SUPER SHITTY - just picks the first card and discards it!		
		else:
			count = 0			# RIGHT NOW THIS JUST CALLS ON ITSELF FOR A SINGLE CARD DISCARD UNTIL SATISFIED...MAKE THIS SMARTER
			while count < number:
				self.friendly_discard(Ref, 1)
				count += 1
			return
		print "POSSIBLE ERROR IN FRIENDLY_DISCARD"
		return False

	def money_discard(self):		# THIS CAN BE MORE EFFICIENT - CONSIDER A HIERARCHICAL LIST OF TREASURE CARDS
	#	print "Discarding money to enact Stables"
		if 'Copper' in self.hand:
			self.card_discard('Copper')
			return True
		elif 'Fools_Gold' in self.hand and self.hand.count('Fools_Gold') == 1:
			self.card_discard('Fools_Gold')
			return True
		elif 'Ill_Gotten_Gains' in self.hand:
			self.card_discard('Ill_Gotten_Gains')
			return True
		elif 'Silver' in self.hand:
			self.card_discard('Silver')
			return True	
		elif 'Cache' in self.hand:
			self.card_discard('Cache')
			return True
		elif 'Gold' in self.hand:
			self.card_discard('Gold')
			return True	
		else: return False			

	def peek_discard(self, Ref):
		card = self.pull(1)[0]
	#	print "Peek on top of deck reveals", card
		if card in Ref.strict_victory_cards:
			self.discard.append(card)
			return
		elif self.treasure == 6 and card == 'Copper':
			self.discard.append(card)
			return
		else:
			self.deck.append(card)
		return
	
	def hand_to_deck(self, card):
		"Moves a specified card from a player's hand to the top of his deck"
		self.deck.append(card)
		self.hand.remove(card)

	def inplay_to_deck(self, card):
		"Moves a specified card from a player's hand to the top of his deck"
		self.deck.append(card)
		self.inplay.remove(card)
	
	# THIS DOESN'T DIRECTLY ADD TO TREASURE FOR A REASON - SO YOU CAN TELL WHAT FUTURE WEALTH WILL BE W/O PLAYING CARDS INTO INPLAY	
	def count_money(self):		# Doesn't have Ill-Gotten Gains yet - need mechanism to add the copper
		"Counts the amount of treasure in the player's hand"
		total = 3*self.hand.count('Gold') + 2*self.hand.count('Silver') + self.hand.count('Copper') + 3*self.hand.count('Cache') + 1*min(1, self.hand.count('Fools_Gold') + 4*max(0, self.hand.count('Fools_Gold') - 1))		
		if 'Coppersmith' in self.inplay or 'Coppersmith' in self.hand: self.treasure += self.hand.count('Copper')
		return(total)	

	def wealth(self):		# Doesn't have Ill-Gotten Gains yet - need mechanism to add the copper
		"Counts the amount of treasure in the player's hand"
		total = self.treasure + self.count_money()
		return(total)	

	def wealth_action(self, Ref):
		"Counts the amount of treasure in the player's hand, including potential money from unplayed action cards"
		"Note: this function doesn't figure out if all action cards are playable."
		total = self.wealth()
		for card in self.hand:
			if card in Ref.add_treasure: total += Ref.add_treasure[card]	# This doesn't count actions with an optional add treasure element
		return(total)	

	# THE GENERAL VERSION OF THESE FUNCTIONS CAN BE USED WITH ANY LIST OF CARDS
	def general_count_money(self, Ref, cards):		# Doesn't have Ill-Gotten Gains yet - need mechanism to add the copper
		"Counts the amount of treasure in a specified list of cards"
		total = sum( [Ref.treasure_value[x] for x in cards if x in Ref.treasure_value] ) + 3*max(0, cards.count('Fools_Gold') - 1)
		if 'Coppersmith' in self.inplay or 'Coppersmith' in self.hand: total += cards.count('Copper')
		return total

	def general_wealth(self, Ref, cards):		# Doesn't have Ill-Gotten Gains yet - need mechanism to add the copper
		"Counts the amount of treasure in a list of cards and adds it to the player's existing treasure count"
		total = self.treasure + self.general_count_money(Ref, cards)
		return total

	def general_wealth_action(self, Ref, cards):
		"Counts the amount of treasure in a list of cards, including potential money from unplayed action cards, and adds it to current amount of player treasure"
		"Note: this function doesn't figure out if all action cards are playable."
		total = self.general_wealth(Ref, cards) + sum( [Ref.add_treasure[x] for x in cards if x in Ref.add_treasure] )		
		return total

	def use_money(self, Ref):
		"This takes player's money from in the hand and place it into the inplay pile, increasing treasure accordingly."
		for card in Ref.treasure_cards:
			while card in self.hand:
				self.hand.remove(card)
				self.inplay.append(card)
				self.treasure += Ref.treasure_value[card]
		self.treasure += 3*max(0, self.inplay.count('Fools_Gold') - 1)
		if 'Coppersmith' in self.inplay: self.treasure += self.inplay.count('Copper')
	
	def action_count(self):
		"Counts the number of action cards in hand and determines if player will be able to play them all; returns True or False"
		available = 1 + sum([Ref.add_actions[x] for x in self.hand if x in Ref.add_actions])
		needed = len( [x for x in self.hand if x in Ref.action_cards] )
		if available >= needed: return True
		else: return False
	
	def duration_effect(self, card):
		if card == 'Caravan': self.draw(1)
		elif card == 'Fishing_Village': self.action += 1; self.treasure += 1
		elif card == 'Haven': self.hand.append( self.haven.pop() )
		elif card == 'Lighthouse': self.treasure += 1
		elif card == 'Merchant_Ship': self.treasure += 2
		elif card == 'Outpost': print "OUTPOST IN DURATION - HAVEN'T CODED A RESOLUTION YET"
		elif card == 'Tactician': print "TACTICIAN IN DURATION - HAVEN'T CODED A RESOLUTION YET"
		elif card == 'Wharf': self.buy += 1; self.draw(2)
	
	def cleanup(self, Ref):
		# IDENTIFY AND ENABLE CARDS THAT PERFORM SPECIAL THINGS DURING CLEANUP PHASE, INCLUDING ACTION-DURATIONS
		
		# IMPLEMENT THE SCHEME CARD HERE
		self.discard += self.duration
		self.duration = []
		for card in self.inplay:
			if card in Ref.duration_cards:
				self.inplay.remove(card)
				self.duration.append(card)
			while 'Treasury' in self.inplay and not intersect(self.bought, Ref.victory_cards):
				self.inplay.remove('Treasury')
				self.deck.append('Treasury')
		self.discard += self.inplay
		self.inplay = []
		self.discard += self.hand
		self.hand = []
		self.draw(5)
		self.action = 1
		self.buy = 1
		self.treasure = 0
		
	def score(self):  #JESUS. REDO THIS.
		"Counts the player's total score"
		all_cards = self.hand + self.deck + self.discard + self.inplay
		total = 6*all_cards.count('Province') + 3*all_cards.count('Duchy') + all_cards.count('Estate') + (len(all_cards)/10)*all_cards.count('Gardens') - all_cards.count('Curse') + 2*all_cards.count('Tunnel') + 2*all_cards.count('Farmland') + 1*all_cards.count('Great_Hall') + 2*all_cards.count('Harem') + 2*all_cards.count('Nobles')
		if 'Silk_Road' in all_cards:
			vic_card_count = all_cards.count('Province') + all_cards.count('Duchy') + all_cards.count('Estate') + all_cards.count('Gardens') + all_cards.count('Tunnel') + all_cards.count('Farmland')+ all_cards.count('Silk_Road')
			total += vic_card_count/4
		return(total + self.victory)	

	def total(self, card):
		"Counts total number of instances of a named card in hand, deck, discard, and inplay"
		all_cards = self.combine()
		return all_cards.count(card)
	
	def combine(self):
		return self.hand + self.deck + self.discard + self.inplay + self.duration + self.island + self.haven
	
	def card_count(self):
		return len( self.hand + self.deck + self.discard + self.inplay + self.duration + self.haven)

	def defender(self, Ref, attack_card):
		if 'Secret_Chamber' in self.hand:	# Add an AI response to Saboteur
			self.draw(2)
			if attack_card not in ['Militia', 'Margrave', 'Torturer']: self.friendly_to_deck(2)
			else: 
				counter = 0
				while counter < 2:
					vic_count = [x for x in self.hand if x in Ref.strict_victory_cards]
					if vic_count > 2: 
						self.hand_to_deck( [x for x in self.hand if x in Ref.strict_victory_cards][0] )
						counter += 1
					elif [x for x in self.hand if (x in Ref.add_treasure or x in Ref.treasure_cards)]:
						self.hand_to_deck( [x for x in self.hand if (x in Ref.add_treasure or x in Ref.treasure_cards)][0] )
						counter += 1
					else:
						self.hand_to_deck( self.hand[0] )
						counter += 1
		# INSERT HORSE TRADERS HERE
	#	if 'Moat' in self.hand or 'Lighthouse' in self.duration: print "Defended with Moat/Lighthouse!"; return True
		return False

	def friendly_to_deck(self, number):
		count = 0
		money = self.wealth_action()
		while count != number:
			if not self.action_count(): card = [x for x in self.hand if x in Ref.action_cards and x not in Ref.add_action][0] # This means that there are too many actions to play in one turn
			elif money in [4, 7, 9] and 'Copper' in player.hand: card = 'Copper'
			elif money > 9 and 'Silver' in self.hand and (number - count) == 1: card = 'Silver'
			elif money > 9 and 'Copper' in self.hand: card = 'Copper'
			elif [x for x in player.hand if x in Ref.strict_victory_cards]: card = [x for x in player.hand if x in Ref.strict_victory_cards][0]
			else: 
				card = self.hand[0] 	# Just selects the first card in hand 
				print "friendly_to_deck function couldn't select a good card to discard"
			self.hand_to_deck( card )
			count += 1
		

	def standard_trash(self):	
		"Trashes one of the standard 3 trash cards, then returns the type of card that was trashed"
		if 'Curse' in self.hand: card = 'Curse'
		elif 'Estate' in self.hand: card = 'Estate'
		elif 'Copper' in self.hand: card = 'Copper'
		self.hand.remove(card)
		try: return card
		except: return False
##########################################################		

class Card_Data(object):
	"""
	This class includes all reference dictionaries containing card bonus data as well as lists of cards by category
	"""
	def __init__(self, n):
		
		self.supply = {
		'Estate':4*min(3,n), 'Duchy':4*min(3,n), 'Province':4*min(3,n), 'Gardens':4*min(3,n), 'Curse':10*(n-1),
		'Copper':200, 'Silver':150, 'Gold':100,
		'Adventurer':10, 'Bureaucrat':10, 'Cellar':10, 'Chancellor':10, 'Chapel':10, 'Council_Room':10, 'Feast':10, 'Festival':10,
		'Laboratory':10, 'Library':10, 'Market':10, 'Militia':10, 'Mine':10, 'Moat':10, 'Moneylender':10, 'Remodel':10,
		'Smithy':10, 'Spy':10, 'Thief':10, 'Throne_Room':10, 'Village':10, 'Witch':10, 'Woodcutter':10, 'Workshop':10,
		# HINTERLANDS EXPANSION CARDS
		'Border_Village':10, 'Cache':10, 'Cartographer':10, 'Crossroads':10, 'Develop':10, 'Duchess':10, 'Embassy':10, 'Farmland':4*min(3,n) , 
		'Fools_Gold':10, 'Haggler':10, 'Highway':10, 'Ill_Gotten_Gains':10, 'Inn':10, 'Jack_of_All_Trades':10, 'Mandarin':10, 'Margrave':10, 
		'Noble_Brigand':10, 'Nomad_Camp':10, 'Oasis':10, 'Oracle':10, 'Scheme':10, 'Silk_Road':4*min(3,n), 'Spice_Merchant':10, 
		'Stables':10, 'Trader':10, 'Tunnel':4*min(3,n),
		# INTRIGUE EXPANSION CARDS
		'Baron':10, 'Bridge':10, 'Conspirator':10, 'Coppersmith':10, 'Coutyard':10, 'Duke':4*min(3,n), 'Great_Hall':4*min(3,n), 'Harem':4*min(3,n), 
		'Ironworks':10, 'Masquerade':10, 'Mining_Village':10, 'Minion':10, 'Nobles':4*min(3,n), 'Pawn':10, 'Saboteur':10, 'Scout':10, 'Secret_Chamber':10, 
		'Shanty_Town':10, 'Steward':10, 'Swindler':10, 'Torturer':10, 'Trading_Post':10, 'Tribute':10, 'Upgrade':10, 'Wishing_Well':10,
		# SEASIDE
		'Ambassador':10, 'Bazaar':10, 'Caravan':10, 'Cutpurse':10, 'Embargo':10, 'Explorer':10, 'Fishing_Village':10, 'Ghost_Ship':10, 'Haven':10,
		'Island': 4*min(3,n), 'Lighthouse':10, 'Lookout':10, 'Merchant_Ship':10, 'Native_Village':10, 'Navigator':10, 'Outpost':10, 'Pearl_Diver':10, 
		'Pirate_Ship':10, 'Salvager':10, 'Sea_Hag':10, 'Smuggler':10, 'Tactician':10, 'Treasure_Map':10, 'Treasury':10, 'Warehouse':10, 'Wharf':10,
		# PROSPERITY
		'Bank':10, 'Bishop':10, 'City':10, 'Contraband':10, 'Counting_House':10, 'Expand':10, 'Forge':10, 'Goons':10, 'Grand_Market':10, 'Hoard':10, 
		'Kings_Court':10, 'Loan':10, 'Mint':10, 'Monument':10, 'Mountebank':10, 'Peddler':10, 'Quarry':10, 'Rabble':10, 'Royal_Seal':10, 'Talisman':10, 
		'Trade_Route':10, 'Vault':10, 'Venture':10, 'Watchtower':10, 'Workers_Village':10
		}
		
		self.card_cost = {'Estate':2, 'Duchy':5, 'Province':8, 'Curse':0, 'Gardens':4, 'Copper':0, 'Silver':3, 'Gold':6, 'Adventurer':6, 'Bureaucrat':4, 'Cellar':2, 
		'Chancellor':3, 'Chapel':2, 'Council_Room':5, 'Feast':4, 'Festival':5, 'Laboratory':5, 'Library':5, 'Market':5, 'Militia':4, 'Mine':5, 'Moat':2, 
		'Moneylender':4, 'Remodel':4, 'Smithy':4, 'Spy':4, 'Thief':4, 'Throne_Room':4, 'Village':3, 'Witch':5, 'Woodcutter':3, 'Workshop':3,
		# HINTERLANDS
		'Border_Village':6, 'Cache':5, 'Cartographer':5, 'Crossroads':2, 'Develop':3, 'Duchess':2, 'Embassy':5, 'Farmland':6 , 
		'Fools_Gold':2, 'Haggler':5, 'Highway':5, 'Ill_Gotten_Gains':5, 'Inn':5, 'Jack_of_All_Trades':4, 'Mandarin':5, 'Margrave':5, 
		'Noble_Brigand':4, 'Nomad_Camp':4, 'Oasis':3, 'Oracle':3, 'Scheme':3, 'Silk_Road':4, 'Spice_Merchant':4, 
		'Stables': 5, 'Trader':4, 'Tunnel':3,
		# INTRIGUE
		'Baron':4, 'Bridge':4, 'Conspirator':4, 'Coppersmith':4, 'Coutyard':2, 'Duke':5, 'Great_Hall':3, 'Harem':6, 'Ironworks':4, 'Masquerade':3, 
		'Mining_Village':4, 'Minion':5, 'Nobles':6, 'Pawn':2, 'Saboteur':5, 'Scout':4, 'Secret_Chamber':2, 'Shanty_Town':3, 'Steward':3, 'Swindler':3, 
		'Torturer':5, 'Trading_Post':5, 'Tribute':5, 'Upgrade':5, 'Wishing_Well':3,
		# SEASIDE
		'Ambassador': 3, 'Bazaar': 5, 'Caravan': 4, 'Cutpurse': 4, 'Embargo': 2, 'Explorer': 5, 'Fishing_Village': 3, 'Ghost_Ship': 5, 'Haven': 2,
		'Island': 4, 'Lighthouse': 2, 'Lookout': 3, 'Merchant_Ship': 5, 'Native_Village': 2, 'Navigator': 4, 'Outpost': 5, 'Pearl_Diver': 2, 
		'Pirate_Ship': 4, 'Salvager': 4, 'Sea_Hag': 4, 'Smuggler': 3, 'Tactician': 5, 'Treasure_Map': 4, 'Treasury': 5, 'Warehouse': 3, 'Wharf': 5,
		# PROSPERITY
		'Bank':7, 'Bishop':4, 'City':5, 'Contraband':5, 'Counting_House':5, 'Expand':7, 'Forge':7, 'Goons':6, 'Grand_Market':6, 'Hoard':6, 
		'Kings_Court':7, 'Loan':3, 'Mint':5, 'Monument':4, 'Mountebank':5, 'Peddler':8, 'Quarry':4, 'Rabble':5, 'Royal_Seal':5, 
		'Talisman':4, 'Trade_Route':3, 'Vault':5, 'Venture':5, 'Watchtower':3, 'Workers_Village':4		
		}
		
		self.add_action = {'Cellar':1, 'Festival':2, 'Laboratory':1, 'Market':1, 'Spy':1, 'Village':2,
		'Border_Village':2, 'Cartographer':1, 'Highway':1, 'Inn':2, 'Scheme':1,
		'Great_Hall':1, 'Mining_Village':2, 'Minion':1, 'Scout':1, 'Shanty_Town':2, 'Upgrade':1, 'Wishing_Well':1,
		'Bazaar':2, 'Caravan':1, 'Fishing_Village':2, 'Haven':1, 'Lighthouse':1, 'Lookout':1, 'Native_Village':2, 'Pearl_Diver':1, 'Treasury':1, 'Warehouse':1,
		'City':2, 'Grand_Market':1, 'Peddler':1, 'Workers_Village':2			
		}
		
		self.add_card = {'Council_Room':4, 'Laboratory':2, 'Market':1, 'Moat':2, 'Smithy':3, 'Spy':1, 'Village':1, 'Witch':2,
		'Border_Village':1, 'Cartographer':1, 'Embassy':5, 'Highway':1, 'Inn':2, 'Margrave':3, 'Scheme':1,
		'Coutyard':3, 'Great_Hall':1,  'Masquerade':2, 'Torturer':3, 'Upgrade':1, 'Wishing_Well':1,
		'Bazaar': 1, 'Caravan': 1, 'Ghost_Ship': 2, 'Haven': 1, 'Pearl_Diver': 1, 'Treasury': 1, 'Warehouse': 3, 'Wharf': 2,
		'City':1, 'Grand_Market':1,  'Peddler':1, 'Rabble':3, 'Vault':2, 'Workers_Village':1}
		
		self.add_buy = {'Council_Room':1, 'Festival':1, 'Market':1, 'Woodcutter':1,
		'Margrave':1, 'Nomad_Camp':1,
		'Baron':1, 'Bridge':1,
		'Salvager': 1, 'Wharf': 1,
		'Grand_Market':1, 'Trade_Route':1, 'Workers_Village':1}
		
		self.add_treasure = {'Chancellor':2, 'Festival':2, 'Market':1, 'Militia':2, 'Woodcutter':2,
		'Duchess':2, 'Haggler':2, 'Mandarin':3, 'Noble_Brigand':1, 'Nomad_Camp':2,
		'Bridge':1, 'Conspirator':2,'Swindler':2,		
		'Bazaar': 1, 'Cutpurse': 2, 'Embargo': 2, 'Fishing_Village': 1, 'Lighthouse': 1, 'Merchant_Ship': 2, 'Navigator': 2, 'Treasury': 1,
		'Bishop':1, 'Goons':2, 'Grand_Market':2, 'Monument':2, 'Mountebank':2, 'Peddler':1}
		
		self.add_victory = {'Bishop':1, 'Monument':1}
		
		self.treasure_value = {'Copper':1, 'Silver':2, 'Gold':3, 'Fools_Gold':1, 'Cache':3, 'Harem':2, 'Contraband': 3, 'Hoard': 2, 'Loan':1, 'Quarry':1, 'Royal_Seal':2, 'Talisman':1, 'Venture':1}
			
#		self.card_value = {'Copper':1, 'Silver':2, 'Gold':3, 'Fools_Gold':1, 'Cache':3, 'Harem':2, 'Contraband': 3, 'Hoard': 2, 'Loan':1, 'Quarry':1, 'Royal_Seal':2, 'Talisman':1, 'Venture':1,
#		'Chancellor':2, 'Festival':2, 'Market':1, 'Militia':2, 'Woodcutter':2,
#		'Duchess':2, 'Haggler':2, 'Mandarin':3, 'Noble_Brigand':1, 'Nomad_Camp':2,
#		'Bridge':1, 'Conspirator':2,'Swindler':2,		
#		'Bazaar': 1, 'Cutpurse': 2, 'Embargo': 2, 'Fishing_Village': 1, 'Lighthouse': 1, 'Merchant_Ship': 2, 'Navigator': 2, 'Treasury': 1,
#		'Bishop':1, 'Goons':2, 'Grand_Market':2, 'Monument':2, 'Mountebank':2, 'Peddler':1}

		self.treasure_cards = ['Copper', 'Silver', 'Gold', 'Cache', 'Fools_Gold', 'Ill_Gotten_Gains', 'Harem',
		'Bank', 'Contraband', 'Hoard', 'Loan', 'Quarry', 'Royal_Seal', 'Talisman', 'Venture']
		
		self.strict_victory_cards = ['Province', 'Duchy', 'Estate', 'Gardens', 'Farmland', 'Silk_Road', 'Duke']
		self.victory_cards = ['Province', 'Duchy', 'Estate', 'Gardens', 'Farmland', 'Silk_Road', 'Tunnel', 'Duke', 'Great_Hall', 'Harem', 'Nobles', 'Island']
	
		self.action_cards = ['Adventurer', 'Bureaucrat', 'Cellar', 'Chancellor', 'Chapel', 'Council_Room', 'Feast', 'Festival', 'Laboratory', 'Library', 'Market', 
		'Militia', 'Mine', 'Moat', 'Moneylender', 'Remodel', 'Smithy', 'Spy', 'Thief', 'Throne_Room', 'Village', 'Witch', 'Woodcutter', 'Workshop',
		# HINTERLANDS
		'Border_Village', 'Cartographer', 'Crossroads', 'Develop', 'Duchess', 'Embassy', 'Haggler', 'Highway', 'Inn', 'Jack_of_All_Trades', 'Mandarin', 
		'Margrave', 'Noble_Brigand', 'Nomad_Camp', 'Oasis', 'Oracle', 'Scheme', 'Spice_Merchant', 'Stables', 'Trader', 'Tunnel'
		# INTRIGUE
       		'Baron', 'Bridge', 'Conspirator', 'Coppersmith', 'Coutyard', 'Great_Hall', 'Harem', 'Ironworks', 'Masquerade', 
		'Mining_Village', 'Minion', 'Nobles', 'Pawn', 'Saboteur', 'Scout', 'Secret_Chamber', 'Shanty_Town', 'Steward', 'Swindler', 
		'Torturer', 'Trading_Post', 'Tribute', 'Upgrade', 'Wishing_Well',
		# SEASHORE
		'Ambassador', 'Bazaar', 'Caravan', 'Cutpurse', 'Embargo', 'Explorer', 'Fishing_Village', 'Ghost_Ship', 'Haven',
		'Island', 'Lighthouse', 'Lookout', 'Merchant_Ship', 'Native_Village', 'Navigator', 'Outpost', 'Pearl_Diver', 
		'Pirate_Ship', 'Salvager', 'Sea_Hag', 'Smuggler', 'Tactician', 'Treasure_Map', 'Treasury', 'Warehouse', 'Wharf',
		# PROSPERITY
		'Bishop', 'City', 'Counting_House', 'Expand', 'Forge', 'Goons', 'Grand_Market', 'Kings_Court', 'Mint', 'Monument', 
		'Mountebank', 'Peddler', 'Rabble', 'Trade_Route', 'Vault', 'Watchtower', 'Workers_Village']
		
		self.special_cards = ['Adventurer', 'Cellar', 'Chancellor', 'Chapel', 'Library', 'Mine', 'Moneylender', 'Workshop',
		'Cartographer', 'Crossroads', 'Develop', 'Duchess', 'Haggler',  'Inn', 'Jack_of_All_Trades', 'Mandarin', 'Oasis', 'Scheme', 'Spice_Merchant', 'Stables', 'Trader', 'Tunnel',
       		'Baron', 'Conspirator', 'Coutyard', 'Ironworks', 'Masquerade', 'Nobles', 'Pawn', 'Scout', 'Secret_Chamber', 'Shanty_Town', 'Steward', 'Trading_Post', 'Upgrade', 'Wishing_Well',
		'Embargo', 'Explorer', 'Haven', 'Island', 'Lookout', 'Native_Village', 'Navigator', 'Outpost', 'Pearl_Diver', 'Salvager', 'Smuggler', 'Tactician', 'Treasure_Map', 'Warehouse',
		'Bishop', 'City',  'Counting_House', 'Expand', 'Forge', 'Goons', 'Grand_Market', 'Kings_Court', 'Mint', 'Mountebank', 'Peddler', 'Rabble', 'Trade_Route', 'Vault', 'Watchtower']
		
		self.attack_cards = ['Bureaucrat', 'Council_Room', 'Feast', 'Militia', 'Remodel', 'Spy', 'Thief', 'Throne_Room', 'Witch',	# INCLUDES CARDS THAT NEED OPPONENT INFO TO ACTIVATE
		'Embassy', 'Ill_Gotten_Gains', 'Margrave', 'Noble_Brigand', 'Oracle', 
       		'Minion', 'Saboteur', 'Swindler', 'Torturer', 'Mining_Village', 'Tribute', 
       		'Ambassador', 'Cutpurse', 'Ghost_Ship', 'Pirate_Ship', 'Sea_Hag']
       		
       		self.true_attack_cards = ['Bureaucrat', 'Militia', 'Spy', 'Thief', 'Witch', # INCLUDES CARDS THAT NEED OPPONENT INFO TO ACTIVATE
		'Margrave', 'Noble_Brigand', 'Oracle', 
       		'Saboteur', 'Swindler', 'Torturer', 
       		'Ambassador', 'Cutpurse', 'Ghost_Ship', 'Pirate_Ship', 'Sea_Hag']
       		
       		self.duration_cards = ['Caravan', 'Fishing_Village', 'Haven', 'Lighthouse', 'Merchant_Ship', 'Outpost', 'Tactician', 'Wharf']
		
		self.gain_effect = ['Cache', 'Farmland', 'Embassy', 'Ill_Gotten_Gains', 'Inn', 'Mandarin', 'Nomad_Camp']

	def feasible(self, player, card):
		return (player.treasure >= self.true_cost(player, card) and self.supply[card] > 0)		
	
	def true_cost(self, player, card):
		return max(0, self.card_cost[card] - player.inplay.count('Highway') - player.inplay.count('Bridge'))
		
	def endgame(self):
		if self.supply['Province'] == 0:
			return True
		elif self.supply.values().count(0) >= 3:
			return True
		else:
			return False
		
