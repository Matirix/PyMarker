# PyMarker v.0.1
Pymarker is a marking automation script I created for the purpose of marking student word documents that have a table
component on the first page. It compares two word documents, one student, and one key and returns the results based on a modifiable 
marking criteria. 

When the script is run, it will compare all of the word documents in a folder you've specified
and produce a text file where all the results of each word document is stored. 

It's still in its personalization phase so it  has to be tweaked for other uses.

To run you can the script, simply do:
- go to the package in the terminal
- python3 main.py <solution_key.docx> <folder_where_all_student_docx_are>

### V.0.1
After the first run I noticed that some of the columns could be confusing so I've changed a couple things.
1. I removed the  # of correct and # of total correct answers and replaced it with just student_answer and solution_key columns.