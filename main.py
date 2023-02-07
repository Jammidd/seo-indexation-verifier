#/usr/bin/python3
import csv
import datetime
import os
import sys, getopt

from util import is_indexed_by_google

base_path = os.path.dirname(os.path.abspath(__file__))

def _generate_csv(records, report_file_name):
    header = ["id", "url", "indexed"]
    report_file = "reports/{}".format(report_file_name)
    report_csv = open(report_file, "a+")
    
    writer = csv.DictWriter(report_csv, fieldnames=header)

    if os.stat(report_file).st_size == 0:
        writer.writeheader()

    for record in records:
        writer.writerow(record)
    
    report_csv.close()

def _process_record(url):
    return is_indexed_by_google(url)

def _process_all_records(urls, offset, limit, random):
    indexation_record = []
    if len(urls) > 0:
        for url in urls:
            indexation_record.append({
                "url": url,
                "status": "indexed" if is_indexed_by_google(url) else False
            })

    return indexation_record

def recursive_records(urls, report_file_name, offset=0, limit=None, num_per_iter=5000, random=True, report=None):
    if limit and limit > num_per_iter:
        record_count = num_per_iter
    elif limit > 0:
        record_count = limit
    else:
        record_count = -1

    records = _process_all_records(urls[offset:record_count])
    if not records or len(records) == 0:
        return 

    print("Processing {} records".format(len(records)))
    if report:
        report["total_urls"] += len(records)
        report["total_indexed_urls"] += len([record for record in records if record['indexed'] == True])

    # generate / print to csv
    _generate_csv(records, report_file_name)

    return recursive_records(urls, report_file_name, offset + record_count, limit - record_count, num_per_iter, random, report)
 
def main(urls, limit=None, random=True, offset=0):
    max_per_iter = 1000
    offset = int(offset)
    limit = int(limit) if limit not in ('None', 'none', 0, None) else None

    today = datetime.datetime.now()
    today_fmt = today.strftime("%Y_%m_%d")
    report_file_name = "url_indexation_report-{}.csv".format(today_fmt)

    report = {
        "total_url_count": 0,
        "indexed_url_count": 0,
        "indexed_percent": 0
    }

    recursive_records(urls, report_file_name, offset, limit, max_per_iter, random, report)
    print(report)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(*args)
