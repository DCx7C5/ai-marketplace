#!/bin/bash
################################################################################
# install-mcp.sh — Install MCPs from the marketplace into CyberSecSuite
#
# This script automates the installation of Model Context Providers (MCPs)
# from the ai-marketplace into a CyberSecSuite instance. It handles:
# - Listing available MCPs from index.json
# - Installing specific MCPs by name
# - Batch installing all MCPs
# - Dependency verification and installation
# - MCP registration in CyberSecSuite configuration
# - Installation verification
#
# Usage:
#   ./install-mcp.sh --help              Show this help message
#   ./install-mcp.sh --list              List all available MCPs
#   ./install-mcp.sh --all               Install all MCPs
#   ./install-mcp.sh <mcp_name>          Install specific MCP
#   ./install-mcp.sh --verify <mcp_name> Verify MCP installation
#
# Requirements:
#   - bash >= 4.0
#   - jq (JSON processor)
#   - uv (Python package manager)
#   - Python >= 3.10
#
################################################################################

set -euo pipefail

# Enable extended debugging if requested
[[ "${DEBUG:-}" == "true" ]] && set -x

# ============================================================================
# CONFIGURATION
# ============================================================================

# Determine the marketplace directory (parent of scripts directory)
readonly MARKETPLACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly SCRIPTS_DIR="${MARKETPLACE_DIR}/scripts"
readonly INDEX_FILE="${MARKETPLACE_DIR}/index.json"
readonly MCPS_DIR="${MARKETPLACE_DIR}/mcps"
readonly DOCS_DIR="${MARKETPLACE_DIR}/docs"

# CyberSecSuite paths (configurable via environment)
readonly CYBERSECSUITE_ROOT="${CYBERSECSUITE_ROOT:-${MARKETPLACE_DIR}/../cybersecsuite}"
readonly CYBERSECSUITE_MCP_DIR="${CYBERSECSUITE_ROOT}/src/csmcp/mcps"
readonly CYBERSECSUITE_CONFIG_DIR="${CYBERSECSUITE_ROOT}/config"

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Exit codes
readonly EXIT_SUCCESS=0
readonly EXIT_INVALID_ARGS=1
readonly EXIT_MCP_NOT_FOUND=2
readonly EXIT_PERMISSION_DENIED=3
readonly EXIT_INSTALL_FAILED=4
readonly EXIT_VERIFY_FAILED=5
readonly EXIT_INVALID_FILE=6

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

# Print error message and exit
error() {
    local -r message="$1"
    local -r exit_code="${2:-${EXIT_INVALID_ARGS}}"
    printf "${RED}✗ ERROR${NC}: %s\n" "$message" >&2
    exit "$exit_code"
}

# Print warning message
warn() {
    local -r message="$1"
    printf "${YELLOW}⚠ WARNING${NC}: %s\n" "$message" >&2
}

# Print success message
success() {
    local -r message="$1"
    printf "${GREEN}✓ SUCCESS${NC}: %s\n" "$message"
}

# Print info message
info() {
    local -r message="$1"
    printf "${BLUE}ℹ INFO${NC}: %s\n" "$message"
}

# Print usage information
usage() {
    cat << 'EOF'
Usage: install-mcp.sh [OPTION] [MCP_NAME]

Install MCP tools from the ai-marketplace into CyberSecSuite.

Options:
  --help                Show this help message and exit
  --list                List all available MCPs in the marketplace
  --all                 Install all MCPs to CyberSecSuite
  --verify <mcp_name>   Verify that an MCP is properly installed
  --info <mcp_name>     Display information about an MCP
  MCP_NAME              Install a specific MCP (e.g., forensic-vault)

Examples:
  ./install-mcp.sh --list
  ./install-mcp.sh forensic-vault
  ./install-mcp.sh --all
  ./install-mcp.sh --verify forensic-vault
  ./install-mcp.sh --info forensic-vault

Environment Variables:
  CYBERSECSUITE_ROOT    Path to CyberSecSuite root (default: ../cybersecsuite)
  DEBUG                 Enable debug output (set DEBUG=true)

For more information, visit: https://github.com/Dystopian/ai-marketplace

EOF
    exit "$EXIT_SUCCESS"
}

# ============================================================================
# FILE & FORMAT VALIDATION
# ============================================================================

# Check if index.json exists and is valid JSON
check_index_file() {
    if [[ ! -f "$INDEX_FILE" ]]; then
        error "Index file not found: $INDEX_FILE" "$EXIT_INVALID_FILE"
    fi

    # Validate JSON format
    if ! jq empty "$INDEX_FILE" 2>/dev/null; then
        error "Invalid JSON in index file: $INDEX_FILE" "$EXIT_INVALID_FILE"
    fi
}

