import res as test
import os

jsonfile ="testResume.json"
#perfekt:pdffile = "Murali_Project Manager QA.pdf"
pdffile = "Abiral_Pandey_Fullstack_Java.pdf"
test.pdf_to_json(pdffile,jsonfile)
print(test.run(jsonfile))
#print(test.get_job()["jobs"][1])
#test.correct_result(pdffile, "Java Developer")