import csv
import datetime
import sys

withvolatility = str(sys.argv[1])
now = datetime.datetime.now()

file_niftystocks = "ind_nifty100list.csv"
file_nsedatafile = "data.csv" #OHL sheet for F&0 from which NIFTY100 stocks will be extracted
file_nifvol = "nifvol.csv"
file_output = "output_"+str(now.hour)+str(now.minute)+'_'+str(now.day)+str(now.month)+str(now.year)+".csv"

nifty_fields = []
nifty_rows = []
data_fields = []
data_rows = []
if withvolatility == "withvol":
    output_fields = ['Symbol','Open','High','Low','Current','Change %','Buy/Sell','','','Day before Yesterday\'s Vol','Yesterday\'s Vol','In range 1-2.5']
    nifvol_fields = []
    nifvol_rows = [] 
else:
    output_fields = ['Symbol','Open','High','Low','Current','Change %','Buy/Sell']
output_rows = []

with open(file_niftystocks, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    nifty_fields = csvreader.next()
    
    for row in csvreader:
        nifty_rows.append(row)

    print('Total rows in Nifty file, %d'%(csvreader.line_num))

with open(file_nsedatafile, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    data_fields = csvreader.next()
    
    for row in csvreader:
        data_rows.append(row)

    print('Total rows in Data file, %d'%(csvreader.line_num))
    

if withvolatility == "withvol":
    with open(file_nifvol, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        
        nifvol_fields = csvreader.next()
        
        for row in csvreader:
            nifvol_rows.append(row)

        print('Total rows in Volatility Report file, %d'%(csvreader.line_num))


for drow in data_rows:
    
    for nrow in nifty_rows:
        
        if nrow[2] == drow[0]:
            
            tempstring = ""
            
            if drow[1] == drow[2]:
                tempstring = "SELL"
            elif drow[1] == drow[3]:
                tempstring = "BUY"
                
            if tempstring != "":
                temp = []
                if withvolatility == "withvol":
                    yvol = ""
                    dbyvol = ""
                    inrange = ""
                    
                    for vrow in nifvol_rows:
                        if vrow[0] == drow[0]:
                            yvol = vrow[5]
                            dbyvol = vrow[4]
                            if(float(yvol) >= 1 and float(yvol) <= 2.5 ):
                                inrange = "TRUE"
                            else:
                                inrange = "#####"
                            temp = [drow[0],drow[1],drow[2],drow[3],drow[4],drow[6],tempstring,'','',dbyvol,yvol,inrange]
                    
                else:
                    temp = [drow[0],drow[1],drow[2],drow[3],drow[4],drow[6],tempstring]
                output_rows.append(temp)

with open(file_output,'w') as csvfile:
    
    csvwriter = csv.writer(csvfile)
    
    csvwriter.writerow(output_fields)
    csvwriter.writerows(output_rows)
    print('Output file generated')
