package com.gautam.metadoc

import android.content.pm.PackageManager
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import kotlinx.android.synthetic.main.activity_record.*

class RecordActivity : AppCompatActivity() {

    private lateinit var speechRecognizerViewModel: SpeechRecognizerViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_record)
        micButton = findViewById<Button>(R.id.mic_button).apply {
            setOnClickListener(micClickListener)
        }

        setupSpeechViewModel()
    }

    private val micClickListener = View.OnClickListener {
        if (!speechRecognizerViewModel.permissionToRecordAudio) {
            ActivityCompat.requestPermissions(this, )
            return@OnClickListener
        }

        if (speechRecognizerViewModel.isListening) {
            speechRecognizerViewModel.stopListening()
        } else {
            speechRecognizerViewModel.startListening()
        }
    }

    private fun setupSpeechViewModel() {
        speechRecognizerViewModel = ViewModelProviders.of(this).get(SpeechRecognizerViewModel::class.java)
        speechRecognizerViewModel.getViewState().observe(this, Observer<SpeechRecognizerViewModel.ViewState> { viewState ->
            render(viewState)
        })
    }

    private fun render(uiOutput: SpeechRecognizerViewModel.ViewState?) {
        if (uiOutput == null) return

        textField.text = uiOutput.spokenText

    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)

        if (requestCode == REQUEST_RECORD_AUDIO_PERMISSION) {
            speechRecognizerViewModel.permissionToRecordAudio = grantResults[0] == PackageManager.PERMISSION_GRANTED
        }

        if (speechRecognizerViewModel.permissionToRecordAudio) {
            micButton.performClick()
        }
    }
}
