package fr.r8.launcher;

import android.accessibilityservice.AccessibilityService;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Intent;
import android.graphics.PixelFormat;
import android.os.Build;
import android.view.Gravity;
import android.view.WindowManager;
import android.view.accessibility.AccessibilityEvent;
import android.widget.TextView;

/** Service persistant : notification (anti-kill) + petite fenêtre des ouvrants
 *  par-dessus les apps (y compris CarPlay) + alerte si un ouvrant s'ouvre en roulant. */
public class CanWatchService extends AccessibilityService {

    private static final String CH = "r8_watch";
    private TextView overlay;

    @Override
    public void onServiceConnected() {
        startStickyNotification();
    }

    private void startStickyNotification() {
        NotificationManager nm = getSystemService(NotificationManager.class);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            nm.createNotificationChannel(new NotificationChannel(CH, "R8 Launcher", NotificationManager.IMPORTANCE_LOW));
        }
        Notification n = new Notification.Builder(this, CH)
                .setContentTitle("R8 Launcher")
                .setContentText("Surveillance des ouvrants active")
                .setSmallIcon(android.R.drawable.ic_lock_idle_alarm)
                .build();
        startForeground(1, n);
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        // L'état est tenu par CarText (même processus) : on ne fait que rafraîchir l'overlay.
        updateOverlay();
    }

    private void updateOverlay() {
        String doors = CarText.doorsCsv;
        if (doors == null || doors.isEmpty()) {
            removeOverlay();
            return;
        }
        if (overlay == null) {
            overlay = new TextView(this);
            overlay.setTextSize(14);
            overlay.setPadding(24, 16, 24, 16);
            overlay.setBackgroundColor(0xDD3A0D18);
            overlay.setTextColor(0xFFFFFFFF);
            WindowManager.LayoutParams p = new WindowManager.LayoutParams(
                    WindowManager.LayoutParams.WRAP_CONTENT,
                    WindowManager.LayoutParams.WRAP_CONTENT,
                    Build.VERSION.SDK_INT >= Build.VERSION_CODES.O
                            ? WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                            : WindowManager.LayoutParams.TYPE_PHONE,
                    WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                            | WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE,
                    PixelFormat.TRANSLUCENT);
            p.gravity = Gravity.TOP | Gravity.CENTER_HORIZONTAL;
            p.y = 80;
            try {
                ((WindowManager) getSystemService(WINDOW_SERVICE)).addView(overlay, p);
            } catch (Exception e) {
                overlay = null;
                return;
            }
        }
        boolean driving = DoorState.speedKmh > 5;
        overlay.setText((driving ? "⚠️ EN ROULANT — " : "🚪 ") + doors);
    }

    private void removeOverlay() {
        if (overlay != null) {
            try {
                ((WindowManager) getSystemService(WINDOW_SERVICE)).removeView(overlay);
            } catch (Exception ignored) {}
            overlay = null;
        }
    }

    @Override
    public void onInterrupt() {}

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        return START_STICKY;
    }
}
