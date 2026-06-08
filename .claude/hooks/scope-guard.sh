#!/usr/bin/env bash
# Scope Guard: warn before Builder writes project files without an approved blueprint.
# Preference: warnings only. Always exits 0 (never blocks).

INPUT=$(cat)

# Extract file_path from tool JSON input (Write and Edit both use file_path)
FILE_PATH=""
if command -v python3 &>/dev/null; then
    FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('file_path', d.get('path', '')))
except Exception:
    print('')
" 2>/dev/null || true)
fi

# Only check paths inside projects/<project-name>/
[[ -z "$FILE_PATH" ]] && exit 0
[[ ! "$FILE_PATH" =~ ^projects/([^/]+)/ ]] && exit 0

PROJECT_NAME="${BASH_REMATCH[1]}"
BLUEPRINT="projects/$PROJECT_NAME/blueprint.md"

# No blueprint — warn
if [[ ! -f "$BLUEPRINT" ]]; then
    echo "SCOPE GUARD WARNING: No blueprint.md for project '$PROJECT_NAME'"
    echo "  Target file: $FILE_PATH"
    echo "  Builder requires an approved blueprint before creating project files."
    exit 0
fi

# Blueprint found — check if approved or in progress.
# Template default lists all options with "/" separators:  **Статус:** draft / approved / ...
# A filled blueprint has a single value:  **Статус:** approved
STATUS_LINE=$(grep -im1 'татус' "$BLUEPRINT" 2>/dev/null || true)
if echo "$STATUS_LINE" | grep -iq 'approved' && ! echo "$STATUS_LINE" | grep -q '/'; then
    exit 0
fi
if echo "$STATUS_LINE" | grep -iq 'in progress' && ! echo "$STATUS_LINE" | grep -q '/'; then
    exit 0
fi

STATUS_LINE=$(grep -im1 'татус' "$BLUEPRINT" 2>/dev/null || echo "(status field not found)")
echo "SCOPE GUARD WARNING: Blueprint not yet approved"
echo "  Project: $PROJECT_NAME"
echo "  $STATUS_LINE"
echo "  Complete Human Approval and set Статус: approved before Builder proceeds."
exit 0
