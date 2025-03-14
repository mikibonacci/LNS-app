import ipywidgets as ipw
import subprocess
import threading
from pathlib import Path

from lns_app.notebook_generator import generate_notebook_file
import shutil

from aiidalab_qe.common.widgets import LinkButton

default_example_folder = root_path = Path.resolve(Path(__file__) / '..' / '..' / '..' / 'examples' / 'Mnf2_oct_2021' / 'data')
default_proposals_folder = root_path = Path('/mnt/camea_data/')

class ProposalsManagerMVC(ipw.VBox):
    """class to manage proposals

    TODO: use traits, and make it more modular, in particular the changing HTML values.
    """
    
    def __init__(
        self, 
        proposals_folder: Path = Path('/mnt/camea_data/'), 
        examples_folder: Path = default_example_folder,
        analysis_folder: Path = Path('/mnt/camea_analysis/'),
        testing_folder: Path = Path('/mnt/camea_testing/'),
    ):
        
        self.rendered = False
        self.examples_folder = examples_folder
        self.proposals_folder = proposals_folder
        self.observed_folder = self.proposals_folder
        self.proposals = []
        
        self.analysis_folder = analysis_folder
        self.testing_folder = testing_folder
        
        self.destination_folder = self.analysis_folder
        
        super().__init__()
        
    def render(self):
        """Render the widget
        """
        if self.rendered:
            return
        
        self.rendered = True
        
        self.proposals = self.discover_proposals()
        
        ###### PROPOSALS FOLDER WIDGETS ######
        
        # 1. provide a proposal folder
        self.proposals_folder_text = ipw.Text(
            value=str(self.observed_folder),
            disabled=False,
        )
        self.proposal_search_button = ipw.Button(
            description='Search path',
            icon="search",
            disabled=False,
        )
        self.proposal_search_button.on_click(self.new_path_refresh_search)

        self.proposal_search_reset_button = ipw.Button(
            description='Reset search path',
            icon="refresh",
            tooltip="Reset the search path to the default one, i.e. /mnt/camea_data/",
            disabled=False,
        )
        self.proposal_search_reset_button.on_click(self.reset_search)
        
        self.search_examples_button = ipw.Button(
            description='Search examples',
            tooltip="Search examples",
            disabled=False,
            icon = "search",
        )
        self.search_examples_button.on_click(self.search_examples)
        
        self.folder_search_box = ipw.HBox([
                    self.proposals_folder_text,
                    self.proposal_search_button,   
                    self.proposal_search_reset_button,
                    self.search_examples_button
                ])
        
        ###### PROPOSALS ID WIDGETS ########
        if not self.proposals or not self.observed_folder:
            self.children = [
                ipw.HTML(f'Directory {self.observed_folder} does not exist. Please provide a valid directory.'),
                self.folder_search_box
            ]
            self.proposals_folder_text.disabled = False
            self.proposal_search_button.disabled = False
            return
        elif len(self.proposals) == 0:
            self.children = [
                ipw.HTML(f'No proposals found in {self.observed_folder}. Please provide a valid directory.'),
                self.folder_search_box,
            ]
            self.proposals_folder_text.disabled = False
            self.proposal_search_button.disabled = False
            return

        self.proposal_id = ipw.Dropdown(
            options=[None]+self.proposals,
            description='Proposal ID:',
            disabled=False,
            value=None,
        )
        self.proposal_id.observe(self.on_proposal_id_change, names='value')
        
        self.refresh_search_button = ipw.Button(
            description='Refresh search',
            icon="refresh",
            disabled=False,
        )
        self.refresh_search_button.on_click(self.refresh_search)
        
        self.proposals_box = ipw.VBox([
            self.folder_search_box,
            ipw.HBox([
                self.proposal_id,
                self.refresh_search_button,
            ]),
        ])
            
        ##### CREATE NOTEBOOK WIDGETS #####
        self.create_analysis_button = ipw.Button(
            description='Create notebook', style={"button_color":"lightgreen"}, disabled=True
        )
        self.create_analysis_button.on_click(self.create_analysis_folder)
        
        self.create_analysis_text = ipw.HTML("")
        
        self.create_notebook_box = ipw.HBox([
            self.create_analysis_button, 
            self.create_analysis_text,
            ])
        
        ##### OPEN NOTEBOOK WIDGETS #####
        self.open_analysis_button = ipw.HTML()
        ############ APP MODE WIDGETS #####
        self.app_mode = ipw.Checkbox(
            value=True,
            description='Open in app mode',
            disabled=False,
            indent=False
        )
        self.app_mode.observe(lambda x: self.init_open_analysis_button(), names='value')
        
        self.open_analysis_box = ipw.HBox([
            self.open_analysis_button,
            self.app_mode,
        ])
        
        ##### DELETE NOTEBOOK WIDGETS #####
        ########## STEP 1 ##########
        self.delete_analysis_button = ipw.Button(
            description='Delete notebook', button_style='danger', disabled=False
        )
        self.delete_analysis_button.on_click(self.delete_analysis_first)
        
        self.delete_analysis_text = ipw.HTML("""This deletes the notebook related to the selected proposal.""")
        
        self.first_step_delete_notebook_box = ipw.HBox([
            self.delete_analysis_button, 
            self.delete_analysis_text,
            ],
        )

        ########## STEP 2 ##########
        self.delete_confirmation_description = ipw.HTML(
        'Please type "DELETE" and press enter to confirm:'
        )
        self.delete_confirmation_text = ipw.Text(
            placeholder='',
            disabled=False,
        )
                
        self.delete_confirmation_button = ipw.Button(
            description='Confirm', button_style='warning', disabled=True
        )
        ipw.dlink((self.delete_confirmation_text, 'value'), (self.delete_confirmation_button, 'disabled'), lambda x: x != 'DELETE')
        self.delete_confirmation_button.on_click(self.delete_analysis_second)
        
        self.delete_confirmation_box = ipw.HBox([
            self.delete_confirmation_description,
            self.delete_confirmation_text,
            self.delete_confirmation_button,
        ])
        
        self.change_display_open_delete_boxes('none')
        
        self.proposal_files= ipw.HTML()
        
        self.children = [
            self.proposals_box,
            self.create_notebook_box,
            self.open_analysis_box,
            self.first_step_delete_notebook_box,
            self.delete_confirmation_box,
            self.proposal_files,
            ]
        
    def refresh_search(self, _):
        self.rendered = False
        self.render()
        
    def new_path_refresh_search(self, _):
        self.observed_folder = Path(self.proposals_folder_text.value)
        self.refresh_search(_)
    
    def reset_search(self, _):
        self.proposals_folder_text.value = str(default_proposals_folder)
        self.observed_folder = default_proposals_folder
        self.new_path_refresh_search(_)
    
    def discover_proposals(self, ):
        """Discover proposals in proposals_folder
        """
        if self.observed_folder.exists() and self.observed_folder.is_dir():
            return [p.name for p in self.observed_folder.iterdir() if p.is_dir()]
        elif not self.observed_folder.exists():
            return None
        
        return []
    
    def search_examples(self, change):
        """Callback when search_examples_button changes
        """
        
        self.proposals_folder_text.value = str(self.examples_folder)
        self.observed_folder = self.examples_folder
        self.destination_folder = self.testing_folder
        self.proposals = self.discover_proposals()
        
        # else:
        #     self.proposals_folder_text.value = str(default_proposals_folder)
        #     self.observed_folder = self.proposals_folder
        #     self.destination_folder = self.analysis_folder
        #     self.proposals = self.discover_proposals()
        
        
        if hasattr(self, 'proposal_id'):
            self.proposal_id.value = None
            self.proposal_id.options = [None]+self.proposals 
            self.proposal_files.value = ""
            self.create_analysis_text.value = ""
            self.change_display_open_delete_boxes('none')
        
        self.refresh_search(None)
        
    
    def on_proposal_id_change(self, change):
        """Callback when proposal_id changes
        """
        if not self.proposal_id.value:
            self.create_analysis_button.disabled = True
            self.change_display_open_delete_boxes('none')
            return
        else:
            self.delete_analysis_text.value = """This deletes the notebook related to the selected proposal."""
            
        # 1. check the proposal folder content
        results = self.run_detect_proposal_history_in_thread(change.new)
        files_info = "<br>".join(results[0])
        self.proposal_files.value = f"""
        <h4>Files contained in the mounted proposal folder (ID: {self.proposal_id.value}):</h4>
        
        {files_info}
        """
        
        # 2. check if we can create a notebook and we have the analysis folder
        if "not correct format" in files_info:
            self.create_analysis_text.value = f"""Proposal data not in the correct format. Are you sure it is the correct folder? Try to change the search path."""
            self.create_analysis_button.disabled = True
            self.change_display_open_delete_boxes('none')
        elif not self.proposal_folder_exists() or not self.analysis_notebook_exists():
            self.create_analysis_text.value = f"""Create notebook for the selected proposal (ID: {self.proposal_id.value})."""
            self.create_analysis_button.disabled = False
            self.change_display_open_delete_boxes('none')
        else:
            self.create_analysis_text.value = f"Analysis notebook exists."
            self.create_analysis_button.disabled = True
            self.change_display_open_delete_boxes('block')
        
        
        
    
    def delete_analysis_first(self, _):
        
        if not self.proposal_id.value:
            return   
        
        self.delete_confirmation_box.layout.display = 'block'

    def delete_analysis_second(self, _):
        """Callback when delete_confirmation_text changes
        """
        # DELETE THE NOTEBOOK, THEN:
        
        # 1. delete the analysis folder
        # not the best way
        if self.proposal_folder_exists():
            (self.destination_folder / self.proposal_id.value / f"notebook_proposal{self.proposal_id.value}.ipynb").unlink(missing_ok=True)
            shutil.rmtree(self.destination_folder / self.proposal_id.value / ".ipynb_checkpoints", ignore_errors=True)
        self.create_analysis_button.disabled = False
        self.delete_confirmation_box.layout.display = 'none'
        self.change_display_open_delete_boxes('none')
        
        self.delete_analysis_text.value = f"Analysis notebook for {self.proposal_id.value} deleted."
        self.create_analysis_text.value = f"""Create notebook for the selected proposal (ID: {self.proposal_id.value})."""
    
    def create_analysis_folder(self, _):
        """Create analysis folder for the proposal
        """   
        if not self.proposal_id.value:
            return 
             
        self.generate_folder()
        self.generate_notebook()
        
        self.create_analysis_button.disabled = True
        self.delete_analysis_text.value = """This deletes the notebook related to the selected proposal."""
        self.create_analysis_text.value = f"Analysis notebook created."
        self.change_display_open_delete_boxes('block')
    
    def detect_proposal_history(self, proposal_name: str):
        """Detect proposal history using MJOLNIRHistory command"""
        files = subprocess.run(f"MJOLNIRHistory {self.observed_folder / proposal_name}/*", shell=True, 
                               capture_output=True, text=True)
        return files.stdout.strip().split("\n"), files.stderr.strip().split("\n")

    def run_detect_proposal_history_in_thread(self, proposal_name: str):
        """Function to run detect_proposal_history in a separate thread and return the results
        
        It uses the MJOLNIRHistory command - as implemented in the *detect_proposal_history* method-to detect the proposal history.
        """
        result = []

        thread = threading.Thread(target=lambda: result.extend(self.detect_proposal_history(proposal_name)))
        thread.start()
        thread.join()  # Wait for the thread to finish
        
        return result

    def proposal_folder_exists(self):
        if not self.proposal_id.value:
            return False
        return (self.destination_folder / self.proposal_id.value).exists()
    
    def analysis_notebook_exists(self):
        if not self.proposal_id.value:
            return False
        return (self.destination_folder / self.proposal_id.value / f"notebook_proposal{self.proposal_id.value}.ipynb").exists()
    
    def generate_folder(self):
        if not self.proposal_folder_exists():
            (self.destination_folder / self.proposal_id.value).mkdir(parents=True, exist_ok=True)
    
    def generate_notebook(self):
        if not self.analysis_notebook_exists():
            # create the analysis notebook via templating it
            generate_notebook_file(
                proposal_id = self.proposal_id.value, 
                dest_path = str(self.destination_folder), 
                data_path = str(self.observed_folder),
                ) 
    
    @staticmethod
    def get_correct_nb_directory(notebook_dir, notebook_name):
        from notebook.notebookapp import list_running_servers
        import urllib.parse
        import os

        # Get the root notebook directory
        servers = list(list_running_servers())
        if servers:
            root_dir = servers[0]['notebook_dir']  # Jupyter root directory
        else:
            root_dir = os.getcwd()  # Fallback to current working directory

        JUPYTERHUB_DOMAIN = os.getenv("JUPYTERHUB_DOMAIN", "http://localhost:8888")  # Default domain
        base_url = servers[0].get("base_url", "/")
        
        # Construct the correct relative URL
        notebook_path = os.path.relpath(notebook_dir, root_dir)
        notebook_rel_path_url = f"{urllib.parse.quote(notebook_path)}/{notebook_name}"
        base_nb_url = f"{JUPYTERHUB_DOMAIN}{base_url}"

        # Print the correct URL
        #print("Correct Notebook URL:", notebook_url)
        
        return base_nb_url, notebook_rel_path_url

    def init_open_analysis_button(self):
        notebook_dir = str(self.destination_folder / self.proposal_id.value) 
        notebook_name = f"notebook_proposal{self.proposal_id.value}.ipynb"
        base_nb_url, notebook_rel_path_url = self.get_correct_nb_directory(notebook_dir, notebook_name)
        mode = "apps" if self.app_mode.value else "notebooks"
        self.open_analysis_box.children =(
            LinkButton(
                description="Open notebook",
                link=f"{base_nb_url}{mode}/{notebook_rel_path_url}",
                #icon="list",
                class_="mod-primary",
                style_="color: white;",
                disabled=False,
            ),
            self.open_analysis_box.children[1],
        )
    
    def change_display_open_delete_boxes(self, display):
        self.open_analysis_box.layout.display = display
        self.first_step_delete_notebook_box.layout.display = display
        self.delete_confirmation_box.layout.display = 'none'
        
        if display == "block" and self.analysis_notebook_exists():
            self.init_open_analysis_button()
                                              
