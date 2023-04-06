import re
from bs4 import BeautifulSoup
import requests

# pré requisitos para o funcionamento do beautifulsoup:
# 1º: user agent: isso faz com que o site pense que a gente está acessando por 
#     um navegador (usar como dicionário)
# >>> {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"}

# 2º: url: url exata de onde você quer extrair os dados
# >>> url = 'suaUrlAqui'

# 3º: rq: request do url do passo 2, usando o user agent
# >>> rq = requests.get(url, headers=useragent)

# 4º: sb: raspagem de dados usando os dados inseridos nos passos anteriores
# >>> sb = BeautifulSoup(rq1.text, 'html.parser')~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~   VARIAVEIS UNIVERSAIS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# CONVERTENDO DAQUI PRO DEB
#useragent = {"User-Agent": 
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

#urlagora = 'https://www.accuweather.com/pt/br/pacatuba/32479/weather-forecast/32479'
#rqagora = requests.get(urlagora, headers=useragent)
#sbagora = BeautifulSoup(rqagora.text, 'html.parser')

#urlgeral = f'https://www.accuweather.com/pt/br/pacatuba/32479/hourly-weather-forecast/32479?day='
#rqgeral = requests.get(urlgeral, headers=useragent)
#sbgeral = BeautifulSoup(rqgeral.text, 'html.parser')



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~     FUNÇÕES SIMPLES      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def fagora(sbatual): # TODOS VALORES DA HORA ATUAL APENAS
    agorahora = sbatual.find('div', class_='minutecast-banner__time__value').text.lower()
    agoratemp = sbatual.find('div', class_='temp').text
    agoracond = sbatual.find('div', class_='phrase').text #manter com inicial maiuscula
    agorachuva = sbatual.find('p', class_='minutecast-banner__phrase').text.lower()
    agorachuva = re.findall('[a-zA-Z0-9çã]+', agorachuva)
    
    return agorahora, agoratemp, agoracond, " ".join(agorachuva)



def fmedia(lista):
    try:
        if round(sum(lista) / len(lista)) != 0:
            return round(sum(lista) / len(lista))
    except ZeroDivisionError:
        return lista[0]

def ftemp(sb): # TEMPERATURAS DA HORA SEGUINTE ÀS 23H
    '''
    retorna lista com temperaturas por hora
    '''
    temp = sb.find_all('div', class_='temp metric')
    templist = []
    for itemp in temp: # adiciona todos resultados na lista acima
        templist.append(itemp.text)
    
    templist2 = str(templist)
    templist2 = re.findall('[0-9]+', templist2) # remove caracteres desnecessários
    
    templistint = []
    for tempint in templist2: # converte de str pra int, p/ calculo de média
        templistint.append(int(tempint))

    return templistint

def fhoras(sb): # HORAS DA HORA SEGUINTE ÀS 23H
    '''
    retorna lista com horas (ou apenas horas seguintes do dia atual)
    '''
    horas = sb.find_all('h2', class_='date')
    horaslist = []
    for ihoras in horas:
        horaslist.append(ihoras.text)
    return horaslist

def fcond(sb): # COND. CLIMÁTICAS DA HORA SEGUINTE ÀS 23H
    '''
    retorna lista com condições climáticas do dia atual (nublado, ensolarado, etc)
    '''
    cond = sb.find_all('div', class_='phrase')
    condlist = []
    for icond in cond:
        condlist.append(icond.text)
    return condlist

def fchuva(sb): # POSSIBILIDADE DE CHUVA DA HORA SEGUINTE ÀS 23H
    '''
    retorna lista com possibilidade de chuva por hora em porcentagem
    '''
    chuva = sb.find_all('div', class_='precip')
    chuvalist = []
    for ichuva in chuva:
        chuvalist.append(ichuva.text)
    
    chuvalist2 = str(chuvalist)
    chuvalist2 = re.findall('[0-9]+%', chuvalist2)
    list(chuvalist2)
    return chuvalist2

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~     FUNÇÕES COMPOSTAS    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





#geral do dia com detalhes sobre manhã/tarde/noite a depender do horario atual
def fcons11(sb, sbatual): 
    try:
        if int(fagora(sbatual)[0][:2]) < int(fhoras(sb)[-12]): # manhã
            return f'\nDe agora até o fim das {fagora(sbatual)[0][:2]}h o clima é de {fagora(sbatual)[1]}. {fagora(sbatual)[2]}.\n'\
            f'\nO clima fica em média em {fmedia(ftemp(sb)[:-12])}ºC nessa manhã.\nMédia climática: {max(set(fcond(sb)[:-12]), key=fcond(sb)[:-12].count)}\n'\
            f'\nNo decorrer da tarde, o clima é de {fmedia(ftemp(sb)[-12:-6])}ºC em média.\nMédia climática: {max(set(fcond(sb)[-12:-6]), key=fcond(sb)[-12:-6].count)}\n'\
            f'\nDurante a noite, o clima fica em {fmedia(ftemp(sb)[-6:])}ºC em média.\nMédia climática: {max(set(fcond(sb)[-6:]), key=fcond(sb)[-6:].count)}\n'
    except IndexError:
        try:
            if int(fagora(sbatual)[0][:2]) < int(fhoras(sb)[-6]): # tarde
                return f'\nDe agora até o fim das {fagora(sbatual)[0][:2]}h o clima é de {fagora(sbatual)[1]}. {fagora(sbatual)[2]}\n'\
                f'No decorrer da tarde, o clima é de {fmedia(ftemp(sb)[:-6])}ºC. {max(set(fcond(sb)[:-6]), key=fcond(sb)[:-6].count)} na maior parte.\n'\
                f'E no periodo da noite, o clima é de {fmedia(ftemp(sb)[-5:])}ºC em média, {max(set(fcond(sb)[-5:]), key=fcond(sb)[-5:].count)}.\n'
        except IndexError:
            try:
                if int(fagora(sbatual)[0][:2]) < int(fhoras(sb)[-1]): # noite
                    return f'\nA temperatura atual é de {fagora(sbatual)[1]}, e até o fim da noite o clima fica na média dos {fmedia(ftemp(sb))}ºC.\n'\
                    f'O tempo fica majoritariamente {(max(set(fcond(sb)), key=fcond(sb).count)).lower()} essa noite.\n'
            except IndexError:
                print('passou direto e n acertou foi nada')

#geral do dia seguinte com detalhes sobre manhã/tarde/noite
def fcons21(sb): 
    return f'\nAssim ficará o tempo amanhã:'\
            f'\nO clima fica em média em {fmedia(ftemp(sb)[:-12])}ºC durante a manhã.\nMédia climática: {max(set(fcond(sb)[:-12]), key=fcond(sb)[:-12].count)}\n'\
            f'\nNo decorrer da tarde, o clima é de {fmedia(ftemp(sb)[-12:-6])}ºC em média.\nMédia climática: {max(set(fcond(sb)[-12:-6]), key=fcond(sb)[-12:-6].count)}\n'\
            f'\nDurante a noite, o clima fica em {fmedia(ftemp(sb)[-6:])}ºC em média.\nMédia climática: {max(set(fcond(sb)[-6:]), key=fcond(sb)[-6:].count)}\n'
 

