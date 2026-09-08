#!/usr/bin/env node

import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, '..');
const defaultSource = resolve(repoRoot, 'interactive/git-mental-model/curriculum.js');
const argumentsList = process.argv.slice(2);
const useHead = argumentsList.includes('--head');
const routeArgument = argumentsList.find(value => value.startsWith('--route='));
const selectedRoute = routeArgument?.slice('--route='.length);
const pathArgument = argumentsList.find(value => !value.startsWith('--'));
const sourcePath = pathArgument ? resolve(pathArgument) : defaultSource;
const sourceLabel = useHead ? 'HEAD:interactive/git-mental-model/curriculum.js' : sourcePath;

function curriculumLessons(path, original) {
  const marker = 'const lessons = {';
  assert.equal(original.split(marker).length, 2, 'curriculum lesson registry must have one extraction point');
  const instrumented = original.replace(marker, 'const lessons = globalThis.__curriculumLessons = {');
  const context = {
    URLSearchParams,
    location: { search: '' },
    matchMedia: () => ({ matches: false }),
    document: { querySelector: () => null },
  };
  vm.runInNewContext(instrumented, context, { filename: path });
  assert.ok(context.__curriculumLessons, 'failed to load the displayed curriculum states');
  return context.__curriculumLessons;
}

function cleanEnv() {
  const env = { ...process.env };
  for (const key of Object.keys(env)) {
    if (key === 'GIT_DIR' || key === 'GIT_WORK_TREE' || key === 'GIT_INDEX_FILE' ||
        key === 'GIT_OBJECT_DIRECTORY' || key === 'GIT_ALTERNATE_OBJECT_DIRECTORIES' ||
        key === 'GIT_CEILING_DIRECTORIES' || key === 'GIT_TEMPLATE_DIR' ||
        key === 'GIT_HOOKS_PATH' || key.startsWith('GIT_CONFIG_')) delete env[key];
  }
  delete env.BASH_ENV;
  delete env.ENV;
  return {
    ...env,
    GIT_CONFIG_NOSYSTEM: '1',
    GIT_CONFIG_GLOBAL: '/dev/null',
    GIT_TERMINAL_PROMPT: '0',
    GIT_PAGER: 'cat',
    LC_ALL: 'C',
  };
}

const gitEnv = cleanEnv();

function git(repo, args, options = {}) {
  const result = spawnSync('git', args, {
    cwd: repo,
    env: gitEnv,
    encoding: options.encoding === null ? null : 'utf8',
    input: options.input,
  });
  if (options.check !== false && result.status !== 0) {
    throw new Error(`git ${args.join(' ')} failed (${result.status})\n${result.stdout ?? ''}${result.stderr ?? ''}`);
  }
  return result;
}

function initRepo(prefix) {
  const repo = mkdtempSync(resolve(tmpdir(), prefix));
  git(repo, ['init', '-q', '-b', 'main']);
  git(repo, ['config', 'user.name', 'Curriculum Command Test']);
  git(repo, ['config', 'user.email', 'curriculum-test@example.invalid']);
  git(repo, ['config', 'commit.gpgSign', 'false']);
  git(repo, ['config', 'gc.auto', '0']);
  git(repo, ['config', 'maintenance.auto', 'false']);
  git(repo, ['config', 'gc.reflogExpire', 'never']);
  git(repo, ['config', 'gc.reflogExpireUnreachable', 'never']);
  return repo;
}

function commitFile(repo, filename, content, message) {
  writeFileSync(resolve(repo, filename), content);
  git(repo, ['add', filename]);
  git(repo, ['commit', '-q', '-m', message]);
  return git(repo, ['rev-parse', 'HEAD']).stdout.trim();
}

function commandWithIds(command, ids) {
  let resolved = command;
  for (const [label, oid] of Object.entries(ids)) resolved = resolved.replaceAll(`<${label}-id>`, oid);
  assert.doesNotMatch(resolved, /<[A-Z][^>]*-id>/, `unresolved teaching placeholder in: ${command}`);
  return resolved;
}

function runDisplayedStep(repo, route, index, command, ids) {
  const resolved = commandWithIds(command, ids);
  const result = spawnSync('bash', ['-euo', 'pipefail', '-c', resolved], {
    cwd: repo,
    env: gitEnv,
    encoding: 'utf8',
  });
  assert.equal(result.status, 0,
    `${route} step ${index + 1} failed\ncommand:\n${resolved}\nstdout:\n${result.stdout}\nstderr:\n${result.stderr}`);
}

function assertFiveStepChoice(lesson, choice) {
  const values = Array.from(lesson.choices, item => item.value);
  assert.ok(values.includes(choice), `missing displayed choice ${choice}`);
  const states = Array.from(lesson.states(choice));
  assert.equal(states.length, 5, `${choice} must remain a five-step path`);
  for (const [index, state] of states.entries()) {
    assert.equal(typeof state.command, 'string', `${choice} step ${index + 1} has no displayed command`);
    assert.ok(state.command.length > 0, `${choice} step ${index + 1} has an empty displayed command`);
  }
  return states;
}

