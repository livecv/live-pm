import sys
import os

class DependencyTree:

    def __init__(self, tree):
        self.tree = tree

    def build_order(self):
        self.build_order = []

        order_solved = False
        while not order_solved:
            order_solved = True
            for key, value in self.tree.items():
                if not self._solve_build_order(key, value):
                    order_solved = False

        return self.build_order

    def _solve_build_order(self, name, node):
        build_order_solved = True

        if len(node) == 0:
            if name not in self.build_order:
                self.build_order.append(name)
        else:
            has_all_deps = True

            for key, value in node.items():
                if not self._solve_build_order(key, value):
                    build_order_solved = False
                    
                if key not in self.build_order:
                    has_all_deps = False

            if has_all_deps and name not in self.build_order:
                self.build_order.append(name)
            if not has_all_deps:
                build_order_solved = False

        return build_order_solved
                    
                    

            

