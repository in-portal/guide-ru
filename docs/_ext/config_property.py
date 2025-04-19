from docutils import nodes
from docutils.parsers.rst import Directive, directives

class ConfigProperty(Directive):
    """
    Этот шаблон создан для того, чтобы его можно было использовать при создании специальным
    образом оформленных списков переменных. Такие переменные так же будут якорями в той статье,
    где они описаны.
    """
    has_content = False
    required_arguments = 0
    option_spec = {
        'name': directives.unchanged_required,
        'type': directives.unchanged,
    }

    def run(self):
        name = self.options.get('name') # название переменной
        type = self.options.get('type') # ип входного значения (напр. int, string, bool)

        ret = []

        # Create anchor for direct access from the URL via "page_url#name".
        target_id = name.lower()
        target = nodes.target('', '', ids=[target_id])
        ret.append(target)

        # Register the label for referencing via ":ref:`name`".
        env = self.state.document.settings.env
        env.domaindata['std']['labels'][target_id] = (env.docname, target_id, name)

        # Create text to show.
        name_node = nodes.strong(text=name)
        ret.append(name_node)

        if type is not None:
            type_node = nodes.emphasis(text=" (" + type + ")")
            ret.append(type_node)

        return ret

def setup(app):
    app.add_directive("config-property", ConfigProperty)
