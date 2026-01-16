@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem ------------------------------------------------------------
rem Light ED protocol launcher (simple).
rem
rem Usage:
rem   Light_ED_Analysis.bat <audio_file>
rem
rem What it does:
rem   1) Run analysis with the experimental ED_Cool_Dive protocol 
rem   2) Generate a report using the associated context file (Cool_ED_Context)
rem ------------------------------------------------------------

if "%~1"=="" (
  echo.
  echo Usage: %~nx0 ^<audio_file^>
  echo Example: %~nx0 shake.wav
  echo.
  exit /b 1
)

set "AUDIO=%~1"

rem Paths (relative to repo root)
set "PROTOCOL=examples\protocols\experimental\ED_Cool_Dive.yaml"
set "CONTEXT=examples\protocols\Baseline\Cool_ED_Context.yaml"

rem Output directory
set "OUT_DIR=output\COOL_ED"

echo.
echo ============================================================
echo Phase 1 - Run analysis
echo ============================================================
echo Audio    : "%AUDIO%"
echo Protocol : "%PROTOCOL%"
echo Output   : "%OUT_DIR%"
echo ============================================================
echo.

python run_analysis.py "%AUDIO%" --config "%PROTOCOL%" --output "%OUT_DIR%"
if errorlevel 1 (
  echo ERROR: Analysis failed.
  exit /b 1
)

echo.
echo ============================================================
echo Phase 2 - Generate report (context-driven, no recomputation)
echo ============================================================
echo Context  : "%CONTEXT%"
echo ============================================================
echo.

python Generate_Report.py "%OUT_DIR%" --protocol "%PROTOCOL%" --context "%CONTEXT%"
if errorlevel 1 (
  echo ERROR: Report generation failed.
  exit /b 1
)

echo.
echo ============================================================
echo Done.
echo Outputs are under: "%OUT_DIR%"
echo ============================================================
echo.

exit /b 0
