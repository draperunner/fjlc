package com.freva.masteroppgave.utils;

import java.util.Arrays;

public class ArrayUtils {
    /**
     * Calculates numerical sum of elements in array.
     *
     * @param array Array to calculate sum of
     * @return Sum of values in array
     */
    public static int sum(int[] array) {
        return Arrays.stream(array).sum();
    }


    /**
     * Calculates sum of 2d array.
     *
     * @param array Array to calculate sum of
     * @return Sum of values in array
     */
    public static int sum(int[][] array) {
        return Arrays.stream(array).mapToInt(ArrayUtils::sum).sum();
    }


    /**
     * Calculates sum of all values in i'th column
     *
     * @param array  Array to calculate column sum of
     * @param column Column to calculate sum of
     * @return Sum of values in column
     */
    public static int sumColumn(int[][] array, int column) {
        return Arrays.stream(array).mapToInt(row -> row[column]).sum();
    }


    /**
     * Calculates sum of all values in i'th row
     *
     * @param array Array to calculate row sum of
     * @param row   Row to calculate sum of
     * @return Sum of values in row
     */
    public static int sumRow(int[][] array, int row) {
        return sum(array[row]);
    }


    /**
     * Performs vector dot-product
     *
     * @param a Vector
     * @param b Vector
     * @return Dot product of a and b
     */
    public static double dotProduct(double[] a, double[] b) {
        double sum = 0;
        for (int i = 0; i < a.length; i++) {
            if (a[i] * b[i] == 0) continue;
            sum += a[i] * b[i];
        }
        return sum;
    }


    /**
     * Performs vector dot-product
     *
     * @param a Vector
     * @param b Vector
     * @return Dot product of a and b
     */
    public static double dotProduct(int[] a, double[] b) {
        double sum = 0;
        for (int i = 0; i < a.length; i++) {
            if (a[i] * b[i] == 0) continue;
            sum += a[i] * b[i];
        }
        return sum;
    }
}
