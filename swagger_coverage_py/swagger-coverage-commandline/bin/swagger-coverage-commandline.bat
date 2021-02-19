@rem
@rem Copyright 2015 the original author or authors.
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem      https://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.
@rem

@if "%DEBUG%" == "" @echo off
@rem ##########################################################################
@rem
@rem  swagger-coverage-commandline startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%..

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

@rem Add default JVM options here. You can also use JAVA_OPTS and SWAGGER_COVERAGE_COMMANDLINE_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS=

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto execute

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto execute

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\lib\swagger-coverage-commandline-1.0-SNAPSHOT.jar;%APP_HOME%\lib\swagger-coverage-commons-1.0-SNAPSHOT.jar;%APP_HOME%\lib\swagger-compat-spec-parser-1.0.52.jar;%APP_HOME%\lib\slf4j-simple-1.7.12.jar;%APP_HOME%\lib\log4j-1.2.17.jar;%APP_HOME%\lib\jcommander-1.78.jar;%APP_HOME%\lib\spring-web-5.2.6.RELEASE.jar;%APP_HOME%\lib\freemarker-2.3.29.jar;%APP_HOME%\lib\swagger-parser-1.0.52.jar;%APP_HOME%\lib\swagger-core-1.6.1.jar;%APP_HOME%\lib\swagger-models-1.6.2.jar;%APP_HOME%\lib\json-patch-1.6.jar;%APP_HOME%\lib\json-schema-validator-2.2.8.jar;%APP_HOME%\lib\json-schema-core-1.2.8.jar;%APP_HOME%\lib\jackson-coreutils-1.8.jar;%APP_HOME%\lib\jackson-databind-2.10.1.jar;%APP_HOME%\lib\jackson-dataformat-yaml-2.9.8.jar;%APP_HOME%\lib\jackson-core-2.10.1.jar;%APP_HOME%\lib\httpclient-4.5.2.jar;%APP_HOME%\lib\slf4j-ext-1.7.28.jar;%APP_HOME%\lib\slf4j-api-1.7.28.jar;%APP_HOME%\lib\spring-beans-5.2.6.RELEASE.jar;%APP_HOME%\lib\spring-core-5.2.6.RELEASE.jar;%APP_HOME%\lib\jackson-annotations-2.9.0.jar;%APP_HOME%\lib\swagger-annotations-1.6.2.jar;%APP_HOME%\lib\commons-lang3-3.2.1.jar;%APP_HOME%\lib\uri-template-0.9.jar;%APP_HOME%\lib\guava-27.0.1-android.jar;%APP_HOME%\lib\validation-api-1.1.0.Final.jar;%APP_HOME%\lib\commons-io-2.4.jar;%APP_HOME%\lib\mailapi-1.4.3.jar;%APP_HOME%\lib\joda-time-2.9.7.jar;%APP_HOME%\lib\libphonenumber-8.0.0.jar;%APP_HOME%\lib\msg-simple-1.1.jar;%APP_HOME%\lib\btf-1.2.jar;%APP_HOME%\lib\jsr305-3.0.2.jar;%APP_HOME%\lib\jopt-simple-5.0.3.jar;%APP_HOME%\lib\httpcore-4.4.4.jar;%APP_HOME%\lib\commons-logging-1.2.jar;%APP_HOME%\lib\commons-codec-1.9.jar;%APP_HOME%\lib\spring-jcl-5.2.6.RELEASE.jar;%APP_HOME%\lib\snakeyaml-1.23.jar;%APP_HOME%\lib\failureaccess-1.0.1.jar;%APP_HOME%\lib\listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar;%APP_HOME%\lib\checker-compat-qual-2.5.2.jar;%APP_HOME%\lib\error_prone_annotations-2.2.0.jar;%APP_HOME%\lib\j2objc-annotations-1.1.jar;%APP_HOME%\lib\animal-sniffer-annotations-1.17.jar;%APP_HOME%\lib\rhino-1.7R4.jar;%APP_HOME%\lib\activation-1.1.jar


@rem Execute swagger-coverage-commandline
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %SWAGGER_COVERAGE_COMMANDLINE_OPTS%  -classpath "%CLASSPATH%" com.github.viclovsky.swagger.coverage.CommandLine %*

:end
@rem End local scope for the variables with windows NT shell
if "%ERRORLEVEL%"=="0" goto mainEnd

:fail
rem Set variable SWAGGER_COVERAGE_COMMANDLINE_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
if  not "" == "%SWAGGER_COVERAGE_COMMANDLINE_EXIT_CONSOLE%" exit 1
exit /b 1

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
