"""Course format value object."""

from enum import Enum


class Format(str, Enum):
    """Format of a course."""

    ONLINE = "online"
    OFFLINE = "offline"
    MIXED = "mixed"


class EducationFormat(str, Enum):
    """Format of education process."""

    GROUP = "group"  # обучение в группе
    INDIVIDUAL = "individual"  # индивидуально с куратором / преподавателем
    SELF_PACED = "self_paced"  # самостоятельное обучение
    MENTORLED = "mentorled"  # с ментором (без фиксированной группы)
    COHORT = "cohort"  # поток / набор с датами
