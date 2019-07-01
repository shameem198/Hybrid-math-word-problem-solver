import pandas as pd
from Preprocess import text_to_wordlist
import csv

def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False
    return True


#train data
train = pd.read_csv('DATASET/Train.csv',engine='python')

questions=train['Questions']
#equations=train['Equations']


questions = train["Questions"].apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))
#equations = train["Equations"].apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))


questions = train["Questions"].apply(text_to_wordlist)
print(questions)
questions.to_csv('preprocessed.csv', sep='\t')

'''
#print(questions)


#template creation
Equations=[]
for eq in equations:
    Eqn=[]
    count=1
    for i in eq.split():
        if(is_number(i)):
            Eqn.append('Num'+str(count))
            count=count+1
        else:
            Eqn.append(i)
    Equations.append(Eqn)

    
with open('Eqn_Template.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow('Equations')
    writer.writerows(Equations)
csvFile.close()

equations.to_csv('equations.csv', sep='\t')
questions.to_csv('questions.csv', sep='\t')

df_E_T = pd.read_csv('DATASET/Eqn_Template.csv',engine='python')    
Eqn_Temp = df_E_T['Equations']

questions.to_csv('questions.csv', sep='\t')
df0 = pd.read_csv('DATASET/questionsTrain.csv',engine='python',sep='\t')
df1 = pd.read_csv('DATASET/equationsTrain.csv',engine='python',sep='\t')

df=df1.join(df0)
df.to_csv('Train.csv', sep='\t')

#testdata
test = pd.read_csv('DATASET/test.csv',engine='python',sep='\t')
questions_test=test['Questions']
equations_test=test['Equations']

questions_test = test["Questions"].apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))
equations_test = test["Equations"].apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))


questions_test = test["Questions"].apply(text_to_wordlist)
print(equations_test)
print(questions_test)


#template creation
Equations=[]
for eq in equations_test:
    Eqn=[]
    count=1
    for i in eq.split():
        if(is_number(i)):
            Eqn.append('Num'+str(count))
            count=count+1
        else:
            Eqn.append(i)
    Equations.append(Eqn)

with open('Eqn_Template.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(Equations)
csvFile.close()

df = pd.read_csv('DATASET/test.csv',engine='python',sep='\t')
Eqn=df['Equations_Template']

for index, row in df.Equations_Template.iteritems():
    ele=[]
    ele=row.split()
    for i in ele:
        if (i=='Pct' or i=='Exp' or len(ele)>8):
            df.drop(index , inplace=True)
            break

df.to_csv('Test.csv', sep='\t')

'''
