# Classements

Historique de mes courses de classement (`leaderboard_run`). Le code exact de chaque
temps correspond au commit qui ajoute la ligne.

| Date | Catégorie | Temps | Rang mondial | Script | Notes |
|---|---|---|---|---|---|
| 2026-10-31 | Hay_Single | 6:25.263 | #542 | `leaderboard/lb_hay.py` | Premier essai : polyculture sur toute la ferme 8x8 avec un seul drone (record mondial : 1:47.096) |
| 2026-10-31 | Hay_Single | 4:20.651 | #269 | `leaderboard/lb_hay_single.py` | 2 herbes au centre entourées de buissons, aller-retour : compagnon déjà en place 1 fois sur 3, sans aucun trajet |
| 2026-10-31 | Hay_Single | 4:17.440 | #262 | \leaderboard/lb_hay_single.py\ | Même code, relancé (variance aléatoire). Mesuré : action 0,03 s, repousse herbe 0,07 s avec eau, bonus x160 (81 920), 34,5 % des récoltes |
| 2026-10-31 | Hay_Single | 4:15.681 | #258 | \leaderboard/lb_hay_single.py\ | Eau gardée ≥ 0,95 + correction des compagnons voisins (40 % de bonus au lieu de 32 %). Stats de course : ~3 000 récoltes, 0,085 s par récolte, ~15 % du temps perdu en calcul |
| 2026-10-31 | Hay_Single | 3:55.271 | #232 | \leaderboard/lb_hay_single.py\ | Boucle déroulée et allégée (moins de calcul par tour) + corrections des compagnons voisins pour les 2 herbes. Boucle : ~235 s |
| 2026-10-31 | Wood | 4:59.081 | #77 | \leaderboard/lb_wood.py\ | Premier essai : damier d arbres, 32 blocs 4x8, compagnons plantés à la demande. Stats : 2,2 s par tour de bloc, ~50 % de récoltes avec bonus (record : 2:38.334) |
