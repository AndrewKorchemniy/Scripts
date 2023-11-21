import os
import click
import subprocess

@click.command()
@click.argument('input_file_path', type=click.Path(exists=True))
def decimate(input_file_path):
    name = os.path.splitext(input_file_path)[0]
    output_file = f"{name}-decimated.mov"
    
    cmd = [
        'ffmpeg',
        '-i', input_file_path,
        '-vf', 'mpdecimate,setpts=N/FRAME_RATE/TB',
        '-c:v', 'dnxhd',
        '-profile:v', 'dnxhr_hqx',
        '-pix_fmt', 'yuv422p10le',
        output_file
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Decimation complete. Output file: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during decimation:\n{e}")

if __name__ == '__main__':
    decimate()
