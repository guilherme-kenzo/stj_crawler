#!/usr/bin/env python3

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from sys import argv
import csv
import re
import json

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
        for i in doclist:
            raw_link = i.find_element_by_xpath('//*[@title="Exibir a íntegra do acórdão."]').get_attribute('href')
            link = linkre.search(raw_link).group()
            titulos = [j.text for j in i.find_elements_by_class_name('docTitulo')]
            conteudo = [j.text for j in i.find_elements_by_class_name('docTexto')]
            if (len(titulos) == len(conteudo)):
                tmp_dict = {titulos[i]:conteudo[i] for i in range(0, len(titulos))}
                tmp_dict['link'] = 'http://www.stj.jus.br' + link
                with open('data.txt', 'a') as f:
                    json.dump(tmp_dict, f)
                    f.write('\n')
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
            except:
                self.auto_get()

STJ('a').auto_get()
