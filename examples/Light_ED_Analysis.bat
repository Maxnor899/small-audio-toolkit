@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem ------------------------------------------------------------
rem Run all example protocols on a single file, then generate
rem two contextual reports (two different contexts) per protocol.
rem
rem Notes:
rem - Context is applied ONLY during report generation.
rem - Visualizations are generated during the analysis phase
rem   if visualization.enabled is true in the protocol YAML.
rem - We duplicate each analysis output folder so that reports
rem   generated with different contexts do not overwrite each other.
rem ------------------------------------------------------------

rem === Inputs (edit if needed) ===
set "AUDIO=shake.wav"

set "PROTO_DIR=examples\protocols\"
set "CTX1=examples\contexts\Cool_ED_Context.yaml"


set "OUT_BASE=output\ED_TESTS"

rem === Protocol list ===
set "PROTOCOLS=ED_Cool_Dive"

echo.
echo ============================================================
echo Phase 1 - Run analyses (protocol-driven, no context)
echo ============================================================
echo.

for %%P in (%PROTOCOLS%) do (
  echo --- Running protocol %%P ---
  python run_analysis.py "%AUDIO%" --config "%PROTO_DIR%\%%P.yaml" --output "%OUT_BASE%\%%P"
  if errorlevel 1 (
    echo ERROR: Analysis failed for protocol %%P
    exit /b 1
  )
)

echo.
echo ============================================================
echo Phase 2 - Generate reports (context-driven, no recomputation)
echo ============================================================
echo.

for %%P in (%PROTOCOLS%) do (
  echo --- Reporting for protocol %%P ---
  call :CopyDir "%OUT_BASE%\%%P" "%OUT_BASE%\%%P__ctx_cool_ED"
  python Generate_Report.py "%OUT_BASE%\%%P" --protocol "%PROTO_DIR%\%%P.yaml" --context "%CTX1%"
  if errorlevel 1 (
    echo ERROR: Report generation failed for protocol %%P with context CTX1
    exit /b 1
  )
)

echo.
echo ============================================================
echo Done.
echo Outputs are under: %OUT_BASE%
echo ============================================================
echo.
exit /b 0

rem ------------------------------------------------------------
rem CopyDir <src> <dst>
rem - Removes destination if it already exists
rem - Copies full directory tree (including visualizations)
rem ------------------------------------------------------------
:CopyDir
set "SRC=%~1"
set "DST=%~2"

if not exist "%SRC%" (
  echo ERROR: Source directory does not exist: "%SRC%"
  exit /b 1
)

if exist "%DST%" (
  rmdir /S /Q "%DST%"
)

mkdir "%DST%" >nul 2>&1

rem /E = copy subdirectories including empty
rem /I = assume destination is a directory
rem /Y = suppress overwrite prompt
xcopy "%SRC%\*" "%DST%\" /E /I /Y >nul
if errorlevel 1 (
  echo ERROR: Copy failed from "%SRC%" to "%DST%"
  exit /b 1
)

exit /b 0
