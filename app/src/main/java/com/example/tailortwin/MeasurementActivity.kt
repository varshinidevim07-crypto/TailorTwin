
package com.example.tailortwin

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity

class MeasurementActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_measurement)

        val garment = intent.getStringExtra("GARMENT_TYPE") ?: "blouse"

        val selectedGarment = findViewById<TextView>(R.id.tvSelectedGarment)
        val chest = findViewById<EditText>(R.id.etChest)
        val waist = findViewById<EditText>(R.id.etWaist)
        val hip = findViewById<EditText>(R.id.etHip)
        val length = findViewById<EditText>(R.id.etLength)
        val generateButton = findViewById<Button>(R.id.btnGeneratePattern)

        selectedGarment.text = "Selected garment: ${garment.uppercase()}"

        generateButton.setOnClickListener {

            val chestValue = chest.text.toString().trim()
            val waistValue = waist.text.toString().trim()
            val hipValue = hip.text.toString().trim()
            val lengthValue = length.text.toString().trim()

            when {
                chestValue.isEmpty() -> chest.error = "Enter chest/bust measurement"
                waistValue.isEmpty() -> waist.error = "Enter waist measurement"
                hipValue.isEmpty() -> hip.error = "Enter hip measurement"
                lengthValue.isEmpty() -> length.error = "Enter garment length"

                listOf(chestValue, waistValue, hipValue, lengthValue)
                    .any { it.toDoubleOrNull() == null || it.toDouble() <= 0 } ->
                    Toast.makeText(
                        this,
                        "Enter valid positive measurements",
                        Toast.LENGTH_SHORT
                    ).show()

                else -> {
                    val intent = Intent(this, PatternResultActivity::class.java)
                    intent.putExtra("GARMENT_TYPE", garment)
                    intent.putExtra("CHEST", chestValue)
                    intent.putExtra("WAIST", waistValue)
                    intent.putExtra("HIP", hipValue)
                    intent.putExtra("LENGTH", lengthValue)
                    startActivity(intent)
                }
            }
        }
    }
}
