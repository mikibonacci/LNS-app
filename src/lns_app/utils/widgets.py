import traitlets
import ipywidgets as ipw

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


