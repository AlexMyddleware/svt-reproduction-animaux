# Révijouer

Une application éducative pour apprendre sur la reproduction des animaux.

## Description

Cette application propose deux types de jeux éducatifs :
- **Texte à trous** : Complétez les phrases en faisant glisser les mots corrects dans les espaces vides.
- **Relier les images** : Connectez les images centrales aux mots corrects en traçant une ligne.

Toutes les questions sont en français et portent sur la reproduction des animaux.

## Installation

1. Clonez ce dépôt :
```
git clone https://github.com/votre-utilisateur/svt-reproduction-animaux.git
cd svt-reproduction-animaux
```

2. Créez un environnement virtuel et activez-le :
```
python -m venv .venv
source .venv/bin/activate
# Sur Windows : 
.venv\Scripts\activate
```
with debug

$env:SVT_DEBUG=1; python run.py


3. Installez les dépendances :
```
pip install -r requirements.txt
```

4. Lancez l'application :
```

python run.py
```

5. Ouvrez votre navigateur à l'adresse : http://localhost:5000

## Structure des données

Les questions sont stockées dans des fichiers JSON dans les répertoires suivants :
- `assets/Data/fill_the_blanks/` pour les questions de type "Texte à trous"
- `assets/Data/image_interaction/` pour les questions de type "Relier les images"

### Format des questions "Texte à trous"

```json
{
  "text": "La reproduction sexuée chez les grenouilles implique ________ qui se rencontrent dans l'eau.",
  "options": [
    "des gamètes",
    "des cellules",
    "des œufs",
    "des embryons"
  ],
  "correct_answer": "des gamètes"
}
```

### Format des questions "Relier les images"

```json
{
  "image": "assets/images/image_interaction/question1.png",
  "words": {
    "correct": "deux espèces différentes de grenouille",
    "incorrect": [
      "Un mâle et une femelle grenouille",
      "Une grenouille et un crapaud",
      "Une salamandre et une grenouille",
      "Un triton et un tétard"
    ]
  }
}
```

## Tests

Pour exécuter les tests :
```
pytest
```

## Licence

Ce projet est sous licence MIT.
