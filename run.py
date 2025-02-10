# -*- encoding:utf-8-*-
import argparse
import random
import unicodedata
from time import time

from termcolor import colored


def fill_str(input_s="", max_size=10, fill_char=" "):
    # https://frhyme.github.io/python-libs/print_kor_and_en_full_half_width/
    l = 0
    for c in input_s:
        if unicodedata.east_asian_width(c) in ['F', 'W']:
            l+=2
        else:
            l+=1
    return input_s+fill_char*(max_size-l)


class CVLabNewSeatSorting:
    def __init__(self, priority_num, num_sort):

        with open('students.txt', 'r') as f:
            students = [l.strip() for l in f.readlines()]
            students = [l for l in students if l]

        self.priority_students = [name.rstrip("*") for name in students if name.endswith("*")]
        self.all_students = [name.rstrip("*") for name in students]
        self.non_priority_students = list(set(self.all_students) - set(self.priority_students))
        assert len(self.priority_students) <= priority_num, "우선순위 학생수가 우선순위 범위보다 더 많습니다."
        
        self.priority_num = priority_num
        self.num_sort = num_sort

        with open('cvlab_seat_preference.csv', 'r') as f:
            self.seat_preference = [l.strip()[1:-1] for l in f.readlines()]

    
    def sorting(self):
        priority_list = random.sample(range(self.priority_num), len(self.priority_students))
        non_priority_list = list(set(range(len(self.all_students)))-set(priority_list))
        
        random.shuffle(priority_list)
        random.shuffle(non_priority_list)

        num_tag_dict =[]
        for num, student in zip(self.priority_students, priority_list):
            num_tag_dict.append((num, student))
        for num, student in zip(self.non_priority_students, non_priority_list):
            num_tag_dict.append((num, student))

        all_numbers = priority_list+non_priority_list
        all_numbers.sort()      
        assert all_numbers == list(range(len(self.all_students))), "중복된 학생이 있습니다. csv 파일 명단 확인부탁드립니다."

        students = self.priority_students+self.non_priority_students
        students.sort()
        self.all_students.sort()
        assert students == self.all_students, "중복된 학생이 있습니다. csv 파일 명단 확인부탁드립니다."

        if self.num_sort:
            num_tag_dict.sort(key=lambda x:x[1])
        else:
            num_tag_dict.sort(key=lambda x:x[0])

        self.print_list(num_tag_dict)
        self.num_tag_dict = num_tag_dict
        
    def print_list(self, num_tag_dict):
        print(f"\n 자리 변경 순번입니다.")
        print(f">> 총 학생 {len(self.all_students)}명 / 우선권 학생: {len(self.priority_students)}명 / 우선권 범위: 1~{self.priority_num} <<\n")
        for k, v in num_tag_dict:
            if self.num_sort:
                print(f' {colored(fill_str(str(v+1)), "yellow")}{k}')
            else:
                print(f' {fill_str(k)}{colored(str(v+1), "yellow")}')

    def assign_seat(self):
        num_tag_dict = self.num_tag_dict
        seat_preference = self.seat_preference
        seat_preference_dict = {}
        for i, preference_sequence in enumerate(seat_preference):
            name = preference_sequence.split(',')[0]
            cur_seat = preference_sequence.split(',')[1]
            pref_seq = preference_sequence.split(',')[2:]
            seat_preference_dict[name] = (cur_seat, pref_seq)

        # check for invalid names
        for name in list(seat_preference_dict.keys()):  # Using list() to avoid runtime modification issues
            if name not in [student for student, num in num_tag_dict]:
                print(f"Invalid name: {name} removed from seat preference")
                seat_preference_dict.pop(name)

        assigned = {}  # Dictionary to track which seats are taken
        assignments = {}  # Dictionary to store final student->seat assignments

        # Assign seats based on ranking order
        for student, rank in num_tag_dict:
            current_seat, preferences = seat_preference_dict.get(student, (None, []))
            
            # Find the first available preferred seat
            assigned_seat = None
            for preferred_seat in preferences:
                if preferred_seat not in assigned and preferred_seat != current_seat:
                    assigned_seat = preferred_seat
                    break
            
            if assigned_seat:
                assigned[assigned_seat] = student
                assignments[student] = assigned_seat
            else:
                print(f"Warning: Could not assign preferred seat to {student}")

        # Print the final assignments
        print("\nFinal Seat Assignments:")
        for student, seat in assignments.items():
            print(f"{fill_str(student)}: {seat}")

        return assignments

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-priority', type=int, help='Max number of priority', default = 20)
    parser.add_argument('-num_first', action = 'store_true', help='Switch to print number first')
    args = parser.parse_args()

    ''' set a random seed as an integer HHMMSS (time: hours HH, minutes MM, seconds SS)'''
    random.seed(int(time()))

    seat = CVLabNewSeatSorting(args.priority, args.num_first)
    seat.sorting()
    seat.assign_seat()
