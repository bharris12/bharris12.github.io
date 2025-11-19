import datetime
from scholarly import scholarly

def fetch_and_update_citations():
    print("Fetching author data...")
    # Replace with your Google Scholar ID
    author_id = 'vEHTfVwAAAAJ'
    
    try:
        author = scholarly.search_author_id(author_id)
        scholarly.fill(author, sections=['publications'])
        print(f"Found {len(author['publications'])} publications.")
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # Sort publications by year (descending)
    pubs = author['publications']
    pubs.sort(key=lambda x: x['bib'].get('pub_year', 0), reverse=True)

    html_content = ""
    
    for pub in pubs:
        # Fill the publication to get full details like journal, etc.
        # Note: filling every publication might be slow and hit rate limits.
        # For a simple list, the basic info might be enough, but 'journal' is often missing in the basic list.
        # Let's try to use the basic info first, and only fill if necessary.
        # The basic info usually has: title, author, pub_year.
        # Journal might be in 'bib' dictionary.
        
        title = pub['bib'].get('title', 'No Title')
        # scholarly returns authors as a string "A Author, B Author" or list? 
        # It usually returns a string in the 'bib' dict.
        authors = pub['bib'].get('author', 'Unknown Authors')
        
        # Highlight the user's name
        authors = authors.replace("Benjamin D Harris", "<b>Benjamin D. Harris</b>")
        authors = authors.replace("Benjamin Harris", "<b>Benjamin Harris</b>")
        authors = authors.replace("BD Harris", "<b>Benjamin D. Harris</b>")
        
        journal = pub['bib'].get('journal', '')
        if not journal:
             journal = pub['bib'].get('citation', '')
             
        year = pub['bib'].get('pub_year', '')
        
        # Attempt to find a link. Scholarly might not provide a direct link to the paper 
        # in the basic object, but 'url_scholarbib' or similar might exist.
        # Actually, for the purpose of this feed, we might just link to the Google Scholar entry 
        # or try to find a DOI if we fill it.
        # Let's just link to the Google Scholar citation for now if no other link.
        link = f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={author_id}&citation_for_view={pub['author_pub_id']}"
        
        html_content += f"""
      <p><i>{title}</i> <br>
        {authors} <br>
        {journal}, {year} <a href="{link}">[Google Scholar]</a>
      </p>
"""

    # Read the existing index.html
    with open('index.html', 'r') as f:
        content = f.read()

    # Replace the content
    start_marker = '<!-- SCHOLAR_START -->'
    end_marker = '<!-- SCHOLAR_END -->'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx + len(start_marker)] + "\n" + html_content + "      " + content[end_idx:]
        
        with open('index.html', 'w') as f:
            f.write(new_content)
        print("Successfully updated index.html")
    else:
        print("Markers not found in index.html")

if __name__ == "__main__":
    fetch_and_update_citations()
