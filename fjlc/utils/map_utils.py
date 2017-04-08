def sort_map_by_value(dictionary):
    """
    Sorts Map by value. Map values must implement Comparable.
    
    :param dictionary: Map to sort 
    :return: Sorted map 
    """
    return sorted(dictionary, key=dictionary.get)


def normalize_map_between(dictionary, norm_min, norm_max):
    """
    Performs linear normalization of all values in Map between normMin and normMax

    :param: map     Map to normalize values for
    :param: normMin Smallest normalized value
    :param: normMax Largest normalized value
    :return: A new map with double values within [normMin, normMax]
    """
    if len(dictionary) < 2:
        return {}

    values = list(dictionary.values())

    norm_range = norm_max - norm_min
    map_min = min(values)
    map_range = max(values) - map_min
    range_factor = norm_range / float(map_range)

    normalized_map = {}
    for key, value in dictionary.items():
        normalized_map[key] = norm_min + (value - map_min) * range_factor

    return normalized_map

"""
    /**
     * Sorts map given a comparator
     *
     * @param map        Map to sort
     * @param comparator Comparator used to sort elements
     * @return Sorted map
     */
    public static <K, V> Map<K, V> sortMapWithComparator(Map<K, V> map, Comparator<Map.Entry<K, V>> comparator) {
        LinkedList<Map.Entry<K, V>> list = new LinkedList<>(map.entrySet());
        Collections.sort(list, comparator);

        Map<K, V> sortedHashMap = new LinkedHashMap<>();
        for (Map.Entry<K, V> entry : list) {
            sortedHashMap.put(entry.getKey(), entry.getValue());
        }

        return sortedHashMap;
    }


    /**
     * Increments value of key by increment if present in the list, otherwise initializes the value to increment.
     *
     * @param map       Map to increment key for
     * @param key       Key to increment
     * @param increment Value to increment by
     */
    public synchronized static <T> void incrementMapByValue(Map<T, Integer> map, T key, int increment) {
        map.put(key, map.getOrDefault(key, 0) + increment);
    }


    /**
     * Removes elements from map that are strictly smaller than the threshold element
     *
     * @param map    Map to remove items from
     * @param thresh Threshold element
     */
    public static <K, V extends Comparable<V>> void removeInfrequentItems(Map<K, V> map, V thresh) {
        Iterator<Map.Entry<K, V>> iter = map.entrySet().iterator();
        while (iter.hasNext()) {
            Map.Entry<K, V> entry = iter.next();
            if (entry.getValue().compareTo(thresh) < 0) {
                iter.remove();
            }
        }
    }

    /**
     * Extracts the map entries with key values found in the toExtract set
     *
     * @param map       Map to extract items from
     * @param toExtract The key values
     */
    public static <K, V> Map<K, V> extractItems(Map<K, V> map, Set<K> toExtract) {
        Map<K, V> extractedItems = new HashMap<>();
        toExtract.stream().filter(map::containsKey).forEach(key -> extractedItems.put(key, map.get(key)));
        return extractedItems;
    }

    /**
     * Merges two maps into a new map
     *
     * @param map1 Map to merge
     * @param map2 Map to merge
     */
    public static <K, V> Map<K, V> mergeMaps(Map<K, V> map1, Map<K, V> map2) {
        Map<K, V> mergedMap = new HashMap<>();
        mergedMap.putAll(map1);
        mergedMap.putAll(map2);
        return mergedMap;
    }
}
"""
