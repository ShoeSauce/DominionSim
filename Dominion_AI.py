############################ AI FUNCTION ##########################################
from Dominion_Player import Player
from Dominion_Player import intersect
from Dominion_Player import Card_Data
from __builtin__ import set

# THE ARITIFICAL INTEL FUNCTIONS

# STRATEGIES TO TRY: Workshop_Lab; 

def ai_chooser(phase, player, opponents, Ref):
	if player.ai == "Money": return( ai_Money1(phase, player, opponents, Ref))
#####				NEW/TEST PHASE STRATEGIES						#####		
	elif player.ai == "Remodel": return( ai_Remodel1(phase, player, opponents, Ref))	
	elif player.ai == "Saboteur": return( ai_Saboteur1(phase, player, opponents, Ref))	
	elif player.ai == "Salvager": return( ai_Salvager1(phase, player, opponents, Ref))					
#####				EFFECTIVE STRATEGIES (70+% win vs. money)			#####
	elif player.ai == "Crossroads_Plus": return( ai_Crossroads_Plus1(phase, player, opponents, Ref))
	elif player.ai == "Nobles": return( ai_Nobles1(phase, player, opponents, Ref))
	elif player.ai == "Attackers": return( ai_Attackers1(phase, player, opponents, Ref))	
	elif player.ai == "Inside_Job": return( ai_Inside_Job1(phase, player, opponents, Ref))
	elif player.ai == "Witch": return( ai_Witch1(phase, player, opponents, Ref))		
	elif player.ai == "High_Mark": return( ai_High_Mark1(phase, player, opponents, Ref))		
	elif player.ai == "Workshop_Gardens": return( ai_Workshop_Gardens1(phase, player, opponents, Ref))	
	elif player.ai == "Baron_Plus": return( ai_Baron_Plus1(phase, player, opponents, Ref))			
	elif player.ai == "Spicey_Fool": return( ai_Spicey_Fool1(phase, player, opponents, Ref))	
	elif player.ai == "Stable_Jack": return( ai_Stable_Jack1(phase, player, opponents, Ref))	
	elif player.ai == "Sea_Hag": return( ai_Sea_Hag1(phase, player, opponents, Ref))
			
#####				MIDLEVEL STRATEGIES (< 70% win vs. money)			#####		
	elif player.ai == "Trader_Cache": return( ai_Trader_Cache1(phase, player, opponents, Ref))	
	elif player.ai == "Fest_Mar_Smith": return( ai_Fest_Mar_Smith1(phase, player, opponents, Ref))
	elif player.ai == "Market_Smith": return( ai_Market_Smith1(phase, player, opponents, Ref))		
	elif player.ai == "Festival_Smith": return( ai_Festival_Smith1(phase, player, opponents, Ref))		
	elif player.ai == "Stable_Crat": return( ai_Stable_Crat1(phase, player, opponents, Ref))
	elif player.ai == "Smithy": return( ai_Smithy1(phase, player, opponents, Ref))	
	elif player.ai == "Scout_Plus": return( ai_Scout_Plus1(phase, player, opponents, Ref))
	elif player.ai == "Moneylender_Market": return( ai_Moneylender_Market1(phase, player, opponents, Ref))	  # only about 53% win vs. money
	elif player.ai == "Jack": return( ai_Jack1(phase, player, opponents, Ref))		
	elif player.ai == "Market_Mine": return( ai_Market_Mine1(phase, player, opponents, Ref))
	elif player.ai == "Margrave": return( ai_Margrave1(phase, player, opponents, Ref))		
	elif player.ai == "Militia": return( ai_Militia1(phase, player, opponents, Ref))			
#####		UNFINISHED/UNVERIFIED/EXTRA AI SINGLE CARD STRATEGIES	#####	
	elif player.ai == "Spice_Merchant": return( ai_Spice_Merchant1(phase, player, opponents, Ref))
	elif player.ai == "Steward": return( ai_Steward1(phase, player, opponents, Ref))	
	elif player.ai == "Trader": return( ai_Trader1(phase, player, opponents, Ref))		
	
	elif player.ai == "Chapel_Adventurer": return( ai_Chapel_Adventurer1(phase, player, opponents, Ref))		
	elif player.ai == "Mandarin": return( ai_Mandarin1(phase, player, opponents, Ref))	
	else:
		print "This is an error in ai_chooser function"

