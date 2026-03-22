# Algorithmes

## Tri cactus — Gradient Bubble Sort
Le cactus demande un tri 2D (valeurs croissantes vers Nord et Est)
pour déclencher une récolte en cascade (rendement n²).

Plusieurs algorithmes ont été évalués :
| Algo | Vitesse relative |
|---|---|
| Bubble Sort simple | ★★☆☆ |
| Cocktail Shaker | ★★★☆ |
| **Gradient Bubble Sort** | **★★★★** |

Le Gradient Bubble Sort combine un tri à bulles avec un backtracking
style insertion sort : après chaque swap, la petite valeur est
propagée aussi loin que possible dans la direction opposée.
Résultat : ~2x plus rapide que le bubble sort classique.

Chaque move() et swap() coûte 200 ticks — minimiser les déplacements
est aussi important que minimiser les swaps.

## Labyrinthe — DFS + heuristique measure()
`measure()` retourne la position du trésor depuis n'importe où.

Algorithmes évalués :
- **Right-hand rule** : simple mais bloque sur les îles
- **Greedy (measure() seul)** : bloque dans les culs-de-sac
- **DFS + visited set** : garanti de trouver le trésor
- **DFS + visited set + measure()** ← choix retenu

`measure()` ne remplace pas le pathfinding — les murs bloquent
toujours le chemin direct. Il sert à classer les directions
à explorer en priorité (heuristique), ce qui réduit le nombre
de cases explorées avant de trouver le trésor.

## Multi-drone — Un drone par colonne
La ferme est divisée en colonnes. Le drone principal se déplace
vers l'Est en spawnant un drone à chaque colonne.
Speedup théorique : ×N (N = nombre de drones disponibles).