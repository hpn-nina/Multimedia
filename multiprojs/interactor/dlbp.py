# This file is for scrape the web for file 
import xml.etree.ElementTree as ET
import mysql.connector
from decouple import config
import requests
import numpy as np

# Publication tags
tags = ['article', 'inproceedings', 'proceedings', 'book', 'incollection', 'phdthesis', 'mastersthesis', 'www']
publ_type = ["encyclopedia", "informal", "edited", "survey", "data", "software", "withdrawn"]

def crawler():
    #TODO
    # Go into the first page and request xml file
    return 



def read_and_store_xml(file_name):
    # This is a xml file of an author, that's why their will be only one author primary data
    
    def make_connection():
        conn = mysql.connector.connect(user=config("MYSQL_USERNAME"),
                                       password=config("MYSQL_ROOT_PASSWORD"),
                                       host=config("MYSQL_HOST"),
                                       database='author',
                                       port='3306')
        return conn
    
    def get_tree(file_name):
        tree = ET.parse(file_name)
        return tree
    
    def get_main_author_advance(main_author):
        date = main_author.get("date")
        others = main_author.findall('person')
        datas = []
        awards = []
        for detail in range(0, len(others)):
            if others[detail].get('award'):
                award = others.pop(detail)
                awards.append(award)
            else:
                data = others.pop(detail)
                datas.append(data)
        
        return {
            "date": date,
            "awards": awards,
            "others": datas
        }
    
    def get_main_author_basic(tree):
        main_author = tree.find('dblpperson')
        name = main_author.get('name')
        pid = main_author.get('pid')
        n = main_author.get('n')
        additional_data = get_main_author_advance(main_author)
        return name, pid, n, additional_data
    
    def send_query(conn, query):
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        
    def send_select_query(conn, query):
        # The method fetches all (or all remaining) rows of a query result set and returns a list of tuples. If no more rows are available, it returns an empty list.
        c = conn.cursor()
        c.execute(query)
        rows = c.fetchall()
        return rows
    
    conn = make_connection() #Start connection
    
    tree = get_tree(file_name)
    name, pid, n, additional_data = get_main_author_basic(tree)
    
    #Send to author
    query = f"INSERT INTO authors(pid, name, n) VALUES({pid}, {name}, {n})"
    send_query(conn, query)
    
    #Send to author_infos
    query = f"INSERT INTO author_infos(pid, date, awards, others) VALUES({pid}, {additional_data.date}, {additional_data.awards}, {additional_data.others})"
    send_query(conn, query)
    
    def get_papers(tree):
        r_tags = tree.findall('r')
        for r_tag in r_tags:
            for tag in tags:
                if(len(r_tag.find(tag)) != 0):
                    paper = r_tag.find(tag)
                
                    key = paper.get('key')
                    mdate = paper.get('mdate')
                    title = paper.find('title').text
                    temp_authors = paper.findall('author')
                    
                    #TODO pages year volume journal ee url
                    # With ee pls add  type
                    # Check type of already exist code
                    #Check which will be return if find element can not be found
                    
                    authors = {}
                    count = 0
                    for author in temp_authors:
                        temp_author = {}
                        temp_author['name'] = author.text
                        temp_author['pid'] = author.get('pid')
                        authors[count] = temp_author
                        count += 1 
                        
                    return {
                        "key" : key,
                        "mdate": mdate,
                        "authors": authors,
                        "title": title
                    }
        
    
    papers = get_papers(tree)
    key_list = []
    for paper in papers:
        authors_list = paper.authors
        #Add all co-author to author
        for author in authors_list:
            query = f"INSERT INTO author(pid, name, n) VALUES({author.pid}, {author.name}, {author.n})"
            send_query(conn, query)
        
    #Add all paper into papers
    for paper in papers:
        key_list.append(paper.key)
        query = f"INSERT INTO papers(paper_key, title, authors, year, another_infos) VALUES({paper.key}, {paper.title}, paper.authors.pid, paper.year, paper.infos)"
        send_query(conn, query)
        
        #Add papers to list of paper by that author except main author
        for author in paper.authors:
            if author.pid == pid:
                continue
            select_query = f"SELECT papers FROM author_papers WHERE pid = {author.pid}"
            row, _ = send_select_query(conn, select_query)
            if len(row) != 0:
                # UPDATE
                total_papers = row
                total_papers.papers = row.append(paper.key)
                query = f"UPDATE author_papers SET papers={total_papers} WHERE pid = {author.pid}"
                send_query(conn, query)
            else:
                # INSERT
                query = f"INSERT INTO author_papers(pid, papers) VALUES({author.pid}, {paper.key})"
                send_query(conn, query)
            
            
    # Send all main author paper to author_papers
    key_list = {"papers": key_list}
    query = f"INSERT INTO author_papers(pid, papers) VALUES({pid}, {key_list})"
    send_query(conn, query)
    
    if conn.is_connected():
        conn.close()

        
        
file_name = "../examples/example.xml"
read_and_store_xml(file_name)