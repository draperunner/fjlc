package com.freva.masteroppgave.preprocessing.preprocessors;

import com.freva.masteroppgave.preprocessing.filters.Filters;
import com.freva.masteroppgave.preprocessing.filters.RegexFilters;
import com.freva.masteroppgave.classifier.ClassifierOptions;
import com.freva.masteroppgave.utils.progressbar.Progressable;
import com.freva.masteroppgave.utils.reader.LineReader;
import com.freva.masteroppgave.utils.tools.Parallel;

import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.concurrent.atomic.AtomicInteger;


public class TweetNGramsPMI implements Progressable {
    private LineReader tweetReader;
    private NGramTree nGramTree;

    /**
     * Finds all frequent (and meaningful) n-grams in a file, treating each new line as a new document.
     *
     * @param input        LineReader initialized on file with documents to generate n-grams for
     * @param n            Maximum n-gram length
     * @param minFrequency Smallest required frequency to include n-gram
     * @param minPMI       Minimum PMI value for n-gram to be included
     * @param filters      List of filters to apply to document before generating n-grams
     * @return Map of n-grams as key and number of occurrences as value
     */
    public final List<String> getFrequentNGrams(LineReader input, int n, double minFrequency, double minPMI, Filters filters) {
        final AtomicInteger lineCounter = new AtomicInteger(0);
        tweetReader = input;
        nGramTree = new NGramTree();

        Parallel.For(tweetReader, tweet -> {
            synchronized (lineCounter) {
                if (lineCounter.incrementAndGet() % 200000 == 0) {
                    nGramTree.pruneInfrequent((int) Math.ceil(minFrequency * lineCounter.intValue() / 2));
                }
            }

            tweet = filters.apply(tweet);
            for (String sentence : RegexFilters.SENTENCE_END_PUNCTUATION.split(tweet)) {
                String[] tokens = RegexFilters.WHITESPACE.split(sentence.trim());
                if (tokens.length == 1) continue;

                for (int i = 0; i < tokens.length; i++) {
                    nGramTree.incrementNGram(Arrays.copyOfRange(tokens, i, Math.min(i + n, tokens.length)));
                }
            }
        });

        return nGramTree.getNGrams((int) (minFrequency * lineCounter.intValue()), minPMI);
    }


    @Override
    public double getProgress() {
        return tweetReader != null ? tweetReader.getProgress() : 0;
    }


    private class NGramTree {
        private Node root = new Node("");

        private synchronized void incrementNGram(String[] nGram) {
            Node current = root;
            current.numOccurrences++;

            for (String word : nGram) {
                if (!current.hasChild(word)) {
                    current.addChild(word);
                }

                current = current.getChild(word);
                current.numOccurrences++;
            }
        }

        private Node getNode(String phrase) {
            Node current = root;
            for (String word : RegexFilters.WHITESPACE.split(phrase)) {
                if (!current.hasChild(word)) {
                    return null;
                }

                current = current.getChild(word);
            }
            return current;
        }

        private void pruneInfrequent(int limit) {
            root.pruneInfrequent(limit);
        }

        private List<String> getNGrams(int limit, double inclusionThreshold) {
            Map<String, Double> allNGrams = new HashMap<>();

            for (Node child : root.children.values()) {
                child.addFrequentPhrases(allNGrams, limit, child.phrase);
            }

            List<String> filteredNGrams = new ArrayList<>();
            for (Map.Entry<String, Double> next : allNGrams.entrySet()) {
                String[] nGramTokens = RegexFilters.WHITESPACE.split(next.getKey());

                if (next.getValue() >= inclusionThreshold &&
                        !ClassifierOptions.containsIntensifier(nGramTokens) &&
                        !ClassifierOptions.isStopWord(nGramTokens[nGramTokens.length - 1])) {
                    filteredNGrams.add(next.getKey());
                }
            }

            return filteredNGrams;
        }
    }


    private class Node {
        private Map<String, Node> children = new HashMap<>();
        private String phrase;
        private int numOccurrences;
        private double logScore = Double.NaN;

        public Node(String phrase) {
            this.phrase = phrase;
        }

        public boolean hasChild(String value) {
            return children.containsKey(value);
        }

        public void addChild(String value) {
            children.put(value, new Node(value));
        }

        public Node getChild(String value) {
            return children.get(value);
        }

        public double getLogScore() {
            if (Double.isNaN(logScore)) logScore = Math.log(numOccurrences);
            return logScore;
        }

        private void pruneInfrequent(int limit) {
            Iterator<Map.Entry<String, Node>> iterator = children.entrySet().iterator();
            while (iterator.hasNext()) {
                Map.Entry<String, Node> child = iterator.next();

                if (child.getValue().numOccurrences < limit) {
                    iterator.remove();
                } else {
                    child.getValue().pruneInfrequent(limit);
                }
            }
        }

        private void addFrequentPhrases(Map<String, Double> map, int limit, String prefix) {
            children.values().stream()
                    .filter(child -> child.numOccurrences >= limit)
                    .forEach(child -> {
                        Node lastWord = nGramTree.getNode(child.phrase);

                        if (lastWord != null && lastWord.numOccurrences >= limit) {
                            double temp = nGramTree.root.getLogScore() + child.getLogScore() - getLogScore() - lastWord.getLogScore();

                            String candidate = prefix + " " + child.phrase;
                            map.put(candidate, temp);
                            child.addFrequentPhrases(map, limit, candidate);
                        }
                    });
        }
    }
}