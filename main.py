from Bio import SeqIO
from Bio import AlignIO
import subprocess
from scipy.stats import entropy
from statistics import mode
import xlwt
from xlwt import Workbook
import xlrd
import xlutils

def find_high_conservation_areas(mode_list, size, min_len=10, min_conserve=0.75, min_avg_conserve=0.75):
    details = list()
    tracking = False
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
    return details


in_file = "test.fasta"
out_file = "aligned.fasta"
cmd = ['./clustalo', '-i', 'test.fasta', '-o', 'aligned.fasta', '--auto', '-v', '--force']
subprocess.call(cmd, stdout=subprocess.PIPE)



#alignment = AlignIO.read('test.fasta', 'fasta')
#print(alignment)

record_dict = SeqIO.to_dict(SeqIO.parse("aligned.fasta", "fasta"))
sequences = list()
for r in record_dict.items():
    sequences.append(r[1].seq)

entropy_list = list()
n = len(sequences[0])
mode_list = list()
for x in range(n):
    columns = [ord(i[x]) for i in sequences]
    columns_char = [(i[x]) for i in sequences]
    entropy_list.append(entropy([ord(i[x]) for i in sequences]))
    mode_list.append(columns_char.count(mode(columns_char)))

areas_of_interest = find_high_conservation_areas(mode_list, len(sequences))
print (areas_of_interest)

wb = Workbook()
column_pos = 0

sheet1 = wb.add_sheet('Alignment Results')
sheet1.write(column_pos, 0, 'Name')
sheet1.write(column_pos, 1, 'Result')

for x in range(len(sequences)):
    outstr = list()
    for i in range(len(mode_list)):
        redness = int(float(mode_list[i])/len(sequences) * 255)

        wb.set_colour_RGB(mode_list[i]+8, redness, 0, 0);
        char_font = xlwt.easyfont('color_index ' + str(mode_list[i]+8))
        outstr.append((sequences[x][i], char_font))
    sheet1.write_rich_text(x + 1, 1, outstr)

wb.save('test.xls')