import sys, json
from getopt import getopt, GetoptError



welcome_text = \
"""
Welcome to Januscore, use score -h for help
"""

help_text = \
"""
This program is designed for scoring SAT practice tests

usage:
    score <testID> <responseID> --options

    -h, --help:
        get help

    -t, --total:
        get total score

    -w <responseID>, --write <responseID>:
        write response

    --writeAnswerKey:
        write answer key
"""



def loadRsct(rsctID = "default"):
    rsctFile = open(".\\RSCT\\" + rsctID + ".rsct", 'rb')
    return json.loads( str( rsctFile.read, 'ascii' ) )

def loadResponse(testID, responseID):
    responseFile = open( testID + "\\responses.json", 'rt' )

    response = json.loads(responseFile)[responseID]
    responseFile.close()

    return response

def dumpResponse(testID, responseID, response):
    responseFile = open( testID + "\\responses.json", 'r+t' )

    allResponses = json.loads(responseFile)
    allResponses[responseID] = response

    responseFile.seek(0)
    responseFile.write( json.dumps(allResponses) )
    responseFile.truncate()
    responseFile.close()


def isTestExist(testID):
    try:
        loadResponse(testID, None)
        raise ValueError
    except KeyError:
        return True
    except FileNotFoundError:
        return False

def isResponseExist(testID, responseID):
    try:
        loadResponse(testID, responseID)
        return True
    except KeyError:
        return False


def getSectionArgs(args):
    sections = arg.lower().split('+')

    if arg == '':
        arg = 
        arg = "reading+writing+mathnc+mathc"
    
    for section in sections:
        if section == "english":
            sections.remove("english")
            sections.append("reading")
            sections.append("writing")
        if section == "math":
            sections.remove("math")
            sections.append("mathc")
            sections.append("mathnc")



def compareSection(sectionResponse, sectionAnswer):
    sectionResults = {}
    for question in sectionResponse:
        sectionResults[question] = \
            sectionResponse[question] == sectionAnswer[question]
    return sectionResults


def compareResponse(response, answer):
    results = {}
    for section in response:
        results[section] = \
            compareSection(response[section], answer[section])
    return results


def getTotalScore(testID, responseID):
    response = loadResponse(testID, responseID)
    answer = loadResponse(testID, "Answer Key")

    results = compareResponse(response, answer)

    for section in results:
        for question in results[section]:
            if question == True: totalscore += 1
    
    return totalscore



def score(opts, args):
    try:
        testID = args[0]
        isTestIdGiven = True
    except IndexError:
        isTestIdGiven = False
        
    try:
        responseID = args[1]
        isResponseIdGiven = True
    except IndexError:
        isResponseIdGiven = False

    for opt, arg in opts:
        if opt in ['-h', "--help"]:
            print(help_text)
        else:
            assert isTestIdGiven
            if not isTestExist(testID):
                print("ERROR: Test \"" + testID + "\" not found")
                assert False

        if opt in ['-t', "--total"]:
            assert isResponseIdGiven
            if not isResponseExist(testID, responseID):
                print("ERROR: Response \"" + responseID + "\" not found")
                assert False

            totalscore = getTotalScore(testID, responseID)

            print( "TestID: " + testID )
            print( "ResponseID: " + responseID )
            print( "Total score: " + totalscore )

        elif opt in ['-w', "--write"]:

            for section in sections:
                try:

                except KeyError:
                    print( "ERROR: Section \"" +  + "\" not found" )



def main(argv):
    try:
        opts, args = getopt(
            argv, "htw", [
                "help", 
                "total", 
                "write", 
                "writeAnswerKey"]
        )
        
        if len(opts) == 0:
            opts.append(("--total", ''))

        score(opts, args)

    except (GetoptError, AssertionError):
        print(welcome_text)
        sys.exit(-1)


if __name__ == "__main__":
    main(sys.argv[1:])
