package integrationConfig

import jetbrains.buildServer.configs.kotlin.BuildSteps
import jetbrains.buildServer.configs.kotlin.buildSteps.ScriptBuildStep
import jetbrains.buildServer.configs.kotlin.buildSteps.script

fun BuildSteps.buildPythonPackage(dockerImage: String): ScriptBuildStep {
    return script {
        name = "Build"
        scriptContent = """
                #! /bin/sh
                
                poetry build
            """.trimIndent()
        this.dockerImage = "%system.docker-registry.group%/$dockerImage"
        dockerPull = true
        dockerImagePlatform = ScriptBuildStep.ImagePlatform.Linux
    }
}