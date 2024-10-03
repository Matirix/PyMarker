from docx import Document
import os
import sys
import pandas as pd
import Paper


class Marker:
    MARKED = ["X", "x"]
    TOTAL = 15
    PENALTY = 0.5

    def __init__(self, student_paper: Paper, solution: Paper, ):
        self.student_paper = student_paper
        self.solution = solution

    def get_row_score(self, correct: list, max_num_correct: int, student_marked):
        """
        Calculates the Row score taking in the penalty, marked answers and correct marks.
        :param correct: Number of Correct student answers
        :param max_num_correct: Number of Correct solutions
        :param student_marked: Number of student marked
        :return:
        """
        score = (len(correct) / max_num_correct) - (self.PENALTY * (student_marked - len(correct)) / max_num_correct)
        return score

    def compare_solution_with_student(self, begin_from_row=2):
        """
        Marks the student papers and returns a graded paper
        :param begin_from_row: Sets the beginning of the row to skip headers
        :return:
        """
        for r in range(begin_from_row, self.solution.table.shape[0]):
            max_num_correct = self.solution.get_row_marked(row=r)
            student_marked = self.student_paper.get_row_marked(row=r)
            errors = []
            correct = []
            for c in range(1, len(self.solution.get_column_labels())):
                solution_cell, student_cell = self.solution.get_cell(r,c), self.student_paper.get_cell(r,c)
                if solution_cell != student_cell:
                    errors.append(self.solution.get_column_labels()[c])
                elif solution_cell == student_cell and student_cell:  # not empty string
                    correct.append(self.solution.get_column_labels()[c])
            score = self.get_row_score(correct, max_num_correct, student_marked)
            self.student_paper.total_score += (score if score > 0 else 0)
            self.student_paper.graded_rows.append({
                "Q": r - 1,
                "Score": f"{score if score > 0 else 0}",
                "Incorrect": errors,
                "Correct": correct,
                "MaxCorrectAnswers": max_num_correct,
            })
        self.student_paper.graded_rows.append({"total": round(self.student_paper.total_score, 2), "percent": round(self.student_paper.total_score / self.TOTAL, 2)})
        print(self.student_paper.graded_rows)



