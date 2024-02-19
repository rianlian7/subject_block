import csv
import numpy as np

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

# Example usage:
file_path = 'studentData.csv'  # Update with your CSV file path
csv_data = read_csv_file(file_path)
print(csv_data[0][1:])
students_data = {}
subject_names = csv_data[0][1:]
for row in csv_data[1:]:
    subjectScore = []
    if row[0] != '':
        for col in row[1:]:
            if col == '':
                subjectScore.append(10)
            else:
                subjectScore.append(int(col))

        students_data[row[0]] = subjectScore

count = 0
for student in students_data.values():
    print("Student", count)
    count+=1
    print(student)


# Convert dictionary to numpy array
students_array = np.array(list(students_data.values()))

# Transpose the data
transposed_data = students_array.T
# Print transposed data
print("Transposed Data:")
for i, subject_data in enumerate(transposed_data, 1):
    print(f"Subject {i}: {subject_data}")


import numpy as np

def process_data_with_keys(data, subject_names):
    subjects_data = {}
    for i, subject_name in enumerate(subject_names):
        subjects_data[subject_name] = np.array(data[i])
    return subjects_data

# Process the data
subjects_data = process_data_with_keys(transposed_data, subject_names)
print(subjects_data)


# Function to count clashes between two subjects
def count_clashes(subject1_data, subject2_data):
    clashes = np.sum((subject1_data <= 7) & (subject2_data <= 7))
    non_selected = np.sum((subject1_data == 10) & (subject2_data == 10))
    return clashes, non_selected

# Function to report clashes between a subject and all other subjects
def report_clashes_for_subject(subject_name, subjects_data):
    clashes_report = {}
    subject_data = subjects_data[subject_name]
    for other_subject_name, other_subject_data in subjects_data.items():
        if other_subject_name != subject_name:
            clashes, non_selected = count_clashes(subject_data, other_subject_data)
            if clashes > 0 or non_selected > 0:
                clashes_report[other_subject_name] = (clashes, non_selected)
    return clashes_report

# Function to pair subjects together with the least amount of clashes
def pair_subjects_with_least_clashes(subjects_data):
    min_clashes = float('inf')
    min_non_selected = float('inf')
    best_pair = None
    for subject_name, subject_data in subjects_data.items():
        clashes_report = report_clashes_for_subject(subject_name, subjects_data)
        for other_subject_name, (clashes, non_selected) in clashes_report.items():
            if clashes < min_clashes or (clashes == min_clashes and non_selected < min_non_selected):
                min_clashes = clashes
                min_non_selected = non_selected
                best_pair = (subject_name, other_subject_name)
    return best_pair, min_clashes, min_non_selected

# Function to create subject blocks
def create_subject_blocks(subjects_data):
    blocks = []
    remaining_subjects = list(subjects_data.keys())
    while remaining_subjects:
        best_pair, min_clashes, min_non_selected = pair_subjects_with_least_clashes({k: subjects_data[k] for k in remaining_subjects})
        blocks.append((best_pair, min_clashes, min_non_selected))
        remaining_subjects.remove(best_pair[0])
        remaining_subjects.remove(best_pair[1])
    return blocks

# Create subject blocks
subject_blocks = create_subject_blocks(subjects_data)

# Display subject blocks with clashes and non-selected count
print("Subject Blocks:")
totalSuccess = 0
totalClash = 0
totalNonSelected = 0
for i, (block, clashes, non_selected_count) in enumerate(subject_blocks, 1):
    success = 13 - clashes - non_selected_count
    subject1, subject2 = block
    totalSuccess += success / 13 * 100
    totalClash += clashes / 13 * 100
    totalNonSelected += non_selected_count / 13 * 100
    print(f"Block {i}: {subject1} & {subject2}, Success: {success} {success / 13 * 100:.2f}%, Clashes: {clashes} {clashes / 13 * 100:.2f}%, Non-selected count: {non_selected_count} {non_selected_count / 13 * 100:.2f}%")

print("Average Success: ", round(totalSuccess / len(subject_blocks),2),"%")
print("Average Clash: ", round(totalClash / len(subject_blocks),2),"%")
print("Average Non-selected: ", round(totalNonSelected / len(subject_blocks),2),"%")
