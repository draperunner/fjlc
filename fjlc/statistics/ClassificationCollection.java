package com.freva.masteroppgave.statistics;

import java.util.LinkedHashMap;
import java.util.Map;

public class ClassificationCollection {
    private Map<String, ClassificationMetrics> classifications = new LinkedHashMap<>();
    private Enum[] labels;

    public ClassificationCollection(Enum[] labels) {
        this.labels = labels;
    }

    public synchronized void updateEvidence(String dataset, Enum yTrue, Enum yPred) {
        if (!classifications.containsKey(dataset)) {
            classifications.put(dataset, new ClassificationMetrics(labels));
        }

        classifications.get(dataset).updateEvidence(yTrue, yPred);
    }

    public String getShortClassificationReport() {
        StringBuilder sb = new StringBuilder();
        String[] columns = {"Testset", "Precision", "Recall", "F1-Score", "Accuracy", "Support"};

        for(String column : columns) {
            sb.append(String.format(ClassificationMetrics.columnFormat, column));
        }

        double weightedPrecision = 0, weightedRecall = 0, weightedF1Score = 0, weightedAccuracy = 0;
        int totalSupport = 0;
        for(Map.Entry<String, ClassificationMetrics> entry : classifications.entrySet()) {
            sb.append("\n").append(String.format(ClassificationMetrics.columnFormat, entry.getKey()))
                    .append(String.format(ClassificationMetrics.numberFormat, entry.getValue().getPrecision()))
                    .append(String.format(ClassificationMetrics.numberFormat, entry.getValue().getRecall()))
                    .append(String.format(ClassificationMetrics.numberFormat, entry.getValue().getF1Score()))
                    .append(String.format(ClassificationMetrics.numberFormat, entry.getValue().getAccuracy()))
                    .append(String.format(ClassificationMetrics.columnFormat, entry.getValue().getSupport()));

            weightedPrecision += entry.getValue().getPrecision() * entry.getValue().getSupport();
            weightedRecall += entry.getValue().getRecall() * entry.getValue().getSupport();
            weightedF1Score += entry.getValue().getF1Score() * entry.getValue().getSupport();
            weightedAccuracy += entry.getValue().getAccuracy() * entry.getValue().getSupport();
            totalSupport += entry.getValue().getSupport();
        }

        sb.append("\n").append(String.format(ClassificationMetrics.columnFormat, "Weighted avg:"))
                .append(String.format(ClassificationMetrics.numberFormat, weightedPrecision/totalSupport))
                .append(String.format(ClassificationMetrics.numberFormat, weightedRecall/totalSupport))
                .append(String.format(ClassificationMetrics.numberFormat, weightedF1Score/totalSupport))
                .append(String.format(ClassificationMetrics.numberFormat, weightedAccuracy/totalSupport))
                .append(String.format(ClassificationMetrics.columnFormat, totalSupport)).append("\n");

        return sb.toString();
    }
}