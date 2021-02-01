from playlist_explanation.src.data.the_chain import save_graph_the_chain
from playlist_explanation.src.interestingness.save_sampled_KB_for_interestingness import save_sampled_KB_for_interestingness
from playlist_explanation.src.run.test_2 import save_sub_graphs_that_match_the_chain_style
from user_trial.user_trial import save_segues
from user_trial.user_trial import save_user_trial_segue_sample



def run():
    print("Saving subgraphs for interestingness ...")
    save_sampled_KB_for_interestingness(20000)
    print("Saving subgraphs for the chain ...")
    save_graph_the_chain()
    print("Saving eligible subgraphs for test2 ...")
    save_sub_graphs_that_match_the_chain_style()


if __name__ == "__main__":
    run()
