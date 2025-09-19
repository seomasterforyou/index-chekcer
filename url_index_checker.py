import streamlit as st
import pandas as pd
import time
from serpapi import GoogleSearch  # <── change this line

# Set page configuration
st.set_page_config(page_title="URL Index Checker", layout="centered")
st.title("🔍 Google Index Checker")

# Markdown description with instructions
st.markdown("""
### Steps to Find API Key:
1. Visit [Serp API](https://www.searchapi.io/)
2. Sign Up to Get Free 100 Requests
3. Dashboard will appear
4. Copy the API Key and Paste in the dialog box below
""")

# Input for API key
api_key = st.text_input("Enter your SerpAPI Key", type="password")

# Textarea for URLs
urls_input = st.text_area("Paste URLs (one per line):")

if st.button("Check Indexing Status"):
    if not api_key:
        st.error("Please enter your SerpAPI Key.")
    elif not urls_input.strip():
        st.error("Please paste at least one URL.")
    else:
        # Prepare list of URLs
        urls = [line.strip() for line in urls_input.strip().splitlines() if line.strip()]
        results_list = []
        progress = st.progress(0)
        status_text = st.empty()

        # Iterate through each URL and check indexing status
        for i, url in enumerate(urls, start=1):
            status_text.text(f"Checking {i}/{len(urls)}: {url}")
            params = {
                "engine": "google",
                "q": f"site:{url}",
                "api_key": api_key
            }

            try:
                # Query SerpAPI
                search = GoogleSearch(params)
                results = search.get_dict()

                if results.get("organic_results"):
                    status = "✅ Indexed"
                else:
                    status = "❌ Not Indexed"
            except Exception as e:
                status = f"⚠️ Error: {e}"

            # Append result for each URL
            results_list.append({"URL": url, "Status": status})

            # Update progress bar
            progress.progress(i / len(urls))

            # Polite delay to avoid hitting the API too quickly
            time.sleep(2)

        # Final status update
        status_text.text("Done!")

        # Convert results to DataFrame for display
        df = pd.DataFrame(results_list)
        
        # Show results in the Streamlit app
        st.subheader("Results")
        st.dataframe(df)

        # Download button for CSV file
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="indexing_results.csv",
            mime="text/csv"
        )
