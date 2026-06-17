import pandas as pd

def analyse_dataset(filepath):
    # Time: O(n) per groupby operation
    # Space: O(n) - loads full dataframe into memory
    df = pd.read_csv(filepath)

    print("\n========== Meeting Analytics ==========\n")

    # Q1 & Q2: most/least words by speaker
    words_per_speaker = df.groupby("name")["num_words"].sum()
    print(f"Most words: {words_per_speaker.idxmax()}, {words_per_speaker.max()} words")
    print(f"Least words: {words_per_speaker.idxmin()}, {words_per_speaker.min()} words")

    # Q3: total speaking time of the meeting
    total_time = df["time_taken_sec"].sum()
    print(f"\nTotal speaking time: {round(total_time, 2)} seconds")

    # Q4: average speaking time per speaker
    avg_time_per_speaker = df.groupby("name")["time_taken_sec"].mean()
    print("\nAverage speaking time per speaker:")
    for name, avg in avg_time_per_speaker.items():
        print(f"  {name}: {round(avg, 2)} seconds")

    # Q5: who asked the most questions
    questions_per_speaker = df[df["question_flag"] == True].groupby("name").size()
    if not questions_per_speaker.empty:
        print(f"\nMost questions: {questions_per_speaker.idxmax()}, {questions_per_speaker.max()} question(s)")
    else:
        print("\nMost questions: none asked")

    # Q6: top 5 speakers by total speaking time
    total_time_per_speaker = df.groupby("name")["time_taken_sec"].sum()
    top5 = total_time_per_speaker.sort_values(ascending=False).head(5)
    print("\nTop 5 speakers by total speaking time:")
    for rank, (name, sec) in enumerate(top5.items(), 1):
        print(f"  {rank}. {name}: {round(sec, 2)} seconds")

    # Q7: average speech rate per speaker
    rate_per_speaker = df.groupby("name")["speech_rate_wps"].mean()
    print("\nAverage speech rate per speaker:")
    for name, wps in rate_per_speaker.items():
        print(f"  {name}: {round(wps, 2)} words/second")

    print("\n========================================\n")