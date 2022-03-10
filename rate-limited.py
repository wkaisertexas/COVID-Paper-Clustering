import os
import time
import warnings

import pandas as pd
import requests

warnings.filterwarnings("ignore")  # I HAVE TURNED TO THE DARK SIDE!

# Request Properties
INPUT = "altmetric_calls.csv"
OUTPUT = "impact_data.csv"

COLUMNS = ['cord_uid', 'doi', 'patents', 'posts', 'wikipedia', 'feeds', 'msm', 'tweeters', 'policies', 'accounts',
           'score', 'readers_count', 'all_count', 'all_mean', 'all_rank', 'all_pct', 'all_higher_than', 'journal_count',
           'journal_mean', 'journal_rank', 'journal_pct', 'journal_higher_than', 'similar_age_3m_count',
           'similar_age_3m_mean', 'similar_age_3m_rank', 'similar_age_3m_pct', 'similar_age_3m_higher_than',
           'similar_age_journal_3m_count', 'similar_age_journal_3m_mean', 'similar_age_journal_3m_rank',
           'similar_age_journal_3m_pct', 'similar_age_journal_3m_higher_than']

MAX_RETRIES = 1
SAVE_INTERVAL = 100
TEST_FRAC = 1
WAIT_TIME = 0.005
SLEEP_TIME = 8
TIMEOUT = 20  # Twenty second timeout for requests
OUTAGE_TIME = 1800  # Waits a half-hour after the outage


def main():
    # Loads the dataset and removes all but the test values
    dataset = pd.read_csv(INPUT)

    if os.path.exists(OUTPUT):
        # Reads the existing dataset
        output = pd.read_csv(OUTPUT)

        prev_index = dataset["doi"].tolist().index(output.iloc[-1]["doi"])
        print(f"Starting at {prev_index}")

        if len(output.columns) > len(COLUMNS):
            # Removes the extra first column
            output.drop(output.column[0], inplace=True)

    else:
        # Creates a data frame to store the responses, this is the final data frame
        output = pd.DataFrame(columns=COLUMNS)
        prev_index = 0

    print(f"Now Getting the Impact of {len(dataset.index):8d} papers")

    # Statistics on the calls
    too_fast = 0
    not_found = 0
    failed = 0
    failed_save = 0

    # For loop that runs through each element in the data frame
    s = requests.Session()

    j = 0
    for i, row in dataset.iterrows(): # Because I fixed iterrows, it should work by default now.
        if j < prev_index:  # Goes to the last point
            j += 1
            continue

        print(f"Now Trying ({i:4d}, {j:4d}): {row['doi'].split('doi')[1]}")

        try:
            # Makes the api calls
            r = s.get(row['doi'], timeout=TIMEOUT)

            # Checks Status Code
            if r.status_code == 404:
                # Not found
                print(f"Error Code:          404")
                not_found += 1
            elif r.status_code == 429:
                # Making requests too fast
                print("Error Code:           429")

                # This should somehow make the requests again.
                time.sleep(SLEEP_TIME)
                too_fast += 1
            elif r.status_code == 504:
                # The site is down for maintenance
                print("\n\n\nSITE IS DOWN\n\n\n")
                time.sleep(OUTAGE_TIME)
            elif r.status_code // 100 == 4:
                # Misc 400 Error codes
                print(f"400-Level Status Code {r.status_code}")
                failed += 1
            elif r.status_code // 100 == 5:
                # Misc 500 Error codes
                print(f"500-Level Status Code {r.status_code}")
                failed += 1
            elif r.status_code == 200:
                # Success, log the data

                json = r.json()  # Gets the JSON FIle

                # Error Checking to Validate the White-House Dataset
                if json['type'] != 'article':
                    print(f"Non-Article Found: {json['type']}")

                """
                Categories of interest:
                - context -> this has a lot of data about how this paper compares to others
                    For each of the following
                    - all
                    - journal
                    - similar_age_3m
                    - similar_age_journal_3m
                        - count
                        - mean
                        - rank
                        - pct
                        - higher than
                - score
                - all of the cited by
                """

                def get_props(context):
                    props_cat = ['count', 'mean', 'rank', 'pct', 'higher_than']
                    return [context[cat] if cat in json else None for cat in props_cat]

                # Compiles the data to be saved (this should really be a dict....)
                row_data = [row['cord_uid'], row['doi']]

                # Cited by
                cited_by = ['patents', 'posts', 'wikipedia', 'feeds', 'msm', 'tweeters', 'policies', 'accounts']
                row_data.extend(
                    [json[f"cited_by_{name}_count"] if f"cited_by_{name}_count" in json else None for name in cited_by])

                # Misc Scores
                row_data.append(json['score'])
                row_data.append(json['readers_count'])

                # Gets all of the context data
                if 'context' in json:
                    context = json['context']

                    for context_cat in ['all', 'journal', 'similar_age_3m', 'similar_age_journal_3m']:
                        if context_cat in context:
                            row_data.extend(get_props(context[context_cat]))
                        else:
                            row_data.extend([None for i in range(5)])
                else:
                    row_data.extend([None for i in range(20)])

                time.sleep(WAIT_TIME)
                # Creates a new data frame
                impact_data = pd.DataFrame(data=[row_data], columns=COLUMNS)

                # Appends the data frame
                output = output.append(impact_data)
            else:
                print(f"Unknown Error Code: {r.status_code:4d}")
        except requests.exceptions.Timeout:
            # Means that the server times out
            failed += 1
            print(f"the {failed:4d} call timed out")
        # except:
        #    failed += 1
        #    print(f"the {failed:6d} call failed ")

        if j % SAVE_INTERVAL == 0 and j != 0:
            try:
                # Prints Out a Summary Card
                print(f"---({j}) Saved File------")
                print(f"Too Fast  {too_fast / j * 100:10.2f} %")
                print(f"Not Found {not_found / j * 100:10.2f} %")
                print(f"Failed    {failed / j * 100:10.2f} %")
                print(f"Save Fail {failed_save / j * 100:10.2f} %")
                print(f"----------------------\n")

                # Saves the File
                output.to_csv(OUTPUT, index=False)
            except:
                failed_save += 1
                print(f"({failed_save:3d})BAD! Unable to save file!")
                input("Enter anything to continue")
        j += 1


if __name__ == "__main__":
    main()
