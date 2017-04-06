package com.freva.masteroppgave.statistics;

import com.freva.masteroppgave.utils.ArrayUtils;

import java.util.*;
import java.util.stream.IntStream;


public class ClassificationMetrics {
    private static final int columnWidth = 13;
    public static final String columnFormat = "%" + columnWidth + "s";
    public static final String numberFormat = "%" + columnWidth + ".4f";

    private final int[][] confusionMatrix;
    private final Enum[] labels;
    private boolean cacheUpToDate = false;

    private final double[] classPrecision;
    private final double[] classRecall;
    private final double[] classF1Score;
    private final int[] classSupport;


    /**
     * Class that generates numerous statistical metrics to judge classification performance.
     * @param yTrue True values
     * @param yPred Predicted values
     */
    public ClassificationMetrics(Enum[] yTrue, Enum[] yPred) {
        this(uniqueLabels(yTrue, yPred));

        for(int i=0; i<yTrue.length; i++) {
            updateEvidence(yTrue[i], yPred[i]);
        }
    }

    public ClassificationMetrics(Enum[] labels) {
        this.labels = labels;
        confusionMatrix = new int[labels.length][labels.length];

        classPrecision = new double[labels.length];
        classRecall = new double[labels.length];
        classF1Score = new double[labels.length];
        classSupport = new int[labels.length];
    }


    /**
     * Adds another result to metric
     * @param yTrue The true result
     * @param yPred The predicted result
     */
    public synchronized void updateEvidence(Enum yTrue, Enum yPred) {
        confusionMatrix[yTrue.ordinal()][yPred.ordinal()]++;
        cacheUpToDate = false;
    }


    /**
     * Calculates classification precision. Precision is defined as ratio of <i>tp / (tp + fp)</i>
     * @return Classification precision, double in range [0, 1]
     */
    public double getPrecision() {
        if(! cacheUpToDate) updateCache();
        return ArrayUtils.dotProduct(classSupport, classPrecision) / ArrayUtils.sum(classSupport);
    }


    /**
     * Calculate classification recall. Recall is defined as ratio of <i>tp / (tp + fn)</i>
     * @return Classification recall, double in range [0, 1]
     */
    public double getRecall() {
        if(! cacheUpToDate) updateCache();
        return ArrayUtils.dotProduct(classSupport, classRecall) / ArrayUtils.sum(classSupport);
    }


    /**
     * Calculates classification F1-Score. F1-Score is defined as ratio of <i>2 * (precision * recall) / (precision + recall)</i>
     * @return Classification F1-Score, double in range[0, 1]
     */
    public double getF1Score() {
        if(! cacheUpToDate) updateCache();
        return ArrayUtils.dotProduct(classSupport, classF1Score) / ArrayUtils.sum(classSupport);
    }


    /**
     * Calculates classification accuracy. Accuracy is defined as <i>(tp + tn) / (tp + tn + fp + fn)</i>
     * @return Classificaion accuracy, double in range [0, 1]
     */
    public double getAccuracy() {
        int correct = IntStream.range(0, labels.length).map(i -> confusionMatrix[i][i]).sum();
        return (double) correct/ArrayUtils.sum(confusionMatrix);
    }


    /**
     * Gets total support
     * @return total class support
     */
    public int getSupport() {
        return ArrayUtils.sum(classSupport);
    }


    /**
     * Returns a pretty formatted table that sums up the classification metrics with Precision, Recall, F1-Score and
     * Support of all the classes, and the overall values
     * @return String with the classification results
     */
    public String getClassificationReport() {
        if(! cacheUpToDate) updateCache();
        String[] headers = {"", "Precision", "Recall", "F1-Score", "Support"};

        StringBuilder sb = new StringBuilder();
        for(String header: headers)
            sb.append(String.format(columnFormat, header));
        sb.append("\n");

        for(int i=0; i<labels.length; i++) {
            sb.append(String.format(columnFormat, labels[i]))
                    .append(String.format(numberFormat, classPrecision[i]))
                    .append(String.format(numberFormat, classRecall[i]))
                    .append(String.format(numberFormat, classF1Score[i]))
                    .append(String.format(columnFormat, classSupport[i])).append("\n");
        }

        sb.append(String.format(columnFormat, "total / avg"))
                .append(String.format(numberFormat, getPrecision()))
                .append(String.format(numberFormat, getRecall()))
                .append(String.format(numberFormat, getF1Score()))
                .append(String.format(columnFormat, getSupport())).append("\n");

        return sb.toString();
    }


    /**
     * Returns a pretty formatted table with normalized confusion matrix and the corresponding labels
     * @return String with normalized confusion matrix
     */
    public String getNormalizedConfusionMatrixReport() {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format(columnFormat, ""));

        for (Object label : labels) {
            sb.append(String.format(columnFormat, label));
        }
        sb.append("\n");

        double[][] confusionMatrix = getPercentageDistributionConfusionMatrix();
        for(int i=0; i<confusionMatrix.length; i++) {
            sb.append(String.format(columnFormat, labels[i]));

            for(int j=0; j<labels.length; j++) {
                sb.append(String.format(numberFormat, confusionMatrix[i][j]));
            }
            sb.append("\n");
        }
        return sb.toString();
    }


    /**
     * Updates the internal cache result for class precision, recall, support and f1-scores.
     */
    private void updateCache() {
        for(int i=0; i<labels.length; i++) {
            classSupport[i] = ArrayUtils.sumRow(confusionMatrix, i);
            classRecall[i] = (double) confusionMatrix[i][i] / classSupport[i];
            classPrecision[i] = (double) confusionMatrix[i][i] / ArrayUtils.sumColumn(confusionMatrix, i);
            classF1Score[i] = 2 * classPrecision[i] * classRecall[i] / (classPrecision[i] + classRecall[i]);
        }
        cacheUpToDate = true;
    }


    private double[][] getPercentageDistributionConfusionMatrix() {
        double[][] normalized = new double[labels.length][labels.length];
        int total = Arrays.stream(confusionMatrix).mapToInt(row -> Arrays.stream(row).sum()).sum();

        for(int i=0; i<labels.length; i++) {
            for(int j=0; j<labels.length; j++) {
                normalized[i][j] = (double) confusionMatrix[i][j]/total;
            }
        }
        return normalized;
    }


    private static Enum[] uniqueLabels(Enum[] yTrue, Enum[] yPred) {
        if(yTrue.length != yPred.length) throw new IllegalArgumentException("yTrue and yPred of different lengths!");
        Set<Enum> set = new HashSet<>();

        for(int i=0; i<yTrue.length; i++) {
            if(! set.contains(yTrue[i])) {
                set.add(yTrue[i]);
            }

            if(! set.contains(yPred[i])) {
                set.add(yPred[i]);
            }
        }

        Enum[] labels = (Enum[]) set.toArray();
        Arrays.sort(labels);

        return labels;
    }
}