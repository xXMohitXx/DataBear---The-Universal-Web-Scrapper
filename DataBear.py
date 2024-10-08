import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Streamlit layout
st.title('DataBear - Universal Web Scrapping Tool')

# User inputs for scraping
url = st.text_input('Enter the URL of the website to scrape:')
tag_name = st.text_input('Enter the tag name to scrape (e.g., div, span, h1):')
class_name = st.text_input('Enter the class name to scrape (leave empty if not applicable):')
filter_keyword = st.text_input('Enter a keyword filter (optional):')

# Button to trigger scraping
if st.button('Scrape Data'):
    if url and tag_name:
        try:
            # Fetch the HTML content
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'html.parser')

            # Scrape based on user inputs
            if class_name:
                elements = soup.find_all(tag_name, class_=class_name)
            else:
                elements = soup.find_all(tag_name)

            # Apply keyword filter if provided
            results = []
            for element in elements:
                text = element.get_text(strip=True)
                if not filter_keyword or filter_keyword.lower() in text.lower():
                    results.append(text)

            # Display the results
            if results:
                st.write(f"Found {len(results)} elements matching your criteria.")
                for i, result in enumerate(results):
                    st.write(f"{i + 1}. {result}")

                # Offer to download as CSV
                df = pd.DataFrame(results, columns=["Scraped Data"])
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download data as CSV", data=csv, file_name="scraped_data.csv",
                                   mime="text/csv")
            else:
                st.write("No matching data found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide both URL and tag name.")

# Instructions for users
st.markdown("""
### How to Use This Tool:
1. **Enter URL**: Type the URL of the website you want to scrape.
2. **Tag Name**: Provide the HTML tag you wish to scrape (like `div`, `h1`, `p`, etc.).
3. **Class Name**: If you want to target a specific section, provide the class name (leave blank if not needed).
4. **Keyword Filter**: Optional, but you can filter the results based on specific keywords in the text.
5. **Scrape**: Press the 'Scrape Data' button to get results and optionally download them as a CSV.
""")
