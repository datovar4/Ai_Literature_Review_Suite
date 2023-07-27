"""
Created on Sat May 13 15:45:12 2023

@author: David Tovar
"""
import os
import tkinter as tk
from tkinter import simpledialog, filedialog
from lisc.collect import collect_citations
from api_key_checker import check_api_key
import requests
import json
import re
import time
from crossref.restful import Works

check_api_key("CORE_API.txt", "CORE")
with open("CORE_API.txt", "r") as f:
    api_key = f.read().strip()
    
CORE_API_KEY = api_key

api_endpoint = "https://api.core.ac.uk/v3/"

def get_title_from_doi(doi):
    try:
        works = Works()
        res = works.doi(doi)
        title = res['title'][0]
        return title
    except Exception as e:
        print(f"Error getting title for DOI {doi}: {e}")
        return 'Title not found in CORE or CrossRef database'

def get_doi(txt_path):
    with open(txt_path, 'r') as file:
        return file.readline().strip()
    
def query_api(url_fragment, query, limit=100):
    headers = {"Authorization": "Bearer " + api_key}
    query = {"q": query, "limit": limit}
    
    for _ in range(5):  # try up to 5 times
        response = requests.post(f"{api_endpoint}{url_fragment}", data=json.dumps(query), headers=headers)
        if response.status_code == 429:
            print("Rate limit reached. Waiting for 60 seconds.")
            time.sleep(30)  # wait for 60 seconds before trying again
        elif response.status_code != 200:
            print(f"Error code {response.status_code}, {response.content}")
            return None, None  # return None for both values if there's an error
        else:
            return response.json(), response.elapsed.total_seconds()
        
def search_core(dois=None, title=None, authors=None):
    if not any([dois, title, authors]):
        raise ValueError("At least one of DOIs, title or authors must be provided.")
        
    if dois:
        # Construct query with OR for multiple DOIs
        query = " OR ".join([f'doi:"{doi}"' for doi in dois])
    elif title:
        query = f'title:"{title}"'
    elif authors:
        query = f'authors:"{authors}"'
    else:
        return None

    results, elapsed = query_api("search/works", query, limit=len(dois))
    return results


def get_unique_filename(file_path, content):
    if os.path.exists(file_path):
        # check if a file with the same size already exists
        existing_size = os.path.getsize(file_path)
        if existing_size == len(content):
            # return None to signify that a file with the same size already exists
            return None
        else:
            base, ext = os.path.splitext(file_path)
            i = 1
            new_file_path = f"{base}_{i}{ext}"
            while os.path.exists(new_file_path):
                i += 1
                new_file_path = f"{base}_{i}{ext}"
            return new_file_path
    else:
        return file_path


