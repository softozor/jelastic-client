package integrationConfig

import jetbrains.buildServer.configs.kotlin.BuildSteps
import jetbrains.buildServer.configs.kotlin.buildSteps.ScriptBuildStep
import jetbrains.buildServer.configs.kotlin.buildSteps.script

fun BuildSteps.toxPythonPackage(dockerImage: String, testArgs: List<String> = listOf()): ScriptBuildStep {
    return script {
        name = "Test"
        scriptContent = """
                #! /bin/sh
                
                pyenv local 3.8 3.9 3.10 3.11
                tox -- ${testArgs.joinToString(" ")}       
            """.trimIndent()
        this.dockerImage = "%system.docker-registry.group%/$dockerImage"
        dockerPull = true
        dockerImagePlatform = ScriptBuildStep.ImagePlatform.Linux
    }
}