
package com.example.tailortwin

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class RegisterActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        val name = findViewById<EditText>(R.id.etName)
        val email = findViewById<EditText>(R.id.etRegisterEmail)
        val phone = findViewById<EditText>(R.id.etPhone)
        val password = findViewById<EditText>(R.id.etRegisterPassword)
        val confirmPassword = findViewById<EditText>(R.id.etConfirmPassword)

        val registerButton = findViewById<Button>(R.id.btnRegister)
        val loginText = findViewById<TextView>(R.id.tvAlreadyAccount)

        registerButton.setOnClickListener {

            val enteredName = name.text.toString().trim()
            val enteredEmail = email.text.toString().trim()
            val enteredPhone = phone.text.toString().trim()
            val enteredPassword = password.text.toString()
            val enteredConfirmPassword = confirmPassword.text.toString()

            when {
                enteredName.isEmpty() ->
                    name.error = "Enter your name"

                !android.util.Patterns.EMAIL_ADDRESS.matcher(enteredEmail).matches() ->
                    email.error = "Enter a valid email"

                enteredPhone.length != 10 || !enteredPhone.all { it.isDigit() } ->
                    phone.error = "Enter a valid 10-digit phone number"

                enteredPassword.length < 6 ->
                    password.error = "Password must have at least 6 characters"

                enteredPassword != enteredConfirmPassword ->
                    confirmPassword.error = "Passwords do not match"

                else -> {
                    Toast.makeText(
                        this,
                        "Registration form validated! Please login.",
                        Toast.LENGTH_SHORT
                    ).show()

                    startActivity(Intent(this, LoginActivity::class.java))
                    finish()
                }
            }
        }

        loginText.setOnClickListener {
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
        }
    }
}