#-----------------------------------------------------------------------------------------------------------------------------	#
#			NEW/UNDER TESTING STRATEGIES										#
#-----------------------------------------------------------------------------------------------------------------------------	#

def ai_TEMPLATE1(phase, player, opponents, Ref):   # THIS IS HERE AS A 1 ACTION TEMPLATE AI
	if phase == 'action':
		if '_____' in player.hand:
			return('_____')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') 
		elif Ref.feasible(player, 'Gold'): return('Gold')
		elif Ref.feasible(player, '_____') and player.total('_____') == 0: return('_____')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	



def ai_Remodel1(phase, player, opponents, Ref): 
	if phase == 'action':
		if 'Remodel' in player.hand:
			return('Remodel')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') 
		elif Ref.feasible(player, 'Gold'): return('Gold')
		elif Ref.feasible(player, 'Remodel') and player.total('Remodel') == 0: return('Remodel')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	

def ai_Salvager1(phase, player, opponents, Ref):   #
	if phase == 'action':
		if 'Salvager' in player.hand:
			return('Salvager')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') 
		elif Ref.feasible(player, 'Gold'): return('Gold')
		elif Ref.feasible(player, 'Salvager') and player.total('Salvager') == 0: return('Salvager')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	

def ai_Saboteur1(phase, player, opponents, Ref):   #
	if phase == 'action':
		if 'Saboteur' in player.hand:
			return('Saboteur')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') 
		elif Ref.feasible(player, 'Gold'): return('Gold')
		elif Ref.feasible(player, 'Saboteur') and player.total('Saboteur') == 0: return('Saboteur')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	


#-----------------------------------------------------------------------------------------------------------------------------	#
#			EFFECTIVE STRATEGIES												#
#				- Usually means has a 70+% win rate vs. Money							#
#-----------------------------------------------------------------------------------------------------------------------------	#
def ai_Nobles1(phase, player, opponents, Ref):   # 72% win vs. money
	if phase == 'action':
		if 'Nobles' in player.hand: 
			return('Nobles')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 2: return('Duchy')  # buy Duchy if there are fewer than 4 estates		
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold') and player.total('Gold') <= 0: return('Gold') 
		elif Ref.feasible(player, 'Nobles'): return('Nobles') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	

def ai_Inside_Job1(phase, player, opponents, Ref):   # THIS IS HERE AS A 1 ACTION TEMPLATE AI
	if phase == 'action':
		if 'Village' in player.hand:
			return('Village')
		elif 'Great_Hall' in player.hand:
			return('Great_Hall')
		elif 'Conspirator' in player.hand and len(player.inplay) >= 2:
			return('Conspirator')
		elif 'Pawn' in player.hand:
			return('Pawn')
		elif 'Minion' in player.hand and player.action == 1:
			return 'Minion'
		elif 'Steward' in player.hand and (player.action > 1 or player.hand.count('Estate') + player.hand.count('Copper') + player.hand.count('Curse') >= 2):
			return('Steward')
		elif 'Bridge' in player.hand:
			return('Bridge')			
		elif 'Steward' in player.hand:
			return('Steward')
		elif 'Conspirator' in player.hand:
			return('Conspirator')
		elif 'Minion' in player.hand:
			return 'Minion'				
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') 
		elif Ref.feasible(player, 'Minion') and player.total('Minion') == 0: return('Minion')
		elif Ref.feasible(player, 'Conspirator') and player.total('Conspirator') + 3 < player.total('Minion') + player.total('Pawn') + player.total('Village') + player.total('Great_Hall'): return('Conspirator')
		elif Ref.feasible(player, 'Steward') and player.total('Steward') == 0: return('Steward')
		elif Ref.feasible(player, 'Silver') and player.total('Silver') == 0: return('Silver')
		elif Ref.feasible(player, 'Bridge') and player.total('Bridge') == 0: return('Bridge')
		elif Ref.feasible(player, 'Great_Hall') and player.total('Village') > 4: return('Great_Hall')
		elif Ref.feasible(player, 'Village'): return('Village')
		elif Ref.feasible(player, 'Pawn'): return('Pawn')
		else: return(False)
	elif phase == 'steward':
		if player.hand.count('Estate') + player.hand.count('Copper') + player.hand.count('Curse') >= 2:
			player.standard_trash()
			player.standard_trash()
		elif player.action > 1 and len(player.deck + player.discard) > 1: player.draw(2)
		else: player.treasure += 2
		return		
	else: raise IOError	

