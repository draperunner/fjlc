package com.freva.masteroppgave.statistics;

import com.freva.masteroppgave.utils.reader.DataSetReader.Classification;

import java.util.*;

public class ClassificationThreshold {
    private List<SentimentTuple> previousResults = new ArrayList<>();
    private double lowThreshold;
    private double highThreshold;
    private double maxAccuracy;
    private boolean cacheUpToDate = false;

    public synchronized void updateEvidence(Classification correctClass, double predictedSentiment) {
        previousResults.add(new SentimentTuple(correctClass, predictedSentiment));
        cacheUpToDate = false;
    }


    private void updateThresholds() {
        Collections.sort(previousResults, Collections.reverseOrder());
        int[][] counters = new int[Classification.values().length][previousResults.size()];

        counters[previousResults.get(0).correct.ordinal()][0]++;
        for(int i=1; i<previousResults.size(); i++) {
            for(int j=0; j<counters.length; j++) {
                counters[j][i] = counters[j][i-1];
            }
            counters[previousResults.get(i).correct.ordinal()][i]++;
        }

        for(int i=1; i<previousResults.size()-2; i++) {
            for (int j=i; j<previousResults.size()-1; j++) {
                double tempAccuracy = getAccuracy(counters, i, j);

                if(tempAccuracy > maxAccuracy) {
                    maxAccuracy = tempAccuracy;
                    lowThreshold = (previousResults.get(i-1).predicted + previousResults.get(i).predicted) / 2;
                    highThreshold = (previousResults.get(j).predicted + previousResults.get(j+1).predicted) / 2;
                }
            }
        }

        cacheUpToDate = true;
    }


    /**
     * Calculates optimal lower bound for neutral class. Optimizes based on accuracy.
     * @return Lower bound threshold
     */
    public synchronized double getLowThreshold() {
        if(! cacheUpToDate) updateThresholds();
        return lowThreshold;
    }

    /**
     * Calculates optimal higher bound for neutral class. Optimizes based on accuracy.
     * @return Higher bound threshold
     */
    public synchronized double getHighThreshold() {
        if(! cacheUpToDate) updateThresholds();
        return highThreshold;
    }

    /**
     * Calculates accuracy achieved if the optimal bounds were used.
     * @return Accuracy measure, value within [0, 1]
     */
    public double getMaxAccuracy() {
        return maxAccuracy;
    }


    private double getAccuracy(int[][] counters, int start, int end) {
        int correctNegative = counters[Classification.NEGATIVE.ordinal()][start-1];
        int correctPositive = counters[Classification.POSITIVE.ordinal()][previousResults.size()-1] - counters[Classification.POSITIVE.ordinal()][end+1];
        int correctNeutral = counters[Classification.NEUTRAL.ordinal()][end] - counters[Classification.NEUTRAL.ordinal()][start];

        return (double) (correctNegative+correctNeutral+correctPositive) / previousResults.size();
    }

    private class SentimentTuple implements Comparable<SentimentTuple> {
        private Classification correct;
        private double predicted;

        private SentimentTuple(Classification correct, double predicted) {
            this.correct = correct;
            this.predicted = predicted;
        }

        public int compareTo(SentimentTuple o) {
            double diff = o.predicted - predicted;
            return diff != 0 ? (int) Math.signum(diff) : o.correct.compareTo(correct);
        }
    }
}
