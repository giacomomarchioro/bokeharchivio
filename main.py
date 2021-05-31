from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput,Button,CustomJS,TableColumn,DataTable,HTMLTemplateFormatter
from bokeh.plotting import figure
#from bokeh.sampledata.catalog_data import movie_path

# Added
import pandas as pd

catalog = pd.read_csv(join(dirname(__file__), r'Dataset_exploded.csv'))
#catalog.fillna(" ", inplace=True)
#catalog.roman_converted.replace('n.d.',0,inplace=True)
#catalog["roman_converted"] = pd.to_numeric(catalog["roman_converted"])

lista_fondi = ['Tutti','Allegri', 'Archivio Capitolare di Verona', 'Bevilacqua-vescovo',
       'Campagna-vari', 'Carlotti-Trivelli', 'Cartolari',
       'Clero Intrinseco', 'Dionisi Piomarta', 'Gazola', 'Giuliari',
       'Istituto Esposti', 'Maggio', 'Malaspina-vari', 'Mensa Vescovile',
       'Monte di Pietà', 'Nogarola', 'Notarile', 'Orfanotrofio Femminile',
       'Ospitale Civico', 'Portalupi', 'San Domenico',
       'San Fermo Maggiore (parrocchia)', 'San Giorgio in Braida',
       'San Giorgio in Braida (ASVat FV 1)', 'San Giovanni in Valle',
       'San Leonardo in Monte', 'San Lorenzo', 'San Martino d’Avesa',
       'San Michele di Campagna', 'San Nicolò',
       'San Pietro in Castello (ASVat FV I)', 'San Pietro in Monastero',
       'San Salvar Corte Regia', 'San Silvestro', 'San Tomio',
       'San Zeno Maggiore', 'Sandrà Parrocchia',
       'Sant’Anastasia Parrocchia', 'Sant’Antonio al Corso',
       'Sant’Eufemia', 'Sant’Eufemia Parrocchia',
       'Santa Caterina Martire', 'Santa Lucia',
       'Santa Maria della Ghiara', 'Santa Maria della Scala Parrocchia',
       'Santa Maria in Organo', 'Santa Teresa agli Scalzi',
       'Santi Apostoli', 'Santi Giuseppe e Fidenzio',
       'Santi Nazaro e Celso',
       'Santi Nazaro e Celso (trasferiti da Venezia)', 'Santo Spirito',
       'Santo Stefano', 'Silvestri', 'Archivio Privato Serego, Verona',
       'Università dei Cittadini', 'Verità', 'VIII vari',
       'Zileri Dal Verme']


axis_map = {
    "Anno (massimo)": "data_f",
}

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")

# Create Input controls
#reviews = Slider(title="Minimum number of reviews", value=80, start=10, end=300, step=10)
min_year = Slider(title="Inizio del periodo in esame", start=700, end=1200, value=700, step=1)
max_year = Slider(title="Fine del periodo in esame", start=700, end=1200, value=1200, step=1)
#oscars = Slider(title="Minimum number of Oscar wins", start=0, end=4, value=0, step=1)
#boxoffice = Slider(title="Dollars at Box Office (millions)", start=0, end=800, value=0, step=1)
#genre = Select(title="Genre", value="All",
#               options=open(join(dirname(__file__), 'genres.txt')).read().split())
parola_notaio = TextInput(title="Notaio o tipologia di documento:")
parola_collocantica = TextInput(title="Collocazione antica:")
colloc = TextInput(title="Collocazione moderna:")
#cast = TextInput(title="Cast names contains")
#x_axis = Select(title="Asse X", options=sorted(axis_map.keys()), value="Ampiezza (mm)")
#y_axis = Select(title="Asse Y", options=sorted(axis_map.keys()), value="Altezza (mm)")
fondo = Select(title="Fondo archivistico:", options=lista_fondi, value='Archivio Capitolare di Verona')
# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[],
                                    notaio=[], year=[], collocazione_antica=[],collocazione=[],fondo_serie=[],recto=[],is_digitized=[]))

plotsource = ColumnDataSource(data=dict(originali=[],copie=[],secolo = ['700', '800', '900', '1000', '1100']))

secolo = ['700', '800', '900', '1000', '1100']
copiaoriginale = ["originali", "copie",]
colors = ["#c9d9d3", "#718dbf"]

p = figure(x_range=secolo, plot_height=400, title="Numero atti per secolo",
           toolbar_location=None, tools="hover", tooltips="$name @secolo: @$name")

p.vbar_stack(copiaoriginale, x='secolo', width=0.9, color=colors, source=plotsource,
             legend_label=copiaoriginale)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

