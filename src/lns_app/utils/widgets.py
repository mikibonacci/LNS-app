import traitlets
import ipywidgets as ipw
import zipfile
import threading
import time
from pathlib import Path
from IPython.display import display, Javascript


# THIS LinkButton is a custom widget that creates a clickable link styled as a button.
# COPIED from aiidalab_qe.common.widgets.LinkButton, it is just faster for what concern the imports.

class LinkButton(ipw.HTML):
    disabled = traitlets.Bool(False)

    def __init__(
        self,
        description=None,
        link="",
        in_place=False,
        class_="",
        style_="",
        icon="",
        tooltip="",
        disabled=False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        html = f"""
            <a
                role="button"
                href="{link}"
                title="{tooltip or description}"
                target="{"_self" if in_place else "_blank"}"
                style="cursor: default; {style_}"
            >
        """
        if icon:
            html += f"<i class='fa fa-{icon}'></i>"

        html += f"{description}</a>"

        self.value = html

        self.add_class("jupyter-button")
        self.add_class("widget-button")
        self.add_class("link-button")
        self.add_class(class_)

        self.disabled = disabled

    @traitlets.observe("disabled")
    def _on_disabled(self, change):
        if change["new"]:
            self.add_class("disabled")
        else:
            self.remove_class("disabled")


class FilesNumberWidget(ipw.VBox):
    """Widget to select file numbers from a list of files."""

    def __init__(self, file_numbers, **kwargs):
        super().__init__(**kwargs)

        self.title = ipw.HTML(
            value="<h3>Select File Numbers</h3>",
            layout=ipw.Layout(margin="0px 0px 10px 0px"),
        )
        self.file_numbers_widget = ipw.SelectMultiple(
            options=file_numbers,
            value=file_numbers[0:1],
            disabled=False,
            layout=ipw.Layout(width="200px", height="100px"),
        ) 
        self.text = ipw.HTML("selected:")
        self.selected_file_numbers_widget = ipw.HTML(
            value=",".join(self.selected_file_numbers),
            layout=ipw.Layout(margin="0px 0px 0px 0px"),
        )
        self.file_numbers_widget.observe(
            lambda change: setattr(
                self.selected_file_numbers_widget, 
                "value", 
                ",".join(self.selected_file_numbers)
            ),
            names="value"
        )

        self.children = [
            self.title,
            self.file_numbers_widget,
            self.text,self.selected_file_numbers_widget,
        ]

    @property
    def selected_file_numbers(self):
        """Return the selected file numbers."""
        return [number for number in self.file_numbers_widget.value]
    
class PlotButton(ipw.HBox):
    def __init__(self, **kwargs):
        self.dQx = ipw.BoundedFloatText(
            value=0.03,
            min=0.01,
            step=0.005,
            description="dQx:",
            layout=ipw.Layout(width="150px"),
        )
        self.dQy = ipw.BoundedFloatText(
            value=0.03,
            min=0.01,
            step=0.005,
            description="dQy:",
            layout=ipw.Layout(width="150px"),
        )
        self.dE = ipw.BoundedFloatText(
            value=0.05,
            min=0.01,
            step=0.005,
            description="dE:",
            layout=ipw.Layout(width="150px"),
        )
        self.button = ipw.Button(
            description="Plot",
            icon="bar-chart",
            button_style="primary",
            layout=ipw.Layout(width="100px", height="40px"),
        )
        super().__init__([self.dQx, self.dQy, self.dE, self.button], **kwargs)


class ZipDownloadWidget(ipw.VBox):
    """Widget to create and download a zip file with selected data."""

    def __init__(self, file_selection_widget, path, year_number, proposal_id, **kwargs):
        """
        Args:
            file_selection_widget: The widget containing file selection (e.g., FilesNumberWidget)
            path: Path object pointing to the directory containing the files
            year_number: List/tuple containing the year number for filename construction
        """
        super().__init__(**kwargs)
        
        self.file_selection_widget = file_selection_widget
        self.path = path
        self.year_number = year_number
        self.proposal_id = proposal_id
        self._is_downloading = False
        
        # Download button
        self.download_button = ipw.Button(
            description="Download selected data",
            icon="download",
            button_style="success",
            layout=ipw.Layout(width="auto", height="40px"),
        )
        
        # Output area for messages
        self.output = ipw.Output()
        
        # Connect callbacks
        self.download_button.on_click(self._build_download_cleanup)
        
        self.children = [
            self.download_button,
            #self.output,
        ]
    
    def _build_download_cleanup(self, _):
        """Build and download zip file with selected data."""
        # Prevent multiple simultaneous downloads
        if self._is_downloading:
            return
        
        self._is_downloading = True
        self.download_button.disabled = True
        self.output.clear_output()
        
        with self.output:
            selected_files = self.file_selection_widget.file_numbers_widget.value
            
            if not selected_files:
                print("No files selected. Please select at least one file.")
                self._is_downloading = False
                self.download_button.disabled = False
                return
            
            try:
                # 1. Create zip file with meaningful name
                first_file = min(selected_files)
                last_file = max(selected_files)
                zip_filename = f"camea_data_{self.proposal_id}_{first_file}_{last_file}.zip"
                zip_path = Path(zip_filename)

                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for f in selected_files:
                        filename = f'camea{int(self.year_number)}n{f.zfill(6)}.hdf'
                        filepath = (self.path / filename).resolve()
                        if filepath.exists():
                            zf.write(filepath, arcname=filepath.name)

                # 2. Trigger browser download
                display(Javascript(f"""
                    (function() {{
                        const a = document.createElement('a');
                        a.href = '{zip_filename}';
                        a.download = '{zip_filename}';
                        a.style.display = 'none';
                        document.body.appendChild(a);
                        a.click();
                        setTimeout(() => document.body.removeChild(a), 100);
                    }})();
                """))

                # 3. Delayed cleanup after 5 minutes (safe)
                def cleanup_later(p, delay=5*60):
                    time.sleep(delay)
                    p.unlink(missing_ok=True)

                threading.Thread(
                    target=cleanup_later,
                    args=(zip_path,),
                    daemon=True
                ).start()
                
                print(f"Zip file created successfully with {len(selected_files)} file(s). Download should start automatically.")
                
            except Exception as e:
                print(f"Error creating zip file: {e}")
            finally:
                self._is_downloading = False
                self.download_button.disabled = False