def ai_Attackers1(phase, player, opponents, Ref):
	if phase == 'action':
		if 'Stables' in player.hand:
			return('Stables')
		elif 'Bazaar' in player.hand:
			return('Bazaar')
		elif 'Market' in player.hand:
			return('Market')			

		elif 'Militia' in player.hand:
			return('Militia')	
		elif 'Oracle' in player.hand:
			return('Oracle')			
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') 
		elif Ref.feasible(player, 'Gold'): return('Gold')
	#	elif Ref.feasible(player, 'Stables') and player.total('Bazaar') > 1: return('Stables')
		elif Ref.feasible(player, 'Stables'): return('Stables')
		elif Ref.feasible(player, 'Militia') and player.total('Militia') == 0: return('Militia')
		elif Ref.feasible(player, 'Militia') and player.total('Militia') == 0 and player.total('Oracle') == 0 and player.turn > 5: return('Militia')
		elif Ref.feasible(player, 'Oracle') and player.total('Oracle') == 0 and player.total('Militia') < 2 and player.turn > 5: return('Oracle')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	

def ai_Crossroads_Plus1(phase, player, opponents, Ref):   # 77.1% win vs. Money
	if phase == 'action':
		if 'Crossroads' in player.hand: 
			return('Crossroads')
		elif 'Great_Hall' in player.hand:
			return('Great_Hall')
		elif 'Nobles' in player.hand:
			return('Nobles')
		elif 'Bridge' in player.hand:
			return('Bridge')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 2: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
	#	elif Ref.feasible(player, 'Harem') and player.total('Harem') + 1 < player.total('Nobles'): return('Harem') 
		elif Ref.feasible(player, 'Nobles'): return('Nobles') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')
		elif Ref.feasible(player, 'Bridge') and player.total('Bridge') == 0: return('Bridge') 
		elif Ref.feasible(player, 'Crossroads') and player.total('Crossroads') <= 1 and player.buy > 1: return('Crossroads') 
	#	elif Ref.feasible(player, 'Great_Hall') and player.total('Great_Hall') < player.total('Silver'): return('Great_Hall')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		elif Ref.feasible(player, 'Crossroads') and player.total('Crossroads') <= 1: return('Crossroads')
		else: return(False)
	else: raise IOError	

def ai_High_Mark1(phase, player, opponents, Ref):   # 95.6% win vs. Money
	if phase == 'action':
		if 'Highway' in player.hand:
			return('Highway')
		elif 'Market' in player.hand:
			return('Market')
		elif 'Chapel' in player.hand:
			return('Chapel')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Highway') and player.total('Highway') <= 1: return('Highway')
		elif Ref.feasible(player, 'Chapel') and player.total('Chapel') == 0: return('Chapel')
		elif Ref.feasible(player, 'Market') and player.total('Market') <= 1: return('Market')
		elif Ref.feasible(player, 'Highway') and player.total('Highway') <= 4: return('Highway')
		elif Ref.feasible(player, 'Market') and player.total('Market') <= 3: return('Market')
		elif Ref.feasible(player, 'Highway') and player.total('Highway') <= 6: return('Highway')		
		elif Ref.feasible(player, 'Province') and not losing_play: return('Province') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Market'): return('Market') 
		elif Ref.feasible(player, 'Silver') and player.total('Silver') < 2: return('Silver')
		else: return(False)
	else: raise IOError	

