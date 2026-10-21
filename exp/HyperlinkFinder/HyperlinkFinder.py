from bs4 import BeautifulSoup

pathToIndex="../index.html"
output_path = "HyperlinkFinder.txt"

def export_links_context(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        with open(output_path, 'w', encoding='utf-8') as out:
            out.write(f"Link Index Report for: {input_path}\n")
            out.write("=" * 50 + "\n\n")
            
            found_count = 0
            for line_num, content in enumerate(lines, start=1):
                # Search for the anchor tag
                if '<a' in content.lower():
                    # Format: [Line XX] Content
                    out.write(f"[Line {line_num:04d}] {content.strip()}\n")
                    found_count += 1
            
            if found_count == 0:
                out.write("No hyperlinks found.")
            else:
                out.write(f"\n" + "=" * 50 + "\n")
                out.write(f"Total links identified: {found_count}")
        
        print(f"Success! Report generated at: {output_path}")

    except FileNotFoundError:
        print(f"Error: Could not find '{input_path}'. Check the filename and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Usage
export_links_context(pathToIndex,output_path)