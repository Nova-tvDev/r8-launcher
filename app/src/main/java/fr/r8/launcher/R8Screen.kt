package fr.r8.launcher

import androidx.car.app.CarContext
import androidx.car.app.Screen
import androidx.car.app.model.Action
import androidx.car.app.model.Pane
import androidx.car.app.model.PaneTemplate
import androidx.car.app.model.Row
import androidx.car.app.model.Template

/** Android Auto : Google impose ses templates — on affiche l'état R8
 *  (ouvrants + vitesse), jamais un launcher complet (interdit). */
class R8Screen(carContext: CarContext) : Screen(carContext) {
    override fun onGetTemplate(): Template {
        val doors = DoorState.doorsOpenCsv
        val status = if (doors.isBlank()) "Tout est fermé — prêt à partir"
        else "Ouvert : $doors"
        val pane = Pane.Builder()
            .addRow(
                Row.Builder()
                    .setTitle("Audi R8")
                    .addText(status)
                    .build()
            )
            .addRow(
                Row.Builder()
                    .setTitle("Vitesse")
                    .addText("${DoorState.speedKmh} km/h")
                    .build()
            )
            .build()
        return PaneTemplate.Builder(pane)
            .setTitle("R8 Launcher")
            .setHeaderAction(Action.BACK)
            .build()
    }
}
