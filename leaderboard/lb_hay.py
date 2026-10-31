# Programme exécuté PENDANT la course Hay_Single (lancée depuis "classement") :
# un seul drone, ferme 8x8, objectif 100M de foin, puis le programme doit s'arrêter.
import polyculture

polyculture.farm(Entities.Grass, Items.Hay, 100000000)
