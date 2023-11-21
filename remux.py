import os
import click
import subprocess


@click.command()
@click.argument('directory', type=click.Path(exists=True))
@click.argument('extension')
@click.argument('new_extension')
def remux_files(directory, extension, new_extension):
    """Remux files in the specified directory with the given extension to a new extension."""
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if os.path.isfile(path) and file.endswith(extension):
            remux_path = os.path.join(directory, f"{os.path.splitext(file)[0]}{new_extension}")
            cmd = ['ffmpeg', '-i', path, '-c', 'copy', remux_path]
            print(' '.join(cmd))
            subprocess.run(cmd)


if __name__ == '__main__':
    remux_files()
