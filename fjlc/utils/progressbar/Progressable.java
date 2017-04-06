package com.freva.masteroppgave.utils.progressbar;

public interface Progressable {
    /**
     * Returns percentage progress of current task. ProgressBar will continue to poll until getProgress returns 100.
     *
     * @return Number [0-100] corresponding to current progress
     */
    double getProgress();
}
