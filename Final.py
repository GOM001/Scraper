from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv
import time
import os
import sys

def navegacao():
    mozila.get('http://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp')
        
def extrair_todos_os_dados():
    print('Trabalhando para obter os dados \n')
    time.sleep(1)
    conteudo_csv = []
    paginacao = WebDriverWait(mozila, 15).until(ec.visibility_of_element_located((By.XPATH, '//*[@class="pagination ng-table-pagination ng-scope"]')))
    ultima_pagina = paginacao.text[18:20]
    #Paginação
    detalhes = mozila.find_elements_by_xpath('//*[@class="glyphicon glyphicon-plus"][@aria-hidden="true"]')
    b = (100/int(ultima_pagina)/len(detalhes))
    c = 0
    for n in range(int(ultima_pagina)):
        pag = str(n + 1)
        WebDriverWait(mozila, 15).until(ec.visibility_of_element_located((By.LINK_TEXT, pag))).click()
        detalhes = WebDriverWait(mozila, 15).until(ec.visibility_of_any_elements_located((By.XPATH, '//*[@class="glyphicon glyphicon-plus"][@aria-hidden="true"]')))
        #Detalhes do estabelecimento/ Botão '+'
        for pagina_detalhe in detalhes:
            if n + 1 == int(ultima_pagina):
                time.sleep(1.5)
            WebDriverWait(mozila, 15).until(ec.visibility_of_any_elements_located((By.XPATH, '//*[@class="glyphicon glyphicon-plus"][@aria-hidden="true"]')))
            pagina_detalhe.click()
            nome = mozila.find_element_by_css_selector('#nome').get_attribute('value')
            WebDriverWait(mozila, 15).until(ec.text_to_be_present_in_element_value((By.CSS_SELECTOR, '#nome'), nome))
            nome = mozila.find_element_by_css_selector('#nome').get_attribute('value')
            nome_empresarial = mozila.find_element_by_xpath('//*[@id="cnpj"][@ng-value="estabelecimento.noEmpresarial"]').get_attribute('value')
            cnes = mozila.find_element_by_id('cnes').get_attribute('value')
            cnpj = mozila.find_element_by_xpath('//*[@id="cnpj"][@ui-mask="99.999.999/9999-99"]').get_attribute('value')
            if cnpj == '---':
                cnpj = ' '
            logradouro = mozila.find_element_by_xpath('//*[@id="cnpj"][@ng-value="estabelecimento.noLogradouro"]').get_attribute('value')
            numero = mozila.find_element_by_xpath('//*[@id="cnpj"][@ng-value="estabelecimento.nuEndereco"]').get_attribute('value')
            complemento = mozila.find_element_by_xpath('//*[@id="cnpj"][@ng-value="estabelecimento.noComplemento"]').get_attribute('value')
            bairro = mozila.find_element_by_xpath('//*[@id="cnpj"][@ng-value="estabelecimento.bairro"]').get_attribute('value')
            a = "estabelecimento.municipio + ' - ' + estabelecimento.noMunicipio"
            municipio = mozila.find_element_by_xpath(f'//*[@id="cnpj"][@ng-value="{a}"]').get_attribute('value')
            municipio_separado = municipio.split('-')[1]
            UF = mozila.find_element_by_xpath('//*[@id="cnpj"][@ng-value="estabelecimento.uf"]').get_attribute('value')
            cep = mozila.find_element_by_xpath('//*[@id="cnpj"][@ui-mask="99999-999"]').get_attribute('value')
            telefone = mozila.find_element_by_id('tel').get_attribute('value')
            if telefone == '--' or telefone == '---':
                telefone = ' '
            mozila.find_element(By.CSS_SELECTOR, ".modal-footer > .btn:nth-child(2)").click()
            conteudo_csv.append([nome, nome_empresarial, cnes, cnpj, logradouro, numero,
                                complemento, bairro, municipio_separado, UF, cep, telefone])
            c = c + b
            sys.stdout.write("\r%d%%" % c)
            sys.stdout.flush()
            time.sleep(0.002)
    with open('CNES.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['Nome', 'Nome Empresarial', 'CNES', 'CNPJ','Logradouro', 'Numero',
                        'Complemento', 'Bairro', 'Municipio', 'UF', 'CEP', 'Telefone'])
        for linha in conteudo_csv:
            writer.writerow(linha)
    print('\n Dados obtidos com sucesso')
mozila = webdriver.Firefox(executable_path=r'geckodriver.exe')
navegacao()
WebDriverWait(mozila, 15).until(ec.visibility_of_element_located((By.XPATH, "//option[. = 'PERNAMBUCO']"))).click()
WebDriverWait(mozila, 15).until(ec.visibility_of_element_located((By.XPATH, "//option[. = 'OLINDA']"))).click()
WebDriverWait(mozila, 15).until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".form-group > .btn"))).click() 
extrair_todos_os_dados()
os.startfile('CNES.csv')
mozila.quit()
