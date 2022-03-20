import csv
import unittest
import parser
import analyzer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SITEMAP_PATH = f'{BASE_DIR}/sitemap_for_tests.xml'


class AnalyzerTest(unittest.TestCase):
    def test_get_sitemap_links(self):
        answer = {
            'http://aviapages.com/buzz/thread/flight-request-10-feb-lrop-eggw-4pax-10-feb-eggw-lrop-4pax-24648/',
            'http://aviapages.com/buzz/thread/2009-quest-kodiak-100-sn-100-0009-rn-n525ah-with-ttaf1012-for-6-passengers-is-for-sale-by-cfs-jets-24628/',
            'http://aviapages.com/buzz/thread/flight-request-31-jan-lfcr-eddb-2pax-24605/',
            'http://aviapages.com/buzz/thread/2005-hawker-800xpi-sn-258729-rn-n709ks-with-ttaf6140-for-7-passengers-is-for-sale-by-swartz-aviation-group-llc-24662/',
            'http://aviapages.com/buzz/thread/guardian-flight-a-global-medical-response-company-has-acquired-sunrise-air-ambulance-and-its-four-air-medical-transport-bases-in-arizona-12349/',
            'http://aviapages.com/buzz/thread/1998-beechcraft-bonanza-b36tc-sn-ea-624-rn-n62tc-with-ttaf2008-for-5-passengers-is-for-sale-by-ogarajets-24680/',
            'http://aviapages.com/buzz/thread/empire-aviation-group-eag-affiliate-empire-aircraft-management-services-private-limited-eamspl-has-been-awarded-a-non-scheduled-operators-permit-nsop-by-the-civil-aviation-department-in-india-4764/',
            'http://aviapages.com/buzz/thread/aviapages-ceo-in-aviapreneurs-podcast-1st-aviation-hosttalkshow-february-10-2022-24655/',
            'http://aviapages.com/buzz/thread/2008-airbus-helicopter-ec135-p2-sn-0682-with-ttaf3425-is-for-sale-by-asian-sky-group-24676/',
            'http://aviapages.com/buzz/thread/flight-request-13-feb-limf-lfkx-3pax-24641/',
            'http://aviapages.com/buzz/thread/flight-request-28-jan-eddb-lfcr-2pax-31-jan-lfcr-eddb-2pax-24604/',
            'http://aviapages.com/buzz/thread/1996-cessna-citation-citationjet-sn-525-0161-rn-n525bt-with-ttaf5411-for-5-passengers-is-for-sale-by-gantt-aviation-inc-24622/',
            'http://aviapages.com/buzz/thread/2016-honda-hondajet-apmg-sn-42000028-rn-n420rp-with-ttaf932-is-for-sale-by-cutter-aviation-24681/',
            'http://aviapages.com/buzz/thread/flight-request-27-feb-lowi-uuww-7pax-24671/',
            'http://aviapages.com/buzz/thread/always-dress-in-layers-for-your-safari-it-can-be-very-cold-for-morning-drives-and-very-hot-in-the-afternoon-11267/',
            'http://aviapages.com/buzz/thread/flight-request-31-jan-lfcr-eddb-2pax-24609/',
            'http://aviapages.com/buzz/thread/2020-pilatus-pc-12-ngx-sn-2057-rn-n521rt-with-ttaf358-is-for-sale-by-jeteffect-inc-24632/',
            'http://aviapages.com/buzz/thread/flight-request-26-jan-eggp-ehrd-4pax-31-jan-ehrd-eggp-4pax-24596/',
            'http://aviapages.com/buzz/thread/2010-gulfstream-g450-sn-4172-rn-t7-bln-with-ttaf3902-for-14-passengers-is-for-sale-by-gulfstream-aerospace-corporation-24678/',
            'http://aviapages.com/buzz/thread/flight-request-24-feb-lebl-levc-5pax-24640/',
            'http://aviapages.com/buzz/thread/revolutionary-tech-on-the-g500-and-g600-is-now-in-service-worldwide-12857/',
            'http://aviapages.com/buzz/thread/flight-request-16-feb-glrb-ebbr-16pax-19-feb-ebbr-gooy-16pax-20-feb-gooy-glrb-16pax-24651/',
            'http://aviapages.com/buzz/thread/flight-request-03-feb-glrb-dgaa-14pax-05-feb-dgaa-glrb-14pax-24623/',
            'http://aviapages.com/buzz/thread/flight-request-05-feb-lppr-smjp-4pax-07-feb-smjp-lppr-4pax-24613/',
            'http://aviapages.com/buzz/thread/flight-request-21-feb-liml-fsia-4pax-24635/',
            'http://aviapages.com/buzz/thread/flight-request-26-jan-eggp-ehrd-4pax-31-jan-ehrd-eggp-4pax-24581/',
            'http://aviapages.com/buzz/thread/1982-boeing-bbj-737-200-advanced-sn-22675-rn-n80ev-with-ttaf69342-for-19-passengers-is-for-sale-by-northern-jet-management-inc-24631/',
            'http://aviapages.com/buzz/thread/2017-gulfstream-g550-sn-5559-rn-n1777u-with-ttaf693-for-16-passengers-is-for-sale-by-acass-24569/',
            'http://aviapages.com/buzz/thread/flight-request-05-feb-dnmm-fkys-12pax-08-feb-fkys-dnmm-12pax-24614/',
            'http://aviapages.com/buzz/thread/flight-request-02-feb-ulli-uuww-1pax-03-feb-uuww-ulli-1pax-24620/',
            'http://aviapages.com/buzz/thread/crypto-payment-charter-request-in-leon-no-more-premium-and-more-24674/',
            'http://aviapages.com/buzz/thread/flight-request-20-feb-umms-lybe-1pax-20-feb-lybe-lira-1pax-24673/',
            'http://aviapages.com/buzz/thread/2008-cessna-citation-encore-sn-560-0782-rn-n247ej-with-ttaf6902-for-8-passengers-is-for-sale-by-qs-partners-24663/',
            'http://aviapages.com/buzz/thread/2002-bombardier-learjet-45-sn-214-rn-n555ck-with-ttaf3607-for-8-passengers-is-for-sale-by-duncan-aviation-inc-24682/',
            'http://aviapages.com/buzz/thread/1975-cessna-p337-skyrocket-rn-n262-with-ttaf4235-for-4-passengers-is-for-sale-by-gardner-aircraft-sales-19037/',
            'http://aviapages.com/buzz/thread/flight-request-13-feb-kcwa-mrlb-8pax-24660/',
            'http://aviapages.com/buzz/thread/flight-request-21-feb-lrtr-edli-4pax-24659/',
            'http://aviapages.com/buzz/thread/2019-gulfstream-g650er-sn-6390-with-ttaf133-for-13-passengers-is-for-sale-by-gulfstream-aerospace-corporation-24666/',
            'http://aviapages.com/buzz/thread/2020-honda-hondajet-elite-sn-42000-190-rn-n1mr-with-ttaf260-for-5-passengers-is-for-sale-by-leviate-air-group-24637/',
            'http://aviapages.com/buzz/thread/volga-dnepr-group-will-be-welcoming-the-guests-of-air-cargo-europe-exhibition-and-conference-in-munich-germany-at-its-joint-booth-with-airbridgecargo-airlines-and-strategic-partner-cargologicair-11232/',
            'http://aviapages.com/buzz/thread/flight-request-28-jan-eddb-lfcr-2pax-31-jan-lfcr-eddb-2pax-24599/',
            'http://aviapages.com/buzz/thread/flight-request-14-feb-gvnp-glrb-10pax-14-feb-glrb-gvnp-10pax-24643/',
            'http://aviapages.com/buzz/thread/stefano-albinati-was-in-sion-airport-lsgs-switzerland-end-of-february-to-admire-the-new-bombardier-global-7500-showcased-to-potential-clients-10093/',
            'http://aviapages.com/buzz/thread/2015-gulfstream-g650er-sn-6117-rn-n650er-with-ttaf1942-for-13-passengers-is-for-sale-by-avpro-inc-24646/',
            'http://aviapages.com/buzz/thread/1999-beechjet-400a-sn-rk-220-rn-n563rj-with-ttaf4563-is-for-sale-by-cfs-jets-24667/',
            'http://aviapages.com/buzz/thread/2018-cirrus-sr20-g6-sn-2461-rn-n190ct-with-ttaf920-is-for-sale-by-eagle-aviation-inc-24602/',
            'http://aviapages.com/buzz/thread/charter-directories-one-more-app-in-aviapages-ecosystem-24652/',
            'http://aviapages.com/buzz/thread/2013-cubcrafters-cc11-160-carbon-cub-for-2-passengers-is-for-sale-by-swt-aviation-inc-19532/',
            'http://aviapages.com/buzz/thread/flight-request-14-feb-ltfm-lfpb-4pax-24658/',
            'http://aviapages.com/buzz/thread/mike-pierce-a-34-year-veteran-of-cessna-aviation-was-a-part-of-the-citation-x-design-team-whos-sole-focus-was-to-engineer-the-fastest-cross-country-business-jet-in-the-world-3588/',
            'http://aviapages.com/buzz/thread/flight-request-18-feb-ltba-ltfe-3pax-24664/',
            'http://aviapages.com/buzz/thread/2016-piper-m350-sn-4636679-rn-n359vm-with-ttaf880-is-for-sale-by-cutter-aviation-24636/',
            'http://aviapages.com/buzz/thread/flight-request-11-feb-eddm-edja-2pax-24654/',
            'http://aviapages.com/buzz/thread/1998-bombardier-learjet-60-sn-130-rn-n384jw-with-ttaf10441-is-for-sale-by-wheels-up-aircraft-sales-24679/',
            'http://aviapages.com/buzz/thread/flight-request-01-feb-gmme-eglf-1pax-24610/',
            'http://aviapages.com/buzz/thread/private-jets-fly-between-la-and-las-vegas-more-often-than-any-two-destinations-in-the-united-states-where-vip-celebrities-high-rollers-hardcore-party-goers-hasty-elopers-and-ritzy-angelenos-go-to-roll-the-dice-or-spice-things-up-a-little-or-a-lot-3652/',
            'http://aviapages.com/buzz/thread/flight-request-27-feb-lowi-uuww-7pax-24670/',
            'http://aviapages.com/buzz/thread/flight-request-19-feb-eddm-edma-2pax-24653/',
            'http://aviapages.com/buzz/thread/flight-request-25-jan-gmme-eglf-4pax-24597/',
            'http://aviapages.com/buzz/thread/1984-sikorsky-76a-sn-760264-rn-n90ev-with-ttaf9141-for-7-passengers-is-for-sale-by-northern-jet-management-inc-24677/',
            'http://aviapages.com/buzz/thread/our-newly-signed-agreement-with-global-jet-services-provides-the-operators-of-nearly-1000-classic-falcon-aircraft-in-service-around-the-globe-with-dedicated-high-quality-training-and-support-10333/',
            'http://aviapages.com/buzz/thread/malta-headquartered-search-platform-getjet-is-to-sponsor-an-award-for-broking-at-the-wings-of-business-ceremony-taking-place-in-moscow-in-february-next-year-5467/',
            'http://aviapages.com/buzz/thread/2018-beechcraft-king-air-250-sn-by-327-rn-n327dw-with-ttaf670-for-6-passengers-is-for-sale-by-textron-aviation-24615/',
            'http://aviapages.com/buzz/thread/2019-gulfstream-g600-sn-73008-rn-n108db-with-ttaf1005-for-13-passengers-is-for-sale-by-gulfstream-aerospace-corporation-24675/',
            'http://aviapages.com/buzz/thread/flight-request-03-mar-mdsd-omdw-25pax-07-mar-omdw-mdsd-25pax-24656/',
            'http://aviapages.com/buzz/thread/flight-request-13-feb-kcwa-mrlb-8pax-24661/',
            'http://aviapages.com/buzz/thread/flight-request-04-jan-kopf-ktrk-9pax-15-jan-ktrk-kopf-9pax-21365/',
            'http://aviapages.com/buzz/thread/flight-request-07-feb-vrmm-wsss-6pax-24612/',
            'http://aviapages.com/buzz/thread/2010-hawker-900xp-sn-169-rn-n51hh-with-ttaf1547-for-9-passengers-is-for-sale-by-leading-edge-aviation-solutions-llc-24626/',
            'http://aviapages.com/buzz/thread/1995-gulfstream-g-iv-sp-sn-1254-rn-n445bj-with-ttaf11055-is-for-sale-by-jet-edge-partners-24650/',
            'http://aviapages.com/buzz/thread/2015-gulfstream-g650er-sn-6117-rn-n650hf-with-ttaf1942-for-13-passengers-is-for-sale-by-avpro-inc-24625/',
            'http://aviapages.com/buzz/thread/honda-aircraft-company-associate-ashley-hayes-not-only-works-in-tech-operations-but-is-also-part-of-only-6-of-women-who-are-pilots-9820/',
            'http://aviapages.com/buzz/thread/flight-request-28-jan-eddb-lfcr-2pax-31-jan-lfcr-eddb-2pax-24603/',
            'http://aviapages.com/buzz/thread/flight-request-20-feb-umms-lira-1pax-24672/',
            'http://aviapages.com/buzz/thread/flight-request-05-feb-mwcr-kmco-2pax-24630/',
            'http://aviapages.com/buzz/thread/flight-request-14-feb-evra-lszs-1pax-24633/',
            'http://aviapages.com/buzz/thread/flight-request-07-feb-lfcr-eddb-2pax-24634/',
            'http://aviapages.com/buzz/thread/flight-request-14-feb-ltfm-lfpb-4pax-24657/',
            'http://aviapages.com/buzz/thread/flight-request-27-jan-vidp-eglf-4pax-24577/',
            'http://aviapages.com/buzz/thread/2012-beechcraft-king-air-250-sn-by-141-with-ttaf905-for-6-passengers-is-for-sale-by-acass-24578/',
            'http://aviapages.com/buzz/thread/flight-request-05-feb-lppr-slvr-4pax-07-feb-slvr-sbbe-4pax-07-feb-sbbe-lppt-4pax-08-feb-lppt-lpbg-4pax-24607/',
            'http://aviapages.com/buzz/thread/bizav-market-forecast-2022-inventory-pilots-shortage-steady-operations-increase-top-trends-2022-24627/',
            'http://aviapages.com/buzz/thread/2016-beechcraft-king-air-250-sn-by-260-rn-n523gc-with-ttaf906-for-6-passengers-is-for-sale-by-textron-aviation-24624/',
            'http://aviapages.com/buzz/thread/flight-request-12-feb-dnmm-gooy-2pax-12-feb-gooy-dnmm-2pax-24617/',
            'http://aviapages.com/buzz/thread/2001-bombardier-learjet-31-sn-31a-229-rn-n229lj-with-ttaf4322-is-for-sale-by-meisner-aircraft-inc-24611/',
            'http://aviapages.com/buzz/thread/flight-request-12-feb-lfat-lfmd-2pax-13-feb-lfmd-lfat-2pax-24644/',
            'http://aviapages.com/buzz/thread/flight-request-25-jan-gmme-eglf-4pax-24598/',
            'http://aviapages.com/buzz/thread/flight-request-26-jan-lrbs-liml-2pax-24600/',
            'http://aviapages.com/buzz/thread/flight-request-10-mar-egcc-tist-16pax-17-mar-tist-egcc-16pax-24618/',
            'http://aviapages.com/buzz/thread/2001-bell-430-sn-49079-rn-n522mv-with-ttaf1667-for-6-passengers-is-for-sale-by-jeteffect-inc-24645/',
            'http://aviapages.com/buzz/thread/2016-embraer-legacy-500-sn-55000050-rn-n655mc-with-ttaf923-for-10-passengers-is-for-sale-by-ogarajets-24668/',
            'http://aviapages.com/buzz/thread/flight-request-02-may-wmkk-tfff-50pax-24642/',
            'http://aviapages.com/buzz/thread/2001-bombardier-learjet-45-sn-123-rn-n750cr-with-ttaf5927-for-9-passengers-is-for-sale-by-jba-aviation-inc-24647/',
            'http://aviapages.com/buzz/thread/flight-request-29-jan-lppt-sbgr-4pax-24608/',
            'http://aviapages.com/buzz/thread/1984-hawker-800sp-sn-258016-rn-n800vr-with-ttaf12501-for-9-passengers-is-for-sale-by-meisner-aircraft-inc-24595/',
            'http://aviapages.com/buzz/thread/flight-request-24-feb-lebl-levc-5pax-24639/',
            'http://aviapages.com/buzz/thread/flight-request-10-feb-lrop-eggw-2pax-24649/',
            'http://aviapages.com/buzz/thread/exploring-contemporary-art-in-china-beijings-art-scene-is-brimming-with-artists-who-have-something-to-say-and-the-world-is-listening-11813/',
            'http://aviapages.com/buzz/thread/flight-request-31-jan-lfpb-eddb-2pax-24606/',
            'http://aviapages.com/buzz/thread/2009-embraer-phenom-100-sn-50000019-rn-n247rw-with-ttaf2054-is-for-sale-by-elliott-jets-24616/'
        }
        self.assertEqual(parser.get_sitemap_links(SITEMAP_PATH), answer)

    def test_get_word_list(self):
        analyzer.download_nltk_data()
        text = 'UUWW - EVRA 2Pax Challenger 300'
        answer = ['UUWW', 'EVRA', '2Pax', 'Challenger']
        self.assertEqual(analyzer.get_words_list(text), answer)
        text = 'I love Python so much. My repositories are located at https://github.com/'
        answer = ['love', 'Python', 'much', 'repository', 'locate']
        self.assertEqual(analyzer.get_words_list(text), answer)
        text = 'My phone number is +(373) 767 411 41'
        answer = ['phone', 'number']
        self.assertEqual(analyzer.get_words_list(text), answer)

    def test_parser(self):
        # MAIN
        parser_obj = parser.Parser(SITEMAP_PATH, 3, False)
        parser_obj.run_test()
        rows_count = 0
        column_correct_count = 6
        with open('/working/sitemap_tester/reports/report_main.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.assertEqual(column_correct_count, len(row))
                rows_count += 1
            self.assertEqual(101, rows_count)
        # BUZZ
        parser_obj = parser.Parser(SITEMAP_PATH, 3, True)
        parser_obj.run_test()
        rows_count = 0
        column_correct_count = 7
        with open('/working/sitemap_tester/reports/report_buzz.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.assertEqual(column_correct_count, len(row))
                rows_count += 1
            self.assertEqual(101, rows_count)

    def test_analyzer(self):
        analyser_obj = analyzer.Analyzer(SITEMAP_PATH)
        analyser_obj.analyze()
        # HEADERS
        rows_count = 0
        column_correct_count = 2
        with open('/working/sitemap_tester/reports/seo_headers.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                print(row)
                self.assertEqual(column_correct_count, len(row))
                rows_count += 1
            self.assertEqual(1, rows_count)
        # BODY
        rows_count = 0
        column_correct_count = 2
        with open('/working/sitemap_tester/reports/seo_bodies.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.assertEqual(column_correct_count, len(row))
                rows_count += 1
            self.assertEqual(10, rows_count)


if __name__ == '__main__':
    unittest.main()