# Extract MCP names from index.json
# Returns space-separated list of MCP names
get_mcp_names() {
    # MCPs are registered as skills with type "mcp"
    # or we look for mcp-specific entries
    jq -r '.skills[]? | select(.type == "mcp" or .name | contains("mcp")) | .name' "$INDEX_FILE" 2>/dev/null | sort
}

# Get count of available MCPs
get_mcp_count() {
    jq '.skills[]? | select(.type == "mcp" or .name | contains("mcp")) | .name' "$INDEX_FILE" 2>/dev/null | wc -l
}

# Check if an MCP exists in the index
mcp_exists() {
    local -r mcp_name="$1"
    jq -e ".skills[]? | select(.name == \"${mcp_name}\")" "$INDEX_FILE" >/dev/null 2>&1
}

# Get MCP metadata from index
get_mcp_info() {
    local -r mcp_name="$1"
    jq ".skills[]? | select(.name == \"${mcp_name}\")" "$INDEX_FILE"
}

# ============================================================================
# DIRECTORY & PERMISSION CHECKS
# ============================================================================

# Check if CyberSecSuite directories exist
check_cybersecsuite_dirs() {
    if [[ ! -d "$CYBERSECSUITE_ROOT" ]]; then
        error "CyberSecSuite root directory not found: $CYBERSECSUITE_ROOT\nSet CYBERSECSUITE_ROOT environment variable." "$EXIT_PERMISSION_DENIED"
    fi

    # Create MCP directory if it doesn't exist
    if [[ ! -d "$CYBERSECSUITE_MCP_DIR" ]]; then
        mkdir -p "$CYBERSECSUITE_MCP_DIR" || \
            error "Cannot create MCP directory: $CYBERSECSUITE_MCP_DIR" "$EXIT_PERMISSION_DENIED"
    fi

    # Create config directory if it doesn't exist
    if [[ ! -d "$CYBERSECSUITE_CONFIG_DIR" ]]; then
        mkdir -p "$CYBERSECSUITE_CONFIG_DIR" || \
            error "Cannot create config directory: $CYBERSECSUITE_CONFIG_DIR" "$EXIT_PERMISSION_DENIED"
    fi
}

# Check write permissions to destination directories
check_write_permissions() {
    if [[ ! -w "$CYBERSECSUITE_MCP_DIR" ]]; then
        error "No write permission to MCP directory: $CYBERSECSUITE_MCP_DIR" "$EXIT_PERMISSION_DENIED"
    fi

    if [[ ! -w "$CYBERSECSUITE_CONFIG_DIR" ]]; then
        error "No write permission to config directory: $CYBERSECSUITE_CONFIG_DIR" "$EXIT_PERMISSION_DENIED"
    fi
}

# ============================================================================
# MCP LISTING
# ============================================================================

# List all available MCPs
list_mcps() {
    check_index_file

    local -r mcp_count=$(get_mcp_count)

    if [[ "$mcp_count" -eq 0 ]]; then
        warn "No MCPs found in marketplace index"
        return "$EXIT_SUCCESS"
    fi

    echo ""
    echo "📦 Available MCPs in marketplace:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    local -i index=1
    while IFS= read -r mcp_name; do
        local -r mcp_info=$(get_mcp_info "$mcp_name")
        local -r description=$(jq -r '.description // "No description"' <<< "$mcp_info")
        local -r version=$(jq -r '.version // "unknown"' <<< "$mcp_info")

        printf "  %2d. ${BLUE}%-30s${NC} (v%s)\n" "$index" "$mcp_name" "$version"
        printf "      %s\n" "$description"
        echo ""
        ((index++))
    done < <(get_mcp_names)

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "\nTotal: %d MCPs available\n" "$mcp_count"
    echo ""
}

# ============================================================================
# MCP INFORMATION
# ============================================================================

