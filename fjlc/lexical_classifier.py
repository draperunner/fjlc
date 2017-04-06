from fjlc.preprocessing.filters.filters import Filters
from fjlc.preprocessing.filters.canonical_form import correct_word_via_canonical

CLASSIFIER_STRING_FILTERS = [
    Filters.html_unescape,
    Filters.parse_unicode_emojis_to_alias,
    Filters.normalize_form,
    Filters.remove_url,
    Filters.remove_rt_tag,
    Filters.protect_hashtag,
    Filters.remove_email,
    Filters.remove_username,
    Filters.parse_emoticons,
    Filters.remove_free_digits,
    str.lower
]

CLASSIFIER_CHARACTER_FILTERS = [
    Filters.remove_inner_word_characters,
    Filters.remove_non_syntactical_text,
    correct_word_via_canonical,
]

CLASSIFIER_FILTERS = Filters(CLASSIFIER_STRING_FILTERS, CLASSIFIER_CHARACTER_FILTERS)

TEST_SETS = {
    "2013-TEST": "res/semeval/2013-2-test-gold-B.tsv",
    "2014-TEST": "res/semeval/2014-9-test-gold-B.tsv",
    "2015-TEST": "res/semeval/2015-10-test-gold-B.tsv",
    "2016-TEST": "res/semeval/2016-4-test-gold-A.tsv"
}

"""
    public static void main(String[] args) throws IOException {
        long startTime = System.currentTimeMillis();
        ClassifierOptions.loadOptions(new File("res/data/options.pmi.json"));

        PriorPolarityLexicon priorPolarityLexicon = new PriorPolarityLexicon(new File("res/data/lexicon.pmi.json"));
        Classifier classifier = new Classifier(priorPolarityLexicon, CLASSIFIER_FILTERS);

        ClassificationCollection classificationCollection = new ClassificationCollection(Classification.values());
        for (Map.Entry<String, File> testSet : TEST_SETS.entrySet()) {
            Parallel.For(new DataSetReader(testSet.getValue(), 3, 2), entry -> {
                Classification predicted = classifier.classify(entry.getTweet());
                classificationCollection.updateEvidence(testSet.getKey(), entry.getClassification(), predicted);
            });
        }

        System.out.println(classificationCollection.getShortClassificationReport());
        System.out.println("In: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}

"""
