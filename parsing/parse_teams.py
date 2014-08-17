from BeautifulSoup import BeautifulSoup
import urllib2

def main(league):
    if league == "NFL":
        getNFL()
    else:
        getNCAA()

def getNCAA():
    f = urllib2.urlopen("http://espn.go.com/college-football/teams")
    soup = BeautifulSoup(f.read())
    f.close()
    teams = soup.findAll("a", {"class" : "bi"})
    print len(teams)
    results = open("NCAAresults.sql", 'w+')
    for team in teams:
        results.write("insert into teams(teamname)\n")

        data = team['href'].split('/')[-1]
        teamname = data.split('-')
        s = ''
        for x in teamname:
            s += "%s " % (x.capitalize())

        results.write("values ('%s');\n\n" % (s.strip()))

    results.close()


def getNFL():
    f = urllib2.urlopen("http://espn.go.com/nfl/teams")
    soup = BeautifulSoup(f.read())
    f.close()
    teams = soup.findAll("a", {"class" : "bi"})
    print len(teams)
    results = open("NFLresults.sql", 'w+')
    for team in teams:
        results.write("insert into teams(teamname)\n")
        results.write("values ('%s');\n\n" % (team.contents[0].strip()))

    results.close()

if __name__ == '__main__':
    main('NFL')

