package fr.r8.launcher

/** État partagé web (CarBridge) / natif / Android Auto. */
object DoorState {
    @Volatile var speedKmh: Int = 0
    @Volatile var doorsOpenCsv: String = ""
}
