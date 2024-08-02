# PDF Transcript Update Scripts

## Description
transcriptdriver.py:  loops through a list of students.  For each student in the list it calls updatepdf.py, passing student SSN and DOB information.
updatepdf.py: Opens the student's PDF Transcript file and updates it with their correct DOB and SSN information (necessary for transcript retrieval).

It's basic, but useful - needed to update 35000 pdf transcripts and did not have the system online to re-run them.  This was actually a much quicker solution.  regenerating would have taken 18 - 20 hours - this program took approx 35 minutes