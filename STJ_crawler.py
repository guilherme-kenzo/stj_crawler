#!/usr/bin/env python3

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from sys import argv
import pandas as pd
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import re

def write_csv(file_name, content):
    with open(file_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(content)

class STJ(object):

    def __init__(self, query):
        self.query = query
        self.startDriver()
        self.search()

    def startDriver(self):
        self.driver = webdriver.Firefox()

    def restartDriver(self):
        self.driver.quit()
        startDriver()

    def search(self):
        url = 'http://www.stj.jus.br/SCON/'
        query_xpath = '//*[@id="pesquisaLivre"]'
        self.driver.get(url)
        search = self.driver.find_element_by_xpath(query_xpath)
        search.send_keys(self.query)
        search_xpath = '/html/body/div/div[6]/div/div/div[3]/div[2]/div/div/div/div/form/div[17]/input[1]'
        self.driver.find_element_by_xpath(search_xpath).click()
        acordaos_xpath = '/html/body/div/div[6]/div/div/div[3]/div[2]/div/div/div/div[3]/div[3]/span[2]/a'
        self.driver.find_element_by_xpath(acordaos_xpath).click()

    def get_info(self):
        supradoclist = self.driver.find_element_by_id('listadocumentos')
        doclist = self.driver.find_elements_by_tag_name('div')
        linkre = re.compile('(?<=\(\').+(?=\'\))')
        counter = 0
        df = pd.DataFrame()
        for i in doclist:
            counter += 1
            i.find_element_by_xpath('//*[@title="Exibir a íntegra do acórdão."]').click()#.get_attribute('href')
            windows = self.driver.window_handles
            self.driver.switch_to_window(windows[1])
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "id_formato_html"))
            )
            element.click()
            arvore = self.driver.find_element_by_class_name('arvore_documentos')
            name = arvore.find_element_by_tag_name('a').text
            arvore.find_element_by_tag_name('a').click()
            handles = self.driver.window_handles
            popup_handle = handles[-1]
            print(popup_handle)
            self.driver.switch_to_window(popup_handle)
            print(self.driver.page_source)
            # link = 'http://www.stj.jus.br' + linkre.search(raw_link).group()
            #
            # titulos = [j.text for j in i.find_elements_by_class_name('docTitulo')]
            # conteudo = [j.text for j in i.find_elements_by_class_name('docTexto')]
            # if (len(titulos) == len(conteudo)):
            #     tmp_dict['link'] = 'http://www.stj.jus.br' + link
            #     tmp_dict = {titulos[i]:conteudo[i] for i in range(0, len(titulos))}
                # print(tmp_dict['Ementa'])
    # write_csv(argv[1], rows)

    def next_page(self):
        self.driver.find_element_by_class_name('iconeProximaPagina').click()

    def auto_get(self):
        while True:
            try:
                self.get_info()
                self.next_page()
            except NoSuchElementException as e:
                print(e)
                self.driver.quit()
            # except:
            #     self.auto_get()

STJ('civil').auto_get()
