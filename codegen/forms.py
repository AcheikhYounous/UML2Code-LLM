from django import forms

class UploadXMIForm(forms.Form):
    xmi_file = forms.FileField(label="Charger un fichier UML (.xmi)")