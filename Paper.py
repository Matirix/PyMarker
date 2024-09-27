from docx import Document
import os
import sys
import pandas as pd


class Paper:

    def __init__(self, file_path, grade=None):
        self.table = self.load_as_table(file_path)
        self.column_labels = self.table.values[:-1][0]
        self.add_num_of_marked_as_col()
        self.grade = grade

    def set_grade(self, grade: dict):
        self.grade = grade

    def get_column_labels(self) -> list:
        """
        :return: Returns the header
        """
        return self.column_labels

    def load_as_table(self, filepath: os) -> pd.DataFrame:
        """
        Takes the first table in a word document and turns it into an iterable array

        :param filepath: Word document
        :pre-condition: Must be a word document
        :pre-condition: Table must be the first table on the page
        :return: list
        """
        doc = Document(filepath)
        table = doc.tables[0]
        translated_table = []
        for row in table.rows:
            translated_table.append([cell.text for cell in row.cells])
        return pd.DataFrame(translated_table)

    def add_num_of_marked_as_col(self) -> None:
        self.table['num_of_marked'] = self.table.apply(lambda row: (row == "X").sum(), axis=1)

