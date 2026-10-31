import polyculture

# Carottes : carottes en polyculture (voir polyculture.py)
def farm(target=None):
	if target == None:
		target = num_items(Items.Carrot) + 1000000
	polyculture.farm(Entities.Carrot, Items.Carrot, target)


# Lancé directement : farme cette ressource sans fin (arrête le programme quand tu veux)
if __name__ == "__main__":
	farm(1000000000000000)
