cd /srv/library/dune/worktrees/p10c
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
L=.tmp/p10c/merge1
mkdir -p $L/tmp
CCACHE_DISABLE=1 DUNE_DEPS_DIR=/srv/library/dune/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > $L/build.log 2>&1
echo "build exit=$?"
D=$(ls -td .tmp/out/logs/*/ | head -1)
tail -n 3 $D/ctest.log
echo "P8A passed: $(grep -c 'P8A .*Passed' $D/ctest.log); P10C passed: $(grep -c 'P10C .*Passed' $D/ctest.log)"
grep -c 'Imminent crash' $D/game-dummy.log $D/stdout-dummy.log
for s in ui_audit_list_and_scales.py ui_audit_unknown_scene.py ui_audit_main_menu_png.py ui_audit_part2_catalog.py ui_audit_part2_scenes.py ui_audit_part3a_catalog.py ui_audit_part3a_scenes.py ui_audit_part3b_catalog.py ui_audit_part3b_scenes.py ui_audit_part3c_catalog.py ui_audit_part3c_scenes.py ui_audit_saves.py ui_audit_language.py ui_audit_translation.py; do
  TMPDIR=$PWD/$L/tmp LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/$s --run-dir .tmp/out/run/bin > $L/run-$s.log 2>&1
  echo "$s exit=$?"
done
tail -n 2 $L/run-ui_audit_translation.py.log
python3 -B -m unittest discover -s tools/ui-audit/tests -p 'test_*.py' > $L/py-all.log 2>&1; echo "py-all exit=$?"; tail -1 $L/py-all.log
python3 -B tools/ui-audit/extract_keys.py --root . --out $L/keys-raw.tsv; echo "extract exit=$?"
python3 -B tools/ui-audit/check_keys.py --keys tools/ui-audit/keys.tsv --raw $L/keys-raw.tsv --binding-check src/controls/cKeyBindings.cpp:findConflict > $L/check-keys.log 2>&1; echo "check_keys exit=$?"; grep 'freshness' $L/check-keys.log
K=$(($(wc -l < $L/keys-raw.tsv) - 1))
python3 -B .tmp/p10c/check_keys_tsv.py $K; echo "keys_tsv exit=$?"
rm -rf tests/ui_audit/__pycache__ tools/ui-audit/__pycache__ tools/ui-audit/tests/__pycache__
rm -rf .tmp/out/logs/*/previous-run
git status --short | head
