package com.freva.masteroppgave.statistics;

import com.freva.masteroppgave.lexicon.LexiconCreator;
import com.freva.masteroppgave.Main;
import com.freva.masteroppgave.classifier.Classifier;
import com.freva.masteroppgave.classifier.ClassifierOptions;
import com.freva.masteroppgave.lexicon.container.PriorPolarityLexicon;
import com.freva.masteroppgave.utils.reader.DataSetReader;
import com.freva.masteroppgave.utils.reader.DataSetReader.Classification;
import com.freva.masteroppgave.utils.reader.DataSetReader.DataSetEntry;
import com.freva.masteroppgave.utils.reader.LineReader;
import com.freva.masteroppgave.utils.tools.Parallel;

import java.io.File;
import java.io.IOException;
import java.util.*;
import java.util.Map.Entry;
import java.util.stream.Collectors;

public class ClassificationOptimizer {
    private static final Map<ClassifierOptions.Variable, double[]> variableValues = new HashMap<>();
    private static final LexiconCreator creator = new LexiconCreator();
    private static final Map<String, double[]> nGrams = new HashMap<>();

    private static final double[][] lexiconVariables = {{5, 6}, //n
            {0.000005, 0.0000075}, //frequencyCutoff
            {3, 3.25, 3.5, 3.75, 4}, //minPMI
            {300, 250, 200, 150, 100}, //minTotalOccurrences
            {1.75, 2, 2.25, 2.5}}; //minSentiment
    private static final double[] bestValues = {lexiconVariables[0][0], lexiconVariables[1][0], lexiconVariables[2][0],
            lexiconVariables[3][0], lexiconVariables[4][0]};


    static {
        try {
            for(String line : new LineReader(new File("res/tweets/out.txt"))) {
                String[] values = line.split("\t");
                nGrams.put(values[2], new double[]{Double.parseDouble(values[0]), Double.parseDouble(values[1])});
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        variableValues.put(ClassifierOptions.Variable.NEGATION_VALUE, new double[]{1.2, 1.3, 1.4, 1.5});
        variableValues.put(ClassifierOptions.Variable.EXCLAMATION_INTENSIFIER, new double[]{2.0, 2.5, 2.75, 3.0, 3.25, 3.5});
        variableValues.put(ClassifierOptions.Variable.QUESTION_INTENSIFIER, new double[]{0.3, 0.5, 0.7, 0.9, 1.0});
        variableValues.put(ClassifierOptions.Variable.NEGATION_SCOPE_LENGTH, new double[]{3, 4, 5});
        variableValues.put(ClassifierOptions.Variable.AMPLIFIER_SCALAR, new double[]{2, 2.5, 3, 3.5, 4});
        variableValues.put(ClassifierOptions.Variable.DOWNTONER_SCALAR, new double[]{0.4, 0.6, 0.8, 0.9, 1, 1.1});
    }

    public static void runOptimizer(List<DataSetEntry> entries) throws IOException {
        Set<String> checked = new HashSet<>();
        int numChangedVariables;
        double bestScore = 0;
        do {
            numChangedVariables = 0;
            for(int i=0; i<lexiconVariables.length; i++) {
                double bestValue = bestValues[i];

                for(int index = 0; index < lexiconVariables[i].length; index++) {
                    bestValues[i] = lexiconVariables[i][index];
                    String check = Arrays.toString(bestValues);
                    if (! checked.contains(check)) {
                        Classifier classifier = new Classifier(new PriorPolarityLexicon(generateLexicon((int) bestValues[0], bestValues[1], bestValues[2], bestValues[3], bestValues[4])));
                        Entry<Map<String, Double>, Double> optimized = optimizeClassifier(classifier, entries);

                        System.out.println(optimized.getValue() + " | " + Arrays.toString(bestValues) + " | " + optimized.getKey());
                        if (optimized.getValue() > bestScore) {
                            bestValue = lexiconVariables[i][index];
                            bestScore = optimized.getValue();
                            numChangedVariables++;
                            System.out.println("new best");
                        }
                        checked.add(check);
                    }
                }

                bestValues[i] = bestValue;
            }
        } while(numChangedVariables != 0);
    }

    public static Entry<Map<String, Double>, Double> optimizeClassifier(Classifier classifier, List<DataSetEntry> entries) throws IOException {
        int numChangedVariables;
        Map<String, Double> bestOptions = null;
        double bestScore = 0;
        do {
            numChangedVariables = 0;
            for (ClassifierOptions.Variable variable : variableValues.keySet()) {
                double bestValue = ClassifierOptions.getVariable(variable);

                for (double value : variableValues.get(variable)) {
                    ClassifierOptions.setVariable(variable, value);
                    final double score = calculateScore(classifier, entries);

                    if (score > bestScore) {
                        bestScore = score;
                        bestValue = value;
                        bestOptions = ClassifierOptions.getOptions();
                        numChangedVariables++;
                    }
                }

                ClassifierOptions.setVariable(variable, bestValue);
            }
        } while (numChangedVariables > 0);

        return new AbstractMap.SimpleEntry<>(bestOptions, bestScore);
    }

    private static Map<String, Double> generateLexicon(int n, double frequencyCutoff, double minPMI, double minTotalOccurrences, double minSentiment) throws IOException {
        final int nubOccurrences = (int) (103895935 * frequencyCutoff);
        List<String> filteredNGrams = nGrams.entrySet().stream()
                .filter(e -> e.getValue()[0] >= nubOccurrences && e.getValue()[1] >= minPMI && e.getKey().split(" ").length <= n)
                .map(Map.Entry::getKey).collect(Collectors.toList());

        DataSetReader dataset = new DataSetReader(new File("res/tweets/classified.txt"), 1, 0);
        return creator.createLexicon(dataset, filteredNGrams, minTotalOccurrences, minSentiment, Main.TWEET_FILTERS);
    }

    private static double calculateScore(Classifier classifier, List<DataSetEntry> entries) {
        ClassificationThreshold threshold = new ClassificationThreshold();
        Parallel.For(entries, entry -> {
            double predictedSentiment = classifier.calculateSentiment(entry.getTweet());
            threshold.updateEvidence(entry.getClassification(), predictedSentiment);
        });
        ClassifierOptions.setVariable(ClassifierOptions.Variable.CLASSIFICATION_THRESHOLD_LOWER, threshold.getLowThreshold());
        ClassifierOptions.setVariable(ClassifierOptions.Variable.CLASSIFICATION_THRESHOLD_HIGHER, threshold.getHighThreshold());

        ClassificationMetrics classificationMetrics = new ClassificationMetrics(Classification.values());
        Parallel.For(entries, entry -> {
            Classification predicted = classifier.classify(entry.getTweet());
            classificationMetrics.updateEvidence(entry.getClassification(), predicted);
        });

        return classificationMetrics.getF1Score();
    }
}
