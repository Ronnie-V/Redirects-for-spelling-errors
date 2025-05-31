# Python3 code 
import pywikibot
import datetime
from pywikibot import pagegenerators as pg

debugMode = False

def addToTable(text, pageTitle, usedSpellingError, targetPageTitle, preferredTextToDisplay, number):
  text += '|-\n'
  if number == 1:
    text +=f'|[[{pageTitle}]]||[[Speciaal:VerwijzingenNaarHier/{usedSpellingError}&namespace=0&limit=5000|{usedSpellingError}]]||{targetPageTitle}||{preferredTextToDisplay}||{number}\n'
  else:
    text +=f'|[[{pageTitle}]]||{usedSpellingError}||{targetPageTitle}||{preferredTextToDisplay}||{number}\n'
  return (text)

def getPreferredTextToDisplay(source):
  p = source.casefold().find('{R spelfout'.casefold() )
  if p < 0:
    return ''
  q = source.casefold().find('van', p)
  if q < 0:
    return ''
  target = source[q+3:]
  target = target.replace('}','').strip()
  if target[0:1] == '=':
    target = target.strip()[1:]
  return target

def showUsedRedirects():
  text =  ''
  countInCat = countOfPages = countOfRedirects = 0
  site = pywikibot.Site("nl", 'wikipedia')
  cat = pywikibot.Category(site, 'Categorie:Wikipedia:Redirect voor spelfout')
  start = datetime.datetime.now()
  text += 'Een overzicht van verwijzingen naar spelfouten, die een redirect zijn. De lezer komt wel op de goede pagina terecht, maar, zeker als de linktekst direct zichtbaar is, is het wenselijk als de juiste tekst leesbaar is.\n'
  text += 'Voel je vrij om deze links te corrigeren, met enige (on)regelmaat wordt deze pagina bijgewerkt. Let bij het corrigeren op bijvoorbeeld citaten, vervang dan niet de zichtbare tekst, wel de link.\n\n'
  text += '{| class="wikitable sortable"\n'
  text += '!Pagina!!Redirect!!Beoogde pagina!!Opmerking!!Nummer voor deze redirect\n'
  if debugMode:
    catstart = 'Bl'
  else:
    catstart = ''
  for page in pg.CategorizedPageGenerator(cat, start=catstart):
    targetPageTitle = ''
    outgoingLinks = 0
    links = page.linkedPages(follow_redirects = False)
    for link in links:
      outgoingLinks += 1
    if outgoingLinks == 1:
      targetPageTitle = link.title()
    preferredTextToDisplay = getPreferredTextToDisplay(page.text)
    backlinks = page.backlinks(follow_redirects=True, filter_redirects=None, namespaces=[0], total=None, content=False)
    addedlinks = 0
    for backlink in backlinks:
      addedlinks += 1
      text = addToTable (text, backlink.title(), page.title(), targetPageTitle, preferredTextToDisplay, addedlinks )
    if addedlinks > 0:
      countOfPages += addedlinks
      countOfRedirects += 1
    if debugMode and countOfRedirects > 20:
      break
    countInCat += 1

  text += '|}\n'
  endtime = datetime.datetime.now()
  text += f'Laatst bijgewerkt op {str(endtime)[:10]} om {str(endtime)[10:19]}'

  if debugMode:
    pywikibot.Page(site, u'Gebruiker:RonnieV/Redirects via spelfout').put(text, summary=f'Update {countOfPages} links gevonden naar {countOfRedirects} verschillende foutgespelde redirects ({countInCat} bekeken)') #Save page
  else:
    pywikibot.Page(site, u'Wikipedia:Redirects via spelfout').put(text, summary=f'Update {countOfPages} links gevonden naar {countOfRedirects} verschillende foutgespelde redirects') #Save page
  print('gestart om: ', start, ' klaar om: ', endtime)

if __name__ == "__main__":
  showUsedRedirects()