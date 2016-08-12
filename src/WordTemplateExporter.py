from docxtpl import DocxTemplate


class WordTemplateExporter:

    def __init__(self, template_path):
        self.template = DocxTemplate(template_path)

    def save_file(self, content, path):
        self.template.render(content)
        self.template.save(path)