def ai_Sea_Hag1(phase, player, opponents, Ref):   # 91.2% win vs. money, 49 - 45 % wins over witch
	if phase == 'action':
		if 'Sea_Hag' in player.hand:
			return('Sea_Hag')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') 
		elif Ref.feasible(player, 'Gold'): return('Gold')
		elif Ref.feasible(player, 'Sea_Hag') and player.total('Sea_Hag') == 0: return('Sea_Hag')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	

def ai_Witch1(phase, player, opponents, Ref):   # 89.8% win vs. Money	This is a single witch strategy
	if phase == 'action':
		if 'Witch' in player.hand: 
			return('Witch')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Witch') and player.total('Witch') == 0: return('Witch')
		elif Ref.feasible(player, 'Gold'): return('Gold') 
		elif Ref.feasible(player, 'Silver'): return('Silver') 
		else: return(False)
	else: raise IOError	

def ai_Workshop_Gardens1(phase, player, opponents, Ref):   # 91.4% win vs. Money
	# This strategy involves exhausting the Village and Workshop supplies and then acquiring Gardens and Estates. It ensures the 
	# deck has 40+ cards before exhausting the 3rd supply pile.
	if phase == 'action':
		if 'Village' in player.hand:
			return('Village')	
		elif 'Workshop' in player.hand:
			return('Workshop')
		else: return(False)
	elif phase == 'buy':  # No province buying because strategy will never have enough money
	#	elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
	#	elif Ref.feasible(player, 'Gold'): return('Gold')
	#	elif Ref.feasible(player, 'Silver') and player.total('Silver') == 0: return 'Silver' # THIS HURTS THE STRATEGY!!!
	#	elif Ref.feasible(player, 'Laboratory'): return('Laboratory')
		if Ref.feasible(player, 'Village') and (player.total('Village') + 1 < player.total('Workshop') or Ref.supply['Workshop']==0): return('Village')
		elif Ref.feasible(player, 'Workshop'): return('Workshop')
		elif Ref.feasible(player, 'Gardens') and Ref.supply['Gardens'] > 1: return('Gardens')
		elif Ref.feasible(player, 'Gardens') and len(player.combine()) >= 39: return('Gardens')
		elif Ref.feasible(player, 'Estate') and len(player.combine()) >= 25: return('Estate') # this number is good, but I haven't done the reps to ensure optimality
		else: return(False)
	else: raise IOError		
	
def ai_Stable_Jack1(phase, player, opponents, Ref):   # 81.6% win vs. Money
	if phase == 'action':
		if 'Stables' in player.hand and player.treasure < 8:
			return('Stables')
		elif 'Jack_of_All_Trades' in player.hand:
			return('Jack_of_All_Trades')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold'): return('Gold') # buy Gold
		elif Ref.feasible(player, 'Jack_of_All_Trades') and player.total('Jack_of_All_Trades') == 0: return('Jack_of_All_Trades')
		elif Ref.feasible(player, 'Stables'): return('Stables')
		elif Ref.feasible(player, 'Silver'): return('Silver') # buy Silver
		else: return(False)
	else: raise IOError	
	
def ai_Spicey_Fool1(phase, player, opponents, Ref):   # 79.1% win vs. Money (Fools_Gold alone is 62.9% win vs. Money)
	# Probably woul be awesome with prosperity's Worker's Village card: extra buy would acquire F_G's faster plus occasional 13 treasure Prov-Duchy buy
	if phase == 'action':
		if 'Spice_Merchant' in player.hand and 'Copper' in player.hand:
			return 'Spice_Merchant'
		return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Spice_Merchant') and player.total('Spice_Merchant') == 0: return('Spice_Merchant')
		elif Ref.feasible(player, 'Fools_Gold'): return 'Fools_Gold'
		elif Ref.feasible(player, 'Gold'): return('Gold') 
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	elif phase == 'spice_merchant':
		player.hand.remove('Copper')
		player.buy += 1
		player.treasure += 2
		#if player.hand.count('Fools_Gold') == 2
	else: raise IOError	
	
