import ipywidgets as ipw
import subprocess
import threading
from pathlib import Path

default_example_folder = root_path = Path.resolve(Path(__file__) / '..' / '..' / 'data-examples' / 'Mnf2_oct_2021' / 'data')

class ProposalsManagerMVC(ipw.VBox):
    """class to manage proposals
    
    TODO: use traits for disabling and enabling buttons.
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
        
        if not self.proposals:
            self.children = [
                ipw.HTML(f'Directory {self.proposals_folder} does not exist.')    
            ]
            return
        elif len(self.proposals) == 0:
            self.children = [
                ipw.HTML(f'No proposals found in {self.proposals_folder}.')    
            ]
            return

        self.proposal_id = ipw.Dropdown(
            options=self.proposals,
            description='Proposal ID:',
            disabled=False,
            value=None,
        )
        self.proposal_id.observe(self.on_proposal_id_change, names='value')
        
        self.examples_id_checkbox = ipw.Checkbox(
            value=False,
            description='Just use examples',
            disabled=False,
            indent=False
        )
        self.examples_id_checkbox.observe(self.on_examples_checkbox_change, names='value')
        
        self.proposal_info = ipw.HTML()
        
        self.create_analysis_button = ipw.Button(
            description='Create notebook', style={"button_color":"lightgreen"}, disabled=True
        )
        self.create_analysis_button.on_click(self.create_analysis_folder)
        
        self.open_analysis_button = ipw.Button(
            description='Open notebook', button_style='primary', disabled=True
        )
        self.open_analysis_button.on_click(self.open_analysis)
        
        self.reset_analysis_button = ipw.Button(
            description='Reset notebook', button_style='warning', disabled=True
        )
        ipw.dlink((self.open_analysis_button, 'disabled'), (self.reset_analysis_button, 'disabled'))
        self.reset_analysis_button.on_click(self.reset_analysis)
        
        self.app_mode = ipw.Checkbox(
            value=True,
            description='Open in app mode',
            disabled=True,
            indent=False
        )
        ipw.dlink((self.open_analysis_button, 'disabled'), (self.app_mode, 'disabled'))
        
        self.proposal_files= ipw.HTML()    
        
        self.children = [
            ipw.HBox([self.proposal_id, self.examples_id_checkbox]),
            self.proposal_info,
            self.create_analysis_button,
            ipw.HBox(
                [
                    self.open_analysis_button,
                    self.app_mode,
                ],
            ),
            ipw.HBox([self.reset_analysis_button, ipw.HTML("""This re-initializes the notebook related to the selected proposal.""")]),
            self.proposal_files,
            ]
    
    def discover_proposals(self, ):
        """Discover proposals in proposals_folder
        """
        if self.observed_folder.exists() and self.observed_folder.is_dir():
            return [p.name for p in self.observed_folder.iterdir() if p.is_dir()]
        elif not self.observed_folder.exists():
            return None
        
        return []
    
    def on_examples_checkbox_change(self, change):
        """Callback when examples_id_checkbox changes
        """
        if change.new:
            self.observed_folder = self.examples_folder
            self.destination_folder = self.testing_folder
            self.proposals = self.discover_proposals()
        else:
            self.observed_folder = self.proposals_folder
            self.destination_folder = self.analysis_folder
            self.proposals = self.discover_proposals()
            
        self.proposal_id.value = None
        self.proposal_info.value = ""
        self.proposal_files.value = ""
    
    def on_proposal_id_change(self, change):
        """Callback when proposal_id changes
        """
        if not self.proposal_id.value:
            self.create_analysis_button.disabled = True
            self.open_analysis_button.disabled = True
            return
        else:
            self.open_analysis_button.disabled = False
            
        
        # 1. check if we have the analysis folder
        if not self.proposal_folder_exists() or not self.analysis_notebook_exists():
            self.proposal_info.value += f"""<br>The notebook for the selected proposal (ID: {self.proposal_id.value}) do not exist.<br>
            It can be initialized by clicking the 'Create notebook' button.
            """
            self.create_analysis_button.disabled = False
            self.open_analysis_button.disabled = True
        else:
            self.proposal_info.value = f"Analysis notebook exists."
            self.open_analysis_button.disabled = False
            self.create_analysis_button.disabled = True
        
        # 2. check the proposal folder content
        results = self.run_detect_proposal_history_in_thread(change.new)
        files_info = "<br>".join(results[0])
        self.proposal_files.value = f"Files contained in the mounted proposal folder:<br>{files_info}"
        if len(results[1]) > 0:
            self.proposal_files.value += "\n" + "\n".join(results[1])
    
    def reset_analysis(self, _):
        
        if not self.proposal_id.value:
            return   
    
    def create_analysis_folder(self, _):
        """Create analysis folder for the proposal
        """   
        if not self.proposal_id.value:
            return 
             
        self.generate_folder()
        self.generate_notebook()
        
        self.create_analysis_button.disabled = True
        self.open_analysis_button.disabled = False
        
        
    def open_analysis(self, _):
        """Callback when open_analysis_button is clicked
        """
        if not self.proposal_id.value:
            return
        
        # 1. open the analysis notebook
        pass
    
    
    def detect_proposal_history(self, proposal_name: str):
        """Detect proposal history using MJOLNIRHistory command"""
        files = subprocess.run(f"MJOLNIRHistory {self.proposals_folder / proposal_name}/*", shell=True, 
                               capture_output=True, text=True)
        return files.stdout.strip().split("\n"), files.stderr.strip().split("\n")

    # Function to run detect_proposal_history in a separate thread and return the results
    def run_detect_proposal_history_in_thread(self, proposal_name: str):
        result = []

        thread = threading.Thread(target=lambda: result.extend(self.detect_proposal_history(proposal_name)))
        thread.start()
        thread.join()  # Wait for the thread to finish
        
        return result

    
    def proposal_folder_exists(self):
        return (self.destination_folder / self.proposal_id.value).exists()
    
    def analysis_notebook_exists(self):
        return (self.destination_folder / self.proposal_id.value / f"{self.proposal_id.value}_analysis.ipynb").exists()
    
    def generate_folder(self):
        if not self.proposal_folder_exists():
            (self.destination_folder / self.proposal_id.value).mkdir(parents=True, exist_ok=True)
            #self.proposal_info.value = f"Analysis folder {self.destination_folder / self.proposal_id.value} created."
    
    def generate_notebook(self):
        if not self.analysis_notebook_exists():
            # create the analysis notebook via templating it
            #self.generate_notebook(self.proposal_id.value)  
            self.proposal_info.value = "(not for real:) Analysis notebook created."
            pass