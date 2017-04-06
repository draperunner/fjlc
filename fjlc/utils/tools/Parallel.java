package com.freva.masteroppgave.utils.tools;

import java.util.Iterator;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Parallel {
    private static final int NUM_CORES = Runtime.getRuntime().availableProcessors();

    /**
     * Executes the for loop in parallel on as many cores as available. The elements are loaded from iterable when
     * needed, and not on load.
     *
     * @param elements  Elements to iterate over
     * @param operation Operation applied to each element
     */
    public static <T> void For(final Iterable<T> elements, final Operation<T> operation) {
        ExecutorService forPool = Executors.newFixedThreadPool(NUM_CORES);

        Iterator<T> iterator = elements.iterator();
        for (int i = 0; i < NUM_CORES; i++) {
            forPool.submit((Runnable) () -> {
                while (true) {
                    T next;
                    synchronized (iterator) {
                        if (!iterator.hasNext()) {
                            return;
                        }
                        next = iterator.next();
                    }
                    operation.perform(next);
                }
            });
        }

        try {
            forPool.shutdown();
            forPool.awaitTermination(10, TimeUnit.DAYS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public interface Operation<T> {
        void perform(T pParameter);
    }
}