def ai_Baron_Plus1(phase, player, opponents, Ref):   # 71.2% win vs. Money
	if phase == 'action':
		if 'Laboratory' in player.hand:
			return('Laboratory')
		elif 'Baron' in player.hand and ('Estate' in player.hand or player.turn > 9):
			return('Baron')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 4: return('Duchy')  # buy Duchy if there are fewer than 6 provinces
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold'): return('Gold') 
		elif Ref.feasible(player, 'Laboratory'): return('Laboratory') 
		elif Ref.feasible(player, 'Baron') and player.total('Baron') == 0: return('Baron')
		elif Ref.feasible(player, 'Silver'): return('Silver') 
		else: return(False)
	else: raise IOError	
#-----------------------------------------------------------------------------------------------------------------------------	#
#			MIDLEVEL STRATEGIES													#
#				- Multicard strategies beating Money less than 70% of the time				#
#				- Some are candidates for improvement									#
#-----------------------------------------------------------------------------------------------------------------------------	#

def ai_Trader_Cache1(phase, player, opponents, Ref):   # 68.8% vs. Money
	if phase == 'action':
		if 'Trader' in player.hand and ('Estate' in player.hand or 'Curse' in player.hand or ('Silver' in player.hand and player.wealth() < 5) or ('Copper' in player.hand and player.wealth() < 5) or ('Copper' in player.hand and player.treasure + player.wealth() == 7) or ('Copper' in player.hand and player.treasure + player.wealth() > 8)): 
			return('Trader')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Cache') and 'Trader' in player.hand: return('Cache')
		elif Ref.feasible(player, 'Gold'): return('Gold') 
		elif Ref.feasible(player, 'Trader') and player.total('Trader') == 0: return('Trader')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	

def ai_Fest_Mar_Smith1(phase, player, opponents, Ref):   # 63.9% vs. Money
	if phase == 'action':
		if 'Festival' in player.hand:
			return('Festival')
		elif 'Market' in player.hand:
			return('Market')
		elif 'Smithy' in player.hand:
			return('Smithy')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold'): return('Gold') # buy Gold
		elif Ref.feasible(player, 'Smithy') and player.total('Smithy') == 0: return('Smithy')
		elif Ref.feasible(player, 'Festival') and player.total('Festival') == 0: return('Festival')
		elif Ref.feasible(player, 'Market'): return('Market')
		elif Ref.feasible(player, 'Silver'): return('Silver') # buy Silver
		else: return(False)
	else: raise IOError	

def ai_Market_Smith1(phase, player, opponents, Ref):   # 65.1% vs. Money
	if phase == 'action':
		if 'Market' in player.hand:
			return('Market')
		elif 'Smithy' in player.hand:
			return('Smithy')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold'): return('Gold') # buy Gold
		elif Ref.feasible(player, 'Smithy') and player.total('Smithy') == 0: return('Smithy')
		elif Ref.feasible(player, 'Market'): return('Market')
		elif Ref.feasible(player, 'Silver'): return('Silver') # buy Silver
		else: return(False)
	else: raise IOError	

def ai_Scout_Plus1(phase, player, opponents, Ref):   # 65.8% vs. Money
	if phase == 'action':
		if 'Scout' in player.hand:
			return('Scout')
		elif 'Great_Hall' in player.hand:
			return 'Great_Hall'
		elif 'Trading_Post' in player.hand:
			return 'Trading_Post'
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Harem'): return('Harem') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Trading_Post') and player.total('Trading_Post') == 0: return('Trading_Post')
		elif Ref.feasible(player, 'Scout') and player.total('Scout') <= 1: return('Scout')
		elif Ref.feasible(player, 'Great_Hall') and player.total('Silver') > player.total('Great_Hall'): return 'Great_Hall' # Win % drops dramatically without Great_Halls!!!
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	

