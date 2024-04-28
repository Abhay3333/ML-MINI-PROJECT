from nbconvert import ScriptExporter
import os

def notebook_to_python(notebook_file):
    # Create a ScriptExporter instance
    exporter = ScriptExporter()

    # Convert the notebook to a Python script
    output, _ = exporter.from_filename(notebook_file)

    # Create a Python script filename
    python_file = os.path.splitext(notebook_file)[0] + '.py'

    # Write the Python script
    with open(python_file, 'w') as f:
        f.write(output)

    print(f"Notebook '{notebook_file}' successfully converted to Python script '{python_file}'.")

if __name__ == "__main__":
    notebook_file = input("Enter the filename of the Jupyter Notebook (with .ipynb extension): ")
    notebook_to_python(notebook_file)
