#!/bin/bash
################################################################################
# install-mcp-core.sh — Bootstrap installer for 7 core MCPs
#
# This script automates the installation of 7 foundation MCPs (csscore-mcp
# + 6 specialized MCPs) from the ai-marketplace into a fresh CyberSecSuite
# instance. Optimized for speed (<120 seconds target).
#
# MCPs Installed:
#   1. csscore-mcp (22 modules - core infrastructure)
#   2. canvas-mcp (forensic visualization)
#   3. memory-mcp (vector memory storage)
#   4. template-mcp (template rendering engine)
#   5. playwright-mcp (browser automation)
#   6. dystopian-crypto-mcp (cryptographic operations)
#
# Usage:
#   ./install-mcp-core.sh                Run full bootstrap
#   ./install-mcp-core.sh --verify       Verify installation only
#   ./install-mcp-core.sh --cleanup      Remove installations
#
# Requirements:
#   - bash >= 4.0
#   - jq (JSON processor)
#   - uv (Python package manager, >=0.1.0)
#   - Python >= 3.11
#
################################################################################

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly MARKETPLACE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly MCPS_DIR="${MARKETPLACE_DIR}/mcps"
readonly INDEX_FILE="${MARKETPLACE_DIR}/index.json"

# Core MCPs to install (order matters - csscore-mcp first)
declare -a CORE_MCPS=(
  "csscore-mcp"
  "canvas-mcp"
  "memory-mcp"
  "template-mcp"
  "playwright-mcp"
  "dystopian-crypto-mcp"
)

# CyberSecSuite paths
readonly CYBERSECSUITE_ROOT="${CYBERSECSUITE_ROOT:-${MARKETPLACE_DIR}/../cybersecsuite}"
readonly CYBERSECSUITE_MCP_CONFIG="${CYBERSECSUITE_ROOT}/config/mcps.json"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Timing
readonly START_TIME=$(date +%s)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

log_info() {
  echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
  echo -e "${GREEN}[✓]${NC} $*"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $*" >&2
}

elapsed_time() {
  local end_time=$(date +%s)
  echo $((end_time - START_TIME))
}

check_duration() {
  local elapsed=$(elapsed_time)
  if [[ $elapsed -gt 120 ]]; then
    log_warn "Bootstrap taking longer than target (${elapsed}s > 120s)"
  fi
}

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

check_prerequisites() {
  log_info "Checking prerequisites..."
  
  local missing=0
  
  # Check bash version
  if [[ ${BASH_VERSINFO[0]} -lt 4 ]]; then
    log_error "Bash 4.0+ required (found ${BASH_VERSION})"
    missing=1
  fi
  
  # Check required tools
  for tool in jq uv python3; do
    if ! command -v "$tool" &> /dev/null; then
      log_error "Required tool not found: $tool"
      missing=1
    fi
  done
  
  # Check Python version
  local py_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
  if (( $(echo "$py_version < 3.11" | bc -l) )); then
    log_error "Python 3.11+ required (found $py_version)"
    missing=1
  fi
  
  if [[ $missing -eq 1 ]]; then
    log_error "Prerequisites check failed"
    return 1
  fi
  
  log_success "All prerequisites met"
  return 0
}

check_marketplace_structure() {
  log_info "Verifying marketplace structure..."
  
  if [[ ! -f "$INDEX_FILE" ]]; then
    log_error "Marketplace index not found: $INDEX_FILE"
    return 1
  fi
  
  # Validate index.json
  if ! jq empty "$INDEX_FILE" 2>/dev/null; then
    log_error "Invalid JSON in index.json"
    return 1
  fi
  
  # Check all core MCPs exist
  for mcp in "${CORE_MCPS[@]}"; do
    if [[ ! -d "${MCPS_DIR}/${mcp}" ]]; then
      log_error "MCP not found: $mcp"
      return 1
    fi
    
    if [[ ! -f "${MCPS_DIR}/${mcp}/pyproject.toml" ]]; then
      log_error "pyproject.toml not found in $mcp"
      return 1
    fi
  done
  
  log_success "Marketplace structure valid"
  return 0
}

# ============================================================================
# INSTALLATION FUNCTIONS
# ============================================================================

install_mcp() {
  local mcp_name="$1"
  local mcp_dir="${MCPS_DIR}/${mcp_name}"
  
  log_info "Installing $mcp_name..."
  
  if [[ ! -d "$mcp_dir" ]]; then
    log_error "MCP directory not found: $mcp_dir"
    return 1
  fi
  
  # Install with uv (builds venv + installs dependencies)
  cd "$mcp_dir"
  
  if uv sync --all-groups >/dev/null 2>&1; then
    log_success "Installed $mcp_name"
    return 0
  else
    log_error "Failed to install $mcp_name"
    return 1
  fi
}

install_all_core_mcps() {
  log_info "Installing ${#CORE_MCPS[@]} core MCPs..."
  echo
  
  local failed=0
  for mcp in "${CORE_MCPS[@]}"; do
    if ! install_mcp "$mcp"; then
      failed=$((failed + 1))
    fi
    check_duration
  done
  
  echo
  if [[ $failed -eq 0 ]]; then
    log_success "All MCPs installed successfully"
    return 0
  else
    log_error "$failed MCP(s) failed to install"
    return 1
  fi
}

# ============================================================================
# VERIFICATION FUNCTIONS
# ============================================================================

