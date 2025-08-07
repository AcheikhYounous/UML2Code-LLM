# Prompt pour CodeLlma-6.7-instruct-hf(On peut en anglais)
def build_prompt_from_code_structure(structure_code):
    return f"""[INST] 
Vous êtes un assistant expert en développement logiciel orienté objet.

Voici un extrait de code Java généré automatiquement à partir d’un diagramme de classes UML. Ce code ne contient que la structure (attributs, méthodes, relations), et chaque méthode est précédée d’un commentaire décrivant son comportement attendu (généré depuis les annotations UML).

Votre tâche est de générer uniquement **le corps des méthodes**, en respectant strictement :
- les signatures existantes,
- les types de retour,
- les noms d’attributs disponibles,
- et les commentaires donnés comme spécification fonctionnelle.

Ne changez pas les noms des méthodes, des classes ni les signatures.
Conservez l’ordre des méthodes et n’ajoutez rien d’autre que le contenu des méthodes.

Note : Générer le code sans commentaire.

Voici le code :

{structure_code}
[/INST]
"""

# Prompt pour Deepseek-Coder--instruct(On peut en anglais)
