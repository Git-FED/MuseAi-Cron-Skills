# Skill format

Each `*.skill.md` starts with YAML-like `key: value` frontmatter. Required fields are `name`, `enabled`, `mode`, `timeout`, and `retries`; non-runonce skills also require `schedule`, while runonce skills require `run_at` as ISO-8601.

`mode = script` runs the sibling `script` executable. `mode = agent` sends the body to `MUSE_AGENT_COMMAND`, or performs a logged dry run when that variable is absent. `hooks` is reserved for future before/after composition.
