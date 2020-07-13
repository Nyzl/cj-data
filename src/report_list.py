# This is a list of all reports we want to create

from report import Report
import epi_report, ga_data, gtm, search_console, tokenise


#  create all the report objects
reports = {
    'epi_public' : Report(
        name='epi_public', 
        source='epi',
        source_fn=epi_report.epi_report, 
        source_kwargs={'site':'public'},
        clean_fn=epi_report.pages_clean,
        clean_kwargs={},
        send_kwargs={'writeType':'WRITE_APPEND'}, 
        site='public'),
    'epi_adviser' : Report(
        name='epi_adviser', 
        source='epi',
        source_fn=epi_report.epi_report,
        source_kwargs={'site':'advisernet'}, 
        clean_fn=epi_report.pages_clean,
        clean_kwargs={},
        send_kwargs={'writeType':'WRITE_APPEND'}, 
        site='advisernet'),
    'ga_public_rating' : Report(
        name='ga_public_rating', 
        source='ga',
        source_fn=ga_data.get_ga_report,
        source_kwargs={'site':'public', 'type':'rating', 'period':90}, 
        clean_kwargs={},
        send_kwargs={}, 
        site='public', 
        source_args='rating'),
    'ga_public_size' : Report(
        name='ga_public_size', 
        source='ga', 
        source_fn=ga_data.get_ga_report, 
        source_kwargs={'site':'public', 'type':'size', 'period':90},
        clean_kwargs={},
        send_kwargs={}, 
        site='public', 
        source_args='size'),
    'ga_adviser_rating' : Report(
        name='ga_adviser_rating', 
        source='ga',
        source_fn=ga_data.get_ga_report,
        source_kwargs={'site':'advisernet', 'type':'rating', 'period':90},
        clean_kwargs={},
        send_kwargs={}, 
        site='advisernet', 
        source_args='rating'),
    'ga_adviser_size' : Report(
        name='ga_adviser_size', 
        source='ga', 
        source_fn=ga_data.get_ga_report,
        source_kwargs={'site':'advisernet', 'type':'size', 'period':90},
        clean_kwargs={},
        send_kwargs={}, 
        site='advisernet', 
        source_args='size'),
    'gtm_mouseflow' : Report(
        name='gtm_mouseflow', 
        source='gtm',
        source_fn=gtm.get_gtm,
        source_kwargs={'variable':'74'},
        clean_kwargs={},
        send_kwargs={}),
    'gtm_ethnio' : Report(
        name='gtm_ethnio', 
        source='gtm',
        source_fn=gtm.get_gtm,
        source_kwargs={'variable':'78'},
        clean_kwargs={},
        send_kwargs={}),
    'gtm_hotjar' : Report(
        name='gtm_hotjar', 
        source='gtm',
        source_fn=gtm.get_gtm,
        source_kwargs={'variable':'82'},
        clean_kwargs={},
        send_kwargs={}),
    'gtm_optimise' : Report(
        name='gtm_optimise', 
        source='gtm',
        source_fn=gtm.get_gtm,
        source_kwargs={'variable':'45'},
        clean_kwargs={},
        send_kwargs={}),
    'gsc_fullsite' : Report(
        name='gsc_fullsite',
        source='gsc',
        source_fn=search_console.get_data,
        source_kwargs={},
        clean_kwargs={},
        send_kwargs={'writeType':'WRITE_APPEND'}),
    'gsc_tokens' : Report(
        name='gsc_tokens',
        source='gsc',
        source_fn=search_console.get_data,
        clean_fn=tokenise.tokenise,
        source_kwargs={},
        clean_kwargs={'col_name':'query'},
        send_kwargs={'writeType':'WRITE_APPEND'}),
    'ga_public_rating_7' : Report(
        name='ga_public_rating_7', 
        source='ga',
        source_fn=ga_data.get_ga_report,
        source_kwargs={'site':'public', 'type':'rating', 'period':7}, 
        clean_kwargs={},
        send_kwargs={}, 
        site='public', 
        source_args='rating'),
    'ga_public_size_7' : Report(
        name='ga_public_size_7', 
        source='ga', 
        source_fn=ga_data.get_ga_report, 
        source_kwargs={'site':'public', 'type':'size', 'period':7},
        clean_kwargs={},
        send_kwargs={}, 
        site='public', 
        source_args='size'),
    'ga_adviser_rating_7' : Report(
        name='ga_adviser_rating_7', 
        source='ga',
        source_fn=ga_data.get_ga_report,
        source_kwargs={'site':'advisernet', 'type':'rating', 'period':7},
        clean_kwargs={},
        send_kwargs={}, 
        site='advisernet', 
        source_args='rating'),
    'ga_adviser_size_7' : Report(
        name='ga_adviser_size_7', 
        source='ga', 
        source_fn=ga_data.get_ga_report,
        source_kwargs={'site':'advisernet', 'type':'size', 'period':7},
        clean_kwargs={},
        send_kwargs={}, 
        site='advisernet', 
        source_args='size')
}
