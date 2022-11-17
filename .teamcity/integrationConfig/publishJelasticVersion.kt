package integrationConfig

import jetbrains.buildServer.configs.kotlin.BuildSteps
import jetbrains.buildServer.configs.kotlin.buildSteps.ScriptBuildStep
import jetbrains.buildServer.configs.kotlin.buildSteps.script

fun BuildSteps.publishJelasticVersion(): ScriptBuildStep {
    return script {
        name = "Publish Jelastic Version"
        scriptContent = """
                #! /bin/sh

                tag=${'$'}(git describe --tags --always --match v* | cut -d "-" -f 1)
                version=${'$'}{tag#v}
                major=${'$'}(echo ${'$'}{version} | cut -d "." -f 1)
                minor=${'$'}(echo ${'$'}{version} | cut -d "." -f 2)
                patch=${'$'}(echo ${'$'}{version} | cut -d "." -f 3)

                echo "##teamcity[setParameter name='jelastic.version' value='${'$'}{major}.${'$'}{minor}.${'$'}{patch}']"
            """.trimIndent()
    }
}
