import ipywidgets as ipw


def get_start_widget(appbase, jupbase, notebase):  # noqa: ARG001
    return ipw.HTML(f"""
        <div class="app-container">
            <h1 
            style="text-align:center; 
            font-size:30px;">
            Tools for the Multiplexing Spectrometer CAMEA</h1>
            <div class="features">
                <a
                    class="feature"
                    href="{appbase}/src/lns_app/plot.ipynb"
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
                    href="{notebase}/src/lns_app/mjolnir.ipynb"
                    target="_blank">
                    <i 
                        class="fa fa-laptop feature-logo" 
                        style="font-size:40px;" 
                        alt="Mjolnir analysis">
                    </i>
                    <div class="feature-label">Mjolnir analysis (Jupyter notebook)</div>
                </a>
            </div>
        </div>
    """)
    
    
    
    return ipw.HTML(
        f"""
        <div class="app-container">
            <h1 style="text-align:center; font-size:50px;">LNS Apps</h1>
            <div class="features">
                <a 
                    class="feature"
                    href="{appbase}/mjolnir.ipynb" 
                    target="_blank">
                    <i 
                        class="fa fa-laptop feature-logo" 
                        style="font-size:40px;" 
                        alt="Mjolnir analysis"
                    </i>
                    <div class="feature-label">Mjolnir analysis</div>
                </a>
            </div>
        </div>
        """
    )

    
