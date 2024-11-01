import argparse
from Paper import Paper
import os
import Mark



def txt_format(results, filename):
    # Extracting total score and percentage
    total_score = results[-1]['total']
    total_percentage = results[-1]['percent'] * 100  # Convert to percentage

    # Creating the report string
    report = f"### {filename}t\n\n"
    report += f"**Total Score:** {total_score:.2f} / {len(results)-1}\n"
    report += f"**Percentage:** {total_percentage:.2f}%\n\n"
    report += "| Question | Score |    Student     |   Solution Key   | Incorrect Ans   |\n"
    report += "|----------|-------|----------------|------------------|-----------------|\n"

    # Adding each question's result to the report
    for item in results[:-1]:  # Exclude the last item (total)
        question = item['Q']
        score = round(float(item['Score']), 2)
        incorrect = ', '.join(item['Incorrect']) if item['Incorrect'] else 'None'
        # correct = ', '.join(item['Correct']) if item['Correct'] else 'None'
        student = ', '.join(item['Student'] if item['Student'] else 'None')
        solution = ', '.join(item['Solution']) if item['Solution'] else 'None'
        # max_correct = item['MaxCorrectAnswers']

        report += f"| {question:<8} | {score:<5} | {student:<15}| {solution:<15} | {incorrect:<15} |\n"

    return report


def delete_answer_sheet_files(student_file):
    os.remove(student_file)


def print_to_file(student_result, folder_path, filename):
    with open(f"{folder_path}/results.txt", 'a+') as f:
        f.write(txt_format(student_result, filename))


def mark_student_papers(solution_file_path, folder_path, delete_keyword=""):
    test_key = Paper(solution_file_path)
    marker = Mark.Marker(test_key)
    for filename in os.listdir(folder_path):
        if delete_keyword and delete_keyword in filename:
            delete_answer_sheet_files(delete_keyword)
        if filename.endswith(".pdf"):
            print(f"{filename} is a PDF file")
        if filename.endswith(".docx"):
            if filename.startswith('~$'):
                continue
            student_file = os.path.join(folder_path, filename)
            student_test = Paper(student_file)
            marker.set_student_paper(student_test)
            print(f"Marking {filename}")
            student_result = marker.compare_solution_with_student()
            print(f"Successfully Marked{filename} w/ {student_result[-1]}")
            print_to_file(student_result, folder_path, filename)


def mark_single_paper(solution_file_path, student_file_path):
    marker = Mark.Marker(Paper(solution_file_path))
    student_file = Paper(student_file_path)
    marker.set_student_paper(student_file)
    student_result = marker.compare_solution_with_student()
    print(txt_format(student_result, student_file_path))


def main():
    parser = argparse.ArgumentParser(description="Mark student papers based on a solution file.")
    parser.add_argument("solution_file", help="Path to the solution file")
    parser.add_argument("student_path", help="Path containing student paper(s)")
    parser.add_argument("-s", "--single", action="store_true", help="Mark Single Student")
    args = parser.parse_args()
    if args.single:
        print("Marking Single Paper")
        mark_single_paper(args.solution_file, args.student_path)
    else:
        mark_student_papers(args.solution_file, args.student_path)


if __name__ == '__main__':
    main()
