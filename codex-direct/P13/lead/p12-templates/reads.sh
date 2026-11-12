set -e
B=/srv/dune/tasks/p12/readbase
rm -rf $B
mkdir -p $B/fork
G="git -C /srv/dune/worktrees/u63"
$G archive 0d186e8b1 .github/workflows/build_pr.yml install_dependencies_ubuntu.sh install_dependencies_macosx.sh resources/bin/settings.ini src/context/AudioContext.cpp | tar -x -C $B
$G archive 9208dcf5a .github/workflows/release.yml packaging/RELEASE_NOTES.md packaging/LINUX_README.txt packaging/MACOS_README.txt packaging/WINDOWS_README.txt README.md | tar -x -C $B/fork
R=$(ls /srv/novgorod-work/codex-direct/home/sessions/2026/11/12/rollout-*01a1d122-364d-71a2-97b4-91f6300ba59f.jsonl)
cd $B
python3 /srv/dune/tasks/load-check/check-reads.py $R \
 fork/.github/workflows/release.yml fork/packaging/RELEASE_NOTES.md fork/packaging/LINUX_README.txt fork/packaging/MACOS_README.txt fork/packaging/WINDOWS_README.txt fork/README.md:1-45 \
 .github/workflows/build_pr.yml install_dependencies_ubuntu.sh install_dependencies_macosx.sh resources/bin/settings.ini:1-100 src/context/AudioContext.cpp:55-75
echo exit=$?
