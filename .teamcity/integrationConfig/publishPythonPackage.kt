package integrationConfig

import jetbrains.buildServer.configs.kotlin.BuildSteps
import jetbrains.buildServer.configs.kotlin.buildSteps.ScriptBuildStep
import jetbrains.buildServer.configs.kotlin.buildSteps.script

fun BuildSteps.publishPythonPackageToHosted(dockerToolsTag: String): ScriptBuildStep {
    return script {
        name = "Publish"
        scriptContent = """
                #! /bin/sh

                set -e

                poetry config repositories.pypi-hosted https://%system.pypi-registry.hosted%/
                poetry config http-basic.pypi-hosted %system.package-manager.deployer.username% %system.package-manager.deployer.password%
                poetry publish -r pypi-hosted
            """.trimIndent()
        this.dockerImage = "%system.docker-registry.group%/docker-tools/poetry:$dockerToolsTag"
        dockerPull = true
        dockerImagePlatform = ScriptBuildStep.ImagePlatform.Linux
    }
}
