import pandas as pd
# pandas: groupby, sum, mean, sort_values for all cals

def analyse_dataset(filepath):
    # Time: O(n) per groupby operation
    # Space: O(n) - loads full dataframe into memory
    df = pd.read_csv(filepath)
    # read csv onto pd df - same as load_csv in helpers.py

    print("\n========== Meeting Analytics ==========\n")

    # Q1 & Q2: most/least words by speaker
    words_per_speaker = df.groupby("name")["num_words"].sum()
    # single expensive groupby, reused for following qs
    print(f"Most words: {words_per_speaker.idxmax()}, {words_per_speaker.max()} words")
    # idmax/max: single winner question - extract one val
    print(f"Least words: {words_per_speaker.idxmin()}, {words_per_speaker.min()} words")
    # idmin/min: same lowest total


    # Q3: total speaking time of the meeting
    total_time = df["time_taken_sec"].sum()
    # no groupby - meeting-wide total
    print(f"\nTotal speaking time: {round(total_time, 2)} seconds")

    # Q4: average speaking time per speaker
    avg_time_per_speaker = df.groupby("name")["time_taken_sec"].mean()
    # single avg. per speaker
    print("\nAverage speaking time per speaker:")
    for name, avg in avg_time_per_speaker.items():
        # "per speaker" - show ea. val. not pull one extreme
        print(f"  {name}: {round(avg, 2)} seconds")

    # Q5: who asked the most questions
    questions_per_speaker = df[df["question_flag"] == True].groupby("name").size()
    # filters only rows w/ question
    # same row structure
    # .size() counts filtered rows per speaker
    if not questions_per_speaker.empty:
        # guard: if not q: empty filter set
        # idmax() would crash w/ empty series w/o this check
        print(f"\nMost questions: {questions_per_speaker.idxmax()}, {questions_per_speaker.max()} question(s)")
    else:
        print("\nMost questions: none asked")

    # Q6: top 5 speakers by total speaking time
    total_time_per_speaker = df.groupby("name")["time_taken_sec"].sum()
    top5 = total_time_per_speaker.sort_values(ascending=False).head(5)
    # enumerate(...,1): starts at 1 inteas of 0
    print("\nTop 5 speakers by total speaking time:")
    for rank, (name, sec) in enumerate(top5.items(), 1):
        print(f"  {rank}. {name}: {round(sec, 2)} seconds")

    # Q7: average speech rate per speaker
    rate_per_speaker = df.groupby("name")["speech_rate_wps"].mean()
    # same as Q4: "per speaker", loops through all vals.
    print("\nAverage speech rate per speaker:")
    for name, wps in rate_per_speaker.items():
        print(f"  {name}: {round(wps, 2)} words/second")

    print("\n========================================\n")