import ipywidgets as ipw


def get_start_widget(appbase, jupbase, notebase):  # noqa: ARG001
    return ipw.HTML(f"""
        <div class="app-container">
            <h1 
            style="text-align:center; 
            font-size:30px;">
            LNS Apps and tools</h1>
            <div class="features">
                <a
                    class="feature"
                    href="{appbase}/plot.ipynb"
                    target="_blank">
                    <i 
                        class="fa fa-bar-chart feature-logo" 
                        style="font-size:40px;" 
                        alt="Plot">
                    </i>
                    <div class="feature-label">Plot GUI</div>
                </a>
                <a
                    class="feature"
                    href="{appbase}/proposal_history.ipynb"
                    target="_blank">
                    <i 
                        class="fa fa-folder-open feature-logo" 
                        style="font-size:40px;" 
                        alt="Mjolnir analysis">
                    </i>
                    <div class="feature-label">Analysis of CAMEA data (MJOLNIR)</div>
                </a>
                <a
                    class="feature"
                    href="{appbase}/image-viewer-demo-ICON.ipynb"
                    target="_blank">
                    <i 
                        class="fa fa-folder-open feature-logo" 
                        style="font-size:40px;" 
                        alt="Mjolnir analysis">
                    </i>
                    <div class="feature-label">Analysis of ICON (imaging data)</div>
                </a>
            </div>
        </div>
        <div style="text-align:left; margin-top:0px;">
            <a href="https://www.psi.ch/en/sinq/camea" target="_blank">Go to CAMEA webpage</a> <br>
            <a href="https://mjolnir.readthedocs.io/en/latest/index.html" target="_blank">Go to MJOLNIR Documentation</a>
            <a href="https://www.psi.ch/en/sinq/icon" target="_blank">Go to ICON webpage</a>
        </div>
    """)
    