# Display information about a specific MCP
display_mcp_info() {
    local -r mcp_name="$1"

    check_index_file

    if ! mcp_exists "$mcp_name"; then
        error "MCP not found: $mcp_name" "$EXIT_MCP_NOT_FOUND"
    fi

    local -r mcp_info=$(get_mcp_info "$mcp_name")

    echo ""
    echo "📋 MCP Information:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  Name:        $(jq -r '.name' <<< "$mcp_info")"
    echo "  Description: $(jq -r '.description // "N/A"' <<< "$mcp_info")"
    echo "  Version:     $(jq -r '.version // "unknown"' <<< "$mcp_info")"
    echo "  Type:        $(jq -r '.type // "unknown"' <<< "$mcp_info")"
    echo "  Location:    $(jq -r '.file // "N/A"' <<< "$mcp_info")"

    # Display dependencies if available
    local -r deps=$(jq -r '.dependencies // empty' <<< "$mcp_info")
    if [[ -n "$deps" ]]; then
        echo "  Dependencies:"
        jq -r '.dependencies[]' <<< "$mcp_info" | while read -r dep; do
            echo "    - $dep"
        done
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# ============================================================================
# DEPENDENCY MANAGEMENT
# ============================================================================

# Get MCP dependencies
get_mcp_dependencies() {
    local -r mcp_name="$1"
    jq -r ".skills[]? | select(.name == \"${mcp_name}\") | .dependencies[]?" "$INDEX_FILE" 2>/dev/null
}

# Install Python dependencies using uv
install_dependencies() {
    local -r mcp_name="$1"
    local -r deps_array=()

    echo "  Checking dependencies for $mcp_name..."

    # Get dependencies from index
    local -r deps=$(get_mcp_dependencies "$mcp_name")

    if [[ -z "$deps" ]]; then
        info "No dependencies required for $mcp_name"
        return "$EXIT_SUCCESS"
    fi

    # Install each dependency with uv
    while IFS= read -r dep; do
        [[ -z "$dep" ]] && continue
        echo "    Installing dependency: $dep"

        if ! cd "$CYBERSECSUITE_ROOT" && uv add "$dep" 2>/dev/null; then
            warn "Failed to install dependency: $dep (may already be installed)"
        fi
    done <<< "$deps"

    return "$EXIT_SUCCESS"
}

# Verify Python imports work
verify_imports() {
    local -r mcp_name="$1"
    local -r imports=$(jq -r ".skills[]? | select(.name == \"${mcp_name}\") | .imports[]?" "$INDEX_FILE" 2>/dev/null)

    if [[ -z "$imports" ]]; then
        return "$EXIT_SUCCESS"
    fi

    local import_check_failed=false

    while IFS= read -r import_module; do
        [[ -z "$import_module" ]] && continue
        echo "    Verifying import: $import_module"

        if ! python3 -c "import $import_module" 2>/dev/null; then
            warn "Import verification failed: $import_module"
            import_check_failed=true
        fi
    done <<< "$imports"

    if [[ "$import_check_failed" == "true" ]]; then
        return "$EXIT_VERIFY_FAILED"
    fi

    return "$EXIT_SUCCESS"
}

# ============================================================================
# MCP INSTALLATION
# ============================================================================

# Install a single MCP
install_single_mcp() {
    local -r mcp_name="$1"

    check_index_file
    check_cybersecsuite_dirs
    check_write_permissions

    # Verify MCP exists
    if ! mcp_exists "$mcp_name"; then
        error "MCP not found in marketplace: $mcp_name" "$EXIT_MCP_NOT_FOUND"
    fi

    echo ""
    echo "📥 Installing MCP: ${BLUE}$mcp_name${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Get MCP metadata
    local -r mcp_info=$(get_mcp_info "$mcp_name")
    local -r mcp_file=$(jq -r '.file // empty' <<< "$mcp_info")
    local -r mcp_version=$(jq -r '.version // "unknown"' <<< "$mcp_info")

    if [[ -z "$mcp_file" ]]; then
        error "MCP file path not found in index for: $mcp_name" "$EXIT_INSTALL_FAILED"
    fi

    local -r src_path="${MARKETPLACE_DIR}/${mcp_file}"

    # Verify source file exists
    if [[ ! -f "$src_path" ]]; then
        error "MCP source file not found: $src_path" "$EXIT_INSTALL_FAILED"
    fi

    # Get destination filename
    local -r dest_filename=$(basename "$src_path")
    local -r dest_path="${CYBERSECSUITE_MCP_DIR}/${dest_filename}"

    # Copy MCP file
    echo "  1. Copying MCP module..."
    if ! cp "$src_path" "$dest_path"; then
        error "Failed to copy MCP file to $dest_path" "$EXIT_INSTALL_FAILED"
    fi
    echo "     ✓ Copied to: $dest_path"

    # Install dependencies
    echo "  2. Installing dependencies..."
    if ! install_dependencies "$mcp_name"; then
        warn "Some dependencies may have failed to install"
    else
        echo "     ✓ Dependencies installed"
    fi

    # Verify imports
    echo "  3. Verifying imports..."
    if verify_imports "$mcp_name"; then
        echo "     ✓ All imports verified"
    else
        warn "Import verification had issues, but continuing..."
    fi

    # Register MCP in CyberSecSuite configuration
    echo "  4. Registering in CyberSecSuite..."
    register_mcp "$mcp_name" "$dest_path" "$mcp_version" || \
        warn "Failed to register MCP in configuration"

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    success "MCP installed successfully: $mcp_name (v$mcp_version)"
    echo ""
}

# Install all MCPs
install_all_mcps() {
    check_index_file

    local -r mcp_count=$(get_mcp_count)

    if [[ "$mcp_count" -eq 0 ]]; then
        warn "No MCPs found to install"
        return "$EXIT_SUCCESS"
    fi

    echo ""
    echo "📥 Installing all MCPs (${BLUE}$mcp_count${NC} total)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    local -i installed=0
    local -i failed=0

    while IFS= read -r mcp_name; do
        if install_single_mcp "$mcp_name" 2>/dev/null; then
            ((installed++))
        else
            ((failed++))
            warn "Failed to install: $mcp_name"
        fi
    done < <(get_mcp_names)

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "Installation Summary: %d succeeded, %d failed\n" "$installed" "$failed"
    echo ""

    if [[ "$failed" -gt 0 ]]; then
        return "$EXIT_INSTALL_FAILED"
    fi

    return "$EXIT_SUCCESS"
}

# ============================================================================
# MCP REGISTRATION
# ============================================================================

# Register MCP in CyberSecSuite configuration
register_mcp() {
    local -r mcp_name="$1"
    local -r mcp_path="$2"
    local -r mcp_version="${3:-unknown}"

    local -r config_file="${CYBERSECSUITE_CONFIG_DIR}/mcps.json"

    # Initialize config file if it doesn't exist
    if [[ ! -f "$config_file" ]]; then
        echo "{\"mcps\": []}" > "$config_file"
    fi

    # Check if MCP is already registered
    if jq -e ".mcps[] | select(.name == \"${mcp_name}\")" "$config_file" >/dev/null 2>&1; then
        info "MCP already registered: $mcp_name (updating...)"
        # Remove old entry
        local -r temp_file=$(mktemp)
        jq ".mcps |= map(select(.name != \"${mcp_name}\"))" "$config_file" > "$temp_file"
        mv "$temp_file" "$config_file"
    fi

    # Add new registration entry
    local -r registration_entry="{
        \"name\": \"${mcp_name}\",
        \"path\": \"${mcp_path}\",
        \"version\": \"${mcp_version}\",
        \"installed_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
        \"enabled\": true
    }"

    if ! jq ".mcps += [${registration_entry}]" "$config_file" > "${config_file}.tmp"; then
        warn "Failed to update MCP registration"
        rm -f "${config_file}.tmp"
        return "$EXIT_INSTALL_FAILED"
    fi

    mv "${config_file}.tmp" "$config_file"
    echo "     ✓ Registered in: $config_file"

    return "$EXIT_SUCCESS"
}

