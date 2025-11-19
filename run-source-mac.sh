#!/bin/bash
#
# uB Suite - macOS Source Runner
# Run any uB app from source
#
# Note: uB Suite is designed for Ubuntu/Linux. macOS support
# is limited as GTK AppIndicator is Linux-specific.
# Most apps will NOT work on macOS without modifications.
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ============================================
# COLORS
# ============================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ============================================
# FUNCTIONS
# ============================================

print_header() {
    echo -e "${CYAN}"
    echo "============================================"
    echo "   uB Suite - macOS Source Runner"
    echo "============================================"
    echo -e "${NC}"
}

print_usage() {
    echo -e "${BLUE}Usage:${NC} ./run-source-mac.sh <app-name>"
    echo ""
    echo -e "${YELLOW}WARNING:${NC} uB Suite is designed for Ubuntu/Linux."
    echo "  GTK AppIndicator is not natively supported on macOS."
    echo "  You may need to install GTK3 via Homebrew:"
    echo "    brew install gtk+3 pygobject3"
    echo ""
    echo -e "${BLUE}Available apps:${NC}"
    echo "  ubcpu   - CPU usage monitor"
    echo "  ubdisk  - Disk I/O bandwidth monitor"
    echo "  ubnet   - Network bandwidth monitor"
    echo "  ubres   - Display resolution switcher"
    echo "  ubtemp  - Hardware temperature monitor"
    echo "  ubtime  - World clock & timezones"
    echo "  ubweat  - Weather display"
    echo ""
    echo -e "${BLUE}Example:${NC} ./run-source-mac.sh ubtime"
}

check_dependencies() {
    echo -e "${BLUE}[CHECK]${NC} Verifying dependencies..."

    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} Python3 is not installed!"
        echo "  Install: brew install python3"
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} Python3 $(python3 --version 2>&1 | awk '{print $2}')"

    echo -e "${YELLOW}[WARN]${NC} GTK AppIndicator may not be available on macOS"
}

run_app() {
    local app_lower="$1"
    local app_upper=""

    case "$app_lower" in
        ubcpu)  app_upper="uBCPU" ;;
        ubdisk) app_upper="uBDISK" ;;
        ubnet)  app_upper="uBNET" ;;
        ubres)  app_upper="uBRES" ;;
        ubtemp) app_upper="uBTEMP" ;;
        ubtime) app_upper="uBTIME" ;;
        ubweat) app_upper="uBWEAT" ;;
        *)
            echo -e "${RED}[ERROR]${NC} Unknown app: $app_lower"
            print_usage
            exit 1
            ;;
    esac

    local script="${app_upper}/${app_lower}.py"
    if [ ! -f "$script" ]; then
        echo -e "${RED}[ERROR]${NC} Script not found: $script"
        exit 1
    fi

    echo -e "${GREEN}[START]${NC} Launching ${app_upper}..."
    python3 "$script"
}

# ============================================
# MAIN EXECUTION
# ============================================

print_header

if [ $# -eq 0 ]; then
    print_usage
    exit 0
fi

check_dependencies
echo ""

run_app "$1"
