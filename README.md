# The Farmer Was Replaced — Automation Scripts

>TheFarmerWasReplaced()_

Scripts d'automatisation pour le jeu [The Farmer Was Replaced](https://store.steampowered.com/app/2060160).

Le jeu consiste à programmer un drone en Python pour automatiser une ferme.

## Structure
- `single_drone/` — scripts pour 1 drone
- `multi_drone/` — scripts parallélisés (N drones)
- `leaderboard/` — scripts optimisés pour les records

## Architecture
Chaque culture a son propre fichier. `main.py` orchestre les priorités selon les seuils de ressources définis en variables.

## Algorithmes
Voir [docs/algorithms.md](docs/algorithms.md)
