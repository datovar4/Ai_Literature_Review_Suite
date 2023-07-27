#add code to kill the gui at the end, make code that takes a review paper and downloads the citations

import os
import requests
import json
import re
import string
import tkinter as tk
from tkinter import ttk
from api_key_checker import check_api_key

check_api_key("CORE_API.txt", "CORE")
with open("CORE_API.txt", "r") as f:
    api_key = f.read().strip()
    
api_key = api_key

api_endpoint = "https://api.core.ac.uk/v3/"


def query_api(url_fragment, query, limit):
    headers = {"Authorization": "Bearer " + api_key}
    query = {"q": query, "limit": limit}
    response = requests.post(f"{api_endpoint}{url_fragment}", data=json.dumps(query), headers=headers)
    if response.status_code == 200:
        return response.json(), response.elapsed.total_seconds()
    else:
        print(f"Error code {response.status_code}, {response.content}")

def get_unique_filename(filepath, incoming_file_content):
    if not os.path.isfile(filepath):
        return filepath

    existing_file_size = os.path.getsize(filepath)
    incoming_file_size = len(incoming_file_content)

    # If the file sizes are the same, return None
    if existing_file_size == incoming_file_size:
        return None

    base, ext = os.path.splitext(filepath)
    for char in string.ascii_lowercase:  # iterate through 'a' to 'z'
        new_filepath = f"{base}_{char}{ext}"
        if not os.path.isfile(new_filepath):
            return new_filepath

    raise ValueError("Unable to generate a unique filename. All alphabetical suffixes are used.")

# GUI code integration

def create_entry_row(parent, operator, columns=3):
    entries = [ttk.Entry(parent, width=30) for _ in range(columns)]
    for column, entry in enumerate(entries):
        entry.grid(row=0, column=column*2)
        if column < columns - 1:
            ttk.Label(parent, text=operator).grid(row=0, column=column*2+1)
    return entries

def create_year_row(parent):
    entry_start = ttk.Entry(parent, width=30)
    ttk.Label(parent, text="TO").grid(row=0, column=1)
    entry_end = ttk.Entry(parent, width=30)
    entry_start.grid(row=0, column=0)
    entry_end.grid(row=0, column=2)
    return entry_start, entry_end


def create_query():
    global author_and_entries, author_or_entries, title_and_entries, title_or_entries, topic_and_entries, topic_or_entries, year_start, year_end
    
    query_parts = []
    if author_and_entries:
        query_parts.append(f" AND ".join(f'authors:{entry.get()}' for entry in author_and_entries if entry.get()))
    if author_or_entries:
        query_parts.append(f" OR ".join(f'authors:{entry.get()}' for entry in author_or_entries if entry.get()))
    if title_and_entries:
        query_parts.append(f" AND ".join(f'title:{entry.get()}' for entry in title_and_entries if entry.get()))
    if title_or_entries:
        query_parts.append(f" OR ".join(f'title:{entry.get()}' for entry in title_or_entries if entry.get()))
    if topic_and_entries:
        query_parts.append(f" AND ".join(f'{entry.get()}' for entry in topic_and_entries if entry.get()))
    if topic_or_entries:
        query_parts.append(f" OR ".join(f'{entry.get()}' for entry in topic_or_entries if entry.get()))
    if year_start.get() and year_end.get():
        query_parts.append(f"yearPublished>={year_start.get()} AND yearPublished<={year_end.get()}")

    query = " AND ".join(f"{part}" for part in query_parts if part)
    results_dict = start_download_process(query)
    return results_dict


def start_download_process(query):
    results, elapsed = query_api("search/works", query, limit=pdf_limit+20)
    results_dict = results['results']
    return results_dict


def submit_query():
    global results_dict
    global output_folder
    global output_folder_entry
    global error_log_file
    global pdf_limit
    output_folder = output_folder_entry.get()
    os.makedirs(output_folder, exist_ok=True)
    error_log_file = os.path.join(output_folder, "download_errors.txt")
    pdf_limit = int(pdf_limit_entry.get())  # new line
    results_dict = create_query()
    process_results()
    root.quit()  # Exit the main event loop


