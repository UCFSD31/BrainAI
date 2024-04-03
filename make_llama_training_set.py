import random
import csv

def clear_csv(input_csv_file, output_csv_file):
    with open(input_csv_file, 'w') as file:
        pass
    with open(output_csv_file, 'w') as file:
        pass

def write_to_csv(data, output_csv_file):
    with open(output_csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

def read_from_csv(input_csv_file):
    with open(input_csv_file, mode = 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    return rows

directions = ["left", "right", "up", "down"]
csv_header = ["Llama_String", "Angle", "Servo", "Direction"]
empty_header = []
llama_string = ""
csv_file = "Llama_Training_Data.csv"
csv_file_random = "Llama_Training_Data_Random.csv"

clear_csv(csv_file, csv_file_random)

write_to_csv(csv_header, csv_file_random)



for runs in range(0, 200):
    for i in range (0, 91):
        for j in range(0, 6):
            degrees = i
            servo = j // 2
            direction = j % 2
            if(j < 4):
                if(random.choice([True, False]) == True):
                    if(random.choice([True, False]) == True):
                        llama_string = "turn " + directions[j] + " " + str(i) + " degrees"
                    else:
                        llama_string = "turn " + str(i) + " degrees " + directions[j]
                else:
                    if(random.choice([True, False]) == True):
                        llama_string = "move " + directions[j] + " " + str(i) + " degrees"
                    else:
                        llama_string = "move " + str(i) + " degrees " + directions[j]
            else:
                if(random.choice([True, False]) == True):
                    llama_string = "twist " + directions[j - 4] + " " + str(i) + " degrees"
                else:
                    llama_string = "twist " + str(i) + " degrees " + directions[j - 4]

            if(random.choice([True, False]) == True):
                if(random.choice([True, False]) == True):
                    llama_string = "please " + llama_string
                else:
                    llama_string = llama_string + " please"


            if(random.choice([True, False]) == True):
                if(random.choice([True, False]) == True):
                    llama_string = "can you " + llama_string
                else:
                    llama_string = "could you " + llama_string

            if(random.choice([True, False]) == True):
                llama_string = "llama " + llama_string

            new_data = [llama_string, degrees, servo, direction]
            write_to_csv(new_data, csv_file)


for runs in range(0, 1000):
    degrees = 0
    servo = 4
    direction = 2
    llama_string = "reset"

    if(random.choice([True, False]) == True):
        if(random.choice([True, False]) == True):
            llama_string = "please " + llama_string
        else:
            llama_string = llama_string + " please"


    if(random.choice([True, False]) == True):
        if(random.choice([True, False]) == True):
            llama_string = "can you " + llama_string
        else:
            llama_string = "could you " + llama_string

    if(random.choice([True, False]) == True):
        llama_string = "llama " + llama_string

    llama_string = llama_string.capitalize()

    new_data = [llama_string, degrees, servo, direction]
    write_to_csv(new_data, csv_file)

rows = read_from_csv(csv_file)
data_rows = rows[1:]
random.shuffle(data_rows)
data_rows = data_rows


for row in data_rows:
    write_to_csv(row, csv_file_random)

# with open("Llama_Training_Data.txt", 'r') as f:
#     lines = f.readlines()

# # Shuffle the lines
# random.shuffle(lines)

# # Write shuffled lines to output file
# with open("Llama_Training_Data_Shuffled.txt", 'w') as f:
#     f.writelines(lines)

print("Done")