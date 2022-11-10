import jetbrains.buildServer.configs.kotlin.BuildSteps
import jetbrains.buildServer.configs.kotlin.buildSteps.ScriptBuildStep
import jetbrains.buildServer.configs.kotlin.buildSteps.script
import utils.readScript

fun BuildSteps.publishCommitShortSha(): ScriptBuildStep {
    return script {
        name = "Publish Commit Short SHA"
        scriptContent = readScript("scripts/publish_commit_short_sha.sh")
    }
}