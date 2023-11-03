from pypdf import PdfReader

def analyze_pdf(filename):

    interesting_objects=("/Title",
                        "/Creator",
                        "/Author",
                        "/Keywords"
                        "/CreationDate",
                        "/ModDate",
                        "/Producer",
                        "/Subject",
                        )

    res = {}

    reader = PdfReader(filename)
    meta = reader.metadata
    if meta:
        res[x.split('/')[1]]=meta.get(x)
        #print([(x,meta.get(x)) for x in interesting_objects])

    return res 

    ### dictionary of the form: {"Author": x, "Title": x}

