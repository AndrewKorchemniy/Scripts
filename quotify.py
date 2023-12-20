import click
import os
import re


def process_token(token, output_content):
    """Ensures each token is quoted and adds them to the output_content. Ignores lonely quotations.

    Args:
        token (string): The token to add.
        output_content (list of str): The output content.
    """
    if not len(token) > 0:
        return
    starts_with, ends_with = (token[0] == '"', token[len(token) - 1] == '"')
    if starts_with and ends_with:
        output_content.append(token)
    elif starts_with:
        output_content.append(f'{token}"')
    elif ends_with:
        output_content.append(f'"{token}')
    else:
        output_content.append(f'"{token}"')


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
def quotify(input_file):
    """Surrounds all tokens within the input text with double quotation marks. Meant for command line text."""
    name, ext = os.path.splitext(input_file)
    output_file = f"{name}-quoted{ext}"
    output_content = []

    with open(input_file, 'r') as f:
        for line in f:
            for token in re.findall(r'"[^"]+"|\S+', line):
                process_token(token, output_content)
            output_content.append('\n')

    with open(output_file, 'w') as f:
        f.write(' '.join(output_content))


if __name__ == '__main__':
    quotify()
