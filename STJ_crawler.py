#!/usr/bin/env python3

from selenium import webdriver
from sys import argv
import csv

def write_csv(file_name, content):
    with open(file_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(content)

class STJ(object):

    def __init__(self, query):
        self.query = query
        self.startDriver()

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
        acordaos_xpath = '/html/body/div/div[6]/div/div/div[3]/div[2]/div/div/div/div[3]/div[3]/span[2]/a'
        self.driver.find_element_by_xpath(acordaos_xpath).click()
        self.driver.find_element_by_id('listadocumentos')
        rows = [(i.find_element_by_id('blocoesquerdo').text.replace('"', "'"),
        i.find_element_by_id('blocodireito').text.replace('"', "'"),
        i.find_element_by_id('linkdocumento').get_attribute('href'))
        for i in self.driver.find_elements_by_class_name('linhaPar')]
        write_csv(argv[1], rows)


    def next_page(self):
        self.driver.find_element_by_class_name('iconeProximaPagina').click()

    def auto_get(self):
        while True:
            self.search()
            self.get_info()
            self.next_page()

STJ('a').auto_get()
