import yfinance as yf
import plotly.express as px
import pandas as pd
import datetime
import requests
import io
import PySimpleGUI as psg

psg.theme('SandyBeach')     
  
layout = [
    [psg.Text('Please fill out the information below')],
    [psg.Text('Type the symbol of the stock you would like to predict, and its stock exchange composite', size =(70, 1)), psg.InputText()],
    [psg.Text('Type the original date you would like to start the prediction for', size =(70, 1)), psg.InputText()],
    [psg.Text('Type in the date you would like to predict your stock for in the following format, 2021 06 05', size =(70, 1)), psg.InputText()],
    [psg.Submit(), psg.Cancel()]
]
  
window = psg.Window('Stock Prediction Program', layout,size=(1000,600))
event,values = window.read()
window.close()
valuesx = list(values.items())
user_input_1 = valuesx[0][1]
user_input_split = user_input_1.split()
user_stock = user_input_split[0]
user_og_datetime = valuesx[1][1]
user_datetime = valuesx[2][1]
userlist_datetime = user_datetime.split()
year = userlist_datetime[0]
month = userlist_datetime[1]
day = userlist_datetime[2]
userlist_og_datetime = user_og_datetime.split()
og_year = userlist_og_datetime[0]
og_month = userlist_og_datetime[1]
og_day = userlist_og_datetime[2]
ts_final= datetime.datetime(int(year), int(month),int(day), 0, 0).timestamp()
ts_og = datetime.datetime(int(og_year), int(og_month),int(og_day), 0, 0).timestamp()
timeframe = int(ts_final) - int(ts_og)

df1_sd = int(ts_og) - timeframe
df1_sd_dt = datetime.datetime.fromtimestamp(df1_sd)  

df1_ed_dt = datetime.datetime.fromtimestamp(ts_og)


df2_sd = ts_og - 2*timeframe
df2_ed = ts_og - timeframe

df2_sd_dt = datetime.datetime.fromtimestamp(df2_sd)  

df2_ed_dt = datetime.datetime.fromtimestamp(df2_ed)

df3_ed = ts_og

df3_ed_dt = datetime.datetime.fromtimestamp(df3_ed)


df = yf.download(user_stock,data_source='yahoo',start=df1_sd_dt, end=df1_ed_dt)
fig = px.scatter(df, trendline="ols",)
df1closeprice = df['Close'][-1]
url_NASDAQ="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
url_NYSE = "https://pkgstore.datahub.io/core/nyse-other-listings/nyse-listed_csv/data/3c88fab8ec158c3cd55145243fe5fcdf/nyse-listed_csv.csv"
s = requests.get(url_NASDAQ).content
s2 = requests.get(url_NYSE).content
companies_NASDAQ = pd.read_csv(io.StringIO(s.decode('utf-8')))
companies_NYSE = pd.read_csv(io.StringIO(s2.decode('utf-8')))
Symbols = companies_NASDAQ['Symbol'].tolist() + companies_NYSE['ACT Symbol'].tolist()
df3 = []
nothing = 0
majority_matrix = []
matching_stocks = []
errors = 0
displayed = []
count = 0
count2 = 0
zyx = 0
zyx2 = 0
progress = 0
progress2 = 0 
spam = 0
positives = []
negatives = []
majorsetpos = []
majorsetneg = []
xvalues = []
yvalues = []
avglist = []
inaccuratey = []
inaccuratex = []
percent = 0
symb = 0

psg.theme('SandyBeach')     
  
layout1 = [psg.Text('Progress')]

layout2 = [
    [psg.Button(str(percent)+'%' + '     ' + str(progress)+'/'+str(len(Symbols)), key='-TEXT-',size=(10,10))],
    [psg.ProgressBar(symb, orientation='h', size=(20, 20), key='progressbar')]
    ]   

window = psg.Window('Stock Prediction Program', layout2,size=(1000,600))

window.read()
progress_bar = window['progressbar']

