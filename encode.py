import click
import os
import subprocess
import appdirs

blueprint = "ffmpeg {input_args} -i \"{input_file}\" {output_args} \"{output_file}\""
h264_codec = "-c:v libx264 -profile:v high -crf {crf} -preset veryslow -pix_fmt yuv420p -level 4.1 -an -movflags +faststart"
hqx_codec = "-c:v dnxhd -profile:v dnxhr_hqx -pix_fmt yuv422p10le -an -movflags +faststart"
default_input_args = "-v quiet -stats -n"
loop_filter = "-filter_complex \"[0]reverse[r];[0][r]concat,loop=2\""
cache_file = os.path.join(appdirs.user_data_dir(), 'script-encode', 'cache')


def set_cached_directory(directory):
    """Sets the cached directory.

    Args:
        directory (string): The directory to cache.
    """
    try:
        cache_directory = os.path.dirname(cache_file)
        os.makedirs(cache_directory, exist_ok=True)
        with open(cache_file, 'w') as file:
            file.write(f'{directory}\n')
    except Exception as e:
        print(f"Failed to read from cache file:\n{e}")
    print("Updated cached directory path.\n")


def get_cached_directory():
    """Gets the cached directory if one exists.

    Returns:
        string: The cached directory.
    """
    cached_directory = ""
    try:
        with open(cache_file, 'r') as file:
            cached_directory = file.readline().strip()
    except Exception as e:
        print(f"An error occurred while reading from the cache file: {e}")
    print("Using cached directory path.\n")
    return cached_directory


def run(input_args, input_file, output_args, output_file):
    """Builds and runs the ffmpeg command.

    Args:
        input_args (string): The input configurations.
        input_file (string): The input file path.
        output_args (string): The output configurations.
        output_file (string): The output file path.
    """
    command = blueprint.format(
        input_args=' '.join(input_args),
        input_file=input_file,
        output_args=' '.join(output_args),
        output_file=output_file)
    print(command)
    subprocess.run(command, shell=True)
    print()


def encode_directory(suffix, output_ext, input_args, output_args, path, useCachedDirectory=False):
    """Encodes files from the mezzanine directory into the post directory - from within the specified path.

    Args:
        suffix (string): The suffix to remove from the input file name.
        output_ext (string): The output file extension.
        input_args (string): The input configurations.
        output_args (string): The output configurations.
        useCachedDirectory (bool, optional): Uses the cached directory if True. Defaults to False.
    """
    if useCachedDirectory:
        path = get_cached_directory()
    else:
        set_cached_directory(path)

    source_directory = f'{path}\\mezzanine'
    output_directory = f'{path}\\post'
    input_files = [os.path.join(source_directory, f) for f in os.listdir(source_directory) if
                   os.path.isfile(os.path.join(source_directory, f))]
    for input_file in input_files:
        output_file = os.path.join(
            output_directory,
            f'{os.path.splitext(os.path.basename(input_file))[0].removesuffix(suffix)}{output_ext}')
        run(input_args, input_file, output_args, output_file)


def encode_file(suffix, output_ext, input_args, output_args, path):
    """Encode a single file.

    Args:
        suffix (string): The suffix to remove from the input file name.
        output_ext (string): The output file extension.
        input_args (string): The input configurations.
        output_args (string): The output configurations.
        path (string): The path to the input file.
    """
    if os.path.isfile(path):
        output_file = os.path.splitext(path)[0].removesuffix(suffix) + output_ext
        run(input_args, path, output_args, output_file)
    else:
        print("Invalid input file path.")


@click.command()
@click.option('--path', '-p', type=click.Path(exists=True))
@click.option('-crf', default=18.0, show_default=True)
@click.option('--fps', '-r', type=int)
@click.option('--codec', '-c', type=click.Choice(['hqx', 'h264']), default='h264', show_default=True)
@click.option('--loop', '-l', is_flag=True, default=False, show_default=True)
@click.option('--suffix', '-s', default='-master', show_default=True, help='Suffix to remove.')
@click.option('--directory', '-d', is_flag=True, default=False, show_default=True, help='Use directory mode.')
@click.option('-cd', is_flag=True, default=False, show_default=True, help="Use cached directory.")
def encode(path, crf, fps, codec, loop, suffix, directory, cd):
    input_args = [default_input_args]
    output_args = []
    output_ext = ""

    if fps:
        input_args.append(f'-r {fps}')
    if loop:
        output_args.append(loop_filter)

    match codec:
        case 'h264':
            output_args.append(h264_codec.format(crf=crf))
            output_ext = ".mp4"
        case 'hqx':
            output_args.append(hqx_codec)
            output_ext = ".mov"

    if directory:
        encode_directory(suffix, output_ext, input_args, output_args, path, cd)
    else:
        encode_file(suffix, output_ext, input_args, output_args, path)


if __name__ == '__main__':
    encode()
