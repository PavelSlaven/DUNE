S = 'C:/Users/Slaven/AppData/Local/Temp/claude/570e86ef5805dee8/ccfbda10-8ab1-41c6-ab77-cb504ef7f2ea/scratchpad/p12/'
tail = '\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n'
msgs = {
    'msg1.txt': ('Add the SDL3 release workflow and drop the Claude review workflow\n\n'
                 'Behavior changes: tagged releases for Windows, Linux and macOS are built and published from the '
                 'port; the claude-review check is gone (owner decision R82).'),
    'msg2.txt': ('Add SDL3 release packaging and installation notes\n\n'
                 'Behavior changes: the common asset archive carries the HD packs, scenes, campaigns, music and '
                 'settings without the classic packs; the Linux archive bundles its SDL3 libraries and starts '
                 'through d2tm.sh; the third-party asset notice ships with the port fonts; the Windows windowed '
                 'launcher matches the fork; the generated Windows binary is ignored.'),
    'msg3.txt': ('Add the author introduction and the screenshot gallery\n\n'
                 'Behavior changes: README opens with the fork introduction, the five fork screenshots, download '
                 'instructions and the font notice before the original README.'),
}
for name, body in msgs.items():
    open(S + name, 'w', encoding='utf-8', newline='\n').write(body + tail)

script = r'''set -e
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
'''
open(S + 'commit.sh', 'w', encoding='utf-8', newline='\n').write(script)
print('ok')
