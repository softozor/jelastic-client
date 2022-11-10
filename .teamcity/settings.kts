import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.buildFeatures.perfmon
import jetbrains.buildServer.configs.kotlin.buildSteps.script
import jetbrains.buildServer.configs.kotlin.triggers.vcs

/*
The settings script is an entry point for defining a TeamCity
project hierarchy. The script should contain a single call to the
project() function with a Project instance or an init function as
an argument.

VcsRoots, BuildTypes, Templates, and subprojects can be
registered inside the project using the vcsRoot(), buildType(),
template(), and subProject() methods respectively.

To debug settings scripts in command-line, run the

    mvnDebug org.jetbrains.teamcity:teamcity-configs-maven-plugin:generate

command and attach your debugger to the port 8000.

To debug in IntelliJ Idea, open the 'Maven Projects' tool window (View
-> Tool Windows -> Maven Projects), find the generate task node
(Plugins -> teamcity-configs -> teamcity-configs:generate), the
'Debug' option is available in the context menu for the task.
*/

version = "2022.10"

project {

    buildType(SharedLibraries_JelasticClient_Build)
}

object SharedLibraries_JelasticClient_Build : BuildType({
    id("BuildWheel")
    name = "Build Wheel"

    //

    vcs {
        root(DslContext.settingsRoot)
    }

    steps {
        publishCommitShortSha()
        script {
            name = "Build"
            scriptContent = """
                #! /bin/sh
                
                poetry build
            """.trimIndent()
        }
        script {
            name = "Test"
            scriptContent = """
                #! /bin/sh
                
                pyenv local 3.8.12 3.9.10 3.10.2
                tox -- -s -v --cov --cov-report term-missing --cov-report html --teamcity --cov-append test -n 4 --api-token=%system.jelastic.access-token% --jelastic-version=%jelastic.version% --commit-sha=%build.vcs.number% --jelastic-user-email=%system.jelastic.user-email%       
            """.trimIndent()
            // TODO: we need a docker-tools repo with a docker image for python tests
            // dockerImage = ""
        }
        // TODO: we need this publish that will just append the git commit to the current version
        // TODO: we also need a separate build config that will push the wheel on tagging
        // TODO: we want to publish to pypi.org too
        script {
            name = "Publish"
            scriptContent = """
                #! /bin/sh
                
                set -e
                
                // TODO: we need a way to define good tags on feature branches and on master branch
                poetry version $(git describe --tags)
                poetry config repositories.pypi-hosted https://%system.pypi-registry.hosted%/
                poetry config http-basic.pypi-hosted %system.package-manager.deployer.username% %system.package-manager.deployer.password%
                poetry publish --build -r pypi-hosted
            """.trimIndent()
        }
    }


    triggers {
        vcs {
        }
    }

    features {
        perfmon {
        }
    }
})
