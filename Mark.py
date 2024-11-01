import Paper


class Marker:
    MARKED = ["X", "x"]
    TOTAL = 15
    PENALTY = 0.5

    def __init__(self, solution: Paper, student_paper: Paper):
        """
        Default constructor used to mark student papers
        :param solution: Answer Key
        :param student_paper: Student Paper
        """
        self.student_paper = student_paper
        self.solution = solution

    @classmethod
    def with_only_solution(cls, solution: Paper):
        """
        Used when marking multiple papers to avoid making multiple Marker Objects for multiple Papers
        :param solution: The Answer Key
        :return: Marker Object
        """
        return cls(solution, None)

    def set_student_paper(self, student_paper: Paper):
        """
        Sets the student paper
        :param student_paper: Paper Object
        :return: None
        """
        self.student_paper = student_paper

    def get_row_score(self, correct: list, max_num_correct: int, student_marked, no_penalty=True):
        """
        Calculates the Row score taking in the penalty, marked answers and correct marks.

        :param correct: Number of Correct student answers
        :param max_num_correct: Number of Correct solutions
        :param student_marked: Number of student marked
        :param no_penalty: Boolean flag to avoid penalizing students for guessing on 2-3 correct solutions.
        :return:
        """
        score = (len(correct) / max_num_correct) - (self.PENALTY * (student_marked - len(correct)) / max_num_correct)
        score = round(score, 2)
        if score == 0.17 and no_penalty:
            score = 0.33
        elif score == .25 and no_penalty:
            score = .5
        return score if score > 0 else 0

    def cell_match(self, student_cell, solution_cell):
        """
        :param student_cell: An X or an x or non-empty
        :param solution_cell:  An x or an X or non-empty
        :return:
        """
        if student_cell.lower() == 'x' and solution_cell.lower() == 'x':
            return True
        else:
            return student_cell and solution_cell

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
            sol_key = []
            stud_ans = []
            for c in range(1, len(self.solution.get_column_labels())):
                solution_cell, student_cell = self.solution.get_cell(r, c), self.student_paper.get_cell(r, c)
                if solution_cell:
                    sol_key.append(self.solution.get_column_labels()[c])
                if student_cell.lower() == 'x':
                    stud_ans.append(self.solution.get_column_labels()[c])
                if self.cell_match(student_cell, solution_cell):  # not empty string
                    correct.append(self.solution.get_column_labels()[c])
                elif solution_cell != student_cell:
                    errors.append(self.solution.get_column_labels()[c])
            score = self.get_row_score(correct, max_num_correct, student_marked)
            self.student_paper.total_score += score
            self.student_paper.graded_rows.append({
                "Q": r - 1,
                "Score": f"{score}",
                "Incorrect": errors,
                "Student": stud_ans,
                "Solution": sol_key,
                # "Correct": correct,
                "MaxCorrectAnswers": max_num_correct,
            })
        self.student_paper.graded_rows.append({"total": round(self.student_paper.total_score, 2),
                                               "percent": round(self.student_paper.total_score / self.TOTAL, 2)})
        return self.student_paper.graded_rows
