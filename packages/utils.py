import subprocess
import os
import sys
import shutil

__all__ = ['markdown_to_docx']

def markdown_to_docx(markdown_filepath: str, output_filepath: str, reference_docx: str = None) -> bool:
    """
    Converts a Markdown file (.md) to a Word document (.docx) using Pandoc.

    Args:
        markdown_filepath: The path to the input Markdown file.
        output_filepath: The path where the output DOCX file will be saved.
        reference_docx: Optional path to a reference DOCX file for custom styling.
                        If provided, Pandoc uses the styles from this file.

    Returns:
        True if the conversion was successful, False otherwise.
    """
    # 1. Check for Pandoc installation
    if shutil.which("pandoc") is None:
        print("Error: Pandoc is not installed or not found in PATH.")
        print("Please install it from https://pandoc.org/installing.html")
        return False

    # 2. Construct the base command
    # -f: from format (markdown)
    # -t: to format (docx)
    # -o: output file
    command = [
        "pandoc",
        markdown_filepath,
        "-f", "markdown",
        "-t", "docx",
        "-o", output_filepath
    ]

    # 3. Add reference document for custom styles if provided
    if reference_docx and os.path.exists(reference_docx):
        # --reference-docx tells pandoc to use the styles from this file
        command.append(f"--reference-docx={reference_docx}")
    elif reference_docx:
        print(f"Warning: Reference DOCX file not found at '{reference_docx}'. Using default styles.")

    print(f"Starting conversion of '{markdown_filepath}'...")

    try:
        # Run the Pandoc command
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        # Check for errors or warnings printed by Pandoc
        if result.stderr:
            print(f"Pandoc output (warnings/info):\n{result.stderr}")

        print(f"Success! DOCX file created at '{output_filepath}'")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error during conversion (Pandoc failed with return code {e.returncode}):")
        print(f"Command: {' '.join(command)}")
        print(f"Error Output:\n{e.stderr}")
        return False
    except FileNotFoundError:
        # Should be caught by shutil.which, but acts as a secondary safeguard
        print("Error: The 'pandoc' command was not found.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
