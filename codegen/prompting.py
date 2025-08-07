# Prompt pour CodeLlma-6.7-instruct-hf(On peut en anglais)
import os

def build(uml_classes, code_structure):
    description = "Voici les informations extraites du diagramme de classes UML :\n\n"

    for cls in uml_classes:
        description += f"Classe : {cls.name}\n"
        if cls.superclass:
            description += f"  Hérite de : {cls.superclass}\n"
        if cls.attributes:
            description += "  Attributs :\n"
            for attr_name, attr_type in cls.attributes:
                description += f"    - {attr_type} {attr_name}\n"
        if cls.methods:
            description += "  Méthodes :\n"
            for method in cls.methods:
                comment = f" // {method.comment}" if method.comment else ""
                description += f"    - {method.name}(){comment}\n"
        if cls.associations:
            description += "  Associations :\n"
            for assoc_class, multiplicity in cls.associations:
                description += f"    - vers {assoc_class} (multiplicité : {multiplicity})\n"
        description += "\n"

    prompt = f"""[INST]
Vous êtes un assistant expert en développement Java orienté objet.

{description}

Voici le code Java structurel à compléter, généré automatiquement à partir du diagramme UML :

{code_structure}

Votre tâche est de générer  **uniquement le corps des méthodes** et réecrire tous les codes, en respectant :
- les signatures existantes,
- les types de retour,
- les noms d’attributs disponibles,
- et les commentaires fournis comme spécification comportementale,
- Réécrivez tout le code en remplaçant les méthodes vides par leur contenu.

N'ajouter pas d'autres constructeurs ni les getters et setters Ne modifiez rien d’autre. N’ajoutez pas de commentaire ou de documentation.
[/INST]
"""

    # 🔐 Sauvegarde automatique dans media/
    output_path = os.path.join("media", "prompt-final.txt")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    return prompt




