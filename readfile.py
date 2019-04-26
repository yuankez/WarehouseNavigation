# import pandas as pd screw pandas

filename = 'qvBox-warehouse-data-s19-v01.txt'

dataFile = open(filename,'r')
print("File read.")
# pd.read_csv(dataBaseFile).to_dict("list")

header = dataFile.readline().strip().split('\t')
print("Headers of Data = ", header)

data = []
dataDict = dict()

# Currently in a list format with nested dictionary for every individual header
for line in dataFile:
    col = line.strip().split('\t')
    row = dict()
    location = dict() # Xloc, Yloc: not sure how to incorporpate into for loop
    AccessD = dict() # N, S, W, E same issue as above ^^
    for j, i in enumerate(header):
        row[i] = col[j]
    data.append(row)

# print the first 2 rows
print(data[:2])
dataFile.close()

# failed nested dict code
# for line in dataFile:
#     col = line.strip().split('\t')
#     row = dict()
#     location = dict()
#     for j, i in enumerate(header):
#         if(i == 'ProductID'):
#             row[i] = col[j]
#         elif(i == 'yLocation' or i =='xLocation'): #location
#             if(i == 'xLocation'):
#                 location[i] = col[j]
#             else:
#                 location[i] = col[j]
#                 row.append(location)    #appen not a dictionary function
#         else: #access
#             row[i] = col[j]