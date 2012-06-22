## Dominion Auto Player v_3.0

# Significant changes from v2: Version 3 implements players as classes with class elements that
# include had, deck, discard, and inplay.
# Class-spcific functions are used to move cards to and from hand, deck, discard, etc.

# TO DO:
# 1. Data collection!!! Including mean/med./mode VP by turn, money by turn

import random
from Dominion_AI import *
from Dominion_Player import *
from Dominion_Cards import Card_Res

###################################
#		PARAMETERS
###################################
n_players = 3
reps = 5000
ai0 = 'Attackers'; ai1 = 'Inside_Job'; ai2 = 'Baron_Plus'; ai3 = 'Witch'
distro = 'random'        # 'random', '34', '43', and '52' are all valid
###################################

ai = [ai0, ai1, ai2, ai3]
ai = ai[0:n_players]

## DOMINION GAME SHELL
def shell(reps, n_players, ai, distro):	
	winner = []
	for r in range(1,reps+1):
	#	print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& NEW GAME &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
	#	print "\nThe AIs are", ai
		win = game(r, n_players, ai, distro, Ref = Card_Data(n_players))   # EVENTUALLY SAVE AS GAME DATA
		winner.append(win)
		# HERE WE ADD GAME_DATA TO TOTAL_DATA

	return(winner)
	
def game(r, n_players, ai, distro, Ref): # We pass in an initialized version of the Ref dict
	
	Cards = Card_Res()
	all_players = []
	for strategy in ai:
		all_players.append( Player( strategy, distro ) )
	#print "Player class objects initialized..."
	#print "Player 0 has hand", all_players[0].hand, "and deck", all_players[0].deck
	#print "Player 1 has hand", all_players[1].hand, "and deck", all_players[1].deck
	#print "Size of all_players vector is", len(all_players)
	
	#p0 = Player(ai[0])
	#p1 = Player(ai[1])
	#all_players = [p0, p1]

	iterator = [r%n_players, (r+1)%n_players]
	if n_players >= 3: iterator.append( (r+2)%n_players )
	if n_players == 4: iterator.append( (r+3)%n_players )
		
	while Ref.endgame() != True:  
	#	print "--------------------------------- NEW ROUND -------------------------------------"
		for i in iterator:   # This alternates between 0,1 and 1,0 (or 0,1,2 or 0,1,2,3 depending on number of player)
			if Ref.endgame() == True: break  # ADD ALTERNATE ENDGAME HERE AS WELL
			
			player = all_players[i] # MAYBE ALSO STORE TURN INFO HERE?
			opponents = all_players[0:i] + all_players[i+1:] # Slice out the ith entry
			player.turn += 1
			
			# CLEAN-UP BEGINNING
			player.bought = []
			player.gained = []
			
			# DURATION PHASE
			for card in player.duration:
				player.duration_effect(card)			
			
		#	print "******************* NEW TURN *******************"
		#	print "Strategy is", player.ai
		#	print "Opponent's last purchase was", opponents[0].bought
		#	if player.ai == 'Caravan':
		#	print "Hand is:", player.hand
		#	print "Discard is:", player.discard
		#	print "Deck is:", player.deck
		#	if player.duration != []:
		#		print "Duration is:", player.duration
		#	print "Inplay is:", player.inplay

			# ACTION PHASE
			stop_action = False
			while stop_action == False:
				if Ref.endgame() == True: break
				[player, opponents, Ref, stop_action] = actionplay(player, opponents, Ref, Cards)
			
			# BUY PHASE	
		#	if player.ai == 'High_Mark': print "Hand is now", player.hand
			stop_buy = False
			while stop_buy == False:
				if Ref.endgame() == True: break
				[player, Ref, stop_buy] = buyplay(player, opponents, Ref)
		
			# GAIN RESOLUTION PART 2 - this is sloppy, but it can't be done in Dominion_Player since the AI functions can't be imported into it
			if 'Border_Village' in player.gained:
				store = player.treasure
				player.treasure = 5
				card = ai_chooser('buy', player, opponents, Ref)
				player.gain(Ref, card)
				player.treasure = store	
			if 'Embassy' in player.gained:
				for opponent in opponents:
					opponent.gain(Ref, 'Silver')
			if 'Noble_Brigand' in player.bought:
				card_play.Noble_Brigand(player, opponents, Ref)
							
			# CLEAN-UP PHASE
		#	print "Before cleanup phase, player.bought is", player.bought
			player.cleanup(Ref)
	
	score = []
	for player in all_players:
		score.append( player.score() )
	
	win = winner(score)
	#print "\nAI_0 - ",ai0," scored ", score0, " points."
	#print "\n", all_players[0].ai, "s deck:", (all_players[0].deck + all_players[0].hand + all_players[0].discard + all_players[0].inplay)
	#print "Deck is",len( Player_Cards[0][0] + Player_Cards[0][1] + Player_Cards[0][2] ),"cards long"
	#print "AI_1 - ",ai1," scored ", score1, " points."
	#print "\n", all_players[1].ai, " deck:", (all_players[1].deck + all_players[1].hand + all_players[1].discard + all_players[1].inplay)
	#print "\nwinner is",win
	#print "Player", all_players[0].ai, "has cards", all_players[0].hand, all_players[0].deck, all_players[0].discard
	
	return(win)
	
