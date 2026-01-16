@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem ------------------------------------------------------------
rem Baseline protocol launcher (simple).
rem
rem Usage:
rem   Baseline_Analysis.bat <audio_file>
rem
rem What it does:
rem   1) Run analysis with the baseline protocol (no context involved)
rem   2) Generate a report using the associated context file (no recomputation)
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
set "PROTOCOL=examples\protocols\Baseline\protocol_baseline_full.yaml"
set "CONTEXT=examples\protocols\Baseline\context_baseline_general_audio.yaml"

rem Output directory
set "OUT_DIR=output\BASELINE"

echo.
echo ============================================================
echo Phase 1 - Run analysis (protocol-driven, no context)
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
