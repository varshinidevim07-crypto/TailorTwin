
package com.example.tailortwin

import android.os.Bundle
import android.widget.Button
import android.content.Intent
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class HomeActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)

        val blouse = findViewById<Button>(R.id.btnBlouse)
        val kurta = findViewById<Button>(R.id.btnKurta)
        val salwar = findViewById<Button>(R.id.btnSalwar)

        blouse.setOnClickListener {
            openGarment("blouse")
        }

        kurta.setOnClickListener {
            openGarment("kurta")
        }

        salwar.setOnClickListener {
            openGarment("salwar")
        }
    }

    private fun openGarment(garment: String) {
        val intent = Intent(this, MeasurementActivity::class.java)
        intent.putExtra("GARMENT_TYPE", garment)
        startActivity(intent)
    }
}
