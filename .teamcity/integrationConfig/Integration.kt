package integrationConfig

import jetbrains.buildServer.configs.kotlin.BuildType
import jetbrains.buildServer.configs.kotlin.DslContext
import jetbrains.buildServer.configs.kotlin.buildFeatures.dockerSupport
import jetbrains.buildServer.configs.kotlin.buildFeatures.perfmon
import jetbrains.buildServer.configs.kotlin.triggers.ScheduleTrigger
import jetbrains.buildServer.configs.kotlin.triggers.schedule
import jetbrains.buildServer.configs.kotlin.triggers.vcs
import publishCommitShortSha

class Integration(
    dockerTag: String
) : BuildType({
    id("Integration")
    name = "Integration"

    vcs {
        root(DslContext.settingsRoot)
        cleanCheckout = true
        branchFilter = """
            +:*
        """.trimIndent()
    }

    triggers {
        vcs {
            branchFilter = """
                +:*
            """.trimIndent()
//            triggerRules = """
//                +:*
//                -:.teamcity/**
//                -:.gitignore
//                -:.pre-commit-config.yaml
//                -:README.md
//            """.trimIndent()
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
        buildPythonPackage("docker-tools/poetry:$dockerTag")
        toxPythonPackage(
            "docker-tools/python-tests:$dockerTag", testArgs = listOf(
                "-n 4",
                "--api-token=%system.jelastic.access-token%",
                "--jelastic-version=%jelastic.version%",
                "--commit-sha=%build.vcs.number%",
                "--jelastic-user-email=%system.jelastic.user-email%"
            )
        )
        publishPythonPackageToHosted("docker-tools/poetry:$dockerTag")
        publishPythonPackageToPypi("docker-tools/poetry:$dockerTag")
    }

    artifactRules = """
        dist/*.whl
        dist/PKG-INFO.txt
        coverage.zip
    """.trimIndent()

    features {
        perfmon {
        }

        dockerSupport {
            cleanupPushedImages = true
            loginToRegistry = on {
                dockerRegistryId = "PROJECT_EXT_3"
            }
        }
    }

    params {
        param("teamcity.vcsTrigger.runBuildInNewEmptyBranch", "true")
    }
})