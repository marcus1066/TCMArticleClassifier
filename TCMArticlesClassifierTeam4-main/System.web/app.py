from flask import Flask, render_template, request, url_for,jsonify
import numpy as np
import tensorflow as tf
import pandas as pd
import os
import re
from werkzeug.utils import secure_filename
import json
import requests
from celery import Celery
import celeryconfig
import copy
import os
from dotenv import load_dotenv

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
load_dotenv(verbose=True)
model = tf.keras.models.load_model(
    os.path.join(os.getcwd(), os.getenv('model_name')))
Allow_extension = ["csv"]
URL = "https://model-apis.semanticscholar.org/specter/v1/invoke"
MAX_BATCH_SIZE = 16


def chunks(lst, chunk_size=MAX_BATCH_SIZE):
    for i in range(0, len(lst), chunk_size):
        yield lst[i: i + chunk_size]


def embed(papers):
    embeddings_by_paper_id: Dict[str, List[float]] = {}
    try:
     for chunk in chunks(papers):
        # Allow Python requests to convert the data above to JSON
        response = requests.post(URL, json=chunk)
        if response.status_code != 200:
            
            raise RuntimeError(
                "Sorry, something went wrong, please try later!")
        for paper in response.json()["preds"]:
            embeddings_by_paper_id[paper["paper_id"]] = paper["embedding"]
    except Exception as e:
        
        return e
    return embeddings_by_paper_id


