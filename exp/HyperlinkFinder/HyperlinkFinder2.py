import os
from bs4 import BeautifulSoup

def deep_scan_links(root_dir='.', output_csv='comprehensive_link_audit.csv'):
    # The URL you want to ignore
    SKIP_URL = "https://g.co/kgs/qucSe8N"
    
    found_count = 0
    skipped_count = 0

    with open(output_csv, 'w', encoding='utf-8') as out:
        # Header for Excel
        out.write("Folder Path | File Name | Line Number | URL (href)\n")
        
        # os.walk travels through every subdirectory automatically
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.lower().endswith('.html'):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            for line_num, content in enumerate(f, start=1):
                                if '<a' in content.lower():
                                    soup = BeautifulSoup(content, 'html.parser')
                                    links = soup.find_all('a', href=True)
                                    
                                    for link in links:
                                        href = link['href']
                                        
                                        # Skip the specific Google link
                                        if href == SKIP_URL:
                                            skipped_count += 1
                                            continue
                                        
                                        # Write to CSV
                                        # root = the folder path, file = the name
                                        out.write(f"{root} | {file} | {line_num} | {href}\n")
                                        found_count += 1
                                        
                    except Exception as e:
                        print(f"Could not process {file_path}: {e}")

    print(f"Deep scan complete!")
    print(f"Total links found: {found_count}")
    print(f"Total links skipped: {skipped_count}")
    print(f"Report saved as: {output_csv}")

# Execute
deep_scan_links()