# -*- coding: utf-8 -*-
"""Rules for compliance of commit messages to the repo."""
import re

from gitlint.rules import CommitMessageTitle, CommitRule, LineRule, RuleViolation

valid_types = [
    "build",
    "chore",
    "devops",
    "docs",
    "feat",
    "fix",
    "perf",
    "refactor",
    "style",
    "test",
]


class ContribType(CommitRule):
    """Type of the contribution.

    Enforces that each commit contains a valid type at the
    beggining of the title.
    """

    name = "title-requires-validate-type"
    id = "UC1"
    target = CommitMessageTitle

    def validate(self, commit):
        """Validate function to be ran by pre-commit for ContribType()."""
        self.log.debug(
            """
            ContribType: title's prefix should match valid types.
            Please check CONTRIBUTING.md for more info.
            """
        )

        if commit.message.title.startswith(tuple(valid_types)):
            return

        # msg = "Commit title does not start with a valid type."
        msg = "Commit title does not start with one of {0}".format(
            ", ".join(valid_types)
        )
        return [RuleViolation(self.id, msg, line_nr=0)]


class TitleFormat(LineRule):
    """Title's compliant format.

    Enforces the commit format stated at CONTRIBUTING.md
    """

    name = "title-must-follow-valid-format"
    id = "UC2"
    target = CommitMessageTitle

    expected_format = "type: [optional-scope] description"
    RULE_REGEX = re.compile(
        r"^("
        + "|".join(valid_types)
        + r")(:)\s"
        + r"(\[(\w+-){0,}\w+\]){0,}"
        + r"[a-zA-Z\d\,\.\/\'\-_\s]+$"
    )

    def validate(self, line, _commit):
        """Validate function to be ran by pre-commit for TitleFormat()."""
        ef = self.expected_format
        self.log.debug("TitleFormat: title's format should be '" + ef + "'")

        if self.RULE_REGEX.match(line):
            return

        msg = "Commit title does not follow the agreed format '" + ef + "'"
        return [RuleViolation(self.id, msg, line_nr=0)]
