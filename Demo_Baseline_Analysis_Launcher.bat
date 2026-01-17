@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem ------------------------------------------------------------
rem Baseline protocol launcher (example).
rem
rem This launcher is meant to be used from within:
rem   Small_Audio_Tool\Analysis_examples
rem
rem Typical workflow for users:
rem   - Copy Analysis_examples -> Analysis
rem   - Adjust launchers to match their own paths (inputs/outputs)
rem
rem Usage:
rem   Baseline_Analysis.bat <audio_file>
rem ------------------------------------------------------------

if "%~1"=="" (
  echo Usage: %~nx0 ^<audio_file^>
  exit /b 1
)

set "AUDIO=%~1"

rem Paths (relative to Small_Audio_Tool\Analysis_examples)
set "PROTOCOL=Analysis_examples\01_protocols\01_Baseline\protocol_baseline_full.yaml"
set "CONTEXTS_DIR=Analysis_examples\02_contexts"

rem Output directory (inside Analysis_examples)
set "OUT_DIR=Analysis_examples\05_Results\BASELINE_ANALYSYS"

echo.
echo ============================================================
echo Phase 1 - Run analysis (protocol-driven)
echo ============================================================
echo Audio       : "%AUDIO%"
echo Protocol    : "%PROTOCOL%"
echo Output      : "%OUT_DIR%"
echo ============================================================
echo.

python run_analysis.py "%AUDIO%" --config "%PROTOCOL%" --output "%OUT_DIR%"
if errorlevel 1 (
  echo.
  echo ERROR: Analysis failed.
  exit /b 1
)

echo.
echo ============================================================
echo Phase 2 - Generate reports (loads contexts per family)
echo ============================================================
echo Output       : "%OUT_DIR%"
echo Protocol     : "%PROTOCOL%"
echo Contexts dir : "%CONTEXTS_DIR%"
echo ============================================================
echo.

python Generate_Report.py "%OUT_DIR%" --protocol "%PROTOCOL%" --contexts-dir "%CONTEXTS_DIR%"
if errorlevel 1 (
  echo.
  echo ERROR: Report generation failed.
  exit /b 1
)

echo.
echo =========================================
echo Done.
echo =========================================
echo.

exit /b 0
