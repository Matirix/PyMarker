from docx import Document
import os
import sys
import pandas as pd

class Marker:

    MARKED = ["X", "x"]
    TOTAL = 15
    PENALTY = 0.5

    def __init__(self, student_paper, solution):
        self.student_paper = student_paper
        self.solution = solution

    def mark_student_papers(self):
        pass

    def compare_solution_with_student(self):
        pass
