import openpyxl
from docxtpl import DocxTemplate


def render_docx(template_file_path, context, outfile):
    doc = DocxTemplate(template_file_path)
    doc.render(context)
    doc.save(outfile.name)


def render_xlsx(template_file_path, context, outfile):
    wb = openpyxl.load_workbook(template_file_path)
    ws = wb.active
    for row in context["tbl_contents"]:
        ws.append(row)
    wb.save(outfile.name)


renders_list = {
    "docx": render_docx,
    "xlsx": render_xlsx,
}


def register_render(name, render):
    if name is not str:
        raise ValueError("Name of render function must be a str")
    if not callable(render):
        raise ValueError("Render must be a callable object")
    renders_list[name] = render
