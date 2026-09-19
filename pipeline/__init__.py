"""The authoring pipeline, v2. Design: research/pipeline/PIPELINE.md.

Takes a topic directory from `not_started` to `ready` and does nothing else.
Stages are functions over the topic directory; the artifact is the state.

    .venv/bin/python -m pipeline author <slug>
    .venv/bin/python -m pipeline status <slug>
"""
