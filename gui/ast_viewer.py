# minicode_ide/gui/ast_viewer.py
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from antlr4.tree.Tree import TerminalNode

class ASTViewer(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderLabel("Árbol Sintáctico (AST)")

    def show_ast(self, tree, parser):
        self.clear()
        if not tree:
            return

        def add_node(parent_item, node):
            if isinstance(node, TerminalNode):
                item = QTreeWidgetItem(parent_item, [node.getText()])
                # item.setForeground(0, QColor("blue")) # Opcional: Colorear terminales
            else:
                rule_name = parser.ruleNames[node.getRuleIndex()]
                item = QTreeWidgetItem(parent_item, [rule_name])
                for i in range(node.getChildCount()):
                    add_node(item, node.getChild(i))

        root_item = QTreeWidgetItem(self, ["programa"]) # O la regla inicial de tu gramática
        add_node(root_item, tree)
        self.expandAll()