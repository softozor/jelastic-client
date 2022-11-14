package integrationConfig

import jetbrains.buildServer.configs.kotlin.BuildType
import jetbrains.buildServer.configs.kotlin.DslContext
import jetbrains.buildServer.configs.kotlin.buildFeatures.dockerSupport
import jetbrains.buildServer.configs.kotlin.buildFeatures.perfmon
import jetbrains.buildServer.configs.kotlin.triggers.vcs
import publishCommitShortSha

class Integration(
    dockerTag: String
) : BuildType({
    id("Integration")
    name = "Integration"

    vcs {
        root(DslContext.settingsRoot)
    }

    triggers {
        vcs {
        }
    }

    steps {
        publishCommitShortSha()
        buildPythonPackage("%system.docker-registry.group%/docker-tools/poetry:$dockerTag")
        toxPythonPackage("docker-tools/python-tests:$dockerTag", testArgs = listOf(
            "-n 4",
            "--api-token=%system.jelastic.access-token%",
            "--jelastic-version=%jelastic.version%",
            "--commit-sha=%build.vcs.number%",
            "--jelastic-user-email=%system.jelastic.user-email%"
        ))
        publishPythonPackageToHosted("docker-tools/poetry:$dockerTag")
    }

    // TODO: add mutmut.*ml
    artifactRules = """
        dist/*.whl
        dist/PKG-INFO.txt
        coverage.zip
    """.trimIndent()

    // TODO: add tab for mutmut

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