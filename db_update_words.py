import pandas as pd

df = pd.read_excel('/Users/alejandra.gutierrez/Desktop/GREvocab.xlsx', sheet_name='Sheet2')

message = 'INSERT INTO public.word\nVALUES '

for row in df.iterrows():
    if row[0]== int(1000):
        word_topic = "('" + row[1][0] + "' , '" + row[1][1] + "');"
    else:
        word_topic = "('" +row[1][0] + "' , '" + row[1][1] +"'), \n"
    message +=  word_topic

print(message)