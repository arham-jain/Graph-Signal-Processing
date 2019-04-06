from scipy.sparse import coo_matrix
from statistics import median
from pygsp import graphs, plotting
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from math import sqrt


class GSP:
    def __init__(self, kpi_zip, conn_zip):
        kpi_zip = dict(kpi_zip)
        conn_zip = dict(conn_zip)
        common = set(kpi_zip.keys()) & set(conn_zip.keys())
        all = set(kpi_zip.keys()) | set(conn_zip.keys())
        self.unique_len = len(common)
        for item in (all - common):
            if item in kpi_zip:
                del kpi_zip[item]
            if item in conn_zip:
                del conn_zip[item]
        self.kpi_dict = kpi_zip
        self.conn_dict = conn_zip
        self.is_connected = False

    def graph_signal(self):
        #connectivity and connected graph creation
        conn_list = [[k,v] for k,v in self.conn_dict.items()]
        node1 = []
        node2 = []
        distance = []
        for i in range(len(conn_list)):
            for j in range(i+1,len(conn_list)):
                node1.append(conn_list[i][0])
                node2.append(conn_list[j][0])
                distance.append(abs(conn_list[i][1] - conn_list[j][1]))

        allnodes = node1 + node2
        allnodes = list(set(allnodes))
        self.ref_nodes = {}
        for i in range(len(allnodes)):
            self.ref_nodes[allnodes[i]] = i

        threshold = median(distance)  # can be optimised

        #computing G for the first time
        filtered_node1 = []
        filtered_node2 = []
        filtered_distance = []
        for i in range(len(distance)):
            if distance[i] <= threshold:
                filtered_node1.append(self.ref_nodes[node1[i]])
                filtered_node2.append(self.ref_nodes[node2[i]])
                filtered_distance.append(distance[i])

        matrix = coo_matrix((filtered_distance, (filtered_node1, filtered_node2)),
                            shape=(self.unique_len, self.unique_len)).todense()
        symm_mat = matrix + matrix.T
        G = graphs.Graph(symm_mat)

        while (G.is_connected() == False):
            filtered_node1 = []
            filtered_node2 = []
            filtered_distance = []
            for i in range(len(distance)):
                if distance[i] <= threshold:
                    filtered_node1.append(self.ref_nodes[node1[i]])
                    filtered_node2.append(self.ref_nodes[node2[i]])
                    filtered_distance.append(distance[i])

            matrix = coo_matrix((filtered_distance, (filtered_node1, filtered_node2)), shape=(self.unique_len, self.unique_len)).todense()
            symm_mat = matrix + matrix.T
            G = graphs.Graph(symm_mat)
            threshold = threshold + (0.005 * threshold)
        self.G = G
        print(symm_mat)
        print(self.kpi_dict)
        print(self.conn_dict)

        # graph signal creation
        signal = [0 for i in range(self.unique_len)]
        for k,v in self.kpi_dict.items():
            signal[self.ref_nodes[k]] = v
        self.signal = np.asarray(signal)

    def gsp_plots(self):
        plt.ioff()
        self.G.set_coordinates('ring2D')
        plotting.plot_graph(self.G, save_as="static/images/gsp/graph", plot_name="Connected Graph")

        plotting.plot_signal(self.G, self.signal, vertex_size=50, save_as="static/images/gsp/graph_signal", plot_name="Graph Signal")

        self.G.compute_fourier_basis()

        #print eigenvectors
        print(self.G.U)

        self.G.set_coordinates('spring')

        #compute fourier coeffecients
        f_hat = self.G.gft(self.signal)
        print(f_hat)
        top_4 = sorted(zip(f_hat,[i for i in range(len(f_hat))]), reverse=True)[:4]

        plotting.plot_signal(self.G, self.G.U[:, top_4[0][1]], vertex_size=50, save_as="static/images/gsp/eigen_vector1", plot_name="Dominant Eigen Vector #1")
        plotting.plot_signal(self.G, self.G.U[:, top_4[1][1]], vertex_size=50, save_as="static/images/gsp/eigen_vector2", plot_name="Dominant Eigen Vector #2")
        plotting.plot_signal(self.G, self.G.U[:, top_4[2][1]], vertex_size=50, save_as="static/images/gsp/eigen_vector3", plot_name="Dominant Eigen Vector #3")
        plotting.plot_signal(self.G, self.G.U[:, top_4[3][1]], vertex_size=50, save_as="static/images/gsp/eigen_vector4", plot_name="Dominant Eigen Vector #4")

    def dist_eu(self, feat_one, feat_two):
        squared_distance = 0
        for i in range(len(feat_one)):
            squared_distance += (feat_one[i]-feat_two[i]) ** 2
        ed = sqrt(squared_distance)
        return ed;

    def clustering(self, num):
        kmeans = KMeans(n_clusters=num)
        kmeans.fit(self.G.U)
        print(kmeans.cluster_centers_)
        print(kmeans.labels_)
        new_dict = {}
        for k,v in self.ref_nodes.items():
            new_dict[v] = k
        for i in range(num):
            print("Cluster #"+str(i))
            for j in range(len(kmeans.labels_)):
                if kmeans.labels_[j] == i:
                    print(new_dict[j])

        #Uncomment the following code to test the clusters