def select_catalog():
    #genre_val = genre.value
    parola_notaio_val = parola_notaio.value.strip()
    parola_collocantica_val = parola_collocantica.value
    fondo_val = fondo.value
    colloc_val = colloc.value
    #cast_val = cast.value.strip()
    selected = catalog[
        #(catalog.Reviews >= reviews.value) &
        #(catalog.BoxOffice >= (boxoffice.value * 1e6)) &
        #TODO: replace data_i
        ((catalog.data_i >= str(min_year.value).zfill(4)) & (catalog.data_i <= str(max_year.value).zfill(4)))
        #((catalog.data_i >= str(min_year.value).zfill(4)) & (catalog.data_f <= str(max_year.value).zfill(4))) |
        #((catalog.data_i >= str(min_year.value).zfill(4) ) & (catalog.data_f <= str(max_year.value).zfill(4))) #&
        #(catalog.Oscars >= oscars.value)
    ]
    # if (genre_val != "All"):
    #     selected = selected[selected.Genre.str.contains(genre_val)==True]
    if fondo_val != "Tutti":
        selected = selected[selected.fondo == fondo_val]
    if (parola_notaio_val != ""):
        selected = selected[selected.notaio.str.contains(parola_notaio_val)==True]
    if (parola_collocantica_val != ""):
        selected = selected[selected.collocazione_antica == parola_collocantica_val]
    if (colloc_val != ""):
        originals = (selected.collocazione.str.startswith(colloc_val) == True)
        added = (selected.collocazione.str.startswith("["+colloc_val) == True)
        selected = selected[ originals| added ]
    return selected


def update():
    df = select_catalog()
    d0700 = df[df.data_i < "0801"]
    d0800 = df[(df.data_i < "0901") & (df.data_i > "0800")]
    d0900 = df[(df.data_i < "1001") & (df.data_i > "0900")]
    d1000 = df[(df.data_i < "1101") & (df.data_i > "1000")]
    d1100 = df[(df.data_i < "1201") & (df.data_i > "1100")]
    #d1200 = df[df.data_i >"1200"]
    orig_d0700 = (d0700['copia'] == "Originale").sum()
    orig_d0800 = (d0800['copia'] == "Originale").sum()
    orig_d0900 = (d0900['copia'] == "Originale").sum()
    orig_d1000 = (d1000['copia'] == "Originale").sum()
    orig_d1100 = (d1100['copia'] == "Originale").sum()
    #orig_d1200 = (d1200['copia'] == "Originale").sum()
    cop_d0700 = d0700.shape[0] - orig_d0700
    cop_d0800 = d0800.shape[0] - orig_d0800
    cop_d0900 = d0900.shape[0] - orig_d0900
    cop_d1000 = d1000.shape[0] - orig_d1000
    cop_d1100 = d1100.shape[0] - orig_d1100
    #cop_d1200 = d1200.shape[0] - orig_d1200


    orig = [orig_d0700,
    orig_d0800,
    orig_d0900,
    orig_d1000,
    orig_d1100,
    #orig_d1200,
    ]

    cop = [cop_d0700,
    cop_d0800,
    cop_d0900,
    cop_d1000,
    cop_d1100,
    #cop_d1200,
    ]

    plotsource.data = dict(
        originali=orig,
        copie=cop,
        secolo = ['700', '800', '900', '1000', '1100']
    )
    p.title.text = "Numero atti per secolo (Totale: %d) " % len(df)
    source.data = dict(
        #x=df[x_name],
        #y=df[y_name],
        #color=df["color"],
        #color_rileg = df["color_rileg"],
        notaio=df["notaio"],
        #numero_del_codice = df["numero_del_codice"],
        year=df["data_f"],
        #marker_dim = df["marker_dim"],
        #revenue=df["revenue"],
        #alpha=df["alpha"],
        fondo_serie=df["fondo_serie"],
        collocazione=df["collocazione"],
        collocazione_antica=df["collocazione_antica"],
        recto = df["recto"],
        is_digitized=df["is_digitized"],
        #preferred_manifest_url=df["preferred_manifest_url"],
        #roman_converted = df["roman_converted"]
    )

def callback():
    source.selected.indices = []

buttondes= Button(label="Resetta selezione", button_type="success")
buttondes.on_click(callback)

# Bottone download
button = Button(label="Scarica selezione", button_type="success")
button.js_on_click(CustomJS(args=dict(source=source),
                            code=open(join(dirname(__file__), "download.js")).read()))

# controls = [reviews, boxoffice, genre, min_year, max_year, oscars, director, cast, x_axis, y_axis]
controls = [min_year, max_year,parola_notaio,parola_collocantica,colloc,fondo]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())



inputs = column(*controls,button,buttondes, width=320, height=600)
#inputs.sizing_mode = "fixed"
l = layout([
    [desc],
    [inputs, p],
],)#sizing_mode="scale_both")

# Table 
columns = [
    TableColumn(field="fondo_serie", title="Fondo e serie",width=100),
    TableColumn(field="collocazione", title="Collocazione",width=40),
    TableColumn(field="collocazione_antica", title="Collocazione antica",width=40),
    TableColumn(field="notaio", title="Notaio o tipologia",width=60),
    TableColumn(field="is_digitized", title="Digitalizzato",width=20,formatter = HTMLTemplateFormatter(template = '<a href="http://cdavr.dtesis.univr.it/<%= recto  %>" target="_blank"><%= value %></a>'))
]

data_table = DataTable(source=source, columns=columns, width=900)

# UPDATE GENERAL


curdoc().add_root(column(l,data_table))
curdoc().title = "catalog"
update()  # initial load of the data
