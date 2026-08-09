# Getting this running in Claude Code

## 1. Unzip and make it a repo

    unzip BulletsOfFury_0809k.zip
    cd BulletsOfFury
    git init
    git add -A
    git commit -m "Bullets of Fury — import from chat sessions through 0809k"

That first commit is the point of the whole move. Every drop until now has been a full zip with
no diff; from here you can see exactly what changed, and revert a bad pass in one command instead
of unzipping the previous build.

## 2. Dependencies

    node --version            # 18+ is fine; the suite is plain node, no packages
    pip install playwright
    playwright install chromium

Node needs nothing installed — `test_fl.js` runs standalone. Playwright is only for `shoot.py`.

## 3. Check it works

    node --check assets/game.js
    node _BUILD_SOURCE/test_fl.js | tail -3
    python3 _BUILD_SOURCE/shoot.py --state TITLE --out _shots

The third one is the important one. If you get a title screen PNG, the capture loop is live.

## 4. Start Claude Code

    claude

It reads `CLAUDE.md` automatically — that carries the art rules, the traps this codebase has, and
the current open list.

## Suggested workflow

    branch per drop           git checkout -b drop-0809l
    verify before delivering  node --check && test_fl.js && shoot.py
    commit with the passover  the docs/ note and the code change in one commit

The single habit worth keeping: **capture a screenshot of anything visual before saying it works.**
Most of the bugs that survived longest in this project survived because the suite was green and
nobody could see the screen.
