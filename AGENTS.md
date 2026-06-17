# AGENTS.md

This project is a Life Copilot MVP.

The product goal is to help procrastination-prone users make real progress on important life tasks by using AI to parse tasks, judge priority, create small next actions, remind the user, review progress, and learn from behavior patterns.

Do not build a generic todo app.

Do not build a complex multi-agent system in the MVP.

## MVP Scope

Implement only:

1. natural language task capture;
2. task parsing;
3. priority classification;
4. plan generation;
5. reminders;
6. review/retrospective flow;
7. basic memory;
8. token-aware model provider abstraction.

Do not implement unless explicitly requested:

1. LangGraph;
2. multi-agent orchestration;
3. vector database;
4. autonomous browser control;
5. broad third-party integrations;
6. medical diagnosis;
7. investment advice;
8. unsupervised external actions.

## Architecture Rules

Use ordinary workflow services first.

All LLM calls must go through ModelProvider.

All scheduled work must go through the task queue.

All persistent user state must be stored in PostgreSQL.

All sensitive external actions must require user confirmation.

Prefer simple, testable code over clever abstractions.

## Product Rules

The app must reduce user burden.

The app must not shame the user.

The app should always prefer the smallest useful next action.

The app should distinguish urgent, important, optional, and low-value tasks.

The app should track what worked, what failed, and why.

The app should control token cost and avoid unnecessary model calls.

The app should prepare for future automation, but the MVP must remain narrow.

## Completion Report

After each task, report:

1. files changed;
2. how to run;
3. how to test;
4. what is mocked;
5. risks or limitations;
6. recommended next task.