def ai_Stable_Crat1(phase, player, opponents, Ref):   # 65.3% win vs. Money
	if phase == 'action':
		if 'Stables' in player.hand and player.treasure < 8:
			return('Stables')
		elif 'Bureaucrat' in player.hand:
			return('Bureaucrat')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold'): return('Gold') # buy Gold
		elif Ref.feasible(player, 'Bureaucrat') and player.total('Bureaucrat') == 0: return('Bureaucrat')
		elif Ref.feasible(player, 'Stables'): return('Stables')
		elif Ref.feasible(player, 'Silver'): return('Silver') # buy Silver
		else: return(False)
	else: raise IOError	

def ai_Margrave1(phase, player, opponents, Ref):   # THIS IS HERE AS A 1 ACTION TEMPLATE AI
	if phase == 'action':
		if 'Margrave' in player.hand:
			return('Margrave')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') 
		elif Ref.feasible(player, 'Gold'): return('Gold')
		elif Ref.feasible(player, 'Margrave') and player.total('Margrave') == 0: return('Margrave')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	

def ai_Moneylender_Market1(phase, player, opponents, Ref):   # 53.5% win, 16% tie vs. Money
	if phase == 'action':
		if 'Market' in player.hand: 
			return('Market')
		elif 'Moneylender' in player.hand: 
			return('Moneylender')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold'): return('Gold') 
		elif Ref.feasible(player, 'Market'): return('Market')
		elif Ref.feasible(player, 'Moneylender') and player.total('Moneylender') == 0: return('Moneylender')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	
	
def ai_Smithy1(phase, player, opponents, Ref):   
	if phase == 'action':
		if 'Smithy' in player.hand: 
			return('Smithy')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold'): return('Gold') 
		elif Ref.feasible(player, 'Smithy') and player.total('Smithy') == 0: return('Smithy')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	
	
def ai_Jack1(phase, player, opponents, Ref):   # 78% win vs money - keep this 
	if phase == 'action':
		if 'Jack_of_All_Trades' in player.hand:
			return('Jack_of_All_Trades')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold'): return('Gold') # buy Gold
		elif Ref.feasible(player, 'Jack_of_All_Trades') and player.total('Jack_of_All_Trades') == 0: return('Jack_of_All_Trades')
		elif Ref.feasible(player, 'Silver'): return('Silver') # buy Silver
		else: return(False)
	else: raise IOError	
	
def ai_Market_Mine1(phase, player, opponents, Ref):   # 59.2% win vs. Money
	if phase == 'action':
		if 'Market' in player.hand: 
			return('Market')		

		elif 'Cellar' in player.hand: 
			return('Cellar')
		elif 'Mine' in player.hand: 
			return('Mine')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Cellar') and player.treasure == 10 and player.buy > 1: return('Cellar')
#		elif Ref.feasible(player, 'Silver') and T >= 11 and player.buy > 1: return('Silver')
		elif Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold'): return('Gold')
		elif Ref.feasible(player, 'Mine') and player.total('Mine') == 0: return('Mine')
		elif Ref.feasible(player, 'Market'): return('Market')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		elif Ref.feasible(player, 'Cellar') and player.total('Cellar') == 0: return('Cellar')
		else: return(False)
	else: raise IOError	
	
def ai_Militia1(phase, player, opponents, Ref):   
	if phase == 'action':
		if 'Militia' in player.hand:
			return('Militia')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') 
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') 
		elif Ref.feasible(player, 'Gold'): return('Gold')
		elif Ref.feasible(player, 'Militia') and player.total('Militia') == 0: return('Militia')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	
#-----------------------------------------------------------------------------------------------------------------------------	#
#			PLAYTEST STRATEGIES													#
#				- Usually 1 card strategies meant to playtest a new card					#
#				- Keep the baseline money strategy										#
#				- Keep strategy forever if it has a unique action card ai component			#
#-----------------------------------------------------------------------------------------------------------------------------	#

