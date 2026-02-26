#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m' # Added RED for errors
RED_BOLD='\033[1;31m' # Added RED_BOLD for important messages
NC='\033[0m' # No Color

DB_FILE="maverick_operational_data.db"
API_LOG_FILE="api_server.log"
DASH_LOG_FILE="dashboard_server.log"

# Initialize PIDs to a non-existent process ID
PID_API=0
PID_DASHBOARD=0

# Cleanup function to kill background processes
cleanup() {
    echo -e "\n${YELLOW}Initiating cleanup...${NC}"
    if [ "$PID_API" -ne 0 ] && ps -p $PID_API > /dev/null; then
        echo -e "${YELLOW}Stopping API server (PID: $PID_API)...${NC}"
        kill $PID_API
        wait $PID_API 2>/dev/null
        echo -e "${GREEN}API server stopped.${NC}"
    else
        echo -e "${CYAN}API server (PID: $PID_API) was not running or PID not captured.${NC}"
    fi

    if [ "$PID_DASHBOARD" -ne 0 ] && ps -p $PID_DASHBOARD > /dev/null; then
        echo -e "${YELLOW}Stopping Dashboard server (PID: $PID_DASHBOARD)...${NC}"
        kill $PID_DASHBOARD
        wait $PID_DASHBOARD 2>/dev/null
        echo -e "${GREEN}Dashboard server stopped.${NC}"
    else
        echo -e "${CYAN}Dashboard server (PID: $PID_DASHBOARD) was not running or PID not captured.${NC}"
    fi
    echo -e "${GREEN}Cleanup complete. Demo finished.${NC}"
    exit 0
}

# Trap SIGINT (Ctrl+C) and SIGTERM to run the cleanup function
trap cleanup SIGINT SIGTERM

# --- Main Demo Flow ---

if [ -f "$DB_FILE" ]; then
    echo -e "${YELLOW}Removing previous demo database ($DB_FILE)...${NC}"
    rm "$DB_FILE"
fi
# Remove previous log files
rm -f "$API_LOG_FILE" "$DASH_LOG_FILE"

echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  MAVERICK - INTEGRATED DASHBOARD PoC DEMO - ADAM TACON${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo -e "${YELLOW}This demo will run the data pipeline, start the API & Dashboard servers.${NC}"
echo -e "${YELLOW}Server logs will be written to '$API_LOG_FILE' and '$DASH_LOG_FILE'.${NC}"
echo -e "${YELLOW}Ensure Python dependencies are installed:${NC}"
echo -e "${YELLOW}  pip install pandas requests Flask dash dash-bootstrap-components plotly${NC}"
echo ""
echo -e "${YELLOW}Press Enter to begin Act I (Data Ingestion)...${NC}"
read

echo -e "${CYAN}STEP 1: Running Act I - Data Ingestion Service${NC}"
echo -e "${CYAN}(maverick_data_ingestion_service.py)${NC}"
echo -e "${CYAN}-----------------------------------------------------------------------${NC}"
python3 maverick_data_ingestion_service.py
echo ""
echo -e "${YELLOW}Act I Complete. Database '${DB_FILE}' is populated.${NC}"
echo -e "${YELLOW}Press Enter to proceed to Act II & III (Start Servers)...${NC}"
read

echo -e "${CYAN}STEP 2: Starting Act II - Operations API Server (in background)${NC}"
echo -e "${CYAN}(maverick_operations_api_service.py)${NC}"
echo -e "${CYAN}-------------------------------------------------------------------------${NC}"
python3 maverick_operations_api_service.py > "$API_LOG_FILE" 2>&1 &
PID_API=$!
if ps -p $PID_API > /dev/null; then
    echo -e "${GREEN}API Server starting in background (PID: $PID_API). Log: $API_LOG_FILE${NC}"
    echo -e "${YELLOW}Allowing a few seconds for initialization...${NC}"
    sleep 3
else
    echo -e "${RED}ERROR: Failed to start API server. Check $API_LOG_FILE for details.${NC}"
    PID_API=0
fi
echo ""

echo -e "${CYAN}STEP 3: Starting Act III - Live Dashboard Server (in background)${NC}"
echo -e "${CYAN}(maverick_live_dashboard.py)${NC}"
echo -e "${CYAN}-------------------------------------------------------------------------${NC}"
python3 maverick_live_dashboard.py > "$DASH_LOG_FILE" 2>&1 &
PID_DASHBOARD=$!
if ps -p $PID_DASHBOARD > /dev/null; then
    echo -e "${GREEN}Dashboard Server starting in background (PID: $PID_DASHBOARD). Log: $DASH_LOG_FILE${NC}"
    echo -e "${YELLOW}Allowing a few seconds for initialization...${NC}"
    sleep 3
else
    echo -e "${RED}ERROR: Failed to start Dashboard server. Check $DASH_LOG_FILE for details.${NC}"
    PID_DASHBOARD=0
fi
echo ""

if [ "$PID_API" -ne 0 ] && [ "$PID_DASHBOARD" -ne 0 ]; then
    echo -e "${GREEN}Both servers should be running!${NC}"
    echo -e "${YELLOW}  - API is on: http://127.0.0.1:5000${NC}"
    echo -e "${YELLOW}  - Dashboard is on: http://127.0.0.1:8050 (Open this in your browser)${NC}"
    echo ""
    echo -e "${YELLOW}You can monitor server activity by tailing their log files in separate terminals:${NC}"
    echo -e "${YELLOW}  tail -f ${API_LOG_FILE}${NC}"
    echo -e "${YELLOW}  tail -f ${DASH_LOG_FILE}${NC}"
    echo ""
    echo -e "${RED_BOLD}Press Ctrl+C IN THIS TERMINAL to stop both servers and exit the demo.${NC}"
    wait # Wait for Ctrl+C or for background processes to terminate (though trap handles Ctrl+C)
else
    echo -e "${RED_BOLD}CRITICAL ERROR: One or both servers failed to start properly.${NC}"
    echo -e "${RED}Please check the log files for details before proceeding with a manual demo:${NC}"
    if [ "$PID_API" -eq 0 ]; then echo -e "${RED}  API Log: ${API_LOG_FILE}${NC}"; fi
    if [ "$PID_DASHBOARD" -eq 0 ]; then echo -e "${RED}  Dashboard Log: ${DASH_LOG_FILE}${NC}"; fi
    cleanup # Attempt to clean up if one started and the other failed
fi
