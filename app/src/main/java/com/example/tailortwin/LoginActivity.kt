
package com.example.tailortwin

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class LoginActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        val email = findViewById<EditText>(R.id.etEmail)
        val password = findViewById<EditText>(R.id.etPassword)
        val loginButton = findViewById<Button>(R.id.btnLogin)
        val signUp = findViewById<TextView>(R.id.tvCreateAccount)
        val forgotPassword = findViewById<TextView>(R.id.tvForgotPassword)

        loginButton.setOnClickListener {
            val enteredEmail = email.text.toString().trim()
            val enteredPassword = password.text.toString()

            when {
                enteredEmail.isEmpty() ->
                    email.error = "Enter your email"

                !android.util.Patterns.EMAIL_ADDRESS.matcher(enteredEmail).matches() ->
                    email.error = "Enter a valid email"

                enteredPassword.isEmpty() ->
                    password.error = "Enter your password"

                else -> {
                    Toast.makeText(
                        this,
                        "Login successful (demo only)",
                        Toast.LENGTH_SHORT
                    ).show()

                    startActivity(Intent(this, HomeActivity::class.java))
                }
            }
        }

        signUp.setOnClickListener {
            startActivity(Intent(this, RegisterActivity::class.java))
        }

        forgotPassword.setOnClickListener {
            Toast.makeText(
                this,
                "Password recovery will be connected later.",
                Toast.LENGTH_SHORT
            ).show()
        }
    }
}
