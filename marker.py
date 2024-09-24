from docx import Document
import pandas as pd


def compare_solution_with_student(solution, student_answer):
    solution, student_answer = pd.DataFrame(solution), pd.DataFrame(student_answer)
    if solution.equals(student_answer):
        print("tables are the same")
    else:
        print("Table values are not the same")

def load

def main():
    doc = Document("/Users/Matthew/Downloads/Quiz1 Submission Sep 23, 2024/1804907-523120 - A01383660_Marc Angelo_Arnaldo_Feb 16, 2024 1027 AM_COMP 2417-Quiz1-Answersheet.docx")
    tables = []
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            table_data.append([cell.text for cell in row.cells])
        tables.append(table_data)
    print(tables[0])


if __name__ == '__main__':
    main()