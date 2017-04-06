package com.freva.masteroppgave.preprocessing.preprocessors;

import com.freva.masteroppgave.preprocessing.filters.Filters;
import com.freva.masteroppgave.preprocessing.filters.RegexFilters;
import com.freva.masteroppgave.utils.MapUtils;
import com.freva.masteroppgave.utils.progressbar.Progressable;
import com.freva.masteroppgave.utils.reader.LineReader;

import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;

public class CanonicalDictionary implements Progressable {
    public static final List<Function<String, String>> filters = Arrays.asList(
            Filters::HTMLUnescape, Filters::removeUnicodeEmoticons, Filters::normalizeForm, Filters::removeURL,
            Filters::removeRTTag, Filters::removeHashtag, Filters::removeUsername, Filters::removeEmoticons,
            Filters::removeInnerWordCharacters, Filters::removeNonAlphanumericalText, Filters::removeFreeDigits,
            String::trim, String::toLowerCase);
    private LineReader tweetReader;

    /**
     * Creates canonical dictionary:
     * Words that are reduced to the same canonical form are grouped together, the frequent words are kept in the final
     * dictionary. F.ex. "god" => ["good", "god"].
     *
     * @param tweetReader LineReader with words to base dictionary off
     */
    public Map<String, Set<String>> createCanonicalDictionary(LineReader tweetReader, double correctFrequency, double termFrequency) {
        this.tweetReader = tweetReader;

        int iteration = 0;
        Map<String, Map<String, Integer>> counter = new HashMap<>();
        for (String tweet : tweetReader) {
            if (iteration++ % 100000 == 0)
                removeInfrequent(counter, (int) (iteration * termFrequency / 2), correctFrequency / 2);

            tweet = Filters.stringChain(tweet, filters);
            for (String word : RegexFilters.WHITESPACE.split(tweet)) {
                String reduced = Filters.removeRepeatingCharacters(word);
                if (!counter.containsKey(reduced)) {
                    counter.put(reduced, new HashMap<>());
                }

                MapUtils.incrementMapByValue(counter.get(reduced), word, 1);
            }
        }

        removeInfrequent(counter, (int) (iteration * termFrequency), correctFrequency);
        return counter.entrySet().stream().collect(Collectors.toMap(Map.Entry::getKey, e -> e.getValue().keySet()));
    }

    private static void removeInfrequent(Map<String, Map<String, Integer>> counter, int termLimit, double cutoff) {
        Iterator<Map.Entry<String, Map<String, Integer>>> canonicals = counter.entrySet().iterator();

        while (canonicals.hasNext()) {
            Map.Entry<String, Map<String, Integer>> canonical = canonicals.next();
            int termCounter = canonical.getValue().values().stream().mapToInt(Integer::intValue).sum();

            if (canonical.getValue().size() < 5 || termCounter <= termLimit) {
                canonicals.remove();
                continue;
            }

            Iterator<Map.Entry<String, Integer>> originals = canonical.getValue().entrySet().iterator();
            while (originals.hasNext()) {
                if (originals.next().getValue() < termCounter * cutoff) {
                    originals.remove();
                }
            }
        }
    }

    public double getProgress() {
        return tweetReader != null ? tweetReader.getProgress() : 0;
    }
}