# kpi = [('Afghanistan', 19.0), ('Albania', 87.0), ('Algeria', 80.0), ('American Samoa', 87.0), ('Andorra', 87.0), ('Angola', 33.0), ('Antigua and Barbuda', 87.0), ('Argentina', 87.0), ('Armenia', 80.0), ('Australia', 87.0), ('Austria', 87.0), ('Azerbaijan', 80.0), ('Bahamas, The', 87.0), ('Bahrain', 87.0), ('Bangladesh', 26.0), ('Barbados', 87.0), ('Belarus', 80.0), ('Belgium', 87.0), ('Belize', 87.0), ('Benin', 45.0), ('Bhutan', 80.0), ('Bolivia', 66.0), ('Bosnia and Herzegovina', 80.0), ('Botswana', 59.0), ('Brazil', 87.0), ('British Virgin Islands', 87.0), ('Brunei Darussalam', 87.0), ('Bulgaria', 80.0), ('Burkina Faso', 28.0), ('Burundi', 35.0), ('Cambodia', 27.0), ('Cameroon', 11.0), ('Canada', 87.0), ('Cayman Islands', 87.0), ('Chile', 87.0), ('China', 33.0), ('Colombia', 80.0), ('Comoros', 57.0), ('Congo, Dem. Rep.', 40.0), ('Congo, Rep.', 80.0), ('Costa Rica', 80.0), ("Cote d'Ivoire", 25.0), ('Croatia', 87.0), ('Cuba', 87.0), ('Cyprus', 87.0), ('Czech Republic', 87.0), ('Denmark', 87.0), ('Djibouti', 80.0), ('Dominican Republic', 80.0), ('East Asia & Pacific', 28.0), ('East Asia & Pacific (excluding high income)', 26.0), ('Ecuador', 80.0), ('Egypt, Arab Rep.', 60.0), ('El Salvador', 80.0), ('Eritrea', 110.0), ('Estonia', 87.0), ('Eswatini', 80.0), ('Ethiopia', 32.0), ('Europe & Central Asia', 83.0), ('Europe & Central Asia (excluding high income)', 82.0), ('Fiji', 80.0), ('Finland', 87.0), ('France', 83.0), ('French Polynesia', 87.0), ('Gambia, The', 68.0), ('Georgia', 37.0), ('Germany', 87.0), ('Ghana', 27.0), ('Greece', 87.0), ('Guam', 87.0), ('Guatemala', 80.0), ('Guinea', 27.0), ('Guinea-Bissau', 34.0), ('Guyana', 80.0), ('Haiti', 45.0), ('High income', 88.0), ('Honduras', 80.0), ('Hong Kong SAR, China', 87.0), ('Hungary', 87.0), ('Iceland', 87.0), ('India', 37.0), ('Indonesia', 11.0), ('Iran, Islamic Rep.', 80.0), ('Iraq', 82.0), ('Ireland', 87.0), ('Israel', 87.0), ('Italy', 87.0), ('Jamaica', 80.0), ('Japan', 87.0), ('Jordan', 80.0), ('Kazakhstan', 100.0), ('Kenya', 45.0), ('Kiribati', 80.0), ('Korea, Dem. People’s Rep.', 29.0), ('Korea, Rep.', 94.0), ('Kuwait', 87.0), ('Kyrgyz Republic', 52.0), ('Lao PDR', 13.0), ('Latin America & Caribbean', 79.0), ('Latin America & Caribbean (excluding high income)', 79.0), ('Latvia', 87.0), ('Lebanon', 87.0), ('Lesotho', 53.0), ('Liberia', 22.0), ('Libya', 63.0), ('Lithuania', 87.0), ('Low & middle income', 35.0), ('Low income', 35.0), ('Lower middle income', 30.0), ('Luxembourg', 87.0), ('Macao SAR, China', 87.0), ('Macedonia, FYR', 80.0), ('Malawi', 53.0), ('Malaysia', 87.0), ('Maldives', 80.0), ('Mali', 50.0), ('Malta', 87.0), ('Marshall Islands', 80.0), ('Mauritania', 45.0), ('Mauritius', 80.0), ('Mexico', 80.0), ('Micronesia, Fed. Sts.', 80.0), ('Middle East & North Africa', 77.0), ('Middle East & North Africa (excluding high income)', 77.0), ('Middle income', 35.0), ('Moldova', 87.0), ('Mongolia', 30.0), ('Morocco', 87.0), ('Mozambique', 23.0), ('Myanmar', 16.0), ('Namibia', 80.0), ('Nauru', 87.0), ('Nepal', 76.0), ('Netherlands', 87.0), ('New Caledonia', 87.0), ('New Zealand', 87.0), ('Nicaragua', 80.0), ('Niger', 22.0), ('Nigeria', 9.6), ('North America', 87.0), ('Northern Mariana Islands', 87.0), ('Norway', 87.0), ('Oman', 87.0), ('Pakistan', 2.9), ('Panama', 80.0), ('Papua New Guinea', 44.0), ('Paraguay', 87.0), ('Peru', 80.0), ('Philippines', 26.0), ('Poland', 87.0), ('Portugal', 87.0), ('Puerto Rico', 87.0), ('Qatar', 87.0), ('Romania', 87.0), ('Russian Federation', 100.0), ('Rwanda', 80.0), ('Samoa', 87.0), ('San Marino', 87.0), ('Sao Tome and Principe', 57.0), ('Saudi Arabia', 87.0), ('Senegal', 56.0), ('Seychelles', 87.0), ('Sierra Leone', 27.0), ('Singapore', 87.0), ('Slovak Republic', 87.0), ('Slovenia', 87.0), ('Solomon Islands', 80.0), ('Somalia', 22.0), ('South Africa', 57.0), ('South Asia', 33.0), ('Spain', 87.0), ('Sri Lanka', 68.0), ('St. Lucia', 87.0), ('St. Vincent and the Grenadines', 87.0), ('Sub-Saharan Africa', 36.0), ('Sub-Saharan Africa (excluding high income)', 36.0), ('Sudan', 57.0), ('Suriname', 80.0), ('Sweden', 87.0), ('Switzerland', 87.0), ('Syrian Arab Republic', 80.0), ('Tajikistan', 20.0), ('Tanzania', 32.0), ('Thailand', 22.0), ('Togo', 55.0), ('Tonga', 87.0), ('Trinidad and Tobago', 87.0), ('Tunisia', 80.0), ('Turkey', 87.0), ('Turkmenistan', 80.0), ('Tuvalu', 87.0), ('Uganda', 46.0), ('Ukraine', 59.0), ('United Arab Emirates', 87.0), ('United Kingdom', 89.0), ('United States', 87.0), ('Upper middle income', 47.0), ('Uruguay', 87.0), ('Uzbekistan', 64.0), ('Vanuatu', 75.0), ('Venezuela, RB', 80.0), ('Vietnam', 57.0), ('West Bank and Gaza', 80.0), ('World', 36.0), ('Yemen, Rep.', 66.0), ('Zambia', 62.0), ('Zimbabwe', 69.0)]
# conn = [('Arab World', 1.16729366986387), ('Bangladesh', 4.765644), ('Belarus', 0.3005007), ('Bolivia', 3.550981), ('Bulgaria', 0.6940063), ('Canada', 0.3394), ('Caribbean small states', 2.04754907223294), ('Central Europe and the Baltics', 1.1564396589314), ('China', 2.747623), ('Early-demographic dividend', 1.76789386657447), ('East Asia & Pacific', 2.1567726613288), ('East Asia & Pacific (IDA & IBRD countries)', 2.22634703927978), ('East Asia & Pacific (excluding high income)', 2.21372260766053), ('Estonia', 1.02089), ('Euro area', 0.956850480713164), ('Europe & Central Asia', 0.981619295415812), ('Europe & Central Asia (IDA & IBRD countries)', 1.04863059569268), ('Europe & Central Asia (excluding high income)', 1.0141755606479), ('European Union', 0.8997432904470841), ('Fragile and conflict affected situations', 1.2309417258347), ('Georgia', 4.733633), ('Guatemala', 2.329756), ('Heavily indebted poor countries (HIPC)', 1.22060469110971), ('High income', 1.19964637092993), ('Hungary', 0.7797513), ('IBRD only', 2.0618684570466), ('IDA & IBRD total', 2.0023270732881), ('IDA blend', 1.61265026893011), ('IDA only', 1.86737947919142), ('IDA total', 1.78233607644293), ('Late-demographic dividend', 2.30806418397949), ('Latin America & Caribbean', 2.58445214876029), ('Latin America & Caribbean (excluding high income)', 2.60485437062383), ('Latin America & the Caribbean (IDA & IBRD countries)', 2.6023015635666003), ('Least developed countries: UN classification', 1.918233229998), ('Lithuania', 2.4275990000000003), ('Low & middle income', 1.99788020399026), ('Low income', 1.14051033119667), ('Lower middle income', 1.89997114162386), ('Macedonia, FYR', 0.5196086), ('Mexico', 2.44168), ('Middle East & North Africa', 1.41836702788375), ('Middle East & North Africa (IDA & IBRD countries)', 1.4646075622133798), ('Middle East & North Africa (excluding high income)', 1.45751581854319), ('Middle income', 2.08454529337942), ('Moldova', 2.721496), ('Morocco', 0.5341136), ('North America', 1.00493943548211), ('OECD members', 1.2532551874726898), ('Other small states', 0.90192123537225), ('Pacific island small states', 0.317672432684007), ('Paraguay', 2.043809), ('Peru', 2.891316), ('Philippines', 0.6134781), ('Poland', 1.461299), ('Post-demographic dividend', 1.14742490988979), ('Pre-demographic dividend', 1.8746698478362096), ('Romania', 1.199346), ('Russian Federation', 0.2896683), ('Rwanda', 1.335144), ('Sao Tome and Principe', 0.9594984), ('Small states', 1.1239678052438895), ('South Africa', 0.34475359999999994), ('South Asia', 2.0794027010423703), ('South Asia (IDA & IBRD)', 2.0794027010423703), ('Sub-Saharan Africa', 1.62739263203559), ('Sub-Saharan Africa (IDA & IBRD countries)', 1.62739263203559), ('Sub-Saharan Africa (excluding high income)', 1.6274958542205), ('Switzerland', 5.34443), ('United Kingdom', 0.2603419), ('United States', 1.077598), ('Upper middle income', 2.27063533198026), ('World', 1.85586345831398)]
# 
# gsp=GSP(kpi, conn)
# gsp.graph_signal()
# gsp.gsp_plots()
# gsp.clustering(5)
# print(gsp.ref_nodes)