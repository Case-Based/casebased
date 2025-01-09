# Solution Adapter
# Takes output from the Retriever and adapts the solution to the case
class Adapter:
    def __init__(self, case_base, vocab, adaptation_rules=None):
        self.case_base = case_base
        self.adaptation_rules = adaptation_rules
        self.vocab = vocab

    def adapt(self, case, k_similar_cases):
        """
        Adapt the solution to the case
        """
        if self.adaptation_rules is None:
            return self.case_base.cases.iloc[k_similar_cases[0]][
                self.vocab.targets
            ].values[0]
