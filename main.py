#!/usr/bin/env python3
"""Describe Your Ex in One Word — make.fun entry.

Writes one word describing an ex to /output/entry.txt. Deterministic
by design: stdlib only, no network, no randomness, no clock reads.
Repeated runs produce byte-identical output.

The word: "Intern".

The joke: an intern is temporary, unpaid, and never promoted — the
relationship was a trial period that ended without a full-time offer.
The ex was never a partner; they were only ever an intern, let go
when the placement ran out.
"""

import os

# The single word that describes the ex. Kept as its own constant so
# the verdict is visible at a glance: one word, no punctuation, no
# tricks — exactly what the gate asks for.
_WORD = "Intern"

MAX_WORD_CHARS = 111  # competition ceiling for the single word


def build_word() -> str:
    """Return the one-word verdict on the ex.

    The result must be exactly one word: a stray space or newline in
    it would silently break the entry format, so fail loudly instead
    of writing a malformed file. It must also be more than whitespace:
    the gate refuses a file that is only white space.
    """
    word = _WORD
    if not word.strip():
        raise ValueError("word must not be only white space")
    if word != word.strip():
        raise ValueError("word must not start or end with white space")
    if any(ch.isspace() for ch in word):
        raise ValueError("word must be exactly one word, with no spaces")
    return word


def resolve_output_path() -> str:
    """Return the path of the file the word is written to.

    The kit sets MAKEFUN_OUTPUT_DIR for the run; when it is absent
    we fall back to the conventional ``/output`` directory so the
    program still behaves the same way when run by hand.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(output_dir, "entry.txt")


def main() -> None:
    """Write the word to the output file, with no trailing newline.

    The gate requires 1 to 111 characters of UTF-8 text, so the
    word is validated here before it is written: one word, no
    spaces or line breaks, and within the limit. After writing, the
    file is read back and re-checked, so a truncated or altered
    write fails loudly instead of shipping a bad entry.
    """
    word = build_word()
    if not 1 <= len(word) <= MAX_WORD_CHARS:
        raise ValueError("word must be 1 to 111 characters")
    output_path = resolve_output_path()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(word)
    with open(output_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != word:
        raise ValueError("written word does not match the built word")
    if not 1 <= len(written) <= MAX_WORD_CHARS:
        raise ValueError("written word is outside 1 to 111 characters")


if __name__ == "__main__":
    main()
