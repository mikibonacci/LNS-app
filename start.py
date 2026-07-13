import ipywidgets as ipw


def get_start_widget(appbase, jupbase, notebase):  # noqa: ARG001
    return ipw.HTML(f"""
        <div class="app-container">
            <h1
            style="text-align:center;
            font-size:30px;">
            LNS apps and tools</h1>
            <div class="features">
                <a
                    class="feature"
                    href=f"{jupbase}/tree/SINQ_data"
                    target="_blank"
                    title="Explore and download SINQ data from assigned instruments"
                >
                    <i
                        class="fa fa-folder-open feature-logo"
                        style="font-size:40px;"
                        alt="Plot">
                    </i>
                    <div class="feature-label">Explore SINQ data</div>
                </a>
                <a
                    class="feature"
                    href="{appbase}/plot.ipynb"
                    target="_blank"
                    title="Plot any 2D data (uploaded as CSV)"
                >
                    <i
                        class="fa fa-bar-chart feature-logo"
                        style="font-size:40px;"
                        alt="Plot">
                    </i>
                    <div class="feature-label">Plot 2D data</div>
                </a>
                <a
                    class="feature"
                    href="{appbase}/proposal_history.ipynb"
                    target="_blank"
                    title="Select and analyze data from the CAMEA instrument (using MJOLNIR)"
                >
                    <i
                        class="fa fa-folder-open feature-logo"
                        style="font-size:40px;"
                        alt="Mjolnir analysis">
                    </i>
                    <div class="feature-label">Analyze CAMEA data (MJOLNIR)</div>
                </a>
                <a
                    class="feature"
                    href="{appbase}/image-viewer-demo-ICON.ipynb"
                    target="_blank"
                    title="Select and analyze data from the ICON imaging instrument"
                >
                    <i
                        class="fa fa-folder-open feature-logo"
                        style="font-size:40px;"
                        alt="Mjolnir analysis">
                    </i>
                    <div class="feature-label">Analyze ICON data</div>
                </a>
            </div>
        </div>
        <div style="text-align:left; margin-top:0px;">
            <a href="https://www.psi.ch/en/sinq/camea" target="_blank">Go to CAMEA webpage</a> <br>
            <a href="https://mjolnir.readthedocs.io/en/latest/index.html" target="_blank">Go to MJOLNIR Documentation</a> <br>
            <a href="https://www.psi.ch/en/sinq/icon" target="_blank">Go to ICON webpage</a>
        </div>
    """)
