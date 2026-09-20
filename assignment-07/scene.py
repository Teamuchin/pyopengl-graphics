# CENG 487 Assignment7 by
# Timuçin Topcu
# StudentId:310201095
# 06.2025
class Scene:
    def __init__(self):
        self.nodes = []
        self.lights = []

    def add(self, node):
        self.nodes.append(node)

    def add_light(self, light):
        self.lights.append(light)

