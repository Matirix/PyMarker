from docx import Document
import os
import sys
import pandas as pd


class Paper:

    def __init__(self, file_path, grade=None):
        self.table = self.load_as_table(file_path)
        self.grade = grade

    def set_grade(self, grade: dict):
        self.grade = grade

    def load_as_table(self, filepath: os) -> list:
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
        return translated_table

