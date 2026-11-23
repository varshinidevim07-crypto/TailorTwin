
package com.example.tailortwin

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class PatternResultActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_pattern_result)

        val garment = intent.getStringExtra("GARMENT_TYPE") ?: "blouse"
        val chest = intent.getStringExtra("CHEST") ?: "-"
        val waist = intent.getStringExtra("WAIST") ?: "-"
        val hip = intent.getStringExtra("HIP") ?: "-"
        val length = intent.getStringExtra("LENGTH") ?: "-"

        val garmentText = findViewById<TextView>(R.id.tvResultGarment)
        val measurementsText = findViewById<TextView>(R.id.tvResultMeasurements)
        val statusText = findViewById<TextView>(R.id.tvPatternStatus)
        val homeButton = findViewById<Button>(R.id.btnBackHome)

        garmentText.text = "Garment: ${garment.uppercase()}"

        measurementsText.text = """
            Chest / Bust: $chest inches
            Waist: $waist inches
            Hip: $hip inches
            Length: $length inches
        """.trimIndent()

        statusText.text =
            "Measurements received successfully.\nConnect the backend to generate the actual stitching pattern."

        homeButton.setOnClickListener {
            val intent = Intent(this, HomeActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_CLEAR_TOP
            startActivity(intent)
            finish()
        }
    }
}
