package integrationConfig

import jetbrains.buildServer.configs.kotlin.BuildType
import jetbrains.buildServer.configs.kotlin.DslContext
import jetbrains.buildServer.configs.kotlin.buildFeatures.dockerSupport
import jetbrains.buildServer.configs.kotlin.buildFeatures.perfmon
import jetbrains.buildServer.configs.kotlin.triggers.vcs
import publishCommitShortSha

class ReleaseToPypi(
    dockerTag: String
) : BuildType({
    id("ReleaseToPypi")
    name = "Release To pypi.org"

    vcs {
        root(DslContext.settingsRoot)
        cleanCheckout = true
        branchFilter = """
            +:v*
            -:<default>
        """.trimIndent()
    }

    triggers {
        vcs {
        }
    }

    steps {
        publishCommitShortSha()
        buildPythonPackage("docker-tools/poetry:$dockerTag")
        toxPythonPackage("docker-tools/python-tests:$dockerTag", testArgs = listOf(
            "-n 4",
            "--api-token=%system.jelastic.access-token%",
            "--jelastic-version=%jelastic.version%",
            "--commit-sha=%build.vcs.number%",
            "--jelastic-user-email=%system.jelastic.user-email%"
        ))
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