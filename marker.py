from docx import Document
import pandas as pd

MARKED = ["X", "x"]
TOTAL = 15
PENALTY = 0.5


def compare_solution_with_student(solution, student_answer) -> list:
    """

    :post-condition: If student has more errors exceeding the total_score then it just is 0
    :param solution:
    :param student_answer:
    :return:
    """
    solution = pd.DataFrame(solution)
    student_answer = pd.DataFrame(student_answer)

    solution['num_of_correct'] = solution.apply(lambda row: (row == "X").sum(), axis=1)
    student_answer['num_of_correct'] = student_answer.apply(lambda row: (row == "X").sum(), axis=1)
    student_total_score = 0

    column_labels = ["Question", "A", "B", "C", "D", "E", "F"]
    if solution.shape != student_answer.shape:
        raise TypeError("Ruh roh - Tables have different dimensions! Please check!")
    rows_sum = []
    # Ignores the first two rows and last column
    for r in range(2, solution.shape[0]):
        student_marked = 0  # In the case where student marks 2 when only 1 is right. This is for leniency
        max_num_correct = solution.iloc[r, -1]
        errors = []
        correct = []
        for c in range(1, len(column_labels) - 1):
            # If solution cell is not equal to student cell
            solution_cell, student_cell = solution.iloc[r, c], student_answer.iloc[r, c]
            student_marked += 1 if student_cell in MARKED else 0
            if solution_cell != student_cell:
                errors.append(column_labels[c])
                # errors.append({
                #     "Q": r - 1,
                #     "Col": column_labels[c],
                #     # "Solution": solution.iloc[r,c],
                #     "Student": student_answer.iloc[r,c],
                #     "MaxCorrectAnswers": max_num_correct,
                # })
            elif solution_cell == student_cell and student_cell:  # not empty string
                correct.append(column_labels[c])
        # Student is penalized for incorrect answer by a factor 1 / max_num_correct
        # TODO Figure out the marking scheme
        score = (len(correct) / max_num_correct) - (PENALTY * (student_marked - len(correct)) / max_num_correct)

        student_total_score += (score if score > 0 else 0)
        rows_sum.append({
            "Q": r - 1,
            "Score": f"{score if score > 0 else 0}",
            "Incorrect": errors,
            "Correct": correct,
            "MaxCorrectAnswers": max_num_correct,
        })
    rows_sum.append({"total": round(student_total_score, 2), "percent": round(student_total_score / TOTAL, 2)})
    return rows_sum


def pretty_print(errors: list):
    print(errors[-1]["percent"])
    for error in errors:
        print(error)


# TODO Develop a filter function that filters by submission time, goes into each folder and extracts data and renaming

def print_to_file:
    pass

def load_as_table(filepath: str) -> list:
    doc = Document(filepath)
    table = doc.tables[0]
    translated_table = []
    for row in table.rows:
        translated_table.append([cell.text for cell in row.cells])
    return translated_table


def main():
    doc = ("/Users/Matthew/Downloads/Quiz1 Submission Sep 23, 2024/1804907-523120 - A01383660_Marc Angelo_Arnaldo_Feb "
           "16, 2024 1027 AM_COMP 2417-Quiz1-Answersheet.docx")
    doc2 = (
        '/Users/Matthew/Downloads/Quiz1 Submission Sep 23, 2024/1692876-523120 - A01349998_Irene_Cheung_Feb 16, 2024 1027 AM_COMP 2417-Quiz1-Answersheet.docx')
    table_1 = load_as_table(doc)
    table_2 = load_as_table(doc2)
    summary = compare_solution_with_student(table_1, table_2)
    pretty_print(summary)


if __name__ == '__main__':
    main()