for i in Symbols : 
    df2 = yf.download(i,data_source='yahoo',start=df2_sd_dt, end=df2_ed_dt)
    fig2 = px.scatter(df2, trendline="ols")
    x = df2.values.tolist()
    results = px.get_trendline_results(fig2)
    if len(x) == 0 : 
        errors = errors + 1
    elif len(x) < 10 : 
        errors = errors + 1
    else : 
        ymxb = results.iloc[3]["px_fit_results"].params
        stored_ymxb_symbols = ymxb[1],i
        df3.append(stored_ymxb_symbols)
        symb = len(Symbols) - errors
        percent = progress/symb
        progress = progress + 1
        print(errors)
        while True:
            print("hello")
            event, values = window._ReadNonBlocking()
            if event == psg.WIN_CLOSED or event == 'Exit':
                break
            elif event == None : 
                window['-TEXT-'].update(str(progress)+'/'+str(symb))
                progress_bar.Update(current_count = progress, max = symb)
                break
            else : 
                window['-TEXT-'].update(str(progress)+'/'+str(symb))
                progress_bar.Update(current_count = progress, max = symb)
                break
window.close()
        
                    
fig = px.scatter(df,trendline="ols")
results = px.get_trendline_results(fig)
input_ymxb = results.iloc[3]["px_fit_results"].params
ts_ogy = ts_og + 604800
df1_ed_dty = datetime.datetime.fromtimestamp(ts_ogy)
dfy = yf.download(user_stock,data_source='yahoo',start=df1_ed_dt, end=df1_ed_dty)
figy = px.scatter(dfy, trendline="ols")
resultsy = px.get_trendline_results(figy)
input_ymxby = resultsy.iloc[3]["px_fit_results"].params
ogy = int(input_ymxby[0])
df4 = []

for i in df3 : 
    m = i[0]
    sym = i[1]
    int_input_m = float(input_ymxb[1])
    str_m = str(m)
    str_input_m = str(int_input_m)
    if str_m[0] == '-' and str_input_m[0] != '-' or str_input_m[0] == '-' and str_m[0] != '-' : 
        nothing =  1
    else : 
        if float(m) >= float(int_input_m):
            Msimilaritymeasure = float(m) - float(int_input_m)
            if Msimilaritymeasure < 0.00000015 : 
                majority_matrix.append(i[1])
                displayed.append([sym,'Similarity Measure :',Msimilaritymeasure,'Slope',m])
            elif Msimilaritymeasure == 0.000000000000000 : 
                nothing = 99
            else : 
                nothing = 2

        else:
            Msimilaritymeasure = float(int_input_m) - float(m)
            if Msimilaritymeasure < 0.00000015 : 
                majority_matrix.append(i[1])
                displayed.append([sym,'Similarity Measure :',Msimilaritymeasure,'Slope',m])
            elif Msimilaritymeasure == 0: 
                nothing = 22
            else : 
                nothing = 3

psg.theme('SandyBeach')     
text = 'This is the list of similair stocks in case you are interested! How do you read the data you ask? The stock symbol of a similair stock is first, then the measure of similarity (The smaller the more accurate), and lastly for comparison here is your input slope.',float(input_ymxb[1])
layout = [[psg.Multiline(text,size=(1000,5))],
    [psg.Multiline(displayed,size=(10000,100))]]
window = psg.Window('Stock Prediction Program', layout,size=(1000,600))
event,values = window.read()
window.close()



layout3 = [
    [psg.Button(str(percent)+'%' + '     ' + str(progress)+'/'+str(len(Symbols)), key='-TEXT-',size=(10,10))]
    ]

window2 = psg.Window('Stock Prediction Program', layout3,size=(1000,600))



for i in majority_matrix : 
    df4 = yf.download(i,data_source='yahoo',start=df2_ed_dt, end=df3_ed_dt)
    fig3 = px.scatter(df4, trendline="ols",labels=i)
    x2 = df4.values.tolist()
    results2 = px.get_trendline_results(fig3)
    if len(x2) == 0 : 
        nothing = 12
    elif len(x2) < 15 : 
        nothing = 12121212
    else : 
        df4closeprice = df4['Close'][0]
        final_closeprice = df4['Close'][-1]
        ymxb2 = results2.iloc[3]["px_fit_results"].params
        ymxbc = str(ymxb2[1])
        ymxbstr = ymxbc[0]
        if str(ymxbstr) == '-' : 
            negatives.append(ymxbstr)
            final_slopes = [i,ymxb2[1],ymxb2[0],Msimilaritymeasure,df4closeprice,final_closeprice]
            majorsetneg.append(final_slopes)
            percent = progress2/len(majority_matrix)
            progress2 = progress2 + 1
            while True:
                event, values = window2._ReadNonBlocking()
                if event == psg.WIN_CLOSED or event == 'Exit':
                    break
                elif event == None : 
                    window2['-TEXT-'].update(str(progress2)+'/'+str(len(majority_matrix)))
                    break
                else : 
                    window2['-TEXT-'].update(str(progress2)+'/'+str(len(majority_matrix)))
                    break
        else : 
            positives.append(ymxbstr)
            final_slopes = [i,ymxb2[1],ymxb2[0],Msimilaritymeasure,df4closeprice,final_closeprice]
            majorsetpos.append(final_slopes) 
            percent = progress2/len(majority_matrix)
            progress2 = progress2 + 1
            while True:
                event, values = window2._ReadNonBlocking()
                if event == psg.WIN_CLOSED or event == 'Exit':
                    break
                elif event == None : 
                    window2['-TEXT-'].update(str(progress2)+'/'+str(len(majority_matrix)))
                    break
                else : 
                    window2['-TEXT-'].update(str(progress2)+'/'+str(len(majority_matrix)))
                    break