# ============================================================================
# MCP VERIFICATION
# ============================================================================

# Verify that an MCP is properly installed
verify_mcp() {
    local -r mcp_name="$1"

    check_cybersecsuite_dirs

    local -r config_file="${CYBERSECSUITE_CONFIG_DIR}/mcps.json"

    if [[ ! -f "$config_file" ]]; then
        error "MCP configuration file not found: $config_file" "$EXIT_VERIFY_FAILED"
    fi

    # Check if MCP is registered
    if ! jq -e ".mcps[] | select(.name == \"${mcp_name}\")" "$config_file" >/dev/null 2>&1; then
        error "MCP not registered: $mcp_name" "$EXIT_VERIFY_FAILED"
    fi

    # Get MCP path from config
    local -r mcp_path=$(jq -r ".mcps[] | select(.name == \"${mcp_name}\") | .path" "$config_file")

    # Verify file exists
    if [[ ! -f "$mcp_path" ]]; then
        error "MCP file not found at: $mcp_path" "$EXIT_VERIFY_FAILED"
    fi

    # Verify imports
    if verify_imports "$mcp_name"; then
        success "MCP verified successfully: $mcp_name"
        return "$EXIT_SUCCESS"
    else
        error "MCP import verification failed: $mcp_name" "$EXIT_VERIFY_FAILED"
    fi
}

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

main() {
    # Handle no arguments
    if [[ $# -eq 0 ]]; then
        usage
    fi

    case "${1:-}" in
        -h|--help)
            usage
            ;;
        -l|--list)
            list_mcps
            ;;
        -a|--all)
            install_all_mcps
            ;;
        -v|--verify)
            if [[ $# -lt 2 ]]; then
                error "Option --verify requires MCP name argument"
            fi
            verify_mcp "$2"
            ;;
        -i|--info)
            if [[ $# -lt 2 ]]; then
                error "Option --info requires MCP name argument"
            fi
            display_mcp_info "$2"
            ;;
        -*)
            error "Unknown option: $1" "$EXIT_INVALID_ARGS"
            ;;
        *)
            # Install specific MCP
            install_single_mcp "$1"
            ;;
    esac
}

# Run main function
main "$@"

exit "$EXIT_SUCCESS"
