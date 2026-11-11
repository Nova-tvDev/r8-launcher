package fr.r8.launcher

import android.content.Intent
import androidx.car.app.Screen
import androidx.car.app.Session

class R8Session : Session() {
    override fun onCreateScreen(intent: Intent): Screen = R8Screen(carContext)
}
