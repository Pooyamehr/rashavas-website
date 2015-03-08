from core.db import *


class Entity(Base, IDMixin):
    name = Column(String(50))

    def __init__(self, name):
        self.name = name


