from docx import Document
import os
import pandas as pd
"""
Old Script, No longer in use
"""

MARKED = ["X", "x"]
TOTAL = 15
PENALTY = 0.5


def delete_answer_sheet_files(student_file):
    os.remove(student_file)


def mark_student_papers(solution_table, folder_path, delete_keyword=""):
    for filename in os.listdir(folder_path):
        if delete_keyword and delete_keyword in filename:
            delete_answer_sheet_files(delete_keyword)
        if filename.endswith(".docx"):
            if filename.startswith('~$'):
                continue
            student_file = os.path.join(folder_path, filename)
            print(student_file)
            student_test = load_as_table(student_file)
            student_result = compare_solution_with_student(solution_table, student_test)
            print_to_file(student_result, filename)


def print_to_file(student_result, filename):
    with open(f"results.txt", 'a+') as f:
        f.write(txt_format(student_result, filename))


def compare_solution_with_student(solution, student_test) -> list:
    """
    :post-condition: If student has more errors exceeding the total_score then it just is 0
    :param solution:
    :param student_test:
    :return:
    """
    solution = pd.DataFrame(solution)
    student_test = pd.DataFrame(student_test)

    column_labels = (solution.values[:-1][0])
    solution['num_of_correct'] = solution.apply(lambda row: (row == "X").sum(), axis=1)
    student_test['num_of_correct'] = student_test.apply(lambda row: (row == "X").sum(), axis=1)
    student_total_score = 0

    if solution.shape != student_test.shape:
        raise TypeError("Ruh roh - Tables have different dimensions! Please check!")
    rows_sum = []
    # Ignores the first two rows and last column
    for r in range(2, solution.shape[0]):
        student_marked = 0  # In the case where student marks 2 when only 1 is right. This is for leniency
        max_num_correct = solution.iloc[r, -1]
        errors = []
        correct = []
        solution_key = []
        for c in range(1, len(column_labels)):
            # If solution cell is not equal to student cell
            solution_cell, student_cell = solution.iloc[r, c], student_test.iloc[r, c]
            # TODO Not really needed as we can do sp.iloc as well
            student_marked += 1 if student_cell in MARKED else 0
            if solution_cell == 'X':
                solution_key.append(column_labels[c])
            if solution_cell != student_cell:
                errors.append(column_labels[c])
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
            "Solution": solution_key,
            # "Correct": correct,
            "MaxCorrectAnswers": max_num_correct,
        })
    rows_sum.append({"total": round(student_total_score, 2), "percent": round(student_total_score / TOTAL, 2)})
    return rows_sum


# TODO Develop a filter function that filters by submission time, goes into each folder and extracts data and renaming
def txt_format(results, filename):
    # Extracting total score and percentage
    total_score = results[-1]['total']
    total_percentage = results[-1]['percent'] * 100  # Convert to percentage

    # Creating the report string
    report = f"### {filename}t\n\n"
    report += f"**Total Score:** {total_score:.2f}\n"
    report += f"**Percentage:** {total_percentage:.2f}%\n\n"
    report += "| Question | Score | Incorrect Answers       | Solution Key | Max Correct Answers |\n"
    report += "|----------|-------|------------------------|-----------------|---------------------|\n"

    # Adding each question's result to the report
    for item in results[:-1]:  # Exclude the last item (total)
        question = item['Q']
        score = round(float(item['Score']), 2)
        incorrect = ', '.join(item['Incorrect']) if item['Incorrect'] else 'None'
        solution = ', '.join(item['Solution']) if item['Solution'] else 'None'
        max_correct = item['MaxCorrectAnswers']

        report += f"| {question:<8} | {score:<5} | {incorrect:<22} | {solution:<15} | {max_correct:<19} |\n"

    return report


def load_as_table(filepath: str) -> list:
    doc = Document(filepath)
    table = doc.tables[0]
    translated_table = []
    for row in table.rows:
        translated_table.append([cell.text for cell in row.cells])
    return translated_table
