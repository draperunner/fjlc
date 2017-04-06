from enum import Enum
"""

import com.freva.masteroppgave.preprocessing.filters.Filters;
import com.freva.masteroppgave.utils.progressbar.Progressable;
import com.freva.masteroppgave.utils.reader.DataSetReader.DataSetEntry;

import java.io.File;
import java.io.IOException;
import java.util.Iterator;
import java.util.regex.Pattern;

public class DataSetReader implements Iterator<DataSetEntry>, Iterable<DataSetEntry>, Progressable {
    private static final Pattern tab_regex = Pattern.compile("\t");

    private final LineReader lineReader;
    private final int tweetIndex;
    private final int classIndex;

    public DataSetReader(File file, int tweetIndex, int classIndex) throws IOException {
        lineReader = new LineReader(file);
        this.tweetIndex = tweetIndex;
        this.classIndex = classIndex;
    }

    public boolean hasNext() {
        return lineReader.hasNext();
    }

    public DataSetEntry next() {
        return new DataSetEntry(lineReader.next(), tweetIndex, classIndex);
    }

    public Iterator<DataSetEntry> iterator() {
        return this;
    }

    public double getProgress() {
        return lineReader.getProgress();
    }


    public class DataSetEntry {
        private final Classification classification;
        private String tweet;

        public DataSetEntry(String line, int tweetIndex, int classIndex) {
            String[] values = tab_regex.split(line);
            tweet = values[tweetIndex];
            classification = Classification.parseClassificationFromString(values[classIndex]);
        }


        public String getTweet() {
            return tweet;
        }

        public Classification getClassification() {
            return classification;
        }

        public void applyFilters(Filters filters) {
            tweet = filters.apply(tweet);
        }
    }
"""


class Classification(Enum):
    POSITIVE = 0
    NEUTRAL = 1
    NEGATIVE = 2

    @staticmethod
    def parse_classification_from_string(classification):
        if classification == "positive":
            return Classification.POSITIVE.name
        if classification == "neutral":
            return Classification.NEUTRAL.name
        if classification == "negative":
            return Classification.NEGATIVE.name

    @staticmethod
    def classify_from_thresholds(value, low_thresh, high_thresh):
        if value < low_thresh:
            return Classification.NEGATIVE.name
        elif value > high_thresh:
            return Classification.POSITIVE.name
        return Classification.NEUTRAL.name

    def is_positive(self):
        return self == Classification.POSITIVE

    def is_neutral(self):
        return self == Classification.NEUTRAL

    def is_negative(self):
        return self == Classification.NEGATIVE
