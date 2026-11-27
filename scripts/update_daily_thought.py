"""Generate daily dark and light Today's Thought SVGs for the profile README."""

from __future__ import annotations

import html
import textwrap
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

IST = timezone(timedelta(hours=5, minutes=30))
EPOCH = date(2026, 1, 1)

THOUGHTS: list[tuple[str, str]] = [
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("Premature optimization is the root of all evil.", "Donald Knuth"),
    ("Controlling complexity is the essence of computer programming.", "Brian Kernighan"),
    ("Good code is its own best documentation.", "Steve McConnell"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("A distributed system is one in which the failure of a computer you didn't even know existed can render your own computer unusable.", "Leslie Lamport"),
    ("Bad programmers worry about the code. Good programmers worry about data structures and their relationships.", "Linus Torvalds"),
    ("Debugging is twice as hard as writing the code in the first place.", "Brian Kernighan"),
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
    ("The best error message is the one that never shows up.", "Thomas Fuchs"),
    ("Simplicity is about subtracting the obvious and adding the meaningful.", "John Maeda"),
    ("Perfection is achieved not when there is nothing more to add, but rather when there is nothing left to take away.", "Antoine de Saint-Exupery"),
    ("Deleted code is debugged code.", "Jeff Sickel"),
    ("The most dangerous phrase in the language is: We've always done it this way.", "Grace Hopper"),
    ("When in doubt, use brute force.", "Ken Thompson"),
    ("Testing leads to failure, and failure leads to understanding.", "Burt Rutan"),
    ("One accurate measurement is worth a thousand expert opinions.", "Grace Hopper"),
    ("The function of good software is to make the complex appear to be simple.", "Grady Booch"),
    ("What one programmer can do in one month, two programmers can do in two months.", "Fred Brooks"),
    ("Give someone a program, you frustrate them for a day; teach them how to program, you frustrate them for a lifetime.", "David Leinweber"),
    ("It's not a bug; it's an undocumented feature.", "Anonymous"),
    ("Before software can be reusable it first has to be usable.", "Ralph Johnson"),
    ("Clean code always looks like it was written by someone who cares.", "Robert C. Martin"),
    ("The cleaner and nicer the program, the faster it's going to run.", "Joshua Bloch"),
    ("Weeks of coding can save you hours of planning.", "Anonymous"),
    ("In theory, theory and practice are the same. In practice, they are not.", "Yogi Berra"),
    ("An investment in knowledge pays the best interest.", "Benjamin Franklin"),
    ("If you think it's expensive to hire a professional to do the job, wait until you hire an amateur.", "Red Adair"),
    ("Intelligence is the ability to avoid doing work, yet getting the work done.", "Linus Torvalds"),
    ("A good API is not just easy to use, it is hard to misuse.", "Joshua Bloch"),
    ("Truth can only be found in one place: the code.", "Robert C. Martin"),
    ("The best way to predict the future is to implement it.", "David Heinemeier Hansson"),
    ("Design is not just what it looks like and feels like. Design is how it works.", "Steve Jobs"),
    ("Focus on the fundamentals; frameworks come and go.", "Anonymous"),
    ("Reliability is not an afterthought; it is a design choice.", "Anonymous"),
    ("Measure twice, cut once; benchmark before you optimize.", "Anonymous"),
    ("Software architecture is about the important stuff, whatever that is.", "Ralph Johnson"),
    ("Every great developer you know got there by solving problems they were unqualified to solve until they did.", "Patrick McKenzie"),
    ("Learn from yesterday, build for today, design for tomorrow.", "Anonymous"),
    ("Knowledge is of no value unless you put it into practice.", "Anton Chekhov"),
    ("A system that fails loudly is easier to fix than one that fails silently.", "Anonymous"),
    ("Understanding the problem deeply is already half the solution.", "Anonymous"),
    ("Consistency compounds faster than intensity.", "Anonymous"),
]


def render_svg(
    quote: str,
    author: str,
    date_label: str,
    *,
    bg: str,
    border: str,
    header_color: str,
    text_color: str,
    author_color: str,
) -> str:
    """Build a crisp, fixed-width responsive SVG card for Today's Thought."""
    wrapped = textwrap.wrap(f'"{quote}"', width=56)
    line_height = 24
    top_pad = 54
    bottom_pad = 44
    height = top_pad + (len(wrapped) * line_height) + bottom_pad

    tspans = []
    for idx, line in enumerate(wrapped):
        y = top_pad + idx * line_height
        tspans.append(
            f'    <tspan x="32" y="{y}">{html.escape(line)}</tspan>'
        )
    tspans_block = "\n".join(tspans)
    author_y = top_pad + (len(wrapped) * line_height) + 18

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="{height}" '
        f'viewBox="0 0 600 {height}" role="img" '
        f'aria-label="Today\'s Thought: {html.escape(quote)} - {html.escape(author)}">\n'
        f'  <rect x="1" y="1" width="598" height="{height - 2}" rx="12" '
        f'fill="{bg}" stroke="{border}" stroke-width="1.5"/>\n'
        f'  <text x="32" y="28" fill="{header_color}" '
        f'font-family="\'Segoe UI\', -apple-system, Arial, sans-serif" '
        f'font-size="12" font-weight="700" letter-spacing="0.6">'
        f'TODAY\'S THOUGHT  ·  {html.escape(date_label)}</text>\n'
        f'  <text fill="{text_color}" '
        f'font-family="\'Segoe UI\', -apple-system, Arial, sans-serif" '
        f'font-size="17" font-style="italic" font-weight="500">\n'
        f'{tspans_block}\n'
        f'  </text>\n'
        f'  <text x="568" y="{author_y}" text-anchor="end" fill="{author_color}" '
        f'font-family="\'Segoe UI\', -apple-system, Arial, sans-serif" '
        f'font-size="14" font-weight="700">— {html.escape(author)}</text>\n'
        f'</svg>\n'
    )


def main() -> None:
    today = datetime.now(IST).date()
    index = (today - EPOCH).days % len(THOUGHTS)
    quote, author = THOUGHTS[index]
    date_label = today.strftime("%b %d, %Y")

    assets_dir = Path(__file__).resolve().parents[1] / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    dark_svg = render_svg(
        quote,
        author,
        date_label,
        bg="#0D1117",
        border="#1F6FEB",
        header_color="#58A6FF",
        text_color="#C9D1D9",
        author_color="#38BDF8",
    )
    light_svg = render_svg(
        quote,
        author,
        date_label,
        bg="#EDF4FF",
        border="#022B6B",
        header_color="#022B6B",
        text_color="#000000",
        author_color="#022B6B",
    )

    (assets_dir / "thought-dark.svg").write_text(dark_svg, encoding="utf-8")
    (assets_dir / "thought-light.svg").write_text(light_svg, encoding="utf-8")
    print(f"Updated Today's Thought ({date_label}): \"{quote}\" — {author}")


if __name__ == "__main__":
    main()