def process_dois(doi_list, output_folder, type_of_doi):
   new_output_folder = os.path.join(output_folder, type_of_doi)
   os.makedirs(new_output_folder, exist_ok=True)
   
   # Define error_log_file and not_in_core_db_file for each type
   error_log_file = os.path.join(new_output_folder, "download_errors.txt")
   not_in_core_db_file = os.path.join(new_output_folder, "Not_In_CORE_Database.txt")

   # Search CORE with all DOIs in one go
   result_list = search_core(dois=doi_list)
   
   if result_list is None:
        print(f"No results returned from search_core for DOIs: {doi_list}")
        return

   # Get the DOIs from the results
   result_dois = [result.get('doi') for result in result_list['results']]

   # Compare the DOIs in the results with the original DOIs
   missing_dois = set(doi_list) - set(result_dois)

   # Write the missing DOIs to the Not_In_CORE_Database.txt file
   with open(not_in_core_db_file, 'a') as f:
       for doi in missing_dois:
           doi_title = get_title_from_doi(doi)
           combined_doi_title = doi + ': ' + doi_title
           f.write(combined_doi_title + '\n')

   for result in result_list['results']:
    
    # Iterating through results from CORE API
     
        if not result.get('abstract') and not result.get('downloadUrl'):
            print(f"{result['title']} because the abstract is empty and url isn't there.")
            continue
    
        # If we can't download the article, log it
        if not result.get('downloadUrl') or result.get('downloadUrl') == '':
            with open(error_log_file, 'a') as f:
                f.write(f"Title: {result['title']}\n")
                f.write(f"Year: {result['yearPublished']}\n")
                f.write(f"Authors: {', '.join([author['name'] for author in result['authors']])}\n")
                f.write(f"Abstract: {result['abstract']}\n\n")
            print(f"Could not download: {result['title']}. Logged the error.")
            continue
       
        author_positions = {}
        for author in result['authors']:
            author_name = author['name'].split()[0]
            if ',' in author['name']:
                author_name = author_name[:-1]
            try:
                if result['fullText'] is not None:
                    full_text = result['fullText']
                    match = re.search(author_name, full_text[10:], re.IGNORECASE)
                    if match is not None:
                        position = match.start()
                        if position <= 100 and "correspondence" in full_text[:position + 50]:
                            match = re.search(author_name, full_text[full_text.index("correspondence") + len("correspondence"):], re.IGNORECASE)
                            position = full_text.index("correspondence") + len("correspondence") + match.start()
                        if any(full_text[max(0, position - 50):position].endswith(char) for char in author_name):
                            match = re.search(author_name, full_text[position:], re.IGNORECASE)
                            position += match.start()
                        author_positions[author_name] = position
                    else:
                        raise ValueError
                    authors_in_order = sorted(author_positions, key=author_positions.get)
                else:
                    authors_in_order = author['name'].split()[0] + 'check_authors'
            except ValueError:
                print(f"Could not find author {author_name} in text.")
                continue
    
        url = result['downloadUrl']
        if "arxiv.org/abs/" in url:
            url = url.replace("arxiv.org/abs/", "arxiv.org/pdf/") + ".pdf"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        
        download_url_file_path = os.path.join(new_output_folder, "download_urls.txt")
        with open(download_url_file_path, 'a') as url_file:
            url_file.write(f"{authors_in_order[0]} et al., ({result['yearPublished']}): {url}\n")
            
        authors = authors_in_order
        author_count = len(result['authors'])
        first_author = authors_in_order[0]
        year = result['yearPublished']
    
        if author_count == 1:
            filename = f"({first_author}, {year}).pdf"
        elif author_count == 2:
            second_author = authors_in_order[1]
            filename = f"({first_author} & {second_author}, {year}).pdf"
        else:
            filename = f"({first_author} et al., {year}).pdf"
    
        file_path = get_unique_filename(os.path.join(new_output_folder, filename), response.content)
    
        if file_path is None:
            print(f"File with the same size already exists for {result['title']}. Skipping.")
            continue
    
        if author_count > 30 or len(filename.split()[0]) == 1:
            subfolder = os.path.join(new_output_folder, "check for errors")
            os.makedirs(subfolder, exist_ok=True)
            file_path = os.path.join(subfolder, filename)
    
        with open(file_path, 'wb') as f:
            if response.content is not None:
                f.write(response.content)
            else:
                print(f"No content to write for {result['title']}.")

    
        if 'doi' in result and result['doi'] is not None:
            doi_folder = os.path.join(new_output_folder, 'dois')
            os.makedirs(doi_folder, exist_ok=True)
            doi_file_path = os.path.join(doi_folder, filename.replace('.pdf', '.txt'))
            with open(doi_file_path, 'w') as doi_file:
                doi_file.write(result['doi'])
        else:
            print(f"DOI not found for {result['title']}. Skipping DOI write.")
    
        file_size_kb = os.path.getsize(file_path) / 1024  # Size in kilobytes
        if file_size_kb < 200:
            with open(error_log_file, 'a') as f:
                f.write(f"Title: {result['title']}\n")
                f.write(f"Year: {result['yearPublished']}\n")
                f.write(f"Authors: {', '.join([author['name'] for author in result['authors']])}\n")
                f.write(f"Abstract: {result['abstract']}\n")
                f.write(f"File Size: {file_size_kb:.2f} KB\n\n")
    
            os.remove(file_path)
            print(f"File {filename} is smaller than 200 KB. Added info to the error log and deleted the file.")
            continue

        print(f"Successfully downloaded :{result['title']}, {first_author}.")
   
root = tk.Tk()
root.withdraw()  # hide the root widget

pdf_file = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])

if pdf_file:
    base_name = os.path.splitext(os.path.basename(pdf_file))[0]
    dir_path = os.path.dirname(pdf_file)
    doi_folder = os.path.join(dir_path, 'dois')
    txt_file_path = os.path.join(doi_folder, base_name + '.txt')
    
    os.makedirs(doi_folder, exist_ok=True)  # Make sure the doi_folder exists
    
    if os.path.exists(txt_file_path):
        doi = get_doi(txt_file_path)
    else:
        doi = simpledialog.askstring("Input", "Enter the DOI for file " + base_name, parent=root)
        
        # Save the entered DOI to a text file with the name of the PDF file
        with open(txt_file_path, 'w') as f:
            f.write(doi)

root.quit()

doi = [doi]

while True:
    n_cites, cite_dois, meta_data = collect_citations(doi, util='citations', collect_dois=True)
    n_refs, refs_dois, meta_data = collect_citations(doi, util='references', collect_dois=True)

    # Check if there are no citation DOIs or the DOIs is None
    if (not cite_dois or all(value is None for value in cite_dois.values())) and \
    (not refs_dois or all(value is None for value in refs_dois.values())):
        print("DOI Missing")
        doi[0] = simpledialog.askstring("Input", "Enter a new DOI", parent=root)
    else:
        break  # Break the loop if either cite_dois or refs_dois contains different DOIs

output_folder = os.path.join(dir_path, base_name)  # Folder named after original PDF
os.makedirs(output_folder, exist_ok=True)
not_in_core_db_file = os.path.join(output_folder, "Not_In_CORE_Database.txt")

if cite_dois and not all(value is None for value in cite_dois.values()):
    process_dois(cite_dois[doi[0]], output_folder, 'Citations')
if refs_dois and not all(value is None for value in refs_dois.values()):
    process_dois(refs_dois[doi[0]], output_folder, 'References')

process_dois(cite_dois[doi[0]], output_folder, 'Citations')
process_dois(refs_dois[doi[0]], output_folder, 'References')
