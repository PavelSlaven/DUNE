set -e
cd /srv/library/dune/worktrees/p12
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
G="git -c lfs.storage=$PWD/.tmp/p12/lfs -c user.name=PavelSlaven -c user.email=55245062+PavelSlaven@users.noreply.github.com"
M=/srv/dune/tasks/p12
$G add .github/workflows/release.yml .github/workflows/claude-code-review.yml
$G commit -q -F $M/msg1.txt
$G add packaging resources/bin/THIRD_PARTY_ASSETS_RU.txt resources/bin/windowed.bat .gitignore
$G commit -q -F $M/msg2.txt
$G add README.md docs/screenshots
$G commit -q -F $M/msg3.txt
echo status:
git status --short | head -10
git log --oneline -4
git ls-files -s packaging/d2tm.sh