def actionplay(player, opponents, Ref, Cards):
	if player.action == 0:
		return[player, opponents, Ref, True]
	else:
		#print "hand is",hand
		card = ai_chooser('action', player, opponents, Ref)

		if card == False:
			return[player, opponents, Ref, True]
		else: 
		#	if player.ai == 'THIS IS NOT AN AI NAME':
		#	print "treasure was", player.wealth()
		#	print "Playing action card", card
			player.hand.remove(card) # OR del hand[playcard]
			player.inplay.append(card)
		#	print "Cards in play are:", player.inplay
			player.action -= 1
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
	return[player, opponents, Ref, False]

def buyplay(player, opponents, Ref): 
	if player.buy == 0:
		return(player, Ref, True)
	else:
	#	if player.inplay != []: 
	#		print "discard is", player.discard		
		player.use_money(Ref)
	#	if player.ai == 'High_Mark':
	#		print "hand is now", player.hand
	#	print "inplay is", player.inplay
	#	print "treasure is", player.treasure
	#	print "number of buys is", player.buy
	#	if 'Scout' in player.inplay:
	#	print "cards in play are", player.inplay
	#	print "deck is not", player.deck
		purchase = ai_chooser('buy', player, opponents, Ref) #Currently using a dumy 0 to pass to action - use **kwargs to clean this up
		if purchase == False:
			return(player, Ref, True)
		else:
			if Ref.card_cost[purchase] - player.inplay.count('Highway') - player.inplay.count('Bridge') > player.treasure: print "ERROR - This card costs too much and shouldn't have been bought"
		#	if player.ai == 'High_Mark':
		#	print "You bought",purchase
			player.xbuy(opponents, Ref, purchase)
			return(player, Ref, False)

##################### END OF FUNCTIONS #######################			
winner = shell(reps, n_players, ai, distro)
winner0 = sum(row == 0 for row in winner)  # THESE SHOULDN'T BE ROWS, JUST Xs OR SOMETHING
winner1 = sum(row == 1 for row in winner)
winner2 = sum(row == 2 for row in winner)
winner3 = sum(row == 3 for row in winner)
tiegame = sum(row == 4 for row in winner)

print "\nModel ran",reps,"simulations"
print "ai_strategy",ai0,"won",100.0*round(winner0/float(winner0+winner1+winner2+winner3+tiegame),3),"percent"
print "ai_strategy",ai1,"won",100.0*round(winner1/float(winner0+winner1+winner2+winner3+tiegame),3),"percent"
if n_players > 2:
	print "ai_strategy",ai2,"won",100.0*round(winner2/float(winner0+winner1+winner2+winner3+tiegame),3),"percent"
if n_players > 3:
	print "ai_strategy",ai3,"won",100.0*round(winner3/float(winner0+winner1+winner2+winner3+tiegame),3),"percent"
print "tie game",100.0*round(tiegame/float(winner0+winner1+winner2+winner3+tiegame),3),"percent"