def get_keyword(title_abstract):
    regex1 = re.compile(r"Ficus lacor|Hemigraphis|Gastrodia elata|Spikenard|Shuteria|Ficus lyrata|Scutellaria|Dioscorea pentaphylla|Cassia|Pteroxygonum|Eclipta|Thamnolia|Gentiana macrophylla|Arundina|Lygodium japonicum|Agastache|Rubus parvifolius|Acronychia pedunculata|Codonopsis pilosula|Salvia trijuga|Ophiopogon japonicus|Amalocalyx|Davallia mariesii|Herminium monorchis|Hedyotis verticillata|Chinese wax|Adenophora|Craspedolobium|Arnebia|Zehneria|Trichosanthes kirilowii|Pileostegia viburnoides|Hibiscus mutabilis|Ficus sarmentosa|Arisaema|Stephania japonica|Pubigera|Pseudobulb|Pinellia|Chinese herbology|Centipeda|Hibiscus taiwanensis|Agrimonia pilosa|Salvia miltiorrhiza|Pedicularis verticillata|Blood stasis|Tylophora|Achyranthes|Knoxia|Hypericum uralum|Glochidion|Clinopodium|Helwingia|Ventilago|Sophora|Baliospermum|Schisandra|Polygonum polystachyum|Tetrapanax|Lycopodium clavatum|Rehmannia|Phellodendron|Acranthera|Cirrhopetalum|Leonurus|Pogonatherum|Alisma orientale|Curcuma aromatica|Rhamnus davurica|Andrographis|Rheum officinale|Corydalis yanhusuo|Hydnocarpus|Leucas zeylanica|Pyrrosia|Metaplexis|Taxillus|Phryma|Saxifraga stolonifera|Schizonepeta|Coptis|Caragana sinica|Ophiopogon|Cornus officinalis|Cayratia|Ardisia japonica|Myrrh|Elecampane|Morinda officinalis|Cicerbita|Lithospermum|Eupatorium japonicum|Coptis chinensis|Alisma|Forsythia suspensa|Cayratia japonica|Polygonum chinense|Lobelia chinensis|Radermachera sinica|Salvia bowleyana|Salvia chinensis|Pseudostellaria|Pollia japonica|Panax pseudoginseng|Dichrocephala|Rubus lambertianus|Pentanema|Breynia|Jasminum grandiflorum|Luculia|Fritillaria cirrhosa|Liriope spicata|Toddalia|Bulbophyllum kwangtungense|Eupatorium chinense|Aspidopterys|Cyathula|Cistanche|Mazus|Wikstroemia indica|Fordia|Swertia punicea|Eleutherococcus brachypus|Atractylodes|Thunbergia fragrans|Borneol|Chinese patent medicine|Euroleon|Securidaca|Tricyrtis macropoda|Perilla|Pharmacopoeia of the People\'s Republic of China|Bupleurum|Scrophularia ningpoensis|Dactylicapnos|Prinsepia|Salvia cavaleriei|Anneslea fragrans|Angelica pubescens|American ginseng|Scutellaria baicalensis|Hydnocarpus hainanensis|Stephania|Sanguisorba officinalis|Smilax glabra|Oldenlandia|Debregeasia orientalis|Callicarpa macrophylla|Eupatorium fortunei|Polygonum aviculare|Inula|Oroxylum indicum|Fallopia multiflora|Kadsura|Calculus bovis|Cryptolepis sinensis|Allium macrostemon|Cuscuta chinensis|Codonopsis|Frankincense|Kudzu|Saruma henryi|Dichroa|Mosla|Pilea peperomioides|Fissistigma|Ainsliaea|Berchemia|Tadehagi|Phlegm|Neuroaid|Grangea|Artemisia stelleriana|Dandelion|Lindera aggregata|Veronicastrum|Bulbus fritillariae cirrhosae|Buddleja asiatica|Mahonia|Platycodon grandiflorus|Constitution type|Polygala|Corydalis|Aletris|Honeysuckle|Phyllodium pulchellum|Curculigo orchioides|Yin and yang|Lysimachia congestiflora|Chaenomeles speciosa|Euphorbia pekinensis|Polyporus umbellatus|Entada phaseoloides|Angelica dahurica|Mahonia bealei|Flemingia|Ligusticum striatum|Buddleja lindleyana|Abroma|Gentiana scabra|Magnolia delavayi|Polygala tenuifolia|Aster tataricus|Peperomia blanda|Trachycarpus|Changium|Angelica sinensis|Strangury|Scutellaria barbata|Gastrodia|Gastroptosis|Dogbane|Pterolobium|Balanophora|Boenninghausenia|Bletilla|Ardisia|Alocasia cucullata|Choerospondias|Agapetes|Loranthus|Hedyotis|Chonemorpha|Ampelopsis|Uncaria|Silene conoidea|Delphinium brunonianum|Aconitum carmichaelii|Stemona|Stephania tetrandra|Cyrtomium|Osbeckia chinensis|Brucea|Briggsia|Gardenia|Penthorum|Prunella|Callicarpa bodinieri|Uncaria rhynchophylla|Carpesium|Cissus repens|Artemisia lactiflora|Uraria|Dysosma|Cnidium|Eucommia|Rehmannia glutinosa|Apricot kernel|Campsis grandiflora|Lindera|Wendlandia|Lycopus lucidus|Parthenocissus dalzielii|Incarvillea|Rhaphidophora decursiva|Zanthoxylum nitidum|Officinal|Elephantopus scaber|Alstonia|Dichondra repens|Anemone chinensis|Chelonopsis|Trichosanthes|Canscora|Sanguisorba|Curculigo|Achyranthes bidentata|Clematis|Ammannia auriculata|Akebia|Eucommia ulmoides|Abacopteris|Hedyotis diffusa|Arctium|Privet|Excoecaria cochinchinensis|Typhonium|Meconopsis horridula|Polygonum plebeium|Notopterygium incisum|Salvia substolonifera|Alangium chinense|Astilbe chinensis|Irregular menstruation|Sigesbeckia orientalis|Rodgersia aesculifolia|Agrimonia|Magnolia officinalis|Homonoia riparia|Anisodus|Ardisia crenata|Salvia digitaloides|Blumea|Astragalus|Ludwigia repens|Thunbergia grandiflora|Verbena officinalis|Veronicastrum sibiricum|Schisandra chinensis|Flueggea|Campylotropis|Serissa|Aconitum fischeri|Amomum villosum|Calanthe tricarinata|Coix|Pinellia ternata|Salvia scapiformis|Debregeasia|Coniogramme|Carbuncle|Asarum|Glehnia|Arthraxon|Herminium|Centaurium pulchellum|Amomum|Arisaema erubescens|Fritillaria|Tribulus terrestris|Laricifomes officinalis|Dipsacus|Eupolyphaga sinensis|Berchemia lineata|Epimedium|Ligusticum|Mukdenia rossii|Pyrrosia lingua|Spatholobus|Pittosporum illicioides|Capparis acutifolia|Auricularia mesenterica|Pedicularis henryi|Cyathula prostrata|Stylophorum lasiocarpum|Scouring Rush|Triplostegia glandulifera|Swertia yunnanensis|Ligustri lucidi|Conyza blinii|Pyrola calliantha|Ainsliaea pertyoides|Asarum sagittarioides|Lagotis glauca|Debregeasia edulis|Eriosolena|Viburnum", re.S | re.I)
    regex2 = re.compile(r"chuanxiong|Ardisia crispa|Berchemia polyphylla|Viola verecunda|Inula cappa|Xiao-Chai-Hu-Tang|Diploclisia|Aconitum gymnandrum|Anemarrhena|Field mint|Gonostegia|Crymodynia|Thalictrum petaloideum|Rohdea japonica|Qingwen baidu|Dioscorea septemloba|Nuphar pumilum|Diploclisia glaucescens|Disporum cantoniense|Plastrum testudinis|Torricellia|Litsea rubescens|Neolepisorus|Begonia fimbristipula|Toad Venom|Cynanchum otophyllum|Aralia fargesii|Gynocardia|Embelia parviflora|Manglietia fordiana|Oxalis griffithii|Ardisia faberi|Aleuritopteris argentea|Wahlenbergia marginata|Tolypanthus|Cibotium barometz|Dicliptera chinensis|Herba Cistanche|Akebia trifoliata|Dioscorea subcalva|Mosla dianthera|Dendrobium jenkinsii|Tinospora sinensis|Lysionotus|Pterospermum heterophyllum|Flemingia philippinensis|Herba Scutellariae Barbatae|Pilea peltata|Chloranthus serratus|Eriolaena spectabilis|Pilea japonica|Wenxin keli|Gynura formosana|Fructus xanthii|Humata tyermanni|Osmorhiza aristata|Cissus assamica|Ophiorrhiza japonica|Lysimachia candida|Seborrhea sicca|Paederia scandens|Cervical hyperplasia|Burmannia coelestis|Utricularia bifida|Lycopodiastrum casuarinoides|Leonurus macranthus|Sedum multicaule|Machilus velutina|Shiny bugleweed|Alpinia chinensis|Liquorices|Fraxinus malacophylla|Osyris wightiana|Didissandra|Imperata Cylindrica Root|Merremia hungaiensis|Viscum multinerve|Aristolochia kaempferi|Picria felterrae|Clinopodium megalanthum|Hylomecon japonica|Pedicularis muscicola|Asystasiella|Uncaria macrophylla|Leucas ciliata|Hedyotis uncinella|Hectic fever|Pale tongue|Smilax ferox|Rodgersia sambucifolia|Snake gourd|Salix chienii|Biondia henryi|Oreas martiana|Patrinia rupestris|Cynanchum atratum|Schizomussaenda|Bai-hu-tang|Rhamnus utilis|Clinopodium chinense|Patrinia heterophylla|Erodium stephanianum|Hemiphragma|Codonopsis convolvulacea|Camellia cuspidata|Pseudodrynaria coronans|Jaundice/hepatitis|Photinia parvifolia|Pellionia repens|Acute mastitis|Elsholtzia fruticosa|Ventilago leiocarpa|Cleidion brevipetiolatum|Scorzonera austriaca|Scutellaria indica|Caesalpinia minax|Lysimachia barystachys|Pinellia cordata|Throat swelling|Red tongue|Rheum delavayi|Viola inconspicua|Adenosma indianum|Pholidota cantonensis|Hypericum japonicum|Prunella vulgaris|Psychotria serpens|Suppurative tonsillitis|Streptocaulon|Aralia chinensis|Adina pilulifera|Gomphostemma chinense|Liver palms|Eclipta alba|Heteropanax fragrans|Begonia palmata|Flueggea virosa|Boehmeria macrophylla|Hypericum wightianum|Heishunpian|Artemisia apiacea|Pachymenia carnosa|Semiaquilegia adoxoides|Cynanchum thesioides|Iodes vitiginea|Desmodium triquetrum|Sheng-Mai San|Common Jujube|Bi syndrome|Pilea peploides|Jasminum", re.S | re.I)
    regex3 = re.compile(r"elongatum|Mentha haplocalyx|Anisodus acutangulus|Symplocos sumuntia|Ligularia tsangchanensis|Ormosia henryi|Urtica laetevirens|Incarvillea arguta|Glechoma longituba|Urena procumbens|Angiopteris fokiensis|Pyrethrum tatsienense|Dioscorea panthaica|Erxian decoction|Mirabilitum|Herminium lanceum|Corydalis turtschaninovii|Yiqi yangyin|Vernonia cumingiana|Radix Aconiti|Jujube Seed|Cyathula officinalis|Disporopsis fuscopicta|Rubia yunnanensis|Crotalaria sessiliflora|Alpinia pumila|Ampelopsis humulifolia|Danggui sini|Gentiana urnula|Cryptotaenia japonica|Selaginella doederleinii|Parnassia wightiana|Berberis julianae|Rheum forrestii|Euonymus macropterus|Peristrophe japonica|Turpinia formosana|Humata repens|Wrightia pubescens|Vaccinium fragile|Tylophora floribunda|Pararuellia|Persicaria perfoliata|Soroseris gillii|Viola arcuata|Polygala arvensis|Cinnamomum obtusifolium|Crotalaria albida|Aralia echinocaulis|Parameria laevigata|Jasminum floridum|Xylocopa dissimilis|Antenoron filiforme|Gnetum parvifolium|Sallow complexion|Stachys kouyangensis|Melica scabrosa|Schizocapsa plantaginea|Dodartia orientalis|Artemisia carvifolia|Pellionia scabra|Longdan xiegan decoction|Bayberry Bark|Angelica morii|Manglietia szechuanica|Lobelia sessilifolia|Ardisia brevicaulis|Yin-chen-hao-tang|Asiatic pennywort|Neopallasia pectinata|Canarium bengalense|Caragana franchetiana|Pogostemon auricularius|Iris confusa|Phlegmariurus hamiltonii|Schisandra propinqua|Rungia chinensis|Veronica linariifolia|Ixora chinensis|Smilax microphylla|Radix Rehmanniae Preparata|Devilpepper|Rhododendron seniavinii|Euphorbia humifusa|Potentilla freyniana|Rabdosia rubescens|Polygala glomerata|Auditory vertigo|Viola diamantiaca|Ficus esquiroliana|Codonacanthus pauciflorus|Sericocalyx|Centranthera cochinchinensis|Aristolochia fordiana|Geranium strictipes|Schizocapsa|Melastoma dodecandrum|Cardamine macrophylla|Taxillus chinensis|Chirita fimbrisepala|Qishenyiqi|Eriophyton wallichii|Pararuellia delavayana|Sapium baccatum|Hemsleya sphaerocarpa|Cudrania cochinchinensis|Tarenna attenuata|Fissistigma polyanthum|Streptopus simplex|Pilea plataniflora|Conyza japonica|Arcangelisia|Hedyotis hedyotidea|Carpesium abrotanoides|Lepisorus ussuriensis|Ampelopsis sinica|You-gui-wan|Blumea lanceolaria|Stomach swelling|Armeniaca mume|Aconitum kusnezoffii|TCM Preparation|Safflowers|Primrose-willow|Chronic tracheitis|Urticaria papulosa|Pterocephalus hookeri|Calceolaria crenatiflora|Saposhnikovia|Dipsacus asper|Cicada Slough|Piper cubeba|Campanula colorata|Scutellaria scordifolia|Jasminum lanceolarium|Abdominal pain type|Remove blood|Hemiboea subcapitata|Crinis Carbonisatus|Typhonium giganteum|Si-jun-zi-tang|Multiple peripheral neuritis|Acute contagious conjunctivitis|Cremastra appendiculata|Spiranthes australis|Hedyotis tenelliflora|Sagina japonica|Diplospora dubia|Ajuga ciliata|Hypogalactia|Polygonatum kingianum|Ecdysanthera rosea|Scabiosa tschiliensis|Pouzolzia zeylanica|Ardisia mamillata|Oreocnide frutescens|Mussaenda philippica|Coridius chinensis|Xiao-qing-long-tang|Cynanchum amplexicaule|Hypericum patulum|Elaeagnus oldhamii|Smilax perfoliata|Michelia hedyosperma|Pleione bulbocodioides|Heracleum rapula|Stahlianthus involucratus|Sarcopyramis|Ren-shen-yang-rong-tang|Chinese trumpet-creeper|Coniogramme intermedia|Cimicifuga foetida|Aletris spicata|Polygonum posumbu|Merremia hederacea|Silene aprica|Botrychium ternatum|Venenum bufonis|Lychnis coronata|Rhododendron mariae|Chronic tympanitis|Neurodynia|Turbid urine|Hibiscus schizopetalus|Alyxia sinensis|Souliea vaginata|Cape Jasmine Fruit|Neoalsomitra|Dichrocephala auriculata|Vegetable sponge|Bidens biternata|Eriocaulon buergerianum|Drymaria diandra|Longdanxiegan|Myricaria bracteata|Ligusticum sinense|Berberis soulieana|Callicarpa longifolia|Hygrophila salicifolia|MaZiRenWan|Teucrium japonicum|Dysosma versipellis|Bauhinia championii|Petrocosmea duclouxii|Late gastric cancer|Asplenium prolongatum|Picrorhiza|Goodyera schlechtendaliana|Thesium chinense|Tetrastigma planicaule|Blumea megacephala|Libanotis buchtormensis|HIBISCUS SYRIACUS BARK|Tetrastigma obtectum|Si-wu decoction|Sambucus chinensis|Eriobotrya seguinii|Gynura japonica|Mongolian snake-gourd|Zuo-Jin-Wan|Dioscorea spongiosa|Morinda parvifolia|Murdannia simplex|Cyclea racemosa|Mulberry Root Bark|Ligusticum pteridophyllum|Botrychium lanuginosum|Aristolochia kwangsiensis|Glossogyne tenuifolia|Siphonostegia|Lagotis brevituba|Ardisia quinquegona|Scrophularia henryi|Sopubia trifida|TCM Formula|Sparganium stoloniferum|Pilea cavaleriei|Schnabelia oligophylla|Pellionia radicans|Chinese Gall|Rheum pumilum|Cynoglossum amabile|Acute eczema|Oxalis corymbosa|Hypericum monogynum|Lespedeza tomentosa|Licorice roots|Tiarella polyphylla|Rosa banksiae|Fructus aurantii immaturus|Senega Root|Hypericum sampsonii|Motherwort|Solanum lyratum|POLYGONUM CUSPIDATUM|Rubus reflexus|Asarum forbesii|Chinese herbs|Loquat Leaf|Aristolochia moupinensis|Gentiana davidii|Chinese knotweed|Aconitum brachypodum|Salvia miltiorrhizae|Pilea notata|Hydrocotyle nepalensis|Pronephrium|Schisandra bicolor|Cynomorium songaricum|Callicarpa rubella|Eria pannea|Cyrtomium fortunei|Floscopa scandens|Saposhnikovia divaricata|Pottsia laxiflora|Acorus tatarinowii|Tephroseris kirilowii|Cinquefoil|Pothos chinensis|Night sweat|Sophora Root|Halenia elliptica|Rodgersia pinnata|Gestational edema|Hypericum attenuatum|ANGELICA ROOT|Radix Ophiopogonis|Chronic simple rhinitis|Malvastrum coromandelianum|Bulbophyllum inconspicuum|Rosa taiwanensis|Radix Astragali seu Hedysari|Vandenboschia|Morinda angustifolia|Pericampylus|Celastrus rosthornianus|Dryopteris bissetiana|Stellaria saxatilis|Pinanga tashiroi|Aristolochia debilis|Adina rubella|Holboellia coriacea|Chronic pelvic inflammatory disease|Artemisia japonica|Daphniphyllum oldhami|Spermatorrhea|Canthium simile|Aster turbinatus|Onychium japonicum|Bulbophyllum levinei|Lung closure|Thladiantha nudiflora|Senna Fruit|Liu-wei-di-huang wan|Japanese ginseng|Smoked Plum|Bergia ammannioides|Rhizoma Coptidis|Liu Wei Di Huang|Ajuga nipponensis|Bridelia fordii|Trichosanthes cucumeroides|Triplostegia|Lychnis fulgens|Astragalus Root|Ephedra herb|Inula japonica|Eurya distichophylla|Potentilla chinensis|Lindernia ciliata|Hedyotis caudatifolia|Dichocarpum|Stellaria uliginosa|Primula efarinosa|Notholirion bulbuliferum|Intestinal abscess|Lysimachia fortunei|Fuzi-lizhong|Ustilago crameri|Diospyros cathayensis|Artemisia anomala|Clematis argentilucida|Diuranthera|Sargentodoxa cuneata|Elatostema stewardii|Abelmoschus sagittifolius|Patrinia scabiosaefolia|Boehmeria", re.S | re.I)
    regex4 = re.compile(r"siamensis|Sarcococca ruscifolia|White dead-nettle|Corydalis decumbens|Craibiodendron|Sporobolus fertilis|Crotalaria ferruginea|Dickinsia hydrocotyloides|Helleborus thibetanus|Cissus hastata|Sword brake|Tetracera asiatica|Syzygium buxifolium|Ambroma augusta|Semiaquilegia|Aconite Root|Ludwigia octovalvis|Atractylis ovata|Bambusa sinospinosa|Schizonepeta Spike|Stegnogramma|Salomonia cantoniensis|Asarum caulescens|Angelica citriodora|Millettia reticulata|Palembus dermestoides|Euonymus nanus|Leuconychia|Dactylicapnos scandens|Zhebeinine|Eurya chinensis|Tianma gouteng yin|Smilacina japonica|Dysosma difformis|Dioscorea glabra|Ainsliaea spicata|Dryopteris atrata|Aralia", re.S | re.I)
    regex5 = re.compile(r"decaisneana|Sichuan lovage|Lysimachia christinae|Melothria heterophylla|Kadsura oblongifolia|Lagedium sibiricum|Elsholtzia blanda|Cymbopogon distans|Kinostemon|Lysidice rhodostegia|Sabia japonica|Tinomiscium|Ledebouriella seseloides|Tylorrhynchus|Typhonium divaricatum|Piper wallichii|Rhododendron microphyton|Wen-dan decoction|Pratia nummularia|Serissa serissoides|Russula rubra|Sambucus adnata|Atropanthe|PELVIC INFLAMMATION|Breynia fruticosa|Limb coldness|Thin sputum|Holostemma annulare|Pogonatherum crinitum|WHITE MUSTARD SEED|Cocculus orbiculatus|Di huang yin zi|Ling-gui-zhu-gan decoction|Veronicastrum axillare|Furred tongue|Lindera megaphylla|Tetradium ruticarpum|Micromeria biflora|Microsorium|Gerbera delavayi|Claoxylon polot|Ajuga taiwanensis|Chinese Medicinal Formulation|Post-traumatic brain syndrome|Sweating disease|TCM Formulation|Drymotaenium miyoshianum|Siphonostegia chinensis|Arisaema ringens|White tongue|Oberonia iridifolia|Radix Trichosanthis|Syneilesis aconitifolia|Viola japonica|Aleuritopteris farinosa|Leucas chinensis|Garden Sorrel|Helminthostachys|Milkvetch Root|Ziziphus apetala|Caryota ochlandra|Ficus variolosa|LIGUSTICUM WALLICHII ROOT|Dictamnus dasycarpus|Equisetum hiemale|Berchemia sinica|Stephania longa|Cinnamomum wilsonii|Paraquilegia|Psychroalgia|Lepidogrammitis|Teucrium viscidum|Aerva sanguinolenta|Aster ageratoides|Ainsliaea henryi|Ajuga lupulina|Uraria lagopodioides|Lytta caraganae|Aechmanthera|Polygala japonica|Angelica apaensis|Attacking heart|Mucuna macrocarpa|Polycarpaea corymbosa|Urocystitis|Urinary calculus removal|Nanocnide lobata|Tripterospermum|Anaphalis sinica|Radix isatidis|Houttuynia|Osteoproliferation|Dysosma pleiantha|Glochidion eriocarpum|Passiflora wilsonii|Fructus bruceae|Celastrus aculeatus|Artemisia eriopoda|Astragalus mongholicus|Hedyotis capitellata|Viola acuminata|Schisandra rubriflora|Polygala arillata|Celastrus gemmatus|Cassiope selaginoides|Cortex Fraxini|Swertia bimaculata|Schisandra glaucescens|Plumbagella micrantha|Clerodendrum japonicum|GALANGAL ROOT|Trema cannabina|Hp - Helicobacter pylori|Lysimachia klattiana|Callicarpa kwangtungensis|Alopecia seborrhoeica|Swertia mileensis|White Mulberry|Abdomen fullness|Campylotropis macrocarpa|Isodon amethystoides|Postpartum alopecia|Canarium pimela|Chaihu-shugan-san|Potentilla kleiniana|Rubus buergeri|Tangerine Peel|Stachys geobombycis|Paliurus ramosissimus|Veronica undulata|Rubus hirsutus|Pleurospermum hookeri|Saussurea nigrescens|Uncaria sessilifructus|Cucubalus baccifer|Ficus pandurata|Bushen tiaochong|RUMEX JAPONICUS ROOT|Chinese squill|Polygonum divaricatum|Phtheirospermum tenuisectum|Sedum sarmentosum|Ficus formosana|Cirsium lineare|Infantile hernia|Damnacanthus|Aspongopus|Hippocampus japonicus|Colla corii asini|Clematis chinensis|Astragalus complanatus|Anemone vitifolia|Xue-Fu-Zhu-Yu decoction|Ardisia maculosa|Aeschynanthus acuminatus|Lysimachia circaeoides|Thermopsis barbata|Pneumonia treating|Phyllanthus virgatus|Viburnum fordiae|Pinellia tuberifera|Atractylodes macrocephala|Gymnocladus chinensis|Pulsatillae|Gerbera piloselloides|Tangerine Seed|Dendrobium densiflorum|Crepis crocea|Micromelum integerrimum|Securinega suffruticosa|Myosoton aquaticum|Celtis biondii|Martianus dermestoides|Haizao yuhu decoction|Yu ping feng san|Ma-xing-shi-gan-tang|Prismatomeris tetrandra|Berberis sargentiana|Rhodobryum roseum|Potentilla multifida|Clerodendrum fortunatum|PLANTAGO SEED|Peucedanum morisonii|Hypserpa nitida|Epipactis mairei|Clematis intricata|Traditional Chinese Medicine Formulation|Rhizoma Pinelliae|Qingrejiedu|Solidago decurrens|Actinodaphne cupularis|Ficus fulva|Pinellia integrifolia|Euphorbia lunulata|Chinese eupatorium|Bolbostemma|Selaginella tamariscina|Euchresta japonica|Cratoneuron filicinum|Adenophora trachelioides|Lepidogrammitis drymoglossoides|Bletilla striata|Piper hainanense|Triosteum himalayanum|Hypodematium", re.S | re.I)
    regex6 = re.compile(r"crenatum|Pachysandra axillaris|Callicarpa longissima|Elatostema involucratum|Psammosilene|Aspongopus chinensis|Muscae volitantes|Buthus martensi|Lindernia ruellioides|Aristolochia mollissima|Euonymus oxyphyllus|Rhodiola dumulosa|Anemone tomentosa|Oxygraphis|Berneuxia", re.S | re.I)
    regex7 = re.compile(r"thibetica|Polygala fallax|Arthrodynia|Crotalaria assamica|Barbed Skullcap Herb|Pharyngolaryngitis|Castanopsis delavayi|Caesalpinia cucullata|Tetraplodon mnioides|Tylophora ovata|Ranunculus chinensis|Nervous tinnitus|Asparagus cochinchinensis|Pimpinella thellungiana|Bu-yang-huan-wu-tang|Chronic pharyngitis|Morinda umbellata|Uraria crinita|Litsea rotundifolia|Heterosmilax japonica|Cistanche salsa|Turpinia arguta|Polemonium coeruleum|Campylandra chinensis|Schisandra henryi|Cervicodynia|Erycibe obtusifolia|Anisodus luridus|Davallia formosana|Symplocos lancifolia|Berchemia floribunda|Stephania excentrica|Stemona japonica|Pothos repens|Polygonum paleaceum|Bu-zhong-yi-qi-tang|Cordyceps liangshanensis|Angelica polymorpha|Dracontomelon duperreanum|Lepisorus thunbergianus|Lysimachia insignis|Asystasiella neesiana|Dioscorea hemsleyi|Ajuga decumbens|Acute laryngopharyngitis|Parthenocissus himalayana|Cicada Molting|Sinochasea trigyna|Phtheirospermum|Angong Niuhuang Pill|Dolichoris|Rhodobryum giganteum|Cardamine tangutorum|Desmodium styracifolium|Glechoma biondiana|Circaea mollis|Fritillaria thunbergii|Trevesia palmata|Hemiphragma heterophyllum|Ardisia villosa|Evodia lepta|Campanumoea|Millettia dielsiana|Liver stomach|Radix Achyranthis Bidentatae|Hemsleya amabilis|Korthalsella japonica|Zingiber kawagoii|Senecio scandens|Dracocephalum heterophyllum|Piper hancei|Achyranthes Root|Cyathocline purpurea|Polygonum runcinatum|Rubus alceaefolius|Gonostegia hirta|Hindu datura|Wikstroemia canescens|Arabis pendula|Geranium wilfordii|Ganoderma tenue|Radix Rehmanniae Glutinosae|Rungia pectinata|Carex scaposa|Decaspermum gracilentum|Filifolium sibiricum|Asarum insigne|Mosla scabra|Lepidagathis incurva|Hypecoum erectum|Oldenlandia diffusa|Abelia biflora|Clerodendranthus|Pedicularis resupinata|Randia cochinchinensis|Monochasma|Synergistic drug effects|Nervilia fordii|Rubus multibracteatus|Orobanche coerulescens|Commelina paludosa|Gualou xiebai baijiu|Celastrus flagellaris|Kyllinga monocephala|Artocarpus styracifolius|Plumbagella|Adiantum flabellulatum|Saposhnikovia divaricata Root|Bastard indigo|Isodon longitubus|Sanguisorba officinalis", re.S | re.I)
    regex8 = re.compile(r"Root|Lobaria retigera|Corydalis adunca|Gnetum montanum|Gentianopsis barbata|Weigela japonica|Corallodiscus|Fructus Akebiae|Ficus erecta|Thready pulse|Veronica eriogyne|Iphigenia indica|Ardisia lindleyana|Siberian Cocklebur|Ficus stenophylla|Shexiang tongxin|Helwingia", re.S | re.I)
    regex9 = re.compile(r"japonica|Primula malacoides|Polystichum braunii|Crotalaria calycina|Viola yedoensis|Rhodobryum|Melodinus suaveolens|Chrysanthemum Flower|Wikstroemia dolichantha|Ardisia gigantifolia|Sargent gloryvine|Lower abdomen pain|Platanthera japonica|Toricellia angulata|Cheilosoria chusana|Asthma Preparation|Gentiana rhodantha|Broussonetia kaempferi|Receptaculum Nelumbinis|Dioscorea collettii|Maxingshigan|Seselopsis|Marsdenia tenacissima|Rabdosia amethystoides|Zaocys dhumnades|Pittosporum glabratum|Adenophora tetraphylla|Lycianthes biflora|Delphinium delavayi|Acute lymphangitis|Polygonum suffultum|Burnet Root|Piper puberulum|Ficus wightiana|Yiqi Huoxue|Massa medicata fermentata|Scorzonera divaricata|Berberis poiretii|Lagochilus lanatonodus|Rock jasmine|Diospyros rhombifolia|Adenocaulon himalaicum|ASARUM", re.S | re.I)
    regex10 = re.compile(r"SIEBOLDII|Corydalis pallida|Fennel Root|Rhynchospermum verticillatum|Desmodium microphyllum|Stephania sinica|Swertia bifolia|Cantharides|Kalanchoe laciniata|Asclepias physocarpa|Lemmaphyllum microphyllum|Lepisorus macrosphaerus|Leukorrhagia|Akebia Stem|Sanicula lamelligera|Clematis henryi|Jasminum nervosum|Alpinia japonica|Celastrus hypoleucus|Thyrocarpus sampsonii|Aristolochia fangchi|Smilax riparia|Impatiens chinensis|Hippophae fructus|Monochasma sheareri|Bothriospermum chinense|Cleisostoma scolopendrifolium|Calamus tetradactylus|Carpesium divaricatum|Ampelopsis japonica|Elatostema umbellatum|Mucuna sempervirens|Weichangshu|Nauclea officinalis|Balanophora harlandii|Renanthera coccinea|Elsholtzia bodinieri|Piper boehmeriaefolium|Costus Root|Lespedeza pilosa|Si-wu-tang|Polygonum orientale|Clematis hexapetala|Euphorbia kansui|Laportea bulbifera|Phaenosperma globosa|Euonymus laxiflorus|Ixeris polycephala|Woodwardia japonica|Embelia laeta|Leonurus pseudomacranthus|Cynanchum paniculatum|Plantago depressa|Zhigancao decoction|Yinqiaosan|Western medicine|Radix bupleuri|Body resistance|Pericarpium citri reticulatae|Chinese traditional medicine|Network pharmacology|Huang lian jie du tang|Flos chrysanthemi|Damp heat|Serum pharmacochemistry|Syndrome differentiation|Yang deficiency|Huang lian jie du decoction|Infantile anorexia|Herb pair|Yin deficiency|Fructus psoraleae", re.S | re.I)
    REGEXMATCH_LIST = []
    REGEXMATCH_LIST.append(regex1)
    REGEXMATCH_LIST.append(regex2)
    REGEXMATCH_LIST.append(regex3)
    REGEXMATCH_LIST.append(regex4)
    REGEXMATCH_LIST.append(regex5)
    REGEXMATCH_LIST.append(regex6)
    REGEXMATCH_LIST.append(regex7)
    REGEXMATCH_LIST.append(regex8)
    REGEXMATCH_LIST.append(regex9)
    REGEXMATCH_LIST.append(regex10)
    keyword_list = []
    for i in range(len(REGEXMATCH_LIST)):
        article_keyword = re.findall(
            REGEXMATCH_LIST[i], title_abstract[0])+re.findall(REGEXMATCH_LIST[i], title_abstract[1])
        keyword_list += article_keyword
    if len(keyword_list) != 0:
        return ','.join(list(set(keyword_list)))
    else:
        return None

