package integrationConfig

import common.git.publishCommitShortSha
import common.python.*
import common.python.toxPythonPackage
import common.templates.NexusDockerLogin
import jetbrains.buildServer.configs.kotlin.BuildType
import jetbrains.buildServer.configs.kotlin.DslContext
import jetbrains.buildServer.configs.kotlin.buildFeatures.perfmon
import jetbrains.buildServer.configs.kotlin.triggers.ScheduleTrigger
import jetbrains.buildServer.configs.kotlin.triggers.schedule
import jetbrains.buildServer.configs.kotlin.triggers.vcs

class Integration(
    dockerToolsTag: String
) : BuildType({
    templates(NexusDockerLogin)

    id("Integration")
    name = "Integration"
    allowExternalStatus = true

    vcs {
        root(DslContext.settingsRoot)
        cleanCheckout = true
        branchFilter = """
            +:*
        """.trimIndent()
    }

    triggers {
        // in general, we only want to trigger a build if there were significant code changes
        vcs {
            branchFilter = """
                +:*
                -:v*
            """.trimIndent()
            triggerRules = """
                +:jelastic_client/**
                +:test/**
            """.trimIndent()
        }
        // on tags, because they are triggered with no code (just a pushed tag), we want no trigger rules, i.e.
        // any change to the repo is significant
        vcs {
            branchFilter = """
                +:v*
            """.trimIndent()
        }
        schedule {
            schedulingPolicy = weekly {
                dayOfWeek = ScheduleTrigger.DAY.Thursday
                hour = 23
                minute = 30
                timezone = "Europe/Zurich"
            }
            branchFilter = "+:<default>"
            triggerBuild = always()
            withPendingChangesOnly = false
            enableQueueOptimization = false
        }
    }

    steps {
        publishCommitShortSha()
        buildPythonPackage(dockerToolsTag)
        publishJelasticVersion()
        lint(dockerToolsTag)
        toxPythonPackage(
            dockerToolsTag,
            testArgs = listOf(
                "-n 4",
                "--api-token=%system.jelastic.access-token%",
                "--jelastic-version=%jelastic.version%",
                "--commit-sha=%build.vcs.number%",
                "--jelastic-user-email=%system.jelastic.user-email%"
            ),
        )
        publishPythonPackageToHosted(dockerToolsTag)
        publishPythonPackageToPypi(dockerToolsTag)
    }

    artifactRules = """
        dist/*.whl
        dist/PKG-INFO.txt
        coverage.zip
    """.trimIndent()

    features {
        perfmon {
        }
    }

    params {
        param("jelastic.version", "1.0.0")
        param("teamcity.vcsTrigger.runBuildInNewEmptyBranch", "true")
    }
})
