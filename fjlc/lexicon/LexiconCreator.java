package com.freva.masteroppgave.lexicon;

import com.freva.masteroppgave.lexicon.container.Adjectives;
import com.freva.masteroppgave.lexicon.container.TokenTrie;
import com.freva.masteroppgave.preprocessing.filters.Filters;
import com.freva.masteroppgave.preprocessing.filters.RegexFilters;
import com.freva.masteroppgave.classifier.ClassifierOptions;
import com.freva.masteroppgave.utils.MapUtils;
import com.freva.masteroppgave.utils.reader.DataSetReader;
import com.freva.masteroppgave.utils.progressbar.Progressable;
import com.freva.masteroppgave.utils.tools.Parallel;

import java.util.*;

public class LexiconCreator implements Progressable {
    private DataSetReader dataSetReader;

    /**
     * Generates sentiment lexicon using PMI on words and classification of context they are in.
     *
     * @param dataSetReader       Dataset containing tweets and their sentiment classification
     * @param nGrams              n-grams to calculate sentiment for (with n>1, singletons are calculated automatically)
     * @param minTotalOccurrences minimum number of times n-gram must have appeared in dataset before a sentiment value
     *                            is assigned (higher value gives more accurate sentiment value)
     * @param minSentimentValue   minimum sentiment value required to be included in lexicon (values close to 0 are
     *                            often words that are used equally in positive or negative context, possibly even
     *                            different words, but with same spelling, and thus having uncertain value)
     * @param filters             filters to apply to tweets before searching for n-grams
     * @return map of n-grams and their sentiment values, sentiment values are in [-5, 5]
     */
    public Map<String, Double> createLexicon(DataSetReader dataSetReader, Collection<String> nGrams, double minTotalOccurrences,
                                             double minSentimentValue, Filters filters) {
        Map<String, Counter> counter = countNGramsByPolarity(dataSetReader, nGrams, filters);
        Map<String, Double> lexicon = new HashMap<>();

        final int pos = counter.values().stream().mapToInt(i -> i.numPositive).sum();
        final int neg = counter.values().stream().mapToInt(i -> i.numNegative).sum();
        final double ratio = (double) neg / pos;

        counter.entrySet().stream()
                .filter(entry -> entry.getValue().getTotalOccurrences() > minTotalOccurrences)
                .forEach(entry -> {
                    int over = entry.getValue().numPositive;
                    int under = entry.getValue().numNegative;

                    double sentimentValue = Math.log(ratio * over / under);
                    if (Math.abs(sentimentValue) >= minSentimentValue) {
                        lexicon.put(entry.getKey(), sentimentValue);

                        if (RegexFilters.WHITESPACE.split(entry.getKey()).length == 1 && !ClassifierOptions.isSpecialClassWord(entry.getKey())) {
                            for (String relatedWord : Adjectives.getAdverbAndAdjectives(entry.getKey())) {
                                if (counter.containsKey(relatedWord) && !lexicon.containsKey(relatedWord)) {
                                    lexicon.put(relatedWord, sentimentValue);
                                }
                            }
                        }
                    }
                });

        return MapUtils.normalizeMapBetween(lexicon, -5, 5);
    }


    /**
     * Returns a map of n-gram and the number of times it appeared in positive context and the number of times it
     * appeared in negative context in dataset file.
     *
     * @param dataSetReader Dataset containing tweets and their classification
     * @param nGrams        n-grams to count occurrences for
     * @param filters       filters to apply to tweets in dataset before searching for n-grams
     * @return Map of Counter instances for n-grams in nGrams Collection
     */
    private Map<String, Counter> countNGramsByPolarity(DataSetReader dataSetReader, Collection<String> nGrams, Filters filters) {
        this.dataSetReader = dataSetReader;
        TokenTrie tokenTrie = new TokenTrie(nGrams);

        Map<String, Counter> counter = new HashMap<>();
        Parallel.For(dataSetReader, entry -> {
            String tweet = filters.apply(entry.getTweet());
            List<String> tokens = tokenTrie.findOptimalTokenization(RegexFilters.WHITESPACE.split(tweet));

            for (String nGram : tokens) {
                String[] nGramWords = RegexFilters.WHITESPACE.split(nGram);
                if (containsIllegalWord(nGramWords)) continue;
                if (!counter.containsKey(nGram)) counter.put(nGram, new Counter());

                if (entry.getClassification().isPositive()) {
                    counter.get(nGram).numPositive++;
                } else if (entry.getClassification().isNegative()) {
                    counter.get(nGram).numNegative++;
                }
            }
        });

        return counter;
    }

    private static boolean containsIllegalWord(String[] nGram) {
        return ClassifierOptions.isStopWord(nGram[nGram.length - 1]) || ClassifierOptions.containsIntensifier(nGram);
    }

    public double getProgress() {
        return dataSetReader == null ? 0 : dataSetReader.getProgress();
    }

    private class Counter {
        private int numPositive = 4;
        private int numNegative = 4;

        private int getTotalOccurrences() {
            return numPositive + numNegative;
        }
    }
}
