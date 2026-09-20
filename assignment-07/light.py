# CENG 487 Assignment7 by
# Timuçin Topcu
# StudentId:310201095
# 06.2025
class Light:
    def __init__(self, light_type="point", position=(0, 0, 0), direction=(0, -1, 0), color=(1, 1, 1), intensity=1.0,
                 cone_angles=(15.0, 20.0), enabled=True):
        self.position = position
        self.direction = direction
        self.color = color
        self.intensity = intensity
        self.cone_angles = cone_angles
        self.enabled = enabled

        # 0: disabled, 1: directional, 2: point, 3: spot
        self.light_type_map = {"directional": 1, "point": 2, "spot": 3}
        self.type = self.light_type_map.get(light_type, 2)

    def toggle(self):
        self.enabled = not self.enabled