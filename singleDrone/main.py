clear()
change_hat(Hats.Gold_Hat)
do_a_flip()

# Imports
import grass
import wood
import carrot
import pumpkin
import sunflower
import cactus
import gold

# Minimum stock thresholds — automatically increased when all are met
hay_needed = 100000
wood_needed = 100000
carrots_needed = 100000
pumpkins_needed = 100000
cactus_needed = 100000
gold_needed = 100000

# Priority loop: power → hay → wood → carrot → pumpkin → cactus → gold
while True:
	if num_items(Items.Power) < 100:
		while num_items(Items.Power) < 10000:
			sunflower.farm()
	elif num_items(Items.Hay) < hay_needed:
		grass.farm()
	elif num_items(Items.Wood) < wood_needed:
		wood.farm()
	elif num_items(Items.Carrot) < carrots_needed:
		carrot.farm()
	elif num_items(Items.Pumpkin) < pumpkins_needed:
		pumpkin.farm()
	elif num_items(Items.Cactus) < cactus_needed:
		cactus.farm()
	elif num_items(Items.Gold) < gold_needed:
		gold.farm()
	else:
		hay_needed += 10000
		wood_needed += 10000
		carrots_needed += 10000
		pumpkins_needed += 10000
		cactus_needed += 10000
		gold_needed += 10000
