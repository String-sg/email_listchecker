import streamlit as st
import pandas as pd


def main():
    st.title("Email Address Checker")

    # Upload CSV files
    master_file = st.file_uploader("Upload Master List CSV", type=["csv"])
    delta_file = st.file_uploader("Upload Delta List CSV", type=["csv"])

    # Filter input
    filter_type = st.radio("Filter type", ('Include', 'Exact'))
    filter_domain = st.text_input(
        "Enter domain (example: moe.gov.sg, tech.gov.sg)")

    if master_file and delta_file and filter_domain:
        try:
            # Read CSV files and convert emails to lowercase
            master_df = pd.read_csv(master_file)
            delta_df = pd.read_csv(delta_file)
            master_df['email'] = master_df['email'].str.lower()
            delta_df['email'] = delta_df['email'].str.lower()

            # Find emails in master not in delta
            master_emails = set(master_df['email'])
            delta_emails = set(delta_df['email'])
            not_in_delta = master_emails - delta_emails

            # Prepare the output DataFrame
            results_df = pd.DataFrame(list(not_in_delta), columns=['email'])
            results_df['In Delta'] = 'No'

            # Filter emails based on domain
            if filter_type == 'Include':
                results_df = results_df[results_df['email'].str.contains(
                    f"@{filter_domain}", case=False, na=False)]
            elif filter_type == 'Exact':
                results_df = results_df[results_df['email'].str.endswith(
                    f"@{filter_domain}", na=False)]

            # Display results
            st.write("Filtered Master List not in Delta List:")
            st.dataframe(results_df)
        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
