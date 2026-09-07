# Why Learn Git When AI Can Operate It?

English | [中文](../why-learn-git.md)

AI can perform more and more operations for us. Yet the questions we ask, the options we notice, and the results we accept still depend on what we understand. Without a concept in mind, we may never think to use it or notice its absence from a plausible answer.

This is why I maintain this handbook: **to explain enduring engineering ideas so people can make informed decisions with AI.**

## The emphasis of learning is changing

Learning a tool has usually meant two things: understanding its design and becoming fluent in its operations. Under time pressure, it is easy to memorize commands and postpone the design.

Agents can now handle many operations. Understanding becomes more visible: knowing that changes can be verified separately prompts you to ask for smaller commits. Knowing that a branch is a reference suggests checking for surviving commits after deleting it. Knowing that the working tree and index can differ prompts you to ask whether the tests and commit describe the same code.

Operational knowledge still matters. People need to read critical commands, recognize destructive actions, and verify ideas through small experiments. Practice gives abstractions evidence; AI can lower the cost of that practice.

## Why learn these ideas through Git?

Git combines content-addressed objects, snapshots, named references, and common ancestry. These ideas transfer to caches, artifacts, collaboration, and recovery.

Some boundaries deserve particular attention:

- **A commit refers to a snapshot; a branch points to a commit.** A branch is not a separate copy of the files.
- **The index describes the complete next snapshot.** It is more than a list of filenames waiting to be committed.
- **Content identity does not establish correctness.** An object ID identifies a version; it does not prove business behavior or replace author authentication.
- **Recovery has a scope.** Git can help recover recorded code, but cannot automatically retract messages or undo database writes.

See [Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects) and [Branches in a Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell).

Git’s value does not require claiming that every alternative is obsolete. Centralized and distributed systems make different tradeoffs. Understand the constraints before comparing designs; see [Git and SVN](git-vs-svn_en.md).

## How this handbook teaches

1. **Build understanding.** Start with a concrete question about snapshots, objects, references, or history. Predict before observing.
2. **Test understanding.** Use pausable animations, temporary repositories, and expected output to check whether an explanation predicts the result.
3. **Apply understanding.** Organize agent changes into reviewable commits, bind verification to a specific revision, then decide whether to integrate and release.

An animation makes relationships visible. Understanding means predicting what happens when a condition changes and recognizing what you do not know.

## What people own, and how AI helps

AI can explain a graph, generate an experiment, compare alternatives, execute authorized operations, and identify review leads. People need to understand the goal and boundaries, evaluate evidence, and take responsibility for accepting change. Teams can assign approvals through policy; “the AI approved it” cannot carry the responsibility alone.

When an agent says “fixed, all tests green,” you should be able to ask:

- Does the fix stay within the intended behavior?
- Were tests run on the final commit or a working tree with additional edits?
- If the change fails after integration, which states can be restored and which require compensation?

Git is one foundation of change control. The complete system also needs tests, review, permissions, artifacts, and release records.

## Start here

Open the [interactive learning page](https://xirong.github.io/my-git/interactive/git-mental-model/?lang=en), then follow the [learning path](git-learning-path_en.md) through the articles, interactives, and temporary-repository labs for all ten topics. Reading material or running a script still needs prediction, reproduction, and transfer to check understanding; then [accept an agent change end to end](../../05-ai-native-development/05-ai-native-development_en/ai-change-control-loop_en.md). When you need to choose between the design, single-change, and team-collaboration paths, use the [knowledge map](knowledge-map_en.md).

Our aim: **let understanding guide judgment, and let tools carry out the work.**
