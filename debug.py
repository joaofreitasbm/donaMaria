from func import *

varinput = input('\nO que você deseja saber?\n> ') # recebe solicitação do usuário
auxinput = re.split(r'[ ? ]+', varinput) # remove  interrogações e espaços desnecessários
listinput = list(filter(None, auxinput)) # remove itens vazios da lista gerada pelo re.split

# as informações daqui funcionam em conjunto com os dicionários pra setar o dia e modo da solicitação
mododia = 0     # (agora = 0, hoje = 1, amanhã = 2, dias da semana = 3.)
modobusca = 0   # (geral = 1, chuva = 2, sol = 3.)

# os dicionários ajudam a entender sobre qual dia e informação foi solicitada
dicagora = ['agora','atual']
dichoje = ['hoje', 'decorrer', 'dia']
dicamanha = ['amanha', 'amanhã']
dicgeral = ['tempo', 'clima', 'geral', 'previsão', 'dia']
dicchuva = ['chuva', 'chover', 'nublado', 'chove']
dicsol = ['sol', 'ensolarado', 'limpo', 'céu']
dicdias = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']


# para saber qual dia o usuário deseja: 
for x in listinput:
    if x in dicagora:
        mododia = 0
        break
    elif x in dichoje:
        mododia = 1
        break
    elif x in dicamanha:
        mododia = 2
        break
    elif x in dicdias:
        mododia = 3
        print(dicdias.index(x))
        break
    
# para saber o que foi solicitado: (ex: se o dia vai ser ensolarado ou se vai chover)
for x in listinput:
    if x in dicgeral:
        modobusca = 1
        break
    elif x in dicchuva:
        modobusca = 2
        break
    elif x in dicsol:
        modobusca = 3
        break

useragent = {"User-Agent": 
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

# para buscas que se referem a dados da hora atual:
urlatual = 'https://www.accuweather.com/pt/br/pacatuba/32479/weather-forecast/32479'
rqatual = requests.get(urlatual, headers=useragent)
sbatual = BeautifulSoup(rqatual.text, 'html.parser')

# para buscas que se referem a dados futuros:
url = f'https://www.accuweather.com/pt/br/pacatuba/32479/hourly-weather-forecast/32479?day={str(mododia)}'
rq = requests.get(url, headers=useragent)
sb = BeautifulSoup(rq.text, 'html.parser')


# onde a magia acontece
# resposta para AGORA:
if mododia == 0: # FUNCIONANDO // RESOLVIDO
    print(f'São {fagora(sbatual)[0]}, e estão fazendo {fagora(sbatual)[1]}\n{fagora(sbatual)[2]}, {fagora(sbatual)[3]}.\n')

# respostas para previsões do dia atual:
elif mododia == 1:
    if modobusca == 1: # geral // FUNCIONANDO
        print(fcons11(sb, sbatual)) 
    elif modobusca == 2: # chuva // FUNCIONANDO (melhorar se possivel)
        print(fcons12(sb, sbatual))
    elif modobusca ==3: # sol # NÃO COMEÇAR
        print('debug 13')
        print('Você quer saber se vai fazer sol hoje mas isso ainda está sendo desenvolvido.')

# respostas para o dia seguinte: # NÃO COMEÇAR
elif mododia == 2:
    if modobusca == 1:
        print('debug 21')
        print(fcons21(sb))
    elif modobusca == 2:
        print('debug 22')
        print(fcons22(sb))
    elif modobusca ==3:
        print('debug 23')
        print('Você quer saber se vai fazer sol amanhã mas isso ainda está sendo desenvolvido.')


