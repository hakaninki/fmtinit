"""CLI definitions for fmtinit."""

import typer

from fmtinit.commands import add, doctor, init, scan

app = typer.Typer(
    name="fmtinit",
    help="Smart formatter bootstrap CLI for multi-language projects.",
    add_completion=False,
)

app.command("init")(init.init_project)
app.command("add")(add.add_language)
app.command("scan")(scan.scan_project)
app.command("doctor")(doctor.doctor_check)