# MONEY1: The baseline strategy, it buys Provinces, Gold, and Silver always and Duchies and Estates as the end of game draw close
# 40.0% win, 20.0% tie against itself
def ai_Money1(phase, player, opponents, Ref):  # T is treasure, S is supply
	if phase == 'action': return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold'): return('Gold') # buy Gold
		elif Ref.feasible(player, 'Silver'): return('Silver') # buy Silver
		else: return(False)
	else: print "Error in ai_Money1"		

def ai_Trader1(phase, player, opponents, Ref):   
	if phase == 'action':
		if 'Trader' in player.hand and ('Estate' in player.hand or 'Curse' in player.hand or ('Copper' in player.hand and player.wealth() < 5) or ('Copper' in player.hand and player.treasure + player.wealth() == 7) or ('Copper' in player.hand and player.wealth() > 8)): 
			return('Trader')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold'): return('Gold') 
		elif Ref.feasible(player, 'Trader') and player.total('Trader') == 0: return('Trader')
		elif Ref.feasible(player, 'Silver'): return('Silver')
		else: return(False)
	else: raise IOError	
	
def ai_Mandarin1(phase, player, opponents, Ref):   # This version ensures you have 1 gold before buying provinces
	if phase == 'action':
		if 'Mandarin' in player.hand: 
			return('Mandarin')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Mandarin') and player.total('Mandarin') == 0: return('Mandarin')
		elif Ref.feasible(player, 'Gold'): return('Gold') # buy Gold
		elif Ref.feasible(player, 'Silver'): return('Silver') # buy Silver
		else: return(False)
	elif phase == 'mandarin': # Here choose a card to put back on top of the deck
		if player.action == 0 and 'Mandarin' in player.hand: return 'Mandarin' 
		elif player.wealth() > 10 and 'Gold' in player.hand: return 'Gold'
		elif player.wealth() >= 10 and 'Silver' in player.hand: return 'Silver'			
		elif player.wealth() >= 9 and 'Copper' in player.hand: return 'Copper'
		elif  'Copper' in player.hand and player.wealth() == 7: return 'Copper'
		elif  'Copper' in player.hand and player.wealth() == 4: return 'Copper'
		elif list(set(Ref.strict_victory_cards) & set(player.hand)) != []:
			union = list(set(Ref.strict_victory_cards) & set(player.hand))
			return union[0]
		elif 'Copper' in player.hand: return 'Copper'
		elif 'Silver' in player.hand: return 'Silver'
		else:
			print "Error in Mandarin1 AI"
			return 'Gold'	
	else: raise IOError	
	
def ai_Cellar1(phase, player, opponents, Ref):   # This version ensures you have 1 gold before buying provinces
	if phase == 'action':
		if 'Cellar' in player.hand: 
			return('Cellar')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Cellar') and player.total('Cellar') == 0 and player.wealth() < 5: return('Cellar')
		elif Ref.feasible(player, 'Gold'): return('Gold') # buy Gold
		elif Ref.feasible(player, 'Silver'): return('Silver') # buy Silver
		else: return(False)
	elif phase == 'cellar': # Here choose a card to put back on top of the deck
		cards = []
		for i in range(len(player.hand)):
			if player.hand[i] in Ref.strict_victory_cards or player.hand[i] == 'Copper':
				cards.append(player.hand[i])
		if cards == []: stopper = 1
		else: stopper = 0
		return cards, stopper						
	else: raise IOError	
	
def ai_Cellar2(phase, player, opponents, Ref):   # This version ensures you have 1 gold before buying provinces
	if phase == 'action':
		if 'Cellar' in player.hand: 
			return('Cellar')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 4 estates
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Cellar') and player.total('Cellar') == 0 and player.wealth() < 5: return('Cellar')
		elif Ref.feasible(player, 'Gold'): return('Gold') # buy Gold
		elif Ref.feasible(player, 'Silver'): return('Silver') # buy Silver
		else: return(False)
	elif phase == 'cellar': # Here choose a card to put back on top of the deck
		cards = []
		for i in range(len(player.hand)):
			if player.hand[i] in Ref.strict_victory_cards or ( player.turn > 4 and player.hand[i] == 'Copper' ):
				cards.append(player.hand[i])
		if cards == []: stopper = 1
		else: stopper = 0
		return cards, stopper						
	else: raise IOError	
	
