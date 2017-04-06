package com.freva.masteroppgave;

import com.freva.masteroppgave.classifier.Classifier;
import com.freva.masteroppgave.classifier.ClassifierOptions;
import com.freva.masteroppgave.lexicon.container.PriorPolarityLexicon;
import com.freva.masteroppgave.preprocessing.filters.Filters;
import com.freva.masteroppgave.statistics.ClassificationMetrics;
import com.freva.masteroppgave.statistics.ClassificationOptimizer;
import com.freva.masteroppgave.utils.JSONUtils;
import com.freva.masteroppgave.utils.reader.DataSetReader;
import com.freva.masteroppgave.utils.reader.DataSetReader.DataSetEntry;
import com.freva.masteroppgave.utils.reader.DataSetReader.Classification;
import com.freva.masteroppgave.utils.reader.LineReader;
import com.freva.masteroppgave.utils.tools.Parallel;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import java.util.function.Function;


public class Test {
    public static final List<Function<String, String>> filters = Arrays.asList(
            Filters::HTMLUnescape, Filters::removeUnicodeEmoticons, Filters::normalizeForm, Filters::removeURL,
            Filters::removeRTTag, Filters::removeHashtag, Filters::removeEMail, Filters::removeUsername,
            Filters::removeFreeDigits, Filters::removeInnerWordCharacters, Filters::removeNonAlphanumericalText,
            String::trim, String::toLowerCase);

    public static void main(String[] args) throws IOException {
        ClassifierOptions.loadOptions(new File("res/data/options.pmi.json"));

        DataSetReader dataSetReader = new DataSetReader(new File("res/semeval/2013-2-train-full-B.tsv"), 3, 2);
        List<DataSetEntry> entries = new ArrayList<>();
        dataSetReader.forEach(entries::add);
        entries.forEach(e -> e.applyFilters(LexicalClassifier.CLASSIFIER_FILTERS));
        Classifier classifier = new Classifier(new PriorPolarityLexicon(new File("res/data/lexicon.pmi.json")));

        final long startTime = System.currentTimeMillis();
//        System.out.println(ClassificationOptimizer.optimizeClassifier(classifier, entries));
        ClassificationOptimizer.runOptimizer(entries);
        System.out.println(System.currentTimeMillis() - startTime);


//        generateClassified();
//        checkSuccessThresh();
//        generateClassDistribution();
    }

    public static void generateClassified() throws IOException {
        ClassifierOptions.loadOptions(new File("res/data/options.afinn.json"));
        LineReader lineReader = new LineReader(new File("res/tweets/filtered.txt"));
        PriorPolarityLexicon polarityLexicon = new PriorPolarityLexicon(new File("res/data/lexicon.afinn.json"));
        Classifier classifier = new Classifier(polarityLexicon, LexicalClassifier.CLASSIFIER_FILTERS);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(new File("res/tweets/classified.txt")))) {
            Parallel.For(lineReader, line -> {
                double predictedSentiment = classifier.calculateSentiment(line);

                if (predictedSentiment >= 10 || predictedSentiment <= -8) {
                    try {
                        writer.write((predictedSentiment > 0 ? "positive" : "negative") + "\t" + line + "\n");
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            });
        }
    }


    public static void checkSuccessThresh() throws IOException {
        ClassifierOptions.loadOptions(new File("res/data/options.afinn.json"));
        PriorPolarityLexicon polarityLexicon = new PriorPolarityLexicon(new File("res/data/lexicon.afinn.json"));
        Classifier classifier = new Classifier(polarityLexicon, LexicalClassifier.CLASSIFIER_FILTERS);
        ClassificationMetrics classificationMetrics = new ClassificationMetrics(Classification.values());

        Parallel.For(new DataSetReader(new File("res/semeval/2016-4-test-gold-A.tsv"), 3, 2), entry -> {
            double predictedSentiment = classifier.calculateSentiment(entry.getTweet());

            if (predictedSentiment >= 10 || predictedSentiment <= -8) {
                classificationMetrics.updateEvidence(entry.getClassification(), classifier.classify(entry.getTweet()));
            }
        });

        System.out.println(classificationMetrics.getClassificationReport());
    }


    public static void generateClassDistribution() throws IOException {
        ClassifierOptions.loadOptions(new File("res/data/options.afinn.json"));
        PriorPolarityLexicon polarityLexicon = new PriorPolarityLexicon(new File("res/data/lexicon.afinn.json"));
        Classifier classifier = new Classifier(polarityLexicon, LexicalClassifier.CLASSIFIER_FILTERS);

        HashMap<String, ArrayList<Double>> outcomes = new HashMap<>();
        for (Classification cls : Classification.values()) {
            outcomes.put(cls.name().toLowerCase(), new ArrayList<>());
        }

        for(String dataset: new String[]{"2013-2-test-gold-B", "2014-9-test-gold-B", "2015-10-test-gold-B", "2016-4-test-gold-A"}) {
            for(DataSetEntry entry: new DataSetReader(new File("res/semeval/" + dataset + ".tsv"), 3, 2)){
                double predictedSentiment = classifier.calculateSentiment(entry.getTweet());
                if(Double.isNaN(predictedSentiment)) {
                    System.out.println(entry.getTweet());
                }
                outcomes.get(entry.getClassification().name().toLowerCase()).add(predictedSentiment);
            }
        }

        JSONUtils.toJSONFile(new File("res/tweets/distrib.txt"), outcomes, false);
    }
}
