# This file is for scrape the web for file 
import xml.etree.ElementTree as ET
import mysql.connector
from decouple import config
import numpy as np
from datetime import date
import json

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
                                       host=config("MYSQL_HOST"),
                                       database='multimedia_author',
                                       port='3306')
        return conn
    
    def get_tree(file_name):
        tree = ET.parse(file_name)
        return tree
    
    def change(str):
        return [str.replace("'", '"')]
    
    def get_main_author_advance(main_author):
        mdate = date.today()
        others = main_author.findall('note')
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
            "date": mdate,
            "awards": awards,
            "others": datas
        }
    
    def get_main_author_basic(tree):
        main_author = tree.find('person')
        name = main_author.find('author').text
        pid = main_author.get('key')[10:]
        additional_data = get_main_author_advance(main_author)
        return name, pid, additional_data
    
    def send_query(conn, query):
        c = conn.cursor()
        try:
            c.execute(query)
            conn.commit()
        except mysql.connector.IntegrityError as err:
            print("Error: {}".format(err))
        
    def send_select_query(conn, query):
        # The method fetches all (or all remaining) rows of a query result set and returns a list of tuples. If no more rows are available, it returns an empty list.
        c = conn.cursor()
        c.execute(query)
        row = c.fetchone()
        return row
    
    conn = make_connection() #Start connection
    
    tree = get_tree(file_name)
    name, pid, additional_data = get_main_author_basic(tree)
    
    #Send to author
    query = f'INSERT INTO authors(pid, name) VALUES("{pid}", "{name}")' #OK
    send_query(conn, query)
    
    #Send to author_infos
    #query = f"INSERT INTO author_infos(pid, date, awards, others) VALUES({pid}, {additional_data.date}, {additional_data.awards}, {additional_data.others})"
    #send_query(conn, query)
    
    def get_papers(tree):
        papers = {}
        count_papers = 0
        r_tags = tree.findall('r')
        for r_tag in r_tags:
            for tag in tags:
                if(r_tag.find(tag) is not None):
                    paper = r_tag.find(tag)
                
                    key = paper.get('key')
                    mdate = paper.get('mdate')
                    title = paper.find('title').text
                    year = paper.find('year').text
                    temp_authors = paper.findall('author')
                    
                    authors = {}
                    count = 0
                    for author in temp_authors:
                        temp_author = {}
                        temp_author['name'] = author.text
                        temp_author['pid'] = author.get('pid')
                        authors[count] = temp_author
                        count += 1 
                        
                    infos = {}
                    urls = paper.findall('url')
                    count_url = 0
                    for url in urls:
                        if(count_url == 0):
                            infos["urls"] = {}
                        infos["urls"][count_url] = url.text
                        count_url += 1
                      
                    ees = paper.findall('ee')
                    count_ee = 0
                    for ee in ees:
                        if(count_ee == 0):
                            infos['ee'] = {}
                        type_ee = (ee.get("type") if ee.get("type") is not None else count_ee)
                        infos['ee'][type_ee] = ee.text
                        count_ee += 1
                        
                    if paper.find('journal') is not None:
                        infos['journal'] = paper.find('journal').text
                    if paper.find('pages') is not None:
                        infos['pages'] = paper.find('pages').text
                    if paper.find('volume') is not None:
                        infos['volume'] = paper.find('volume').text
                    
                        
                    papers[count_papers] = {
                            'key' : key,
                            'mdate': mdate,
                            'authors': authors,
                            'title': title,
                            'year': year,
                            'infos': infos
                    }
                    count_papers += 1
                    break

        return papers
                        
                    
        
    
    papers = get_papers(tree)
    key_list = []
    all_authors = [pid]
    for paper in papers:
        authors_list = papers[paper]['authors']
        #Add all co-author to author
        for author in authors_list:
            apid = authors_list[author]["pid"]
            if apid not in all_authors:
                query = f'INSERT INTO authors(pid, name) VALUES("{apid}", "{authors_list[author]["name"]}")' 
                all_authors.append(apid)
                send_query(conn, query)
        
    #Add all paper into papers
    for paper in papers:
        paper = papers[paper]
        key_list.append(paper['key'])
        list_ids = []
        for id in paper["authors"]:
            list_ids.append(paper["authors"][id]['pid'])
            
        pinfos = json.dumps(paper["infos"], indent=4)
        query = f""" INSERT INTO papers(paper_key, title, authors) VALUES('{paper["key"]}', "{paper["title"]}", '{json.dumps(list_ids, ensure_ascii=False)}') """
        send_query(conn, query)
        
        #Add papers to list of paper by that author except main author
        for author in paper["authors"]:
            author = paper["authors"][author]
            if author["pid"] == pid:
                continue
            select_query = f"""SELECT papers FROM author_papers WHERE pid='{author["pid"]}' """
            rows = send_select_query(conn, select_query)
            if rows is not None:
                # UPDATE
                total_papers = rows
                decoded = total_papers[0].decode("utf-8")
                decoded = decoded[1:-1]
                total_papers = decoded.split(",")
                count_p = 0
                for one in total_papers:
                    one = one.replace('"', "")
                    total_papers[count_p] = one
                    
                total_papers.append(paper["key"])
                total_papers = json.dumps(total_papers, ensure_ascii=False)
                query = f"""UPDATE author_papers SET papers='{total_papers}' WHERE pid = '{author["pid"]}'"""
                send_query(conn, query)
            else:
                # INSERT
                pkey = json.dumps(paper["key"], ensure_ascii=False)
                apid = author["pid"]
                query = f"""INSERT INTO author_papers(pid, papers) VALUES('{apid}', '[{pkey}]')"""
                send_query(conn, query)
            
            
    # Send all main author paper to author_papers
    key_list = json.dumps(key_list, ensure_ascii=False)
    query = f"""INSERT INTO author_papers(pid, papers) VALUES('{pid}', '{key_list}')"""
    send_query(conn, query)
    
    if conn.is_connected():
        conn.close()

        
file_name = "../examples/example.xml"
read_and_store_xml(file_name)



