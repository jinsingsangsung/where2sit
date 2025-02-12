# Where to sit in [CVLab](http://cvlab.postech.ac.kr/lab/index.php)?
This repository provides a simple interface to determine where to sit in CVLab.

## How to use
### Prepare files
You have two files to control the seat assignment: `students.txt`, and `cvlab_seat_preference.csv`.

- `students.txt` should contain names of all students who participate to the raffle.
Students with priorities are marked with asterisks.

- `cvlab_seat_preference.csv` shows seat preferences of each student. 
Each row contains {name}, {current seat}, {preference sequence} of a student.
To create this file, you may distribute this link (https://jinsingsangsung.github.io/where2sit/) to participants to create their rows,
and make people fill out the shared google spreadsheet. Make sure all people to use *copy to clipboard* button to ensure uniformity of each row.
<p align="center">
  <img src="https://github.com/user-attachments/assets/382231aa-5aba-4f00-a328-91316696bdc5" width="700"/>
</p>

### Run the seat assignment
Once you completed the above step, you may update both files of the repository.
Now you can go to https://jinsingsangsung.github.io/where2sit/seat_assignment.html to start the raffle!
The current version of the program can not handle some edge case of move chain, but still shows a valid cycles.
