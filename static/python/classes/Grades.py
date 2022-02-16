from dataclasses import dataclass, field
from typing import Dict, List

from .Snowflake import Snowflake


@dataclass
class Grades(Snowflake):
    """
    Class to store the grades of a student in one course.
    :params:
        - student_id: The student's id.
        - course_id: The course's id.
        - grades: The grades of the student in the course. Is expected to be a dictionary in the format:
            {assignment_id: [grade, weight]}
        Default: {}
    :autogenerated attributes:
        - grades_list: A list of the student's grades with the weight taken into account.
        - average: The average of the student's grades.
        - median: The median of the student's grades.
        - mode: The mode of the student's grades.
        - range: The range of the student's grades.
        - grade_frequency: A dictionary with the frequency of each grade.
    """

    course_id: int
    student_id: int
    grades: Dict[int, List[float]] = field(default_factory=dict)
    grades_list: List[float] = field(default_factory=list)
    average: float = 0.0
    median: float = 0.0
    mode: float = 0.0
    range: float = 0.0
    grade_frequency: List[int] = field(default_factory=list)

    def __post_init__(self):
        self.grades_list = [
            grade[0] * (grade[1] / 100) for grade in self.grades.values()
        ]
        self.average = self.get_average()
        self.median = self.get_median()
        self.mode = self.get_mode()
        self.range = self.get_range()
        self.grade_frequency = self.get_grade_frequency()

    def get_average(self):
        return sum(self.grades_list) / len(self.grades_list)

    def get_median(self):
        self.grades_list.sort()
        if len(self.grades_list) % 2 == 0:
            return (
                self.grades_list[int(len(self.grades_list) / 2)]
                + self.grades_list[int(len(self.grades_list) / 2) - 1]
            ) / 2
        return self.grades_list[int(len(self.grades_list) / 2)]

    def get_mode(self):
        mode = []
        for grade in self.grades_list:
            if self.grades_list.count(grade) > len(self.grades_list) / 2:
                mode.append(grade)
        return mode

    def get_range(self):
        self.grades_list.sort()
        return self.grades_list[-1] - self.grades_list[0]

    def get_grade_frequency(self):
        return {grade: self.grades_list.count(grade) for grade in self.grades_list}
