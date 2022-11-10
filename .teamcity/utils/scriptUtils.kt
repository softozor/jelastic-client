package utils

import jetbrains.buildServer.configs.kotlin.DslContext
import java.io.BufferedReader
import java.io.File

/**
 * Helper function to read the content of a script file
 * @param path, the path to the script file to read, relative to settings.kts
 * @return a string containing the content of the script file
 *
 * source: https://www.jetbrains.com/help/teamcity/kotlin-dsl.html#How+to+Access+Auxiliary+Scripts+from+DSL+Settings
 */
fun readScript(path: String): String {
    val bufferedReader: BufferedReader = File(DslContext.baseDir, path).bufferedReader()
    return bufferedReader.use { it.readText() }.trimIndent()
}