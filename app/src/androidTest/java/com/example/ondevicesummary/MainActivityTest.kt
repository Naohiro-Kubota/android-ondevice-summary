package com.example.ondevicesummary

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class MainActivityTest {
    @get:Rule val composeRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun ordinaryLaunchShowsSharingInstructions() {
        composeRule.onNodeWithText("記事を共有して要約").assertIsDisplayed()
        composeRule.onNodeWithText("Chromeで記事を開き、共有からこのアプリを選んでください。")
            .assertIsDisplayed()
    }
}
