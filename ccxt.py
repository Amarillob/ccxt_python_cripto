# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 13:31:18 2021

@author: Brian
"""
import ccxt
import pandas as pd
from datetime import datetime

#exchange
exchange = ccxt.binance({
    "enableLimit": True,
})


# En terminos de milisegungos
msec = 1000
minute = 60*msec
hour = 60*minute
now = exchange.milliseconds()


# obtengo data
def get_candles(symbol,timeframe,limit, from_timestamp):
    try:
        candles = exchange.fetch_ohlcv(
            symbol = symbol,
            timeframe = timeframe,
            limit = limit,
            since = from_timestamp,
            )
        
        header = ["timestamp", "open", "high", "low", "close", "volume"]
        

        df = pd.DataFrame(candles, columns = header)

        # de segundos a fecha normal
        df.insert(1, "datetime", [datetime.fromtimestamp(d/1000) for d in df.timestamp]) #lo divido para que se trasforme de milisegundos a segundos

        return df.sort_values(by = "timestamp", ascending = False)

    except:
        print("no more data")
        pass
    

#%% ejemplo individual, correrlo para evitar bug

data =get_candles(
symbol = "BTC/USDT",
timeframe = "1d",
limit = 1000,
from_timestamp = exchange.parse8601("2021-10-25 00:00:00")
)


#%%
#criptos
currencies = exchange.currencies
list_currencies = list(currencies.keys())
str = "/USDT"
list_currencies_usdt = []
for currenci in currencies:
    precio_usdt = currenci + str
    list_currencies_usdt.append(precio_usdt)
# list_currencies_usdt



# proceso data
def processig(symbol,timeframe,limit, from_timestamp):
    df_completo =  get_candles(symbol,timeframe,limit, from_timestamp)
    df_filtrado = df_completo[["datetime","close"]]
    return df_filtrado




# generalizacion

# symbol = "BTC/USDT"
timeframe = "1d"
limit = 1000
from_timestamp = exchange.parse8601("2021-10-25 00:00:00")

contador_de_errores = 0
criptonames = []
list_df = []
for currencie in list_currencies_usdt:
    try:
        data = processig(currencie,timeframe,limit, from_timestamp)
        list_df.append(data) 
        criptonames.append(currencie)

    except:
        contador_de_errores += 1 
        # print(f"Hubo un problema con {currencie}")

# print(contador_de_errores)



#%% key:criptonames, valor asociado:list_df 
dict_cripto = {}
for i in range(len(criptonames)):
    dict_cripto[criptonames[i]] = list_df[i] 



#%%     graficos
import matplotlib.pyplot as plt



#limpio el dictionary para poder graficar bien
for name in list(dict_cripto.keys()):
    if dict_cripto[name].shape != (18, 2):   #actualizar el numero 18 pq depende del dia
        del dict_cripto[name]



lista_nombres = list(dict_cripto.keys())

figures = {}
for name in lista_nombres:
    fig = plt.figure()
    plt.plot(dict_cripto[name]["datetime"], dict_cripto[name]["close"] )
    plt.title(name)
    # plt.legend()
    # plt.show()
    figures[name] = fig


#%%  indicadores
import statistics as stc

variance = {}
mean = {}
variance_relative = {}
for name in lista_nombres:
    var = stc.variance(dict_cripto[name]["close"])
    variance[name] = var

    m = stc.mean(dict_cripto[name]["close"])
    mean[name] = m    

    cociente = variance[name]/mean[name]
    variance_relative[name] = cociente

# variance_relative


#%% ordenamiento
import operator
sort_variance_relative = sorted(variance_relative.items(), key=operator.itemgetter(1), reverse=True)

# sort_variance_relative
# figures = {}

#%% Grafico las 3 criptos mas volatiles
figures[sort_variance_relative[0][0]]
figures[sort_variance_relative[1][0]]
figures[sort_variance_relative[2][0]]

