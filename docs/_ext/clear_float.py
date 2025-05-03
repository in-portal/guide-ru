from docutils import nodes
from docutils.parsers.rst import Directive

class ClearFloat(Directive):
    has_content = False

    def run(self):
        return [nodes.raw('', '<div style="clear: both;"></div>', format='html')]

def setup(app):
    app.add_directive("clear-float", ClearFloat)
