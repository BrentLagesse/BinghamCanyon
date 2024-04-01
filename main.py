from Bio import SeqIO
from Bio import AlignIO
import subprocess
from scipy.stats import entropy
from statistics import mode
import xlwt
from xlwt import Workbook
import xlrd
import xlutils

def find_high_conservation_areas(mode_list, size, min_len=4, min_conserve=0.75, min_avg_conserve=0.0):
    details = list()
    tracking = False

    if min_avg_conserve == 0.0:
        for i in range(len(mode_list)):
            percent = float(mode_list[i])/size
            if percent >= min_conserve and not tracking:
                start = i
                tracking = True
            if percent < min_conserve and tracking:
                stop = i
                tracking = False
                if stop - start >= min_len:
                    details.append((start, stop))
    else:
        running_perc = 0.0
        running_len = 1
        start = 0
        for i in range(len(mode_list)):
            percent = float(mode_list[i]) / size
            running_perc += percent
            if tracking:
                running_len += 1
            if running_perc/(running_len) >= min_avg_conserve and not tracking:
                start = i
                tracking = True
            if running_perc/(running_len) < min_avg_conserve and tracking:
                running_len = 1
                running_perc = 0.0
                stop = i
                tracking = False
                if stop - start >= min_len:
                    details.append((start, stop))
    return details


in_file = "test.fasta"
out_file = "aligned.fasta"
cmd = ['./clustalo', '-i', 'test.fasta', '-o', 'aligned.fasta', '--auto', '-v', '--force']
#subprocess.call(cmd, stdout=subprocess.PIPE)



#alignment = AlignIO.read('test.fasta', 'fasta')
#print(alignment)

record_dict = SeqIO.to_dict(SeqIO.parse("aligned.fasta", "fasta"))
sequences = list()
names = list()
for r in record_dict.items():
    sequences.append(r[1].seq)
    names.append(r[0])
entropy_list = list()
n = len(sequences[0])
mode_list = list()
for x in range(n):
    columns = [ord(i[x]) for i in sequences]
    columns_char = [(i[x]) for i in sequences]
    entropy_list.append(entropy([ord(i[x]) for i in sequences]))
    if mode(columns_char) != '-':
        mode_list.append(columns_char.count(mode(columns_char)))
    else:
        mode_list.append(0)

areas_of_interest = find_high_conservation_areas(mode_list, len(sequences))#, min_avg_conserve=0.75)
print (areas_of_interest)

wb = Workbook()
column_pos = 0

sheet1 = wb.add_sheet('Alignment Results')
sheet1.write(column_pos, 0, 'Name')
sheet1.write(column_pos, 1, 'Result')

#for x in range(len(sequences)):
#    outstr = list()
#    for i in range(len(mode_list)):
#        redness = int(float(mode_list[i])/len(sequences) * 255)

#        wb.set_colour_RGB(mode_list[i]+8, redness, 0, 0);
#        char_font = xlwt.easyfont('color_index ' + str(mode_list[i]+8))
#        outstr.append((sequences[x][i], char_font))
#    sheet1.write_rich_text(x + 1, 1, outstr)

char_font = xlwt.easyfont('color_index black')
conserve_font = xlwt.easyfont('color_index red')

for x in range(len(sequences)):
    outstr = list()
    start = 0
    sheet1.write(x + 1, 0, names[x])
    for segments in areas_of_interest:
        outstr.append((str(sequences[x][start:segments[0]]), char_font))
        outstr.append((str(sequences[x][segments[0]:segments[1]]), conserve_font))
        start = segments[1]
    sheet1.write_rich_text(x + 1, 1, outstr)
sheet1.write(len(sequences) + 1, 1, str(mode_list))
wb.save('test.xls')