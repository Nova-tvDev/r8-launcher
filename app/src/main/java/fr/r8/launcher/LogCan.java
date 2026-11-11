package fr.r8.launcher;

import android.content.Context;
import android.webkit.JavascriptInterface;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/** Journal de diagnostic : LogCan.log("…") depuis la page → r8_diag.txt.
 *  Réglages › Diagnostic CAN : Vider / Exporter (le chemin s'affiche en bas d'écran). */
public class LogCan {
    private final File logFile;
    private final SimpleDateFormat fmt = new SimpleDateFormat("HH:mm:ss", Locale.FRANCE);

    public LogCan(Context ctx) {
        File dir = ctx.getExternalFilesDir(null);
        logFile = new File(dir, "r8_diag.txt");
    }

    @JavascriptInterface
    public synchronized void log(String line) {
        try (FileWriter w = new FileWriter(logFile, true)) {
            w.write(fmt.format(new Date()) + " " + line + "\n");
        } catch (IOException ignored) {}
    }

    @JavascriptInterface
    public synchronized void clear() {
        try (FileWriter w = new FileWriter(logFile, false)) {
        } catch (IOException ignored) {}
    }

    @JavascriptInterface
    public String path() {
        return logFile.getAbsolutePath();
    }
}
