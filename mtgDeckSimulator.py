import random
## runSimulation() draws from a particular MTG deck. Checks for
## mulligan, mana screw, mana flood, and color screw. Ignored factors
## include mana curve and creature/non-creature.
class Card():
def __init__(self, isLand=True, colors=None):
#color order: R, W, U
self.produce = [0,0,0]
self.cost = [0,0,0]
self.isLand = isLand
if isLand:
self.produce = list(colors)
self.tapped = (sum(colors) != 1) #non-basics enter tapped
else:
self.cost = list(colors)
self.tapped = False
def print(self):
if self.isLand:
print("Land with colors", self.produce)
else:
print("Spell with cost", self.cost)
def createCardList():
cardList = []
#Basic Lands
for i in range(5):
cardList.append(Card(isLand=True, colors=[1,0,0]))
for i in range(4):
cardList.append(Card(isLand=True, colors=[0,1,0]))
for i in range(3):
cardList.append(Card(isLand=True, colors=[0,0,1]))
#Non-basic lands
for i in range(2):
cardList.append(Card(isLand=True, colors=[1,1,1]))
cardList.append(Card(isLand=True, colors=[1,1,0]))
cardList.append(Card(isLand=True, colors=[1,0,1]))
cardList.append(Card(isLand=True, colors=[0,1,1]))
#morphs count as uncolored spells
for i in range(9):
cardList.append(Card(isLand=False, colors=[0,0,0]))
for i in range(3): #R
cardList.append(Card(isLand=False, colors=[1,0,0]))
for i in range(2): #W
cardList.append(Card(isLand=False, colors=[0,1,0]))
for i in range(1): #U
cardList.append(Card(isLand=False, colors=[0,0,1]))
for i in range(2): #RR
cardList.append(Card(isLand=False, colors=[2,0,0]))
for i in range(1): #UU
cardList.append(Card(isLand=False, colors=[0,0,2]))
for i in range(5): #RWU
cardList.append(Card(isLand=False, colors=[1,1,1]))
return cardList
def countLands(hand):
return sum([1 for card in hand if card.isLand])
def colorSources(hand):
return [sum([card.produce[i] for card in hand]) for i in range(3)]
#Assuming WRU is castable if we have source of all three; this isn't
#actually true when we have a W/R land and lots of U.
def castable(card, sources):
for color in range(3):
if card.cost[color] > sources[color]: return False
else:
return True
def mulliganCheck(hand):
lands = countLands(hand)
if(lands <= 1 or lands >= 6): return True
sources = colorSources(hand)
if(sources.count(0) <=1 ): return False #multiple colors, so keep
for card in hand:
if card.isLand: continue
if castable(card, sources): return False #Found castable spell, so keep
return True
def runSimulation(onThePlay = True):
cardList = createCardList()
random.shuffle(cardList)
#print("starting hand")
#for card in cardListcardList[:7]: card.print()
shs = 7 # startingHandSize
if(mulliganCheck(cardList[:shs])):
random.shuffle(cardList)
shs -= 1
if(mulliganCheck(cardList[:shs])): return 1 #mul to 5 fail
if onThePlay: shs-=1 # on turn n, we will have startingHandSize + n cards.
## Mana Screw
#missed three drop on turn four
turn4Lands = countLands(cardList[:shs+4])
if turn4Lands <= 2: return 2
if turn4Lands == 3 and cardList[shs+3].tapped == True: return 2
#missed four drop on turn five
turn5Lands = countLands(cardList[:shs+5])
if turn5Lands <= 3: return 3
if turn5Lands == 4 and cardList[shs+4].tapped == True: return 3
#4 land on turn 8
if countLands(cardList[:shs+8]) <= 4: return 4
## Mana Flood
# <= 4 spells on turn 6
turn6Spells = 6 + shs - countLands(cardList[:shs+6])
if turn6Spells <= 4: return 5
## Color screw
# count uncastable
sources = colorSources(cardList[:shs+6])
uncastable = sum([1 for card in cardList if not castable(card, sources)])
if uncastable >= 3: return 6
return 0
print("on the play")
a = [runSimulation(onThePlay = True) for i in range(1000)]
print([a.count(i) for i in range(7)])
print("on the draw")
a = [runSimulation(onThePlay = False) for i in range(1000)]
print([a.count(i) for i in range(7)])
