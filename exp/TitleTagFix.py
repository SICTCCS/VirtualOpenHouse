import os
from bs4 import BeautifulSoup

def fix_html_titles(root_dir='.', dry_run=True):
    TARGET_TITLE = "SICTC Virtual Open House"
    
    found_count = 0
    fixed_count = 0
    
    status = "EXAMINATION ONLY" if dry_run else "LIVE REPAIR MODE"
    print(f"--- Starting {status} in: {os.path.abspath(root_dir)} ---")

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.html'):
                file_path = os.path.join(root, file)
                file_modified = False
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        soup = BeautifulSoup(f, 'html.parser')
                    
                    title_tag = soup.title
                    print(title_tag)
                    
                    # Case 1: Title exists but is wrong
                    if title_tag:
                        if title_tag.string != TARGET_TITLE:
                            title_tag.string = TARGET_TITLE
                            file_modified = True
                    
                    # Case 2: Title tag is missing entirely
                    else:
                        new_title = soup.new_tag("title")
                        new_title.string = TARGET_TITLE
                        if soup.head:
                            soup.head.append(new_title)
                        else:
                            # If no <head> exists, prepend to the <html> tag
                            if soup.html:
                                soup.html.insert(0, new_title)
                        file_modified = True

                    # Save the changes if we are not in dry_run mode
                    if file_modified:
                        if not dry_run:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(str(soup))
                            print(f"[FIXED] {file_path}")
                        else:
                            print(f"[WOULD FIX] {file_path}")
                        fixed_count += 1
                    
                    found_count += 1
                        
                except Exception as e:
                    print(f"[ERROR] Could not process {file_path}: {e}")

    print(f"\n--- Process Complete ---")
    print(f"Files scanned: {found_count}")
    print(f"Files {'to be ' if dry_run else ''}fixed: {fixed_count}")

# 1. First, run with dry_run=True to see what will happen
# 2. Then, change to dry_run=False to actually save the changes
fix_html_titles(dry_run=True)