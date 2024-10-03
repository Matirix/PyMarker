from docx import Document
import os
import sys
import Paper


class Marker:
    MARKED = ["X", "x"]
    TOTAL = 15
    PENALTY = 0.5

    def __init__(self, solution: Paper, ):
        self.student_paper = None
        self.solution = solution
    def set_student_paper(self, student_paper: Paper):
        self.student_paper = student_paper

    # def mark_student_papers(self, solution_file_path, folder_path, delete_keyword=""):
    #     test_key = Paper(solution_file_path)
    #     for filename in os.listdir(folder_path):
    #         if delete_keyword and delete_keyword in filename:
    #             self.delete_answer_sheet_files(delete_keyword)
    #         if filename.endswith(".docx"):
    #             if filename.startswith('~$'):
    #                 continue
    #             student_file = os.path.join(folder_path, filename)
    #             student_test = Paper(student_file)
    #             student_result = self.compare_solution_with_student(test_key, student_test)
    #             self.print_to_file(student_result, filename)

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
        return self.student_paper.graded_rows
    # def delete_answer_sheet_files(self, student_file):
    #     os.remove(student_file)
    #
    # def print_to_file(self, student_result, filename):
    #     with open(f"results.txt", 'a+') as f:
    #         f.write(self.txt_format(student_result, filename))

    def txt_format(self, results, filename):
        # Extracting total score and percentage
        total_score = results[-1]['total']
        total_percentage = results[-1]['percent'] * 100  # Convert to percentage

        # Creating the report string
        report = f"### {filename}t\n\n"
        report += f"**Total Score:** {total_score:.2f}\n"
        report += f"**Percentage:** {total_percentage:.2f}%\n\n"
        report += "| Question | Score | Incorrect Answers       | Correct Answers | Max Correct Answers |\n"
        report += "|----------|-------|------------------------|-----------------|---------------------|\n"

        # Adding each question's result to the report
        for item in results[:-1]:  # Exclude the last item (total)
            question = item['Q']
            score = round(float(item['Score']), 2)
            incorrect = ', '.join(item['Incorrect']) if item['Incorrect'] else 'None'
            correct = ', '.join(item['Correct']) if item['Correct'] else 'None'
            max_correct = item['MaxCorrectAnswers']

            report += f"| {question:<8} | {score:<5} | {incorrect:<22} | {correct:<15} | {max_correct:<19} |\n"

        return report


