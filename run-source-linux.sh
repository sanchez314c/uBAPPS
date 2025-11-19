#!/bin/bash
#
# uB Suite - Linux Source Runner
# Run any uB app from source
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
    echo "   uB Suite - Linux Source Runner"
    echo "============================================"
    echo -e "${NC}"
}

print_usage() {
    echo -e "${BLUE}Usage:${NC} ./run-source-linux.sh <app-name>"
    echo ""
    echo -e "${BLUE}Available apps:${NC}"
    echo "  ubcpu   - CPU usage monitor"
    echo "  ubdisk  - Disk I/O bandwidth monitor"
    echo "  ubnet   - Network bandwidth monitor"
    echo "  ubres   - Display resolution switcher"
    echo "  ubtemp  - Hardware temperature monitor"
    echo "  ubtime  - World clock & timezones"
    echo "  ubweat  - Weather display"
    echo "  all     - Launch all apps"
    echo ""
    echo -e "${BLUE}Example:${NC} ./run-source-linux.sh ubcpu"
}

check_dependencies() {
    echo -e "${BLUE}[CHECK]${NC} Verifying dependencies..."

    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} Python3 is not installed!"
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} Python3 $(python3 --version 2>&1 | awk '{print $2}')"

    # Check GTK3
    if ! python3 -c "import gi; gi.require_version('Gtk', '3.0')" 2>/dev/null; then
        echo -e "${RED}[ERROR]${NC} GTK3 Python bindings not found!"
        echo "  Install: sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0"
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} GTK3 bindings available"

    # Check AppIndicator
    if ! python3 -c "import gi; gi.require_version('AyatanaAppIndicator3', '0.1')" 2>/dev/null; then
        echo -e "${YELLOW}[WARN]${NC} AyatanaAppIndicator3 not found"
        echo "  Install: sudo apt install gir1.2-ayatanaappindicator3-0.1"
    else
        echo -e "${GREEN}[OK]${NC} AyatanaAppIndicator3 available"
    fi
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
    python3 "$script" &
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

APP="$1"

if [ "$APP" = "all" ]; then
    echo -e "${CYAN}[LAUNCH]${NC} Starting all uB apps..."
    for app in ubcpu ubdisk ubnet ubres ubtemp ubtime ubweat; do
        run_app "$app"
        sleep 1
    done
    echo -e "${GREEN}[DONE]${NC} All apps launched. Press Ctrl+C to stop."
    wait
else
    run_app "$APP"
    wait
fi
