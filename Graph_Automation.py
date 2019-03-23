from scipy.sparse import coo_matrix

class GSP:
    def __init__(self, kpi_zip, conn_zip):
        kpi_zip = dict(kpi_zip)
        conn_zip = dict(conn_zip)
        common = set(kpi_zip.keys()) & set(conn_zip.keys())
        all = set(kpi_zip.keys()) | set(conn_zip.keys())
        for item in (all - common):
            if item in kpi_zip:
                del kpi_zip[item]
            if item in conn_zip:
                del conn_zip[item]
        self.kpi_dict = kpi_zip
        self.conn_dict = conn_zip
        self.is_connected = False

    def graph_signal(self):
        pass

    def gsp_plots(self):
        pass
