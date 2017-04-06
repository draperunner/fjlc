package com.freva.masteroppgave.utils.reader;

import com.freva.masteroppgave.utils.FileUtils;
import com.freva.masteroppgave.utils.progressbar.Progressable;

import java.io.File;
import java.io.IOException;
import java.util.Iterator;
import java.util.Scanner;

public class LineReader implements Iterator<String>, Iterable<String>, Progressable {
    private Scanner scanner;
    private int totalLines = 0;
    private int lineCounter = 0;

    public LineReader(File file) throws IOException {
        this.totalLines = FileUtils.countLines(file);
        this.scanner = new Scanner(file, "UTF-8");
    }

    public boolean hasNext() {
        return scanner.hasNext();
    }

    public String next() {
        lineCounter++;
        return scanner.nextLine();
    }

    public Iterator<String> iterator() {
        return this;
    }

    public double getProgress() {
        return (totalLines == 0 ? 0 : 100.0 * lineCounter / totalLines);
    }
}
