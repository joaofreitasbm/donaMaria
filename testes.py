from func import *

horas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
temp =  [11, 22, 33, 44, 55, 66, 77, 88, 99, 11, 22, 33, 44, 55, 66, 77, 88, 99, 11, 22, 33, 44, 55, 66]

manhã = horas[:-12]
tarde = horas[-12:-6]
noite = horas[-6:]  

print(horas[:-18])
print(horas[-18:-12])

print(manhã)
print(tarde)
print(noite)
print('')


mododia = 2
useragent = {"User-Agent": 
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

url = f'https://www.accuweather.com/pt/br/pacatuba/32479/hourly-weather-forecast/32479?day={str(mododia)}'
rq = requests.get(url, headers=useragent)
sb = BeautifulSoup(rq.text, 'html.parser')

t1 = fchuva(sb)[:-12].index(max(fchuva(sb)[:-12]))
t2 = fchuva(sb)[-12:-6].index(max(fchuva(sb)[-12:-6]))
t3 = fchuva(sb)[-6:].index(max(fchuva(sb)[-6:]))


print(fhoras(sb)[:-12][t1])
print(fhoras(sb)[-12:-6][t2])
print(fhoras(sb)[-6:][t3])