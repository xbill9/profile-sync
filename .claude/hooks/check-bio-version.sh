#!/usr/bin/env bash
# PostToolUse: tell Claude when bio.md was edited without setting version to today.
f=$(jq -r '.tool_response.filePath // .tool_input.file_path // empty')
[ "$(basename "$f")" = "bio.md" ] && [ -f "$f" ] || exit 0

today=$(date +%F)
version=$(sed -n 's/^version:[[:space:]]*//p' "$f" | head -1)
[ "$version" = "$today" ] && exit 0

jq -n --arg msg "bio.md version is '$version' but today is $today. Set the frontmatter version to $today." \
  '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $msg}}'
