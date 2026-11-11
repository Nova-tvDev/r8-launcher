package fr.r8.launcher;

import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import java.util.ArrayList;
import java.util.List;

/** 2e source des ouvrants : lit la fenêtre « display door info » de l'appli CarCan
 *  (laisser sur Open dans CarCan) + parse la page infos véhicule (ordinateur de bord).
 *  Dernier état exposé via getDoors() pour la page et l'overlay. */
public class CarText extends AccessibilityService {

    public static volatile String doorsCsv = "";
    public static volatile String obc = "";

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event == null) return;
        CharSequence pkg = event.getPackageName();
        if (pkg == null || !pkg.toString().toLowerCase().contains("carcan")) return;
        AccessibilityNodeInfo root = getRootInActiveWindow();
        if (root == null) return;
        try {
            List<String> texts = new ArrayList<>();
            collect(root, texts);
            parse(texts);
        } finally {
            root.recycle();
        }
    }

    private void collect(AccessibilityNodeInfo n, List<String> out) {
        if (n == null) return;
        CharSequence t = n.getText();
        if (t != null && t.length() > 0 && t.length() < 80) out.add(t.toString());
        for (int i = 0; i < n.getChildCount(); i++) {
            AccessibilityNodeInfo c = n.getChild(i);
            collect(c, out);
            if (c != null) c.recycle();
        }
    }

    private void parse(List<String> texts) {
        String joined = texts.toString().toLowerCase();
        List<String> open = new ArrayList<>();
        // Heuristique : la fenêtre portes CarCan marque l'ouvrant ouvert.
        if (joined.contains("left") || joined.contains("gauche") || joined.contains("avg")) open.add("porte conducteur");
        if (joined.contains("right") || joined.contains("droit") || joined.contains("avd")) open.add("porte passager");
        if (joined.contains("trunk") || joined.contains("coffre") || joined.contains("hood")) open.add("coffre avant");
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < open.size(); i++) {
            if (i > 0) sb.append(",");
            sb.append(open.get(i));
        }
        doorsCsv = sb.toString();
        // Ordinateur de bord : garde les lignes contenant une unité connue.
        StringBuilder obc = new StringBuilder();
        for (String t : texts) {
            String l = t.toLowerCase();
            if (l.contains("km") || l.contains("°c") || l.contains("v") || l.contains("%") || l.contains("l/")) {
                if (obc.length() > 0) obc.append(" | ");
                obc.append(t);
            }
        }
        CarText.obc = obc.toString();
    }

    @Override
    public void onInterrupt() {}
}
