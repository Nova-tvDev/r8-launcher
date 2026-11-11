package fr.r8.launcher;

import android.content.Context;
import android.os.Handler;
import android.os.Looper;
import android.webkit.JavascriptInterface;
import java.lang.reflect.Method;
import java.util.LinkedHashMap;
import java.util.Map;

/** Pont JS → natif : lit les propriétés système Junsun « hcn » (portes, clignos, vitesse).
 *  Appels JS : CanBridge.poll() → "avg:0;avd:0;frunk:0;tl:0;tr:0;speed:0"
 *              CarBridge.setState(vitesse, "porte conducteur") depuis la page (état partagé). */
public class CanBridge {
    private final Context ctx;
    private final Handler ui = new Handler(Looper.getMainLooper());

    /** Clés lues en premier, puis secours si le firmware les nomme autrement. */
    private static final Map<String, String[]> PROP_FALLBACKS = new LinkedHashMap<>();
    static {
        PROP_FALLBACKS.put("hcn.door.fl", new String[]{"hcn.door.fl", "persist.hcn.door.fl"});
        PROP_FALLBACKS.put("hcn.door.fr", new String[]{"hcn.door.fr", "persist.hcn.door.fr"});
        // R8 : pas de portes arrière — restent à 0.
        PROP_FALLBACKS.put("hcn.door.trunk", new String[]{"hcn.door.trunk", "hcn.door.luggage"});
        PROP_FALLBACKS.put("hcn.light.turn_l", new String[]{"hcn.light.turn_l"});
        PROP_FALLBACKS.put("hcn.light.turn_r", new String[]{"hcn.light.turn_r"});
        PROP_FALLBACKS.put("hcn.car.speed", new String[]{"hcn.car.speed"});
    }

    public CanBridge(Context ctx) { this.ctx = ctx.getApplicationContext(); }

    public static String sysProp(String key, String def) {
        try {
            Class<?> sp = Class.forName("android.os.SystemProperties");
            Method get = sp.getMethod("get", String.class, String.class);
            return (String) get.invoke(null, key, def);
        } catch (Exception e) {
            return def;
        }
    }

    private static String firstOf(String[] keys, String def) {
        for (String k : keys) {
            String v = sysProp(k, "");
            if (!v.isEmpty()) return v;
        }
        return def;
    }

    @JavascriptInterface
    public String poll() {
        String fl = firstOf(PROP_FALLBACKS.get("hcn.door.fl"), "0");
        String fr = firstOf(PROP_FALLBACKS.get("hcn.door.fr"), "0");
        String trunk = firstOf(PROP_FALLBACKS.get("hcn.door.trunk"), "0");
        String tl = firstOf(PROP_FALLBACKS.get("hcn.light.turn_l"), "0");
        String tr = firstOf(PROP_FALLBACKS.get("hcn.light.turn_r"), "0");
        String speed = firstOf(PROP_FALLBACKS.get("hcn.car.speed"), "0");
        return "avg:" + fl + ";avd:" + fr + ";frunk:" + trunk
                + ";tl:" + tl + ";tr:" + tr + ";speed:" + speed;
    }

    @JavascriptInterface
    public void setState(int speedKmh, String doorsOpenCsv) {
        DoorState.speedKmh = speedKmh;
        DoorState.doorsOpenCsv = doorsOpenCsv == null ? "" : doorsOpenCsv;
    }
}
