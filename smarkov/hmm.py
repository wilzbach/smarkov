
from collections import defaultdict
from markov import Markov
from itertools import chain
import utils


__author__ = "greenify"
__copyright__ = "Copyright 2016, greenify"


class HMM(Markov):

    """ A simple HMM

        Attributes:
            corpus: given corpus (a corpus_entry needs to be a tuple or array)
            order: maximal order to look back for a given state
            order_emissions: maximal order to look back at previous emissions for a given emission (only HMM)
    """

    def __init__(self, corpus, order=1, order_emissions=1):
        """ Initializes the Markov Chain with a given corpus and order """
        Markov.__init__(self, corpus, order)
        self.pos_tag = lambda x: x
        self.order_emissions = order_emissions
        self._compute_emissions(corpus, self.order)

    def _compute_emissions(self, corpus, order=1):
        """ Computes the emissions and transitions probabilities of a corpus
            based on word types
        Args:
            corpus: the given corpus (a corpus_entry needs to be iterable)
            order: the maximal Markov chain order
        Computes:
            self.emissions: Probabilities to emit word (token_value) at state x (token_type)
            self.transitions_hmm: Transition probabilities to switch between states (token_type)
            self.emissions_past: Probabilities to emit a word (token_value) at state x
                                 (token_type) based on previous emissions (token_value)
        """
        self.emissions = defaultdict(lambda: defaultdict(int))
        self.transitions_hmm = defaultdict(lambda: defaultdict(int))
        self.emissions_past = defaultdict(
            lambda: defaultdict(lambda: defaultdict(int)))

        for corpus_entry in corpus:
            tokens = self.pos_tag(corpus_entry)

            last_tokens = utils.prefilled_buffer(
                self._start_symbol, length=self.order)
            last_emissions = utils.prefilled_buffer(
                self._start_symbol, length=self.order_emissions)

            for token in chain(tokens, [[self._end_symbol] * 2]):
                token_value = token[0]
                token_type = token[1]

                for suffix in utils.get_suffixes(last_tokens):
                    self.transitions_hmm[suffix][token_type] += 1
                    self.emissions[token_type][token_value] += 1

                for suffix in utils.get_suffixes(last_emissions):
                    self.emissions_past[token_type][
                        suffix][token_value] += 1

                last_tokens.append(token_type)
                last_emissions.append(token_value)

        self._compute_relative_probs(self.emissions)
        self._compute_relative_probs(self.transitions_hmm)
        for val in self.emissions_past.values():
            self._compute_relative_probs(val)

    def generate_text(self, generation_type='markov'):
        """ Generates sentences from a given corpus
        Args:
            generation_type: 'markov' | 'hmm' | 'hmm_past'
        Returns:
            Properly formatted string of generated sentences
        """
        assert generation_type in ['markov', 'hmm', 'hmm_past']
        if generation_type == "markov":
            return self._text_generator(next_token=self._generate_next_token)
        elif generation_type == "hmm":
            return self._text_generator(next_token=self._generate_next_token_hmm, emit=self._emitHMM)
        elif generation_type == "hmm_past":
            return self._text_generator(next_token=self._generate_next_token_hmm, emit=self._emitHMM_with_past)

    def _generate_next_token_hmm(self, past_states):
        """ generates next token based previous word types """
        return self._generate_next_token_helper(past_states, self.transitions_hmm)

    def _emitHMM(self, token_type, past_states, past_emissions):
        """ emits a word based on previous tokens """
        assert token_type in self.emissions
        return utils.weighted_choice(self.emissions[token_type].items())

    def _emitHMM_with_past(self, token_type, past_states, past_emissions):
        """ emits a word based on previous states (=token) and previous emissions (=words)
        The states and emissions are weighted according to their defined probabilities
            self.prob_hmm_states and self.prob_hmm_emissions"""
        assert token_type in self.emissions
        states_items = [(x[0], x[1] * self.prob_hmm_states)
                        for x in self.emissions[token_type].items()]
        key_emissions = tuple(past_emissions)
        if key_emissions in self.emissions_past[token_type]:
            states_emissions = [(x[0], x[1] * self.prob_hmm_emissions) for x in self.emissions_past[
                                token_type][tuple(past_emissions)].items()]
            return utils.weighted_choice(states_items + states_emissions)
        return utils.weighted_choice(states_items)
