# This is a list of all reports we want to create

from report import Report
import epi_report, ga_data, gtm

#  create all the report objects
reports = {
    "epi_public" : Report(name="epi_public", source="epi",source_fn=epi_report.epi_report, dest="", site="public"),
    "epi_adviser" : Report(name="epi_adviser", source="epi",source_fn=epi_report.epi_report, dest="", site="advisernet"),
    "ga_public_rating" : Report(name="ga_public_rating", source="ga",source_fn=ga_data.get_ga_report ,dest="", site="public", source_args="rating"),
    "ga_public_size" : Report(name="ga_public_size", source="ga", source_fn=ga_data.get_ga_report,dest="", site="public", source_args="size"),
    "ga_adviser_rating" : Report(name="ga_adviser_rating", source="ga",source_fn=ga_data.get_ga_report ,dest="", site="advisernet", source_args="rating"),
    "ga_adviser_size" : Report(name="ga_adviser_size", source="ga", source_fn=ga_data.get_ga_report,dest="", site="advisernet", source_args="size"),
    "gtm_mouseflow" : Report(name="gtm_mouseflow", source="gtm",source_fn=gtm.get_gtm,dest="",source_args="74"),
    "gtm_ethnio" : Report(name="gtm_ethnio", source="gtm",source_fn=gtm.get_gtm,dest="",source_args="78"),
    "gtm_hotjar" : Report(name="gtm_hotjar", source="gtm",source_fn=gtm.get_gtm,dest="",source_args="82"),
    "gtm_optimise" : Report(name="gtm_optimise", source="gtm",source_fn=gtm.get_gtm,dest="",source_args="45")
}
