import urllib2
import unicodedata
from bs4 import BeautifulSoup

# Get recipe
link = raw_input('Enter a recipe URL: ')
url = link.replace("\"", "")
req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urllib2.urlopen(req).read()
soup = BeautifulSoup(webpage, "html.parser")

# Get title
title = soup.find("h1", class_="recipe-header__title")
file_name = title.text + ".txt"
file = open(file_name, "w")
print title.text
file.write(unicodedata.normalize('NFKD', title.get_text()).encode('ascii', 'ignore') + "\n")

# Get meta-data
# rating
stars = soup.findAll("span", class_="rate-fivestar-btn-filled")
temp = "Rating: " + str(len(stars))
rating = temp.replace("\n", "")
print rating
file.write(rating + "\n")

# Skill level
skill = soup.find("section", class_="recipe-details__item--skill-level")
temp = skill.get_text()
level = temp.replace("\n", "").replace(" ", "")
print level
file.write("Difficulty: " + level + "\n")

# Serves
serve = soup.find("section", class_="recipe-details__item--servings")
temp = serve.get_text()
serving = temp.replace("\n", "").replace(" ", "").replace("Serves", "")
print serving
file.write("Serves: " + serving + "\n")

# prep time
prep = soup.find("span", class_="recipe-details__cooking-time-prep")
temp = prep.get_text()
prep_time = temp.replace("\n", "")
print prep_time
file.write(prep_time + "\n")

# cooking time
cook = soup.find("span", class_="recipe-details__cooking-time-cook")
temp = cook.get_text()
cook_time = temp.replace("\n", "")
print cook_time
file.write(cook_time + "\n")

# ingredients
print "\n"
print "Ingredients"
file.write("\n" + "Ingredients" + "\n")
for li in soup.findAll("li", class_="ingredients-list__item"):
    a = li.find('a', class_="ingredients-list__glossary-link")
    if a:
        item = li.get_text()
        lines = item.split("\n")
        print lines[0]
        file.write(unicodedata.normalize('NFKD', lines[0]).encode('ascii', 'ignore') + "\n")
    else:
        print li.get_text()
        file.write(unicodedata.normalize('NFKD', li.get_text()).encode('ascii', 'ignore') + "\n")
print "\n"

# method
print "Method"
file.write("\n" + "Method" + "\n")
method_counter = 0
for li in soup.findAll("li", class_="method__item"):
    method_counter += 1
    method_item = li.get_text().replace("\n", "")
    print method_item
    file.write(unicodedata.normalize('NFKD', method_item).encode('ascii', 'ignore') + "\n" + "\n")

# Nutrition
file.write("Nutrition \n")
nutrition = soup.find("ul", class_="nutrition")
for li in nutrition.findAll("li"):
    label = li.find("span", class_="nutrition__label")
    value = li.find("span", class_="nutrition__value")
    print label.get_text() + ": " + value.get_text()
    file.write(label.get_text() + ": " + value.get_text() + "\n")

# write source
file.write("\nRecipe from:\n")
file.write("URL: " + url)

# close file
file.close()