window.close()
neglength = len(negatives)
poslength = len(positives)
print(majorsetneg)
print(majorsetpos)
if poslength < neglength : 
    for i in majorsetneg : 
        div = df1closeprice / 5
        minus = df1closeprice - div
        plus = df1closeprice + div
        if minus <= i[4] <= plus : 
            xvalues.append(i[1])
            yvalues.append(i[2])
        else : 
            inaccuratex.append(i[1])
            inaccuratey.append(i[2])

else : 
    for i in majorsetpos : 
        div = df1closeprice / 5
        minus = df1closeprice - div
        plus = df1closeprice + div
        if minus <= i[4] <= plus : 
            xvalues.append(i[1])
            yvalues.append(i[2])
        else : 
            inaccuratex.append(i[1])
            inaccuratey.append(i[2])

if len(xvalues) == 0 or len(yvalues) == 0 : 
    xavg = sum(inaccuratex) / len(inaccuratex)
    yavg = sum(inaccuratey) / len(inaccuratey)
    int_ts = int(ts_final)
    mval = xavg*int_ts
    predictionequation2 = mval + ogy
    negstr = 'Negatives :' + ' ' + str(neglength)
    posstr = 'Positives :' + ' ' + str(poslength)
    longstr = 'The predicted stock price for' + ' ' + str(user_stock) + ' ' + 'on the' + ' ' + str(user_datetime) + ' ' + 'is' + ' ' + str(predictionequation2)
    if poslength < neglength : 
        predicval = "Negative"
    elif poslength == neglength : 
        predicval = "Flat/Stable"
    else : 
        predicval = "Positive"
    predic = 'The predicted trend for' + ' ' + str(user_stock) + ' ' + 'is' + predicval
    inacc = 'The stock you chose, has a pattern unlike anything in our database'
    psg.theme('SandyBeach')     
    layout = [
        [psg.Multiline(inacc,size=(1000,10))],
        [psg.Multiline(predic,size=(1000,10))],
        [psg.Multiline(negstr,size=(1000,10))],
        [psg.Multiline(posstr,size=(1000,10))],
        [psg.Multiline(longstr,size=(1000,10))]
        ]
    window = psg.Window('Stock Prediction Program', layout,size=(1000,600))

    event,values = window.read()
    window.close()
else : 
    xavg = sum(xvalues) / len(xvalues)
    yavg = sum(yvalues) / len(yvalues)
    int_ts = int(ts_final)
    mval = xavg*int_ts
    predictionequation2 = mval + ogy
    negstr = 'Negatives :' + ' ' + str(neglength)
    posstr = 'Positives :' + ' ' + str(poslength)
    longstr = 'The predicted stock price for' + ' ' + str(user_stock) + ' ' + 'on the' + ' ' + str(user_datetime) + ' ' + 'is' + ' ' + str(predictionequation2)
    if poslength < neglength : 
        predicval = "Negative"
    elif poslength == neglength : 
        predicval = "Flat/Stable"
    else : 
        predicval = "Positive"
    predic = 'The predicted trend for' + ' ' + str(user_stock) + ' ' + 'is' + predicval
    psg.theme('SandyBeach')     
    layout = [
        [psg.Multiline(predic,size=(1000,10))],
        [psg.Multiline(negstr,size=(1000,10))],
        [psg.Multiline(posstr,size=(1000,10))],
        [psg.Multiline(longstr,size=(1000,10))]
        ]
    window = psg.Window('Stock Prediction Program', layout,size=(1000,600))
    event,values = window.read()
    window.close()