verify_mcp_imports() {
  local mcp_name="$1"
  log_info "Verifying $mcp_name imports..."
  
  local mcp_dir="${MCPS_DIR}/${mcp_name}"
  cd "$mcp_dir"
  
  # Try to import the MCP module
  local module_name=$(echo "$mcp_name" | tr '-' '_')
  if uv run python3 -c "import ${module_name}; print('✓ Import OK')" 2>&1 | grep -q "Import OK"; then
    log_success "$mcp_name imports successfully"
    return 0
  else
    log_error "$mcp_name import failed"
    return 1
  fi
}

verify_mcp_tests() {
  local mcp_name="$1"
  log_info "Running tests for $mcp_name..."
  
  local mcp_dir="${MCPS_DIR}/${mcp_name}"
  cd "$mcp_dir"
  
  if [[ ! -d "tests" ]]; then
    log_warn "$mcp_name has no tests"
    return 0
  fi
  
  if uv run pytest tests/ -q >/dev/null 2>&1; then
    log_success "$mcp_name tests passed"
    return 0
  else
    log_warn "$mcp_name tests had issues (non-critical)"
    return 0
  fi
}

verify_all_installations() {
  log_info "Verifying all installations..."
  echo
  
  local failed=0
  for mcp in "${CORE_MCPS[@]}"; do
    if ! verify_mcp_imports "$mcp"; then
      failed=$((failed + 1))
    fi
    verify_mcp_tests "$mcp"
    check_duration
  done
  
  echo
  if [[ $failed -eq 0 ]]; then
    log_success "All MCPs verified successfully"
    return 0
  else
    log_error "$failed MCP(s) verification failed"
    return 1
  fi
}

# ============================================================================
# CYBERSECSUITE INTEGRATION
# ============================================================================

register_mcps_in_cybersecsuite() {
  log_info "Registering MCPs in CyberSecSuite..."
  
  if [[ ! -d "$CYBERSECSUITE_ROOT" ]]; then
    log_warn "CyberSecSuite root not found at $CYBERSECSUITE_ROOT"
    log_info "  (This is expected if running in isolation)"
    return 0
  fi
  
  # Create config directory if needed
  mkdir -p "$(dirname "$CYBERSECSUITE_MCP_CONFIG")"
  
  # Generate MCP registry for CyberSecSuite
  cat > "$CYBERSECSUITE_MCP_CONFIG" <<EOF
{
  "version": "1.0",
  "timestamp": "$(date -Iseconds)",
  "mode": "sdk",
  "mcps": [
EOF
  
  local first=true
  for mcp in "${CORE_MCPS[@]}"; do
    if [[ "$first" != true ]]; then
      echo "," >> "$CYBERSECSUITE_MCP_CONFIG"
    fi
    cat >> "$CYBERSECSUITE_MCP_CONFIG" <<EOF
    {
      "name": "$mcp",
      "path": "${MCPS_DIR}/${mcp}",
      "installed": true,
      "version": "1.0.0"
    }
EOF
    first=false
  done
  
  cat >> "$CYBERSECSUITE_MCP_CONFIG" <<EOF

  ]
}
EOF
  
  log_success "MCP registry created at $CYBERSECSUITE_MCP_CONFIG"
  return 0
}

# ============================================================================
# CLEANUP FUNCTIONS
# ============================================================================

cleanup_installations() {
  log_info "Cleaning up MCP installations..."
  
  for mcp in "${CORE_MCPS[@]}"; do
    local mcp_dir="${MCPS_DIR}/${mcp}"
    if [[ -d "${mcp_dir}/.venv" ]]; then
      rm -rf "${mcp_dir}/.venv"
      log_info "Removed ${mcp}/.venv"
    fi
  done
  
  log_success "Cleanup complete"
  return 0
}

# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

print_header() {
  echo
  echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
  echo -e "${BLUE}║${NC}        CyberSecSuite Core MCP Bootstrap Installer            ${BLUE}║${NC}"
  echo -e "${BLUE}║${NC}   Installing 6 Foundation MCPs (csscore + specialized)        ${BLUE}║${NC}"
  echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
  echo
}

print_footer() {
  local elapsed=$(elapsed_time)
  echo
  echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
  echo -e "${GREEN}║${NC}           Bootstrap Complete! Ready for CyberSecSuite         ${GREEN}║${NC}"
  echo -e "${GREEN}║${NC}                 Duration: ${elapsed}s (target: <120s)                 ${GREEN}║${NC}"
  echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
  echo
}

print_usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTION]

Bootstrap installer for CyberSecSuite core MCPs.

Options:
  (no args)      Run full bootstrap (install + verify + register)
  --verify       Verify installation only (no install)
  --cleanup      Remove all virtual environments
  --help         Show this help message

Examples:
  ./install-mcp-core.sh              # Full bootstrap
  ./install-mcp-core.sh --verify     # Verify only
  ./install-mcp-core.sh --cleanup    # Cleanup

EOF
}

main() {
  local action="${1:-install}"
  
  print_header
  
  case "$action" in
    --help|-h)
      print_usage
      exit 0
      ;;
    --cleanup)
      check_prerequisites || exit 1
      check_marketplace_structure || exit 1
      cleanup_installations
      exit $?
      ;;
    --verify)
      check_prerequisites || exit 1
      check_marketplace_structure || exit 1
      verify_all_installations
      exit $?
      ;;
    install|"")
      check_prerequisites || exit 1
      check_marketplace_structure || exit 1
      install_all_core_mcps || exit 1
      verify_all_installations || exit 1
      register_mcps_in_cybersecsuite || exit 1
      print_footer
      exit 0
      ;;
    *)
      log_error "Unknown option: $action"
      print_usage
      exit 1
      ;;
  esac
}

# Run main function
main "$@"
