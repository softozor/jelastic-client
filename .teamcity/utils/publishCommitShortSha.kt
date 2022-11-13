import jetbrains.buildServer.configs.kotlin.BuildSteps
import jetbrains.buildServer.configs.kotlin.buildSteps.ScriptBuildStep
import jetbrains.buildServer.configs.kotlin.buildSteps.script

fun BuildSteps.publishCommitShortSha(): ScriptBuildStep {
    return script {
        name = "Publish Commit Short SHA"
        scriptContent = """
            #! /bin/bash

            GIT_COMMIT_SHA=%build.vcs.number%
            GIT_COMMIT_SHORT_SHA=${'$'}{GIT_COMMIT_SHA:0:8}

            echo "##teamcity[setParameter name='build.vcs.number' value='${'$'}{GIT_COMMIT_SHORT_SHA}']"
        """.trimIndent()
    }
}