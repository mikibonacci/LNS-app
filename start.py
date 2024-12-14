import ipywidgets as ipw


def get_start_widget(appbase, jupbase, notebase):  # noqa: ARG001
    return ipw.HTML(
        f"""
        <table>
        <tr>
        <th style="text-align:center">Options</th>
        </tr>
        <tr>
        <td style="text-align:center">
            <a href="{appbase}/mjolnir.ipynb" target="_blank">
                <img src="https://example.com/mjolnir_logo.jpg" height="60px" width="60px"><br>
                Mjolnir
            </a>
        </td>
        <td style="text-align:center">
            <a href="{appbase}/plot.ipynb" target="_blank">
                <img src="https://example.com/plot_logo.jpg" height="60px" width="60px"><br>
                Plot
            </a>
        </td>
        </tr>
        </table>
        """
    )
    
    #<div align="center">
    #    <a href="{appbase}/qe.ipynb" target="_blank">
    #        <img src="https://gitlab.com/QEF/q-e/raw/develop/logo.jpg" height="120px" width=243px">
    #    </a>
    #</div>"""
    #)
