import enum
class STATUS_CHOICES(enum.Enum):
    Pending = "Pending"
    Completed = "Completed"
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)