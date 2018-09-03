import json
import re
from datetime import datetime
import urllib.request
from string import Template

TEXT = "http://oeis.org/search?q=id:{}&fmt=json"
OEIS = "https://oeis.org/{}"

TEMPLATE = Template(r"""@MISC{OEIS:$id,
    AUTHOR       = {$author},
    TITLE        = {The {O}n-{L}ine {E}ncyclopedia of {I}nteger {S}equences},
    HOWPUBLISHED = {\href{$url}{$id}},
    MONTH        = {$month},
    YEAR         = {$year},
    NOTE         = {$note}
}""")

def validate(id):

    if len(id) != 7:

        print("ERROR-1: Bad length!")
        return False

    first, *sequence = id

    if first != "A":

        print("ERROR-3: The Sequence does not begin with A.")
        return False

    digits = set("0123456789")

    for d in sequence:

        if d not in digits:

            print("ERROR-2: Wrong characters on input string!")
            return False

    return True


def bibtex(id):
    r"""

            >>> from sak.oeis import bibtex
            >>> bibtex( "A00004" )
            ERROR-1: Bad length!
            >>> bibtex( "B000045" )
            ERROR-3: The Sequence does not begin with A.
            >>> bibtex( "A0P0045" )
            ERROR-2: Wrong characters on input string!
            >>> bibtex( "A000045" ) # doctest: +NORMALIZE_WHITESPACE
            @MISC{OEIS:A000045,
                AUTHOR       = {N. J. A. Sloane},
                TITLE        = {The {O}n-{L}ine {E}ncyclopedia of {I}nteger {S}equences},
                HOWPUBLISHED = {\href{https://oeis.org/A000045}{A000045}},
                MONTH        = {Apr},
                YEAR         = {1991},
                NOTE         = {Fibonacci numbers: F(n) = F(n-1) + F(n-2) with F(0) = 0 and F(1) = 1.}
            }
            >>> bibtex( "A000108" ) # doctest: +NORMALIZE_WHITESPACE
            @MISC{OEIS:A000108,
                AUTHOR       = {N. J. A. Sloane},
                TITLE        = {The {O}n-{L}ine {E}ncyclopedia of {I}nteger {S}equences},
                HOWPUBLISHED = {\href{https://oeis.org/A000108}{A000108}},
                MONTH        = {Apr},
                YEAR         = {1991},
                NOTE         = {Catalan numbers: C(n) = binomial(2n,n)/(n+1) = (2n)!/(n!(n+1)!). Also called Segner numbers.}
            }
            >>> bibtex( "A001010" ) # doctest: +NORMALIZE_WHITESPACE
            @MISC{OEIS:A001010,
                    AUTHOR       = {N. J. A. Sloane, Stéphane Legendre},
                    TITLE        = {The {O}n-{L}ine {E}ncyclopedia of {I}nteger {S}equences},
                    HOWPUBLISHED = {\href{https://oeis.org/A001010}{A001010}},
                    MONTH        = {Apr},
                    YEAR         = {1991},
                    NOTE         = {Number of symmetric foldings of a strip of n stamps.}
            }

    """

    if not validate(id):
        return

    url = TEXT.format(id)

    try:

        response = urllib.request.urlopen(url)

    except urllib.error.HTTPError as e:

        print(e, ": could not open url %s" % url)
        return

    doc = json.load(response)["results"][0]

    date = datetime.strptime(doc["created"][:10], '%Y-%m-%d')
    year = date.strftime('%Y')
    month = date.strftime('%b')

    author = ', '.join(re.findall('_([^,]*)_', doc["author"]))

    description = doc["name"]

    entry = TEMPLATE.substitute( id=id , author=author , url=OEIS.format(id) , month=month , year=year , note=description )

    print(entry)
