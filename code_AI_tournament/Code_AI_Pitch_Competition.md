# Codebase for AI Pitch Competition



## Existing Implementations

Suggestions on existing code? Maybe something like:
- [https://pypi.org/project/swissdutch/](https://pypi.org/project/swissdutch/)
- [https://github.com/JeffHoogland/pypair](https://github.com/JeffHoogland/pypair)
- [https://github.com/thurstonemerson/swiss-system-tournament](https://github.com/thurstonemerson/swiss-system-tournament)


## Draft Outline

The following is a pretty weak outline of how to approach this based on my weak understanding of ELO; someone who knows these ranking systems should jump in here and tell me I'm an idiot and fix things! Also we need a system that is robust to failed API calls.



Define a function to parse and store the proposals in a DataFrame

    def load_proposals(folder_path):

Define a function for updating Elo rankings

    def update_elo_rankings(winner_elo, loser_elo, k=32):

Define a function to pair the next competitors based on their current ranking

    def pair_competitors(proposals_df):

Define a function to simulate a competition round, update the rankings, and store the results

    def competition_round(proposals_df, pairings):

Define a function to check the stopping criterion

    def stopping_criterion_met(proposals_df, max_rounds):


Main loop to run the competition


    def run_competition(folder_path, max_rounds):
        proposals_df = load_proposals(folder_path)

        round_number = 0
        while not stopping_criterion_met(proposals_df, round_number, max_rounds):
            round_number += 1
            print(f"Starting round {round_number}...")

            pairings = pair_competitors(proposals_df)
            proposals_df = competition_round(proposals_df, pairings)

        return proposals_df.sort_values(by="elo", ascending=False)



    if __name__ == "__main__":
        folder_path = "path/to/proposals"
        max_rounds = 5  # Set the number of rounds

        final_rankings = run_competition(folder_path, max_rounds)
        print("Final rankings:")
        print(final_rankings)


