import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from pandas import DataFrame
from pandas_datareader import data

class StockMarketAnalysis:
    def __init__(self,stock,units,startD,endD,period):
        self.stock = stock
        self.startD = startD
        self.endD = endD
        self.period = period
        self.units = units


    def CalculateInvestment(self):
        msft = yf.Ticker(self.stock)
        if self.period=="max":
            msft_h = msft.history(period="max")
        else:
            msft_h = msft.history(start=self.startD, end=self.endD)
        
        msft_h1 = msft_h[(msft_h['Stock Splits']>0.0) | (msft_h['Dividends']>0.0) ]
        msft_h1['Stock Splits'].mask(msft_h1['Stock Splits'] == 0.0,1.0,inplace=True)
        
   		# if Dividends are there or not     
        # if msft_h1==0.0:
        #     print("This company do not provide dividends")

        msft_h2 = msft_h1[['Close']]
        msft_h2_ch = msft_h2.pct_change()

        Inv_1 = self.units*msft_h1.Close[0]
        Inv_3 = []
        for ii in range(1,msft_h1.Dividends.shape[0]):

        	if(msft_h1['Stock Splits'][ii] > 0.0):
        		self.units = msft_h1['Stock Splits'][ii]*self.units
        		Inv_1 = self.units*msft_h1.Close[ii]
        	else:
        		self.units = self.units
	
#        	Inv_1 = self.units*msft_h1.Close[ii]			# ii or 0
#        	print("INV_1: ",format(Inv_1))
        	Inv_2 = (Inv_1 + (Inv_1*msft_h2_ch.Close[ii]))

        	if(msft_h1['Dividends'][ii] > 0.0):
        		Inv_1 = Inv_2 + Inv_2*msft_h1.Dividends[ii]/100
        	else:
        		Inv_1 = Inv_2

        	Inv_3.append(Inv_1)
        
        Inv_3.insert(0, msft_h1.Close[0])
        msft_h1["Total Returns"] = Inv_3
        print("Total Stocks: ",self.units)
#        return msft_h1

#    def plot_plots(data1,data2):
        data1, data2 = msft_h1["Total Returns"], msft_h1['Dividends']
        fig, ax1 = plt.subplots()
        color = 'tab:red'
        ax1.set_xlabel('time (YR)')
        ax1.set_ylabel('Investment(CAD)', color=color)
        ax1.plot(data1, color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel('Divident (%)', color=color)  # we already handled the x-label with ax1
        ax2.plot(data2, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        ax1.set_title('Growth of {} {} stocks with Total Inital Investment {}'.format(self.units,self.stock,self.units*msft_h1.Close[0]))
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()





