import json
from pathlib import Path

TEXT_FIRST_CELL = """
# Data Analysis for Proposal --PROPOSAL_ID--

This notebook provides a tools for a detailed analysis of the measured data for the specified proposal. 

You can use the notebook both in Editable or App mode.
"""

def generate_notebook_file(proposal_id: str, dest_path: str, data_path: str, index_cell: int = 2, notebook_template_path: str = None):
    """_summary_

    Args:
        proposal_id (_type_): _description_
        path (_type_): _description_
        index_cell (_type_): _description_
        notebook_template_path (_type_): _description_
    """
    
    if notebook_template_path is None:
        notebook_template_path = Path(__file__).parent / '..' / '..' / '..' / 'templates' / 'template_1.ipynb'
    
    
    with open(notebook_template_path, 'r') as f:
        notebook = json.load(f)
    
    source = "SPLIT".join(notebook['cells'][index_cell]['source'])
    source = source.replace("--PROPOSAL_ID--", proposal_id)
    source = source.replace("--PATH--", data_path)
    
    notebook['cells'][index_cell]['source'] = source.split("SPLIT")
    
    notebook['cells'][0]['source'] = TEXT_FIRST_CELL.replace("--PROPOSAL_ID--", proposal_id)
    
    with open(dest_path+f'/{proposal_id}/notebook_proposal{proposal_id}.ipynb', 'w') as f:
        json.dump(notebook, f, indent=4)
    
