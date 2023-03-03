import argparse
import requests
import re

# Pour le check de dispo Amazon : --regex "<div id=\"outOfStock\""
parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, help="Fichier d'URLs à checker", default='')
parser.add_argument("--output", type=str, help="Fichier de sortie pour les résultats", default="results.txt")
parser.add_argument("--regex", type=str, help="(facultatif) Regex à checker dans le code HTML", default="")

args = parser.parse_args()

if args.input == '':
    parser.print_usage()
    exit()


headers = {'user-agent': 'MyBot'}
output_file = open(args.output, 'w')
output_file.write("start_url;final_url;nb_redir;final_status_code;regex_find\n")
with open(args.input, 'r') as f:
    for line in f:
        start_url = line.strip()
        try:
            r = requests.get(start_url, headers=headers, timeout=5)
            final_url = r.url
            final_status_code = r.status_code
            nb_redir = len(r.history)
            regex_find = 'NA'
            if args.regex != '':
                if re.search(args.regex, r.text):
                    regex_find = True
                else:
                    regex_find = False
            print(start_url, final_url, nb_redir, final_status_code, regex_find)
        except requests.exceptions.ReadTimeout:
            print(start_url, "TIMEOUT")
            final_url = ''
            final_status_code = 'TIMEOUT'
            nb_redir = ''
            regex_find = ''
        output_file.write(start_url + ';' + final_url + ';' + str(nb_redir) + ';' + str(final_status_code) + ';' + str(regex_find) + '\n')
output_file.close()