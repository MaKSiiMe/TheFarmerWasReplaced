# The Farmer Was Replaced — Automation Scripts

>TheFarmerWasReplaced()_

Scripts d'automatisation pour le jeu [The Farmer Was Replaced](https://store.steampowered.com/app/2060160).

Le jeu consiste à programmer un drone en Python pour automatiser une ferme.
Ferme 32x32, 32 drones, toutes les améliorations au maximum.

## Structure

Un dossier par ressource, plus le code commun et les scripts de classement.

| Dossier | Fichiers | Rôle |
|---|---|---|
| `Hay/` | `grass.py`, `polyculture.py` | Foin, et le moteur de polyculture partagé avec le bois et les carottes |
| `Wood/` | `wood.py` | Bois (arbres en polyculture) |
| `Carrots/` | `carrot.py` | Carottes (polyculture) |
| `Pumpkins/` | `pumpkin.py` | Méga-citrouille sur toute la ferme |
| `Sunflowers/` | `sunflower.py` | Power, avec banc d'essai de 3 méthodes |
| `Cactus/` | `cactus.py` | Tri colonnes puis lignes, une seule récolte |
| `Dinausor/` | `bone.py` | Snake (chapeau dinosaure) |
| `Maze/` | `gold.py` | Labyrinthes réutilisés |
| `core/` | `main.py`, `move_to.py`, `succes.py`, `clear.py` | Orchestrateur, déplacements, succès Steam |
| `leaderboard/` | `classement.py`, `lb_hay.py`, `reset.py`, … | Courses de classement |

Le jeu impose des fichiers à plat dans son dossier de sauvegarde (les `import` se font
par nom de fichier). Ce dépôt les range par dossier, et [`sync.sh`](sync.sh) fait le lien :

```bash
./sync.sh             # copie les scripts du jeu vers le dépôt (avant un commit)
./sync.sh --to-game   # remet les scripts du dépôt dans le jeu
```

Chaque fichier de ferme se lance seul dans le jeu (`if __name__ == "__main__":`),
ou via `main.py` qui farme ce qui manque pour les déblocages.

## Classements

Historique des temps : [CLASSEMENTS.md](CLASSEMENTS.md).

## Architecture
Chaque culture a son propre fichier avec une fonction `farm(target)`. `main.py` choisit
la ressource la plus en retard par rapport au coût des déblocages restants et farme ses
ingrédients d'abord si besoin.

Les drones ne partagent pas de mémoire : chaque drone reçoit ses paramètres via
`spawn_drone(fonction, args...)` et travaille sur sa propre zone.

## Ressources cultivables

> Temps de pousse moyens tirés de [`docs/__builtins__.py`](docs/__builtins__.py).  
> **Eau** : `vitesse = 1 + (water_level × 4)` — à niveau max (1.0) → ÷5.  
> **Engrais** : retire **2s** du temps restant (usage unique, cumulable).

| Culture | Sol requis | Récolte | Temps de base | Avec eau max (÷5) | Avec engrais (−2s) |
|---------|-----------|---------|:-------------:|:-----------------:|:-----------------:|
| Dinosaur | Grassland ou Sol | Bone | ~0.2s | ~0.04s | **instantané** |
| Grass | Grassland ou Sol | Hay | ~0.5s | ~0.1s | **instantané** |
| Cactus | Sol | Cactus | ~1s | ~0.2s | **instantané** |
| Pumpkin | Sol | Pumpkin | ~2s | ~0.4s | **instantané** |
| Bush | Grassland ou Sol | Wood | ~4s | **~0.8s** | ~2s |
| Sunflower | Sol | Power | ~5s | **~1s** | ~3s |
| Carrot | Sol | Carrot | ~6s | **~1.2s** | ~4s |
| Tree | Grassland ou Sol | Wood | ~7s* | **~1.4s*** | ~5s* |

*\* Tree pousse plus lentement si des arbres voisins sont présents.*

## Algorithmes

- **Polyculture** (`Hay/polyculture.py`) — chaque drone gère un bloc de 4x8 : quelques
  cases « maison » portent la culture principale, les autres reçoivent le compagnon
  demandé (bonus x5, doublé à chaque amélioration). Si le compagnon tombe hors du bloc
  ou n'est pas abordable, on replante pour tirer une autre demande.
- **Cactus** (`Cactus/cactus.py`) — trier toutes les colonnes puis toutes les lignes
  suffit. Tri cocktail « double face » : sur chaque case on remet en ordre la paire
  derrière et devant (`measure()` coûte 1 tick, seuls `swap`/`move` coûtent cher).
  Simulé : ~490 actions par colonne au lieu de ~650.
- **Snake** (`Dinausor/bone.py`) — cycle hamiltonien + raccourcis vers la pomme sans
  dépasser la queue, coupés quand le serpent dépasse 30 % de la ferme (sinon les trous
  dans le corps forcent des tours complets). Simulé sur 32x32 : ~155k moves / ~8,4M ticks
  contre ~244k / 18M. Les méthodes à plus court chemin (arbre de cellules, DHCR) font
  4x moins de moves mais coûtent 50x plus en calcul dans ce jeu.
- **Labyrinthes** (`Maze/gold.py`) — 16 labyrinthes 8x8, 2 drones chacun (une moitié
  chacun). Chaque labyrinthe est cartographié une fois puis réutilisé 300 fois avec un
  plus court chemin (BFS) ; la carte s'enrichit quand des murs disparaissent.
- **Tournesols** (`Sunflowers/sunflower.py`) — vagues synchronisées sur `get_time()` :
  tous les drones récoltent les 15 pétales en même temps, puis les 14, etc.
