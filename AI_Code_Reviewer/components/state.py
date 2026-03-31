import reflex as rx
import datetime
from AI_Code_Reviewer.backend.code_parser import parse_code
from AI_Code_Reviewer.backend.error_detector import detect_errors
from AI_Code_Reviewer.backend.ai_suggester import get_ai_suggestion
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

SUPPORTED_LANGUAGES = ["Python", "C", "C++", "Java", "JavaScript", "SQL"]


class SubmissionRecord(rx.Base):
    id: str = ""
    timestamp: str = ""
    language: str = ""
    score: int = 0
    score_label: str = ""
    syntax_ok: bool = False
    error_count: int = 0
    full_code: str = ""
    syntax_output: str = ""
    errors_output: str = ""
    ai_output: str = ""
    before_snippet: str = ""
    after_snippet: str = ""
    time_complexity_original: str = ""
    time_complexity_optimized: str = ""
    has_snippets: bool = False


class State(rx.State):

    # ── Core ──────────────────────────────────────
    user_code: str = ""
    language: str = "Python"

    syntax_output: str = "— run analysis to see results —"
    errors_output: str = "— run analysis to see results —"
    ai_output: str = "— run analysis to see AI suggestions —"
    is_loading: bool = False

    # ── Score ─────────────────────────────────────
    style_score: int = 0
    score_label: str = ""
    prev_score: int = 0
    has_prev_score: bool = False

    # ── Time complexity ───────────────────────────
    time_complexity_original: str = ""
    time_complexity_optimized: str = ""
    time_complexity_explanation: str = ""
    has_complexity: bool = False

    # ── Before/After ──────────────────────────────
    before_snippet: str = ""
    after_snippet: str = ""
    has_snippets: bool = False

    # ── History ───────────────────────────────────
    history: list[SubmissionRecord] = []
    selected_record_id: str = ""
    upload_error: str = ""

    # ── Theme ─────────────────────────────────────
    is_dark: bool = False

    # ── AI Assistant ──────────────────────────────
    last_analyzed_code: str = ""
    last_analyzed_language: str = ""
    assistant_messages: list[dict] = []
    assistant_input: str = ""
    assistant_loading: bool = False

    # ── Setters ───────────────────────────────────
    def set_user_code(self, value: str):
        self.user_code = value

    def set_language(self, value: str):
        self.language = value
        self.syntax_output  = "— run analysis to see results —"
        self.errors_output  = "— run analysis to see results —"
        self.ai_output      = "— run analysis to see AI suggestions —"
        self.has_snippets   = False
        self.has_complexity = False

    def set_assistant_input(self, value: str):
        self.assistant_input = value

    def select_record(self, record_id: str):
        self.selected_record_id = record_id

    def close_record(self):
        self.selected_record_id = ""

    def toggle_theme(self):
        self.is_dark = not self.is_dark

    @property
    def bg_base(self):
      return "#0a0a0f" if self.is_dark else "#f2f0eb"

    @property
    def bg_card(self):
      return "#111118" if self.is_dark else "#eceae4"

    @property
    def bg_code(self):
      return "#0d0d12" if self.is_dark else "#1a1a1a"

    @property
    def text_primary(self):
      return "#f1f1f5" if self.is_dark else "#1a1a1a"

    @property
    def text_secondary(self):
      return "#cfcfd6" if self.is_dark else "#5a5a5a"

    @property
    def border_color(self):
      return "#2a2a35" if self.is_dark else "#d4d0c8"    

    # ── File upload ───────────────────────────────
    async def handle_upload(self, files: list[rx.UploadFile]):
        self.upload_error = ""
        if not files:
            return
        file = files[0]
        filename = file.filename.lower()
        ext_map = {
            ".py": "Python", ".c": "C", ".cpp": "C++",
            ".java": "Java", ".js": "JavaScript", ".sql": "SQL",
        }
        matched_lang = next(
            (lang for ext, lang in ext_map.items() if filename.endswith(ext)), None
        )
        if matched_lang is None:
            self.upload_error = "Unsupported file. Upload .py .c .cpp .java .js or .sql"
            return
        content = await file.read()
        try:
            self.user_code = content.decode("utf-8")
            self.language  = matched_lang
        except UnicodeDecodeError:
            self.upload_error = "Could not read file — must be a plain text source file."

    # ── Helpers ───────────────────────────────────
    def _calc_score(self, errors: list) -> int:
        score = 100
        for e in errors:
            score -= 15 if e.get("severity") == "error" else 7
        return max(0, min(100, score))

    def _score_label(self, score: int) -> str:
        if score >= 90: return "Excellent"
        if score >= 75: return "Good"
        if score >= 55: return "Fair"
        return "Needs Work"

    def _strip_fences(self, text: str) -> str:
        lines = text.strip().splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()

    def _parse_ai_output(self, raw: str):
        clean = raw.replace("**", "").replace("*", "").strip()

        # ── Extract time complexity first ──────────
        self.time_complexity_original  = ""
        self.time_complexity_optimized = ""
        self.time_complexity_explanation = ""
        self.has_complexity = False

        if "TIME COMPLEXITY:" in clean:
            try:
                tc_block = clean.split("TIME COMPLEXITY:")[1]
                # End of TC block is either BEFORE: or PART 3
                for end_marker in ["BEFORE:", "PART 3", "---"]:
                    if end_marker in tc_block:
                        tc_block = tc_block.split(end_marker)[0]
                tc_block = tc_block.strip()
                explanation_lines = []
                for line in tc_block.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    low = line.lower()
                    if low.startswith("original:"):
                        self.time_complexity_original = line.split(":", 1)[1].strip()
                    elif low.startswith("optimized:"):
                        self.time_complexity_optimized = line.split(":", 1)[1].strip()
                    else:
                        explanation_lines.append(line)
                self.time_complexity_explanation = " ".join(explanation_lines).strip()
                self.has_complexity = bool(
                    self.time_complexity_original and self.time_complexity_optimized
                )
            except Exception:
                pass

        # ── Extract before/after ───────────────────
        self.before_snippet = ""
        self.after_snippet  = ""
        self.has_snippets   = False

        if "BEFORE:" in clean and "AFTER:" in clean:
            try:
                before = clean.split("BEFORE:")[1].split("AFTER:")[0].strip()
                after  = clean.split("AFTER:")[1].strip()
                for m in ["FEEDBACK:", "TIME COMPLEXITY:", "---", "PART"]:
                    if m in after:
                        after = after.split(m)[0].strip()
                self.before_snippet = self._strip_fences(before)
                self.after_snippet  = self._strip_fences(after)
                self.has_snippets   = bool(self.before_snippet and self.after_snippet)
            except Exception:
                pass

        # ── Clean AI output (feedback only) ───────
        display = clean
        for marker in ["TIME COMPLEXITY:", "BEFORE:", "PART 2", "PART 3"]:
            if marker in display:
                display = display.split(marker)[0].strip()
        self.ai_output = display

    # ── Main analysis ─────────────────────────────
    def analyze_code(self):
        if not self.user_code.strip():
            self.syntax_output = "⚠  No code provided."
            self.errors_output = self.ai_output = ""
            self.style_score   = 0
            self.score_label   = ""
            self.has_snippets  = self.has_complexity = False
            return

        if self.style_score > 0:
            self.prev_score     = self.style_score
            self.has_prev_score = True
        else:
            self.prev_score     = 0
            self.has_prev_score = False

        self.is_loading      = True
        self.has_snippets    = False
        self.has_complexity  = False
        self.syntax_output   = "Analyzing…"
        self.errors_output   = "…"
        self.ai_output       = "Waiting for AI…"

        result = parse_code(self.user_code, self.language)
        if not result["success"]:
            err = result["error"]
            if isinstance(err, dict):
                msg    = err.get("message", str(err))
                lineno = err.get("lineno", "")
            else:
                msg, lineno = str(err), ""
            loc = f" (line {lineno})" if lineno else ""
            self.syntax_output = f"✗ Syntax Error{loc}:\n  {msg}"
            self.errors_output = "Analysis stopped — fix syntax error first."
            self.ai_output     = ""
            self.style_score   = 0
            self.score_label   = "Syntax Error"
            self.is_loading    = False
            return

        self.syntax_output = "✓ No syntax errors found."

        errors = detect_errors(self.user_code, self.language)
        self.errors_output = (
            "\n".join(f"  {e['type']}: {e.get('message', '')}" for e in errors)
            if errors else "✓ No issues detected."
        )

        self.style_score = self._calc_score(errors)
        self.score_label = self._score_label(self.style_score)

        raw = get_ai_suggestion(self.user_code, errors, self.language)
        self._parse_ai_output(raw)

        self.last_analyzed_code     = self.user_code
        self.last_analyzed_language = self.language

        self._save_to_history(errors)
        self.is_loading = False

    def _save_to_history(self, errors: list):
        record = SubmissionRecord(
            id=datetime.datetime.now().isoformat(),
            timestamp=datetime.datetime.now().strftime("%d %b %Y, %H:%M"),
            language=self.language,
            score=self.style_score,
            score_label=self.score_label,
            syntax_ok="✓" in self.syntax_output,
            error_count=len(errors),
            full_code=self.user_code,
            syntax_output=self.syntax_output,
            errors_output=self.errors_output,
            ai_output=self.ai_output,
            before_snippet=self.before_snippet,
            after_snippet=self.after_snippet,
            time_complexity_original=self.time_complexity_original,
            time_complexity_optimized=self.time_complexity_optimized,
            has_snippets=self.has_snippets,
        )
        self.history = [record] + self.history[:19]

    def clear_history(self):
        self.history = []
        self.selected_record_id = ""

    # ── AI Assistant ──────────────────────────────
    def send_assistant_message(self):
        if not self.assistant_input.strip():
            return
        user_msg = self.assistant_input.strip()
        self.assistant_input   = ""
        self.assistant_loading = True
        self.assistant_messages = self.assistant_messages + [
            {"role": "user", "content": user_msg}
        ]
        code_ctx = ""
        if self.last_analyzed_code:
            code_ctx = (
                f"\n\nThe user recently analyzed this {self.last_analyzed_language} code:\n"
                f"{self.last_analyzed_code[:1500]}\nKeep this in mind when answering."
            )
        history_text = "\n".join(
            f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
            for m in self.assistant_messages[-8:]
        )
        full_prompt = (
            f"You are a helpful coding assistant specializing in code review and improvement.{code_ctx}\n\n"
            f"Conversation:\n{history_text}\n\nAssistant:"
        )
        try:
            from AI_Code_Reviewer.backend.ai_suggester import model
            response = model.invoke(full_prompt)
            reply = response.content.strip()
        except Exception as e:
            reply = f"Error: {str(e)}"
        self.assistant_messages = self.assistant_messages + [
            {"role": "assistant", "content": reply}
        ]
        self.assistant_loading = False

    def clear_assistant(self):
        self.assistant_messages = []
        self.assistant_input    = ""

    