def ai_Spice_Merchant1(phase, player, opponents, Ref):   # So far, a pretty shitty strategy
	if phase == 'action':
		if 'Spice_Merchant' in player.hand:
			return('Spice_Merchant')
		else: return(False)
	elif phase == 'buy':
		losing_play = Ref.supply['Province'] == 1 and player.score() + 6 < max( opponent.score() for opponent in opponents )
		if Ref.feasible(player, 'Province') and not losing_play: return('Province') # buy Province
		elif Ref.feasible(player, 'Duchy') and Ref.supply['Province'] <= 5: return('Duchy')  # buy Duchy if there are fewer than 6 provinces
		elif Ref.feasible(player, 'Estate') and Ref.supply['Province'] == 1 and len(player.deck) >= 10: return('Estate') # buy Estate if only 1 province and cards in deck
		elif Ref.feasible(player, 'Gold'): return('Gold') # buy Gold
		elif Ref.feasible(player, 'Spice_Merchant') and player.total('Spice_Merchant') == 0: return('Spice_Merchant')
		elif Ref.feasible(player, 'Silver'): return('Silver') # buy Silver
		else: return(False)
	else: raise IOError	

# THE FOLLOWING CARDS HAVE BEEN PLAY-TESTED AS 1 CARD STRATEGIES:
# DOMINION - BASE SET
# Non-Special Resolution Cards: Festival, Laboratory, Market, Smithy, Village, Woodcutter, Gardens
# Adventurer (44% win, 18% tie vs. money)
# Bureaucrat (54.7% win vs. money)
# Cellar
# Chancellor (48.5% win. 17% tie vs. money)
# Chapel (37% win vs. money)
# Council Room (56% win vs. money)
# Feast (silly by itself)
# Library (58% win. 16% tie vs. money)
# Militia (60% win vs. money)
# Mine (50% win, 20% tie vs. money)
# Moat (46% win, 18% tie vs. money)
# Moneylender (42% win, 20% tie vs. money)
# Remodel (43% win, 4% tie vs. money - but the baseline ai is incredibly stupid...I really phoned it in on this one)
# Spy (36% win vs. money)
# Thief (47.5% win, 15% tie vs. money)
# Throne Room (silly by itself)
# Workshop (a terrible 8% win vs. money)

# INTRIGUE
# Non-Special Resolution Cards: Great Hall, Harem
# Baron (58.2% win vs. money)
# Border Village
# Coppersmith (shitty so far)
# Inn (39% win vs money - a losing record!)
# Minion (44% win, 17% tie vs. money)
# Mining Village (shit vs. money)
# Pawn (super rudimentary)
# Steward (
# Shanty Town (45% win, 18% tie vs. money)
# Steward (51% win, 6% tie vs. money)
# Trading Post (50% win, 6% tie vs. money)
# Tribute (60% win, 15% tie vs. money)


# HINTERLANDS
# Non-Special Resolution Cards: Silk Road, Cache (resolved via gain function), Border Village, 
# Crossroads - terrible by itself
# Fools Gold - buy all 10, not 1 (62% win vs. money)
# Highway - 47% win, 17% tie vs. money
# Jack of all Trades - 77% win vs. money
# Margrave - 69% win vs. money
# Noble Brigand - 64.5% win vs. money
# Nomad Camp - 43% win, 20% tie vs. money
# Oasis - 38.5% win, 19% tie vs. money
# Stables - 47% win, 19% tie vs. money
# Steward - 54% win, 5% tie vs. money

# SEASHORE
# Non-Special Resolution Cards: Caravan, Fishing Village, Wharf, Treasury (resolved via cleanup function), Lighthouse
# Cutpurse (56.9% win vs. money)
# Explorer (61.5% win vs. money)
# Haven (34% win vs. money)
# Merchant Ship (58.2% win vs. money)
# Treasure Map (37% win vs. money)
# Warehouse (45% win, 19% tie vs. money)


