#!/usr/bin/env bash
# Synchronise les scripts entre le dossier de sauvegarde du jeu et ce dépôt.
#   ./sync.sh             jeu -> dépôt (à faire avant un commit)
#   ./sync.sh --to-game   dépôt -> jeu (recharger la sauvegarde si un fichier est nouveau pour le jeu)
# Le dossier du jeu peut être changé avec la variable TFWR_SAVE.
set -euo pipefail

GAME="${TFWR_SAVE:-/mnt/c/Users/maxim/AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced/Saves/Main}"
REPO="$(cd "$(dirname "$0")" && pwd)"

# Nom du fichier dans le jeu -> dossier dans le dépôt
declare -A MAP=(
	[grass]=Hay [polyculture]=Hay
	[wood]=Wood
	[carrot]=Carrots
	[pumpkin]=Pumpkins
	[sunflower]=Sunflowers
	[cactus]=Cactus
	[bone]=Dinausor
	[gold]=Maze
	[main]=core [move_to]=core
	[classement]=leaderboard [lb_hay]=leaderboard [reset]=leaderboard
)

# Fichiers du jeu volontairement non versionnés (utilitaires, succès Steam)
IGNORE=" __builtins__ succes clear leaderboard_pumpkins "

if [[ ! -d "$GAME" ]]; then
	echo "Dossier du jeu introuvable : $GAME" >&2
	exit 1
fi

if [[ "${1:-}" == "--to-game" ]]; then
	for name in "${!MAP[@]}"; do
		src="$REPO/${MAP[$name]}/$name.py"
		if [[ -f "$src" ]]; then
			cp "$src" "$GAME/$name.py"
			echo "-> jeu : $name.py"
		fi
	done
	exit 0
fi

for f in "$GAME"/*.py; do
	name="$(basename "$f" .py)"
	if [[ "$IGNORE" == *" $name "* ]]; then
		continue
	fi
	dir="${MAP[$name]:-}"
	if [[ -z "$dir" ]]; then
		echo "!! $name.py n'est rangé nulle part : ajoute-le dans MAP (sync.sh)"
		continue
	fi
	mkdir -p "$REPO/$dir"
	cp "$f" "$REPO/$dir/$name.py"
done

for name in "${!MAP[@]}"; do
	if [[ ! -f "$GAME/$name.py" && -f "$REPO/${MAP[$name]}/$name.py" ]]; then
		echo "!! $name.py n'existe plus dans le jeu (gardé dans le dépôt)"
	fi
done

echo "Synchronisé depuis $GAME"
