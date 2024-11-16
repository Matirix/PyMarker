from docx import Document
import os
import pandas as pd
import camelot.io


class DOCTYPE:
    PDF = ".pdf"
    DOC = ".docx"


class Paper:

    def __init__(self, file_path, grade=None, total_score=0, table_index=0):
        self.table = self.load_doc_as_table(filepath=file_path, table_index=table_index)
        self.column_labels = self.table.values[:-1][0]
        self.add_num_of_marked_as_col()
        self.grade = grade
        self.total_score = total_score
        self.graded_rows = []

    def load_as_table(self, file_path):
        if file_path.endswith(DOCTYPE.PDF):
            self.load_pdf_as_table(filepath=file_path)
        else:
            self.load_doc_as_table(filepath=file_path)

    def set_grade(self, grade: dict):
        self.grade = grade

    def get_column_labels(self):
        """
        :return: Returns the header
        """
        return self.column_labels

    def get_row_marked(self, row: int):
        return self.table.iloc[row, -1]

    def get_cell(self, row: int, col: int):
        return self.table.iloc[row, col]

    def load_doc_as_table(self, filepath: os, table_index=0) -> pd.DataFrame:
        """
        Takes the first table in a word document and turns it into an iterable array

        :param filepath: Word document
        :pre-condition: Must be a word document
        :pre-condition: Table must be the first table on the page
        :return: list
        """
        doc = Document(filepath)
        table = doc.tables[int(table_index)]
        translated_table = []
        for row in table.rows:
            translated_table.append([cell.text for cell in row.cells])
        return pd.DataFrame(translated_table)

    def load_pdf_as_table(self, filepath: str) -> pd.DataFrame:
        """
        Extracts the first table from a PDF document using camelot and converts it into a pandas DataFrame.

        :param filepath: PDF file path
        :pre-condition: Must be a valid PDF document
        :pre-condition: PDF must contain at least one table
        :return: pandas DataFrame
        """
        # Extract tables from the PDF file
        tables = camelot.read_pdf(filepath, pages='all', strip_text='\n')

        if tables:
            # Assuming the first table is the one we want
            first_table = tables[0].df
            return first_table

        raise ValueError("No tables found in the PDF document.")

    def add_num_of_marked_as_col(self) -> None:
        self.table['num_of_marked'] = self.table.apply(lambda row: (row.str.contains("X|x")).sum(), axis=1)


class GradedRow:
    def __init__(self, q_num, row_score, inc, cor, max_corr):
        self.q_num = q_num
        self.row_score = row_score
        self.inc = inc
        self.cor = cor
        self.max_corr = max_corr