frontEndDir=os.path.join("my-app","build","static")

app = Flask(__name__,static_url_path="",static_folder=frontEndDir,template_folder="./my-app/build/templates")
celery = Celery()
celery.config_from_object('celeryconfig')



def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in Allow_extension


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/predict', methods=["post"])
def predict():
    if request.data == None:
        return "sry you havent submit a file"
    upload_files = request.files.getlist('file[]')

    filenames = []
    for file in upload_files:
        filename = secure_filename(file.filename)
        filenames.append(filename)
        file.save(os.path.join(os.getcwd(), filename))
    file=open(os.path.join(os.getcwd(),'/cancel_task' ),'w')
    file.write('for_stop_celery')
    file.close()    
    task = process_model.delay(filenames)
    task_id=task.id
    
    return {'Location': url_for('getfinish', task_id=task_id)}


@celery.task(bind=True, name='app.process_model')
def process_model(self, filenames):

    TCM_articles = []
    count_paperwithkeyword = 0
    count_TCM = 0
    count = 0
    prob = 0
    dataset_json = []
    for filename in filenames:
      try:  
        data = pd.read_csv(os.path.join(os.getcwd(), filename), dtype=str)
        data = data.drop_duplicates(subset=['PaperId'], keep='first')
        for i, row in data.iterrows():
         if os.path.exists(os.path.join(os.getcwd(),'/cancel_task' )):
            count += 1
            title = row['Title']
            abstract = row['Abstract']
            paperId = row['PaperId']
        # ensure that everything is right type
            if type(abstract) == type(title) == type(paperId) == str:
                        dataset_json.append({'title': title,
                                            'abstract': abstract,
                                            'paper_id': paperId})
            

            if count == 50 or i == len(data)-1:
                
                count = 0

                all_embeddings = embed(dataset_json)
                
                
                if type(all_embeddings)==requests.exceptions.ConnectionError:
                    
                    raise ConnectionError("please ensure you get your network connected")
                
                dataset_json = []
                fifity_data = copy.deepcopy(data)
                fifity_data = fifity_data[fifity_data['PaperId'].isin(
                    all_embeddings)]

                embed_vectors = np.array(
                    [all_embeddings[PaperId] for PaperId in fifity_data['PaperId'].values.tolist()])

                predict_result = [
                    0 if x < 0.5 else 1 for x in model.predict(embed_vectors)]

                for x in range(len(predict_result)):
                    if predict_result[x] == 1:
                        count_TCM += 1
                        keyword_to_paper = get_keyword(
                            (fifity_data.iloc[x]["Title"], fifity_data.iloc[x]["Abstract"]))
                        if keyword_to_paper != None:
                            count_paperwithkeyword += 1
                        TCM_articles.append(
                            {"Title": fifity_data.iloc[x]["Title"], "keyword": keyword_to_paper})
                        prob = count_paperwithkeyword/count_TCM
                        self.update_state(state='progress', meta={
                                          'current': TCM_articles, 'prob': prob, 'status': 'progressing'})
         else:
             return {"current": TCM_articles, "prob": prob, 'status': 'stop'}
      except Exception as e:
          if type(e)==KeyError:
              r={
                  'status':'error',
                "message":"lack of required col in csv"
              }
          else:
                r={
                'status':'error',
                "message":e.args
                }
          

          return r

    return {"current": TCM_articles, "prob": prob, 'status': 'complete'}


@app.route('/getfinish/<task_id>')
def getfinish(task_id):
    task = process_model.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {
            'finished': [],
            'prob': 0,
            'status': 'preparing data '
        }
    elif task.state == 'progress':
        response = {

            'finished': task.info.get('current'),
            'prob': task.info.get('prob'),
            'status': 'progressing'
        }
        
    elif task.info.get('status') == 'error':
        response = {
            'status':'error',
            'message':task.info.get("message")

        }

    elif task.info.get('status')=='stop':
        response={
            'finished': task.info.get('current'),
            'prob': task.info.get('prob'),
            'status': 'stop',
        }


    else:

        response = {
            'finished': task.info.get('current'),
            'prob': task.info.get('prob'),
            'status': 'done',
        }

    return response


@app.route('/cancel_task')
def cancel_task():
    os.remove(os.path.join(os.getcwd(),'/cancel_task' ))
    return "has stop the task"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
