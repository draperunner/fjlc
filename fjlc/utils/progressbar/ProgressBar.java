package com.freva.masteroppgave.utils.progressbar;

public class ProgressBar implements Runnable {
    private static final String fullProgress = "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||";
    private static final String noProgress = "----------------------------------------------------------------------------------------------------";
    private static final String format = "%02d:%02d";
    private static final int updateResolution = 1000;

    private static final Object lock = new Object();
    private static String currentThread = null;

    private final Progressable progressable;
    private final String taskName;
    private final long taskStart;

    private ProgressBar(Progressable progressable, String taskName) {
        this.taskStart = System.currentTimeMillis();
        this.progressable = progressable;
        this.taskName = taskName;
    }


    /**
     * Class that regularly checks progress of a Progressable and prints it in a nicely formatted ASCII progress bar
     *
     * @param progressable Instance that implements Progressable interface
     * @param taskName     Name of the task, is printed right before the progress bar
     */
    public static void trackProgress(Progressable progressable, String taskName) {
        synchronized (lock) {
            while (currentThread != null) {
                try {
                    lock.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            currentThread = Thread.currentThread().getName();
        }
        new Thread(new ProgressBar(progressable, taskName)).start();
    }

    private String getProgress(double perc) {
        long secondsElapsed = (System.currentTimeMillis() - taskStart) / 1000;
        String timeElapsed = convertSeconds(secondsElapsed);
        String timeRemaining = perc != 0 ? convertSeconds((long) ((100 - perc) * secondsElapsed / perc)) : "Infin";
        String progress = getProgressBar(perc) + " Elapsed: " + timeElapsed + " | Remaining: " + timeRemaining;

        return "\r" + progress;
    }

    private static String getProgressBar(double percent) {
        String bar = fullProgress.substring(0, (int) percent) + noProgress.substring((int) percent);
        String status = (percent >= 100 ? "Finish" : String.format("%05.2f%%", percent));
        return "[" + bar.substring(0, 46) + " " + status + " " + bar.substring(54) + "]";
    }

    private static String convertSeconds(long seconds) {
        long sec = seconds % 60;
        long min = seconds / 60;
        return String.format(format, min, sec);
    }

    @Override
    public void run() {
        System.out.println(taskName);
        double progress;
        while ((progress = progressable.getProgress()) < 100) {
            System.out.print(getProgress(progress));
            try {
                Thread.sleep(updateResolution);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        System.out.println(getProgress(progress) + "\n");

        synchronized (lock) {
            currentThread = null;
            lock.notifyAll();
        }
    }
}
