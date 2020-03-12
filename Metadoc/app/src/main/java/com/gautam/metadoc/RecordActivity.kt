package com.gautam.metadoc

import android.R.attr
import android.app.Activity
import android.content.ActivityNotFoundException
import android.content.Intent
import android.os.Bundle
import android.speech.RecognizerIntent
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_record.*


class RecordActivity : AppCompatActivity() {
    val REQUEST_CODE = 123
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_record)


    }
    fun onClick(v: View?) { //Trigger the RecognizerIntent intent//
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        try {
            startActivityForResult(intent, 123)
        } catch (a: ActivityNotFoundException) {
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        when (requestCode) {
            REQUEST_CODE -> {
                //If RESULT_OK is returned...//
                if (resultCode === Activity.RESULT_OK && null != attr.data) { //...then retrieve the ArrayList//
                    val result: ArrayList<String> = data!!.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
                    //Update our TextView//
                    textOutput.text = result[0]
                }
            }
        }
    }
}
