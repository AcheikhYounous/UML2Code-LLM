from django.shortcuts import render
from .xmi_parser import XMIParser
from .java_generator import JavaCodeGenerator
from .prompt_builder import build_enriched_prompt
from .prompting import build
from .llm_engine import generate_code_with_llm
from .forms import UploadXMIForm

def generate_view(request):
    if request.method == "POST":
        form = UploadXMIForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["xmi_file"]
            parser = XMIParser(file)
            classes = parser.parse()

            generator = JavaCodeGenerator(classes)
            java_code = generator.generate()


            #prompt = build_enriched_prompt(classes, java_code)
            prompt = build(classes, java_code)


            llm_result = generate_code_with_llm(prompt)

            return render(request, "interface.html", {
                "structure_code": java_code,
                "prompt": prompt,
                "llm_code": llm_result  # ✅ correspond au nom attendu dans le template
             })
    else:
        form = UploadXMIForm()
    
    return render(request, "interface.html", {"form": form})
