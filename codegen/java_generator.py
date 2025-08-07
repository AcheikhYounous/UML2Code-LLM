class JavaCodeGenerator:
    def __init__(self, classes):
        self.classes = classes

    def generate(self):
        code = ""
        uses_list = any(
            assoc[1] not in ("1", "0..1") for cls in self.classes for assoc in getattr(cls, 'associations', [])
        )

        if uses_list:
            code += "import java.util.List;\n\n"

        for cls in self.classes:
            # Héritage
            extends_clause = f" extends {cls.superclass}" if getattr(cls, 'superclass', None) else ""
            code += f"public class {cls.name}{extends_clause} " + "{\n"

            # Attributs
            for attr_name, attr_type in cls.attributes:
                code += f"    private {attr_type} {attr_name};\n"

            # Associations
            for target_class, multiplicity in getattr(cls, 'associations', []):
                if multiplicity in ("1", "0..1"):
                    code += f"    private {target_class} {target_class.lower()};\n"
                else:
                    code += f"    private List<{target_class}> {target_class.lower()}s;\n"

            # Constructeur vide
            code += f"\n    public {cls.name}() {{}}\n\n"

            # Méthodes
            for method in cls.methods:
                code += f"    public void {method.name}() {{\n"
                if method.comment:
                    code += f"        // {method.comment}\n"
                code += "    }\n"

            code += "}\n\n"

        return code


