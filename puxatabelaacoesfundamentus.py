# 1) INSTALAÇÕES INICIAIS NO TERMINAL
# pip install pandas
# pip install selenium
# pip install webdriver-manager
# pip install lxml
# pip install datetime

# 2) IMPORTAÇÕES DAS BIBLIOTECAS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime

# 3) ABRE NAVEGADOR --> ACESSA SITE
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://www.fundamentus.com.br/resultado.php'

driver.get(url)

# 4) LÊ A TABELA DE AÇÕES --> FECHA SITE
local_tabela = '/html/body/div[1]/div[2]/table'

elemento = driver.find_element("xpath", local_tabela)

html_tabela = elemento.get_attribute('outerHTML')

tabela = pd.read_html(str(html_tabela), thousands = '.', decimal = ',')[0]


#EXIBE TABELA IMPORTADA PARA VERIFICAÇÃO SE A IMPORTAÇÃO E LEITURA DERAM CERTO
# print(tabela)

#EXIBE O TIPO DE DADO QUE TEM NAS COLUNAS DA TABELA. INT É NÚMERO INTEIRO, FLOAT64 É NÚMERO DECIMAL, 
# tabela.info()

# 5) TRATAMENTO DO TIPO DE DADO DAS COLUNAS. DE OBJECT PARA FLOAT
#5.1) COLUNA DIV. YIELD
tabela['Div.Yield'] = tabela['Div.Yield'].str.replace("%", "")
tabela['Div.Yield'] = tabela['Div.Yield'].str.replace(".", "")
tabela['Div.Yield'] = tabela['Div.Yield'].str.replace(",", ".")
tabela['Div.Yield'] = tabela['Div.Yield'].astype(float)

#5.2) COLUNA Mrg Ebit
tabela['Mrg Ebit'] = tabela['Mrg Ebit'].str.replace("%", "")
tabela['Mrg Ebit'] = tabela['Mrg Ebit'].str.replace(".", "")
tabela['Mrg Ebit'] = tabela['Mrg Ebit'].str.replace(",", ".")
tabela['Mrg Ebit'] = tabela['Mrg Ebit'].astype(float)

#5.3) COLUNA Mrg Ebit
tabela['Mrg. Líq.'] = tabela['Mrg. Líq.'].str.replace("%", "")
tabela['Mrg. Líq.'] = tabela['Mrg. Líq.'].str.replace(".", "")
tabela['Mrg. Líq.'] = tabela['Mrg. Líq.'].str.replace(",", ".")
tabela['Mrg. Líq.'] = tabela['Mrg. Líq.'].astype(float)

#5.4) COLUNA ROIC
tabela['ROIC'] = tabela['ROIC'].str.replace("%", "")
tabela['ROIC'] = tabela['ROIC'].str.replace(".", "")
tabela['ROIC'] = tabela['ROIC'].str.replace(",", ".")
tabela['ROIC'] = tabela['ROIC'].astype(float)

#5.5) COLUNA ROE
tabela['ROE'] = tabela['ROE'].str.replace("%", "")
tabela['ROE'] = tabela['ROE'].str.replace(".", "")
tabela['ROE'] = tabela['ROE'].str.replace(",", ".")
tabela['ROE'] = tabela['ROE'].astype(float)

#5.6) COLUNA Cresc. Rec.5a
tabela['Cresc. Rec.5a'] = tabela['Cresc. Rec.5a'].str.replace("%", "")
tabela['Cresc. Rec.5a'] = tabela['Cresc. Rec.5a'].str.replace(".", "")
tabela['Cresc. Rec.5a'] = tabela['Cresc. Rec.5a'].str.replace(",", ".")
tabela['Cresc. Rec.5a'] = tabela['Cresc. Rec.5a'].astype(float)

#6) ELIMINANDO EMPRESAS COM LIQUIDEZ DIÁRIA ABAIXO DE r$1.000.000,00. 
# ISTO SIGNIFICA QUE É RÁPIDO E FÁCIL COMPRAR E VENDER ESSAS AÇÕES
tabela = tabela[tabela['Liq.2meses'] > 1000000]

#7) ELIMINANDO EMPRESAS COM EV/EBIT BAIXO OU NEGATIVO
tabela = tabela[tabela['EV/EBIT'] > 0]

#8) ELIMINANDO EMPRESAS COM ROIC BAIXO OU NEGATIVO
tabela = tabela[tabela['ROIC'] > 0]

#9) ELIMINANDO EMPRESAS COM P/VP MAIOR QUE 1
tabela = tabela[tabela['P/VP'] < 1]

#10) ELIMINANDO EMPRESAS COM ...... MAIOR QUE .....
#tabela = tabela[tabela['P/VP'] < 1]

#11) CLASSIFICA TABELA PELO EV/EBIT EM ORDEM CRESCENTE (MENOR PARA O MAIOR)
tabela['ranking_ev_ebit'] = tabela['EV/EBIT'].rank(ascending = True)

#11) CLASSIFICA TABELA PELO ROIC EM ORDEM DECRESCENTE (MAIOR PARA O MENOR)
tabela['ranking_roic'] = tabela['ROIC'].rank(ascending = False)

#12) CLASSIFICA TABELA PELO DIVIDEND YIELD EM ORDEM DECRESCENTE (MAIOR PARA O MENOR)
tabela['ranking_dividend'] = tabela['Div.Yield'].rank(ascending = False)

#13) CONSTRUÇÃO DO RANKING
tabela['ranking_total'] = tabela['ranking_ev_ebit'] + tabela['ranking_roic'] + tabela['ranking_dividend']

tabela = tabela.sort_values('ranking_total')

#14) EXIBE AS 10 MELHORES AÇÕES:
print(tabela.head(10))

#15) OBTÉM A DATA ATUAL
data_atual = datetime.datetime.today()

#16) PREPARA O NOME DO ARQUIVO
nome_arquivo = f"top_10_acoes_{data_atual.strftime('%Y-%m-%d')}.xlsx"

#17) EXPORTA PARA EXCEL
tabela.to_excel(f'{nome_arquivo}', index=False)
