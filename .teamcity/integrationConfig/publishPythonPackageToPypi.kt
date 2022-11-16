package integrationConfig

import jetbrains.buildServer.configs.kotlin.BuildSteps
import jetbrains.buildServer.configs.kotlin.buildSteps.ScriptBuildStep
import jetbrains.buildServer.configs.kotlin.buildSteps.script

fun BuildSteps.publishPythonPackageToPypi(dockerToolsTag: String): ScriptBuildStep {
    return script {
        name = "Publish To Pypi"
        scriptContent = """
                #! /bin/sh
                
                set -e
                
                tag=${'$'}(git describe --always --tags --match v*)
                distance=${'$'}(echo ${'$'}tag | cut -d "-" -f 2)
                if [ "${'$'}tag" != "${'$'}distance" ] ; then
                  # we are not on a tag
                  echo "##teamcity[message text='not publishing to pypi.org' status='NORMAL']"
                  exit 0
                fi
                
                echo "##teamcity[message text='publishing to pypi.org' status='NORMAL']"
                poetry publish -u %system.pypi-registry.pypi-org.username% -p %system.pypi-registry.pypi-org.password%
            """.trimIndent()
        this.dockerImage = "%system.docker-registry.group%/docker-tools/poetry:$dockerToolsTag"
        dockerPull = true
        dockerImagePlatform = ScriptBuildStep.ImagePlatform.Linux
    }
}