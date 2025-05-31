from app.cli import shell
import click

def show_banner():
    click.secho(r"""
    ███╗   ███╗ ██████╗ ██╗   ██╗███╗   ██╗██╗   ██╗
    ████╗ ████║██╔═══██╗██║   ██║████╗  ██║██║   ██║
    ██╔████╔██║██║   ██║██║   ██║██╔██╗ ██║██║   ██║
    ██║╚██╔╝██║██║   ██║██║   ██║██║╚██╗██║╚██╗ ██╔╝
    ██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║ ╚████║ ╚████╔╝ 
    ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  
                Track it. Bill it. Bank it.
    """, fg='red', bold=True)
    click.secho("Starting SimpleBilling Shell (type 'exit' to quit)\n", fg="cyan", bold=True)
    click.secho("Welcome to SimpleBilling CLI!", fg='green', bold=True)
    click.secho("Type '--help' to see available commands\n",fg='blue', bold=True)

if __name__ == "__main__":
    show_banner()
    shell()
