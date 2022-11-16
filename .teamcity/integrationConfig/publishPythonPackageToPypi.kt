package integrationConfig

import jetbrains.buildServer.configs.kotlin.BuildSteps
import jetbrains.buildServer.configs.kotlin.buildSteps.ScriptBuildStep
import jetbrains.buildServer.configs.kotlin.buildSteps.script

fun BuildSteps.publishPythonPackageToPypi(dockerImage: String): ScriptBuildStep {
    return script {
        name = "Publish To Pypi"
        scriptContent = """
                #! /bin/sh
                
                set -e
                
                tag=${'$'}(git describe --always --tags --match v*)
                distance=${'$'}(echo ${'$'}tag | cut -d "-" -f 2)
                if [ "${'$'}tag" != "${'$'}distance" ] ; then
                  # we are not on a tag
                  exit 0
                fi
                
                poetry publish -u %system.pypi-registry.pypi-org.username% -p %system.pypi-registry.pypi-org.password%
            """.trimIndent()
        this.dockerImage = "%system.docker-registry.group%/$dockerImage"
        dockerPull = true
        dockerImagePlatform = ScriptBuildStep.ImagePlatform.Linux
    }
}