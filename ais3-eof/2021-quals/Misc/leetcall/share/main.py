import ast

import epicbox

from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.markdown import Markdown

console = Console(color_system='256', force_terminal=True)
epicbox.configure(profiles=[
    epicbox.Profile('python', 'python:3.9-alpine')
])
SANDBOX_TEMPLATE = open("sandbox.tpl.py").read()
FLAG = open('flag.txt').read()


def is_valid_source(source):
    '''
    check a source code contains only function call and literal constant using ast.
    ast: https://docs.python.org/3.9/library/ast.html
    '''
    try:
        # eval mode, only accept one expression
        tree = ast.parse(source, mode='eval')
    except SyntaxError:
        return False

    whitelist = (
        ast.Expression,  # root node of the ast
        ast.Call, ast.Name, ast.Constant,  # only accept call, name and constant
        ast.Load  # call a function need to "load" its function name
    )
    for node in ast.walk(tree):
        if not isinstance(node, whitelist):
            return False
    return True


def propose_problem(id, title, description, sample_input, sample_output, test_cases, length_limit, time_limit=1):
    # UI: print problem information
    layout = Layout()
    layout.split_column(
        Layout(Panel(
            f"[bold green]Problem {id}: {title}[/bold green]\n\n"
            f"[bold]Time Limit:[/bold] {time_limit}s\n"
            f"[bold]Code Length Limit:[/bold] {length_limit} bytes\n\n"
            f"[bold]Description:[/bold]\n{description}",
            title=f"Challenge {id} / 3",
        ), ratio=5),
        Layout(name="samples", ratio=4)
    )
    layout["samples"].split_row(
        Layout(Panel('\n'.join(sample_input), title="Sample Input")),
        Layout(Panel('\n'.join(sample_output), title="Sample Output"))
    )
    console.print(layout)

    # OJ: submit code
    code = console.input("Input your code here: ")

    if not is_valid_source(code):
        console.print("[red]This is not leetcall![/red]")
        exit()

    if len(code) > length_limit:
        console.print("[red]Your code is too long![/red]")
        exit()

    from time import sleep
    with console.status("[bold]Start Judging...",) as status:
        cases_num = len(test_cases)

        for i, (test_in, test_out) in enumerate(test_cases):
            status.update(f"[bold]Test Case {i+1} / {cases_num}...[/bold]")

            files = [{
                'name': 'main.py',
                'content': SANDBOX_TEMPLATE.format(code=code).encode()
            }]
            limits = {'cputime': time_limit, 'memory': 64}

            res = epicbox.run('python', 'python main.py',
                              files=files, limits=limits, stdin=test_in)
            if res['exit_code'] is None or res['exit_code'] != 0:
                # print(res['stderr'].decode())
                console.print(f"[red]Stage {i+1}: Runtime Error[/red]")
                exit()
            if res['stdout'].decode().strip() != test_out.strip():
                # print(res['stdout'].decode())
                console.print(f"[red]Stage {i+1}: Wrong Answer[/red]")
                exit()
            console.print(f"[green]Stage {i+1}: Passed[/green]")
            sleep(0.5)

        status.update(f"[bold green]✅ Accept![/bold green]")
        sleep(1)
    console.print(f"[bold green]✅ Accept![/bold green]")


def main():
    console.print(Markdown(open("README.md").read()), "\n")
    console.rule("(Press enter to start)")
    console.input()

    import json
    problems = json.load(open("problems.json"))
    for prob in problems:
        propose_problem(**prob)

    console.print("Here is your flag: ", f"[green bold]{FLAG}")


if __name__ == '__main__':
    main()
