#!/usr/bin/env python3

import os
import sys
import subprocess
import re


def run_git(repo, *args):
    return subprocess.check_output(
        ['git', '-C', repo] + list(args),
        stderr=subprocess.DEVNULL,
        text=True
    ).strip()


def checkout(repo, branch):
    subprocess.call(
        ['git', '-C', repo, 'checkout', branch],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def find_branch(branches, suffix):
    matches = [b for b in branches if b.lower().replace('-', '').endswith(suffix)]
    return matches[0] if len(matches) == 1 else None


def check_branches(repo):
    branches = run_git(repo, 'branch', '--format=%(refname:short)').splitlines()
    bf = find_branch(branches, '-branch-for-merge')
    pb = find_branch(branches, '-personal_branch')
    tb = find_branch(branches, '-temp-branch')
    return {
        'count': len(branches),
        'main': 'main' in branches,
        'bf': bf is not None,
        'pb': pb is not None,
        'tb': tb is not None,
        'bf_name': bf,
        'pb_name': pb
    }


def list_files(repo):
    return [
        f for f in os.listdir(repo)
        if os.path.isfile(os.path.join(repo, f)) and f != '.gitignore'
    ]


def check_files(repo, branches):
    results = {}

    # branch-for-merge
    checkout(repo, branches['bf_name'])
    files = list_files(repo)
    results['bf_Assignment'] = 'Assignment.txt' in files
    results['bf_Icarus'] = any(f.startswith('Icarus') for f in files)

    # personal_branch
    checkout(repo, branches['pb_name'])
    files = list_files(repo)
    results['pb_Assignment'] = 'Assignment.txt' in files
    results['pb_Goblet'] = any(f.startswith('Goblet') for f in files)

    # main
    checkout(repo, 'main')
    files = list_files(repo)
    results['main_Icarus'] = any(f.startswith('Icarus') for f in files)
    results['main_noGoblet'] = not any(f.startswith('Goblet') for f in files)

    return results


def check_instructions(repo, branches):
    info = {}

    # conflict resolution commit
    log = run_git(repo, 'log', '--oneline')
    info['conflict_resolved'] = 'resolved conflict with Assignment.txt' in log

    # merge into main
    checkout(repo, 'main')
    logm = run_git(repo, 'log', '--oneline')
    merge_pattern = rf"Merge branch .*{re.escape(branches['bf_name'])}"
    info['merged_bf_to_main'] = bool(re.search(merge_pattern, logm))

    # temp branch deletion
    br = run_git(repo, 'branch', '--format=%(refname:short)').splitlines()
    info['temp_deleted'] = find_branch(br, '-temp-branch') is None

    return info


def grade_repo(repo):
    print(f"\n=== Grading {repo} ===")
    b = check_branches(repo)
    print(
        f"Branches: {b['count']} (expect 3) | main:{b['main']} | "
        f"bf:{b['bf']} | pb:{b['pb']} | temp exists:{b['tb']}"
    )
    if b['main'] and b['bf'] and b['pb']:
        f = check_files(repo, b)
        print(
            "branch-for-merge ➔ Assignment:", f['bf_Assignment'],
            "Icarus:", f['bf_Icarus']
        )
        print(
            "personal_branch   ➔ Assignment:", f['pb_Assignment'],
            "Goblet:", f['pb_Goblet']
        )
        print(
            "main              ➔ Icarus:", f['main_Icarus'],
            "no Goblet:", f['main_noGoblet']
        )
        i = check_instructions(repo, b)
        print(
            "Instr: conflict_resolved:", i['conflict_resolved'],
            "merged_bf_to_main:", i['merged_bf_to_main'],
            "temp_deleted:", i['temp_deleted']
        )
    else:
        print("Missing required branches; skipping file/instruction checks.")


if __name__ == '__main__':
    repo_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    grade_repo(repo_path)
