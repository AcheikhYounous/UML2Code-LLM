import xml.etree.ElementTree as ET

class UMLClass:
    def __init__(self, name, id_):
        self.name = name
        self.id = id_
        self.attributes = []
        self.methods = []
        self.superclass = None
        self.associations = []  # [(target_class_name, multiplicity)]

class UMLMethod:
    def __init__(self, name, method_id):
        self.name = name
        self.id = method_id
        self.comment = None

class XMIParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.classes = []
        self.id_to_name = {}

    def parse(self):
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        comments = {}
        class_dict = {}

        # 1. Collecter tous les commentaires
        for elem in root.iter():
            tag = elem.tag.split("}")[-1]
            xmi_type = elem.attrib.get('xmi:type') or \
                       elem.attrib.get('{http://www.omg.org/spec/XMI/20131001}type') or \
                       elem.attrib.get('{http://www.omg.org/XMI}type')

            if tag == "ownedComment" and xmi_type == "uml:Comment":
                annotated_id = elem.attrib.get('annotatedElement')
                body = elem.find('./body')
                if annotated_id and body is not None:
                    comments[annotated_id] = body.text.strip()

        # 2. Collecter toutes les classes
        for elem in root.iter():
            tag = elem.tag.split("}")[-1]
            xmi_type = elem.attrib.get('xmi:type') or \
                       elem.attrib.get('{http://www.omg.org/spec/XMI/20131001}type') or \
                       elem.attrib.get('{http://www.omg.org/XMI}type')

            if tag == "packagedElement" and xmi_type == "uml:Class":
                class_id = elem.attrib.get('{http://www.omg.org/spec/XMI/20131001}id')
                class_name = elem.attrib.get('name')
                if not class_name or not class_id:
                    continue

                uml_class = UMLClass(class_name, class_id)
                self.id_to_name[class_id] = class_name

                for child in elem:
                    subtag = child.tag.split("}")[-1]

                    if subtag == "ownedAttribute":
                        name = child.attrib.get('name')
                        type_ = "String"
                        type_tag = child.find("type")
                        if type_tag is not None:
                            href = type_tag.attrib.get("href", "")
                            if "#Integer" in href:
                                type_ = "int"
                            elif "#Boolean" in href:
                                type_ = "boolean"
                            elif "#String" in href:
                                type_ = "String"
                        uml_class.attributes.append((name, type_))

                    elif subtag == "ownedOperation":
                        name = child.attrib.get('name')
                        method_id = child.attrib.get('{http://www.omg.org/spec/XMI/20131001}id')
                        uml_method = UMLMethod(name, method_id)
                        if method_id in comments:
                            uml_method.comment = comments[method_id]
                        uml_class.methods.append(uml_method)

                    elif subtag == "generalization":
                        superclass_id = child.attrib.get("general")
                        uml_class.superclass = superclass_id  # temp, resolved later

                class_dict[class_id] = uml_class

        # 3. Résoudre les noms de superclasses
        for cls in class_dict.values():
            if cls.superclass and cls.superclass in self.id_to_name:
                cls.superclass = self.id_to_name[cls.superclass]

        # 4. Récupérer les associations et les rattacher
        for elem in root.iter():
            tag = elem.tag.split("}")[-1]
            xmi_type = elem.attrib.get('xmi:type') or elem.attrib.get('{http://www.omg.org/spec/XMI/20131001}type')

            if tag == "packagedElement" and xmi_type == "uml:Association":
                member_ends = elem.attrib.get('memberEnd', '').split()
                ends = []

                for owned_end in elem.findall(".//ownedEnd"):
                    end_type = owned_end.attrib.get("type")
                    multiplicity = "1"
                    lower = owned_end.attrib.get("lowerValue")
                    upper = owned_end.attrib.get("upperValue")

                    if upper == "*" or (upper is None and "upperValue" in [e.tag for e in owned_end]):
                        multiplicity = "*"
                    elif upper is not None:
                        multiplicity = upper

                    ends.append((end_type, multiplicity))

                if len(ends) == 2:
                    (type1, mult1), (type2, mult2) = ends

                    class1 = class_dict.get(type1)
                    class2 = class_dict.get(type2)

                    if class1 and class2:
                        class1.associations.append((class2.name, mult2))
                        class2.associations.append((class1.name, mult1))

        self.classes = list(class_dict.values())
        return self.classes
