from docutils import nodes
from docutils.parsers.rst import Directive, directives

class ConfigProperty(Directive):
    """
    This template is created to be used for creating specially formatted lists
    of variables. Such variables will also serve as anchors in the article
    where they are described.
    """
    has_content = False
    required_arguments = 0
    option_spec = {
        'name': directives.unchanged_required,
        'type': directives.unchanged,
        'ref_prefix': directives.unchanged,
    }

    def run(self):
        name = self.options.get('name') # variable name (e.g., Require_SSL)
        type = self.options.get('type') # data type (e.g., int, string, bool)
        ref_prefix = self.options.get('ref_prefix') # prefix for referencing this link on another page (e.g., cfg_)

        ret = []

        if ref_prefix is not None:
            # Create anchor for direct access from the URL via "page_url#name".
            target_id = name.lower()
            target = nodes.target('', '', ids=[target_id])
            ret.append(target)

            # Register the label for referencing via ":ref:`name`".
            env = self.state.document.settings.env

            label_id = ref_prefix.lower() + target_id
            env.domaindata['std']['labels'][label_id] = (env.docname, target_id, name)

        # Create text to show.
        name_node = nodes.strong(text=name)
        ret.append(name_node)

        if type is not None:
            type_node = nodes.emphasis(text=" (" + type + ")")
            ret.append(type_node)

        return ret

def setup(app):
    app.add_directive("config-property", ConfigProperty)
