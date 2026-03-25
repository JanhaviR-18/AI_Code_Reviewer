import reflex as rx
import json
import datetime
from AI_Code_Reviewer.backend.code_parser import parse_code
from AI_Code_Reviewer.backend.error_detector import detect_errors
from AI_Code_Reviewer.backend.ai_suggester import get_ai_suggestion


class SubmissionRecord(rx.Base):
    """A single submission history record."""
    timestamp: str = ""
    score: int = 0
    syntax_ok: bool = False
    error_count: int = 0
    code_snippet: str = ""   # first 80 chars of code


class State(rx.State):
    # ── Core fields ───────────────────────────────────
    user_code: str = ""
    syntax_output: str = "— run analysis to see results —"
    errors_output: str = "— run analysis to see results —"
    ai_output: str = "— run analysis to see AI suggestions —"
    is_loading: bool = False

    # ── Score ─────────────────────────────────────────
    style_score: int = 0
    score_label: str = ""

    # ── Before/After snippets ─────────────────────────
    before_snippet: str = ""
    after_snippet: str = ""
    has_snippets: bool = False

    # ── Submission history ────────────────────────────
    history: list[SubmissionRecord] = []

    # ── Setters ───────────────────────────────────────
    def set_user_code(self, value: str):
        self.user_code = value

    # ── Helpers ───────────────────────────────────────
    def _calc_score(self, errors: list) -> int:
        score = 100
        for e in errors:
            severity = e.get("severity", "warning")
            if severity == "error":
                score -= 15
            else:
                score -= 7
        return max(0, min(100, score))

    def _score_label(self, score: int) -> str:
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 55:
            return "Fair"
        else:
            return "Needs Work"

    def _strip_fences(self, text: str) -> str:
        """Remove markdown code fences from a snippet."""
        lines = text.strip().splitlines()
        # Remove opening fence (```python or ```)
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        # Remove closing fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()

    def _extract_snippets(self, ai_text: str):
        """
        Parse before/after code blocks from AI output.
        Handles both plain text and fenced code blocks.
        """
        before, after = "", ""
        if "BEFORE:" in ai_text and "AFTER:" in ai_text:
            try:
                before_raw = ai_text.split("BEFORE:")[1].split("AFTER:")[0].strip()
                after_raw  = ai_text.split("AFTER:")[1].strip()
                # Remove any trailing sections
                for marker in ["SUGGESTION", "NOTE", "---", "PART"]:
                    if marker in after_raw:
                        after_raw = after_raw.split(marker)[0].strip()
                before = self._strip_fences(before_raw)
                after  = self._strip_fences(after_raw)
            except Exception:
                pass
        self.before_snippet = before
        self.after_snippet  = after
        self.has_snippets   = bool(before and after)

    def _save_to_history(self, errors: list):
        snippet = (self.user_code[:80] + "…") if len(self.user_code) > 80 else self.user_code
        record = SubmissionRecord(
            timestamp=datetime.datetime.now().strftime("%d %b %Y, %H:%M"),
            score=self.style_score,
            syntax_ok="✓" in self.syntax_output,
            error_count=len(errors),
            code_snippet=snippet,
        )
        self.history = [record] + self.history[:19]

    # ── Main action ───────────────────────────────────
    def analyze_code(self):
        if not self.user_code.strip():
            self.syntax_output = "⚠  No code provided."
            self.errors_output = ""
            self.ai_output     = ""
            self.style_score   = 0
            self.score_label   = ""
            self.has_snippets  = False
            return

        self.is_loading    = True
        self.has_snippets  = False
        self.syntax_output = "Analyzing…"
        self.errors_output = "…"
        self.ai_output     = "Waiting for AI…"

        # ── Step 1: Parse ──────────────────────────────
        result = parse_code(self.user_code)
        if not result["success"]:
            error = result["error"]
            if isinstance(error, dict):
                msg    = error.get("message", str(error))
                lineno = error.get("lineno", "")
            else:
                msg    = str(error)
                lineno = ""
            loc    = f" (line {lineno})" if lineno else ""
            self.syntax_output = f"✗ Syntax Error{loc}:\n  {msg}"
            self.errors_output = "Analysis stopped — fix syntax error first."
            self.ai_output     = ""
            self.style_score   = 0
            self.score_label   = "Syntax Error"
            self.is_loading    = False
            return

        self.syntax_output = "✓ No syntax errors found."

        # ── Step 2: Detect errors ─────────────────────
        errors = detect_errors(self.user_code)
        if errors:
            self.errors_output = "\n".join(
                f"  {e['type']}: {e.get('message', '')}" for e in errors
            )
        else:
            self.errors_output = "✓ No issues detected."

        # ── Step 3: Score ──────────────────────────────
        self.style_score = self._calc_score(errors)
        self.score_label = self._score_label(self.style_score)

        # ── Step 4: AI suggestions + snippets ──────────
        raw = get_ai_suggestion(self.user_code, errors)
        clean = raw.replace("**", "").replace("*", "").strip()

        # Store AI output without the BEFORE/AFTER block (cleaner display)
        if "BEFORE:" in clean:
            self.ai_output = clean.split("BEFORE:")[0].strip()
        else:
            self.ai_output = clean

        self._extract_snippets(clean)

        # ── Step 5: Save history ───────────────────────
        self._save_to_history(errors)

        self.is_loading = False

    def clear_history(self):
        self.history = []