function recoverySetup() {
  const repo = initRepo('my-git-curriculum-recovery-');
  const C1 = commitFile(repo, 'ledger.txt', 'state=baseline\n', 'baseline');
  const C2 = commitFile(repo, 'recoverable.txt', 'recoverable commit\n', 'recoverable commit');
  git(repo, ['reset', '--hard', C1]);
  git(repo, ['update-ref', '-d', 'ORIG_HEAD']);
  git(repo, ['switch', '-q', '-c', 'discard-after-expiry']);
  const C3 = commitFile(repo, 'expiring.txt', 'state=expires\n', 'discard after expiry');
  git(repo, ['switch', '-q', 'main']);
  git(repo, ['branch', '-D', 'discard-after-expiry']);
  git(repo, ['update-ref', '-d', 'ORIG_HEAD']);
  return { repo, ids: { C2, C3 } };
}

function runRecovery(lesson, choice) {
  const states = assertFiveStepChoice(lesson, choice);
  const { repo, ids } = recoverySetup();
  try {
    states.forEach((state, index) => runDisplayedStep(repo, `recovery/${choice}`, index, state.command, ids));
    assert.equal(git(repo, ['rev-parse', 'refs/heads/recovered']).stdout.trim(), ids.C2,
      `recovery/${choice}: recovered must point exactly to C2`);
    assert.equal(git(repo, ['cat-file', '-e', 'recovered^{commit}'], { check: false }).status, 0,
      `recovery/${choice}: recovered^{commit} must remain readable`);
    assert.notEqual(git(repo, ['cat-file', '-e', `${ids.C3}^{commit}`], { check: false }).status, 0,
      `recovery/${choice}: C3 must be missing after reflog expiration and prune`);
    console.log(`ok: recovery/${choice} ran 5 displayed steps; recovered=C2; C3 exit is nonzero`);
  } finally {
    rmSync(repo, { recursive: true, force: true });
  }
}

function storageSetup() {
  const repo = initRepo('my-git-curriculum-storage-');
  const C = commitFile(repo, 'stable.txt', 'stable content\n', 'stable commit');
  const O = git(repo, ['hash-object', '-w', '--stdin'], { input: 'disposable orphan\n' }).stdout.trim();
  assert.equal(git(repo, ['cat-file', '-e', `${O}^{blob}`], { check: false }).status, 0,
    'storage setup must create a readable orphan');
  return { repo, ids: { C, O } };
}

function runStorage(lesson, choice) {
  const states = assertFiveStepChoice(lesson, choice);
  const { repo, ids } = storageSetup();
  try {
    states.forEach((state, index) => runDisplayedStep(repo, `storage/${choice}`, index, state.command, ids));
    const before = readFileSync(resolve(repo, 'show-before.txt'));
    const after = readFileSync(resolve(repo, 'show-after.txt'));
    assert.deepEqual(after, before, `storage/${choice}: stable C git show output changed byte-for-byte`);
    assert.equal(git(repo, ['cat-file', '-e', `${ids.C}^{commit}`], { check: false }).status, 0,
      `storage/${choice}: stable C must remain readable`);
    if (choice === 'prune') {
      assert.notEqual(git(repo, ['cat-file', '-e', `${ids.O}^{blob}`], { check: false }).status, 0,
        'storage/prune: O must be missing and its cat-file exit must be nonzero');
    }
    console.log(`ok: storage/${choice} ran 5 displayed steps; stable C output is byte-identical${choice === 'prune' ? '; O exit is nonzero' : ''}`);
  } finally {
    rmSync(repo, { recursive: true, force: true });
  }
}

const sourceText = useHead
  ? execFileSync('git', ['show', 'HEAD:interactive/git-mental-model/curriculum.js'], {
      cwd: repoRoot, env: gitEnv, encoding: 'utf8',
    })
  : readFileSync(sourcePath, 'utf8');
const lessons = curriculumLessons(sourceLabel, sourceText);
assert.deepEqual(Array.from(lessons.recovery.choices, item => item.value), ['recover', 'expire']);
assert.deepEqual(Array.from(lessons.storage.choices, item => item.value), ['repack', 'prune']);
const routes = {
  'recovery/recover': () => runRecovery(lessons.recovery, 'recover'),
  'recovery/expire': () => runRecovery(lessons.recovery, 'expire'),
  'storage/repack': () => runStorage(lessons.storage, 'repack'),
  'storage/prune': () => runStorage(lessons.storage, 'prune'),
};
if (selectedRoute) {
  assert.ok(routes[selectedRoute], `unknown route: ${selectedRoute}`);
  routes[selectedRoute]();
} else {
  Object.values(routes).forEach(run => run());
}
console.log(`ok: curriculum command regression passed for ${sourceLabel}`);