def process_results():
    doi_folder = os.path.join(output_folder, 'dois')
    os.makedirs(doi_folder, exist_ok=True)  # Create folder for DOIs
    for i, result in enumerate(results_dict[:pdf_limit], start=1):
        # Check if the abstract is empty
        if not result.get('abstract') and not result.get('downloadUrl'):
            print(f"Skipping {i}: {result['title']} because the abstract is empty and url isn't there.")
            continue
    
        # If we can't download the article, log it
        if not result.get('downloadUrl') or result.get('downloadUrl') == '':
            with open(error_log_file, 'a') as f:
                f.write(f"Title: {result['title']}\n")
                f.write(f"Year: {result['yearPublished']}\n")
                f.write(f"Authors: {', '.join([author['name'] for author in result['authors']])}\n")
                f.write(f"Abstract: {result['abstract']}\n\n")
            print(f"Could not download {i}: {result['title']}. Logged the error.")
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
                        # Check if "correspondence" is found within the first 100 characters
                        if position <= 100 and "correspondence" in full_text[:position + 50]:
                            # Ignore the text before "correspondence" and search again
                            match = re.search(author_name, full_text[full_text.index("correspondence") + len("correspondence"):], re.IGNORECASE)
                            position = full_text.index("correspondence") + len("correspondence") + match.start()
                        # Check if the author's name is within 50 characters
                        if any(full_text[max(0, position - 50):position].endswith(char) for char in author_name):
                            # Ignore the text before the author's name and search again
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
    
        # Sort authors by position in text
    
    
        url = result['downloadUrl']
        if "arxiv.org/abs/" in url:
            url = url.replace("arxiv.org/abs/", "arxiv.org/pdf/") + ".pdf"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
        response = requests.get(url, headers=headers)
    
        # Extract author information
        authors = authors_in_order
        author_count = len(result['authors'])
        first_author = authors_in_order[0]
        year = result['yearPublished']
        
        response = requests.get(url, headers=headers)
        # Generate filename based on author information
        if author_count == 1:
            filename = f"({first_author}, {year}).pdf"
        elif author_count == 2:
            second_author = authors_in_order[1]
            filename = f"({first_author} & {second_author} {year}).pdf"
        else:
            filename = f"({first_author} et al., {year}).pdf"
    
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        file_path = get_unique_filename(os.path.join(output_folder, filename), response.content)
        
        download_url_file_path = os.path.join(output_folder, "download_urls.txt")
        with open(download_url_file_path, 'a') as url_file:
            url_file.write(f"{authors_in_order[0]} et al., ({result['yearPublished']}): {url}\n")

     # If file_path is None, it means a file with the same size already exists
        if file_path is None:
             print(f"File with the same size already exists for {result['title']}. Skipping.")
             continue
        
        if author_count > 30:
            subfolder = os.path.join(output_folder, "check for errors")
            os.makedirs(subfolder, exist_ok=True)
            file_path = os.path.join(subfolder, filename)
        else:
            file_path = os.path.join(output_folder, filename)
             
        if len(filename.split()[0]) == 1:
           subfolder = os.path.join(output_folder, "check for errors")
           os.makedirs(subfolder, exist_ok=True)
           file_path = os.path.join(subfolder, filename)
    
        # Save the PDF file in the output folder
        with open(file_path, 'wb') as f:
            f.write(response.content)
        # Check if DOI exists and save it in a separate text file
        if 'doi' in result and result['doi'] is not None:
            doi_folder = os.path.join(output_folder, 'dois')
            os.makedirs(doi_folder, exist_ok=True)
            doi_file_path = os.path.join(doi_folder, filename.replace('.pdf', '.txt'))
            with open(doi_file_path, 'w') as doi_file:
                doi_file.write(result['doi'])
        else:
            print(f"DOI not found for {result['title']}. Skipping DOI write.")
        # Check the size of the PDF file
        file_size_kb = os.path.getsize(file_path) / 1024  # Size in kilobytes
        if file_size_kb < 200:
            # Add info to the error log
            with open(error_log_file, 'a') as f:
                f.write(f"Title: {result['title']}\n")
                f.write(f"Year: {result['yearPublished']}\n")
                f.write(f"Authors: {', '.join([author['name'] for author in result['authors']])}\n")
                f.write(f"Abstract: {result['abstract']}\n")
                f.write(f"File Size: {file_size_kb:.2f} KB\n\n")
    
            # Delete the file from the folder
            os.remove(file_path)
            print(f"File {filename} is smaller than 200 KB. Added info to the error log and deleted the file.")
            continue
    
        print(f"Successfully downloaded {i}: {result['title']}, {first_author}.")
    
    print("Operation complete.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PDF Downloader")
    root.geometry("1000x600")

    for idx, (label_text, operator) in enumerate([("Author", "AND"), ("Author", "OR"), 
                                                  ("Title", "AND"), ("Title", "OR"),
                                                  ("Topic", "AND"), ("Topic", "OR")], start=1):
        frame = ttk.LabelFrame(root, text=label_text)
        frame.grid(row=idx, column=0, padx=10, pady=10, sticky='we')
        if "AND" in operator:
            globals()[f"{label_text.lower()}_and_entries"] = create_entry_row(frame, operator)
        else:
            globals()[f"{label_text.lower()}_or_entries"] = create_entry_row(frame, operator)

    frame_year = ttk.LabelFrame(root, text="Year")
    frame_year.grid(row=7, column=0, padx=10, pady=10, sticky='we')
    year_start, year_end = create_year_row(frame_year)
    year_start.insert(0, '2000')  # Set default value for year start
    year_end.insert(0, '2023')  # Set default value for year end

    frame_output = ttk.Frame(root)
    frame_output.grid(row=8, column=0, padx=10, pady=10, sticky='we')

    ttk.Label(frame_output, text="Output Folder:").grid(row=0, column=0)
    output_folder_entry = ttk.Entry(frame_output)
    output_folder_entry.insert(0, 'default_pdf_folder')  # Set default value for output folder
    output_folder_entry.grid(row=0, column=1)

    frame_pdf_limit = ttk.Frame(root)
    frame_pdf_limit.grid(row=9, column=0, padx=10, pady=10, sticky='we')

    ttk.Label(frame_pdf_limit, text="Number of PDFs:").grid(row=0, column=0)
    pdf_limit_entry = ttk.Entry(frame_pdf_limit)
    pdf_limit_entry.insert(0, '20')  # Set default value for pdf limit
    pdf_limit_entry.grid(row=0, column=1)

    # Defining output label
    output_label = ttk.Label(root, text="")
    output_label.grid(row=9, column=1, padx=10)

    button_submit = ttk.Button(root, text="Submit", command=submit_query)
    button_submit.grid(row=9, column=0, pady=10)

    root.mainloop()
    root.destroy()


