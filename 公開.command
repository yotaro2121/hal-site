#!/bin/zsh
# hal-site をインターネットに公開(GitHub Pages へプッシュ)するスクリプト。
# Finder でダブルクリックして使う。
cd "$(dirname "$0")"

echo "=== /HAL/ サイト公開 ==="
git add -A
if git diff --cached --quiet; then
  echo "変更はありません(すでに最新の状態です)"
else
  git commit -m "update: $(date '+%Y-%m-%d %H:%M')"
  if git push; then
    echo ""
    echo "✔ 公開しました。反映まで1〜2分かかります。"
  else
    echo ""
    echo "✘ プッシュに失敗しました。ネット接続を確認するか、Claude Code に相談してください。"
  fi
fi
echo ""
read -s -k 1 "?何かキーを押すと閉じます"
