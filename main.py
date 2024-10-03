from Paper import Paper
import os
import Mark


def txt_format(results, filename):
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
        if filename.endswith(".docx"):
            if filename.startswith('~$'):
                continue
            student_file = os.path.join(folder_path, filename)
            student_test = Paper(student_file)
            marker.set_student_paper(student_test)
            student_result = marker.compare_solution_with_student()
            print(f"Successfully Marked{filename} w/ {student_result[-1]}")
            print_to_file(student_result, folder_path, filename)


def main():
    key2 = '/Users/Matthew/Downloads/AnswerKey.docx'
    folder_path = '/Users/Matthew/Downloads/Quiz1 Oct 3 2024'
    mark_student_papers(key2, folder_path)

    #     # if len(sys.argv) != 3:
    #     #     print("Usage: python mark_papers.py <solution_file> <folder_path>")
    #     #     sys.exit(1)
    #     #
    #     # key = load_as_table(sys.argv[1])
    #     # folder_path = sys.argv[2]


if __name__ == '__main__':